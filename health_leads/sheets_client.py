"""Client async → webhook Apps Script LYRA_PORTFOLIO_COMMAND_CENTER (LEADS_PIPELINE)."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Optional

import httpx

from health_leads.config import get_settings

logger = logging.getLogger("graal.health_leads.sheets")


class SheetsSyncError(RuntimeError):
    """Levée quand le webhook Apps Script rejette ou échoue à traiter un lead."""


async def push_lead_to_sheet(
    *,
    lead_id: str,
    email: str,
    first_name: str,
    company: Optional[str] = None,
    status: str = "NEW",
) -> None:
    settings = get_settings()
    if not settings.sheets_webhook_url:
        logger.warning("GRAAL_HEALTH_SHEETS_WEBHOOK_URL absent — synchronisation ignorée pour %s", lead_id)
        raise SheetsSyncError("SHEETS_WEBHOOK_URL manquant dans la configuration.")

    payload = {
        "secret": settings.sheets_webhook_secret,
        "lead_id": lead_id,
        "entity": "graal",
        "email": email,
        "first_name": first_name,
        "company": company or "",
        "status": status,
        "captured_at": datetime.now(timezone.utc).isoformat(),
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            response = await client.post(settings.sheets_webhook_url, json=payload)
        except httpx.HTTPError as exc:
            logger.exception("Erreur de transport vers le webhook Sheets pour %s", lead_id)
            raise SheetsSyncError(str(exc)) from exc

    if response.status_code >= 300:
        logger.error("Webhook Sheets a rejeté le lead %s (status=%s)", lead_id, response.status_code)
        raise SheetsSyncError(f"Sheets webhook HTTP {response.status_code}: {response.text}")
