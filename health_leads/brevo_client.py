"""Client async Brevo pour le microservice Graal Health Leads."""
from __future__ import annotations

import base64
import logging
from typing import Optional

import httpx

from health_leads.config import get_settings

logger = logging.getLogger("graal.health_leads.brevo")
BREVO_ENDPOINT = "https://api.brevo.com/v3/smtp/email"


class BrevoDeliveryError(RuntimeError):
    """Levée quand Brevo rejette ou échoue à livrer un message."""


async def send_transactional_email(
    *,
    to_email: str,
    to_name: str,
    subject: str,
    html_content: str,
    attachment_bytes: Optional[bytes] = None,
    attachment_name: Optional[str] = None,
) -> dict:
    settings = get_settings()
    if not settings.brevo_api_key:
        logger.warning("GRAAL_HEALTH_BREVO_API_KEY absent — envoi ignoré pour %s", to_email)
        raise BrevoDeliveryError("BREVO_API_KEY manquant dans la configuration.")

    payload: dict = {
        "sender": {"name": settings.brevo_sender_name, "email": settings.brevo_sender_email},
        "to": [{"email": to_email, "name": to_name}],
        "subject": subject,
        "htmlContent": html_content,
    }
    if attachment_bytes and attachment_name:
        payload["attachment"] = [{
            "content": base64.b64encode(attachment_bytes).decode("ascii"),
            "name": attachment_name,
        }]

    headers = {"api-key": settings.brevo_api_key, "content-type": "application/json", "accept": "application/json"}

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            response = await client.post(BREVO_ENDPOINT, json=payload, headers=headers)
        except httpx.HTTPError as exc:
            logger.exception("Erreur de transport Brevo pour %s", to_email)
            raise BrevoDeliveryError(str(exc)) from exc

    if response.status_code >= 300:
        logger.error("Brevo a rejeté l'envoi pour %s (status=%s)", to_email, response.status_code)
        raise BrevoDeliveryError(f"Brevo HTTP {response.status_code}: {response.text}")

    return response.json()
