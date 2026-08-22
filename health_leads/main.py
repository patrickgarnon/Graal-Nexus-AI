"""Graal Health Leads — microservice FastAPI indépendant.

Capture les leads Jouvence du Graal (Protocole Sommeil & Récupération 2026).
Tourne sur son propre port, séparé du webhook.py / main.py autopilot
existants à la racine du repo — aucun couplage entre les deux.

Lancement local :
    uvicorn health_leads.main:app --reload --port 8100
"""
from __future__ import annotations

import html
import logging
import uuid
from typing import Literal, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, field_validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from health_leads import brevo_client, pdf_generator, sheets_client
from health_leads.config import get_settings

logger = logging.getLogger("graal.health_leads")
logging.basicConfig(level=logging.INFO)

settings = get_settings()

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Graal Health Leads",
    description="Microservice de capture de leads — Jouvence du Graal",
    version="1.0.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class GraalLeadCapture(BaseModel):
    """Charge utile de capture de lead Jouvence du Graal."""

    email: EmailStr = Field(..., max_length=254)
    first_name: str = Field(..., min_length=1, max_length=100)
    consent_given: bool = Field(
        ..., description="Consentement explicite LPRPDE/RGPD — obligatoire."
    )
    source: Optional[str] = Field(default=None, max_length=100)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        # EmailStr (email-validator) fait déjà une validation RFC complète —
        # on ne fait plus que normaliser la casse ici.
        return str(value).lower()

    @field_validator("first_name")
    @classmethod
    def strip_and_reject_blank_first_name(cls, value: str) -> str:
        # Champ obligatoire : un nom uniquement composé d'espaces doit être
        # rejeté (422), jamais silencieusement transformé en valeur vide —
        # sinon le pipeline en arrière-plan (PDF/email) plante plus loin
        # sur une valeur qui a pourtant passé la validation.
        stripped = value.strip()
        if not stripped:
            raise ValueError("Le prénom ne peut pas être vide.")
        return stripped

    @field_validator("source")
    @classmethod
    def strip_optional_source(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        stripped = value.strip()
        return stripped or None


class GraalLeadResponse(BaseModel):
    lead_id: str
    status: Literal["accepted"]
    message: str


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    version: str
    environment: str


async def _dispatch_graal(lead_id: str, lead: GraalLeadCapture) -> None:
    try:
        pdf_bytes = pdf_generator.generate_graal_protocol_pdf(lead.first_name)
        # Échappement HTML explicite avant interpolation dans le corps de
        # l'email Brevo : lead.first_name est fourni par un appelant non
        # authentifié et ne doit jamais pouvoir injecter du markup dans un
        # message envoyé depuis l'expéditeur de confiance.
        safe_first_name = html.escape(lead.first_name)
        await brevo_client.send_transactional_email(
            to_email=lead.email,
            to_name=lead.first_name,
            subject="Votre Protocole Sommeil & Récupération 2026",
            html_content=(
                f"<p>Bonjour {safe_first_name},</p>"
                "<p>Votre document est en pièce jointe. Merci pour votre "
                "confiance envers Jouvence du Graal.</p>"
            ),
            attachment_bytes=pdf_bytes,
            attachment_name="Protocole-Sommeil-Recuperation-2026.pdf",
        )
    except Exception:  # noqa: BLE001
        logger.exception("Échec du pipeline Graal pour le lead %s", lead_id)
    finally:
        try:
            await sheets_client.push_lead_to_sheet(
                lead_id=lead_id, email=lead.email, first_name=lead.first_name
            )
        except Exception:  # noqa: BLE001
            logger.exception("Échec de synchronisation Sheets pour le lead %s", lead_id)


@app.post(
    "/api/v1/graal/lead-capture",
    response_model=GraalLeadResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def graal_lead_capture(
    request: Request,
    payload: GraalLeadCapture,
    background_tasks: BackgroundTasks,
) -> GraalLeadResponse:
    """Capture un lead Jouvence du Graal (Protocole Sommeil & Récupération 2026)."""
    if not payload.consent_given:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consentement LPRPDE/RGPD requis pour traiter cette demande.",
        )

    lead_id = str(uuid.uuid4())
    background_tasks.add_task(_dispatch_graal, lead_id, payload)

    logger.info("Lead Graal accepté id=%s", lead_id)
    return GraalLeadResponse(
        lead_id=lead_id,
        status="accepted",
        message="Lead reçu, traitement asynchrone en cours.",
    )


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="graal-health-leads",
        version=app.version,
        environment=settings.environment,
    )
