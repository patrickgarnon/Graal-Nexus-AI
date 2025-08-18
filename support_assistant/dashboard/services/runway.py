import os
from typing import Any, Dict, List

import requests

RUNWAY_API_BASE = "https://api.runwayml.com/v1"
RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY", "")


def _auth_headers() -> Dict[str, str]:
    """Return headers required for authentication with Runway."""
    if not RUNWAY_API_KEY:
        # The API will reject requests without a token but we avoid raising
        # exceptions inside helper functions and instead let the caller handle
        # the resulting error response.
        return {"Content-Type": "application/json"}
    return {
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "Content-Type": "application/json",
    }


def list_generated_videos() -> List[Dict[str, Any]]:
    """Retrieve the list of previously generated videos from Runway."""
    try:
        resp = requests.get(
            f"{RUNWAY_API_BASE}/videos",
            headers=_auth_headers(),
            timeout=10,
        )
        resp.raise_for_status()
        payload = resp.json()
    except Exception:
        return []

    results = []
    for item in payload.get("results", []):
        # The Runway API returns different structures depending on the model.
        # We normalise the output into a minimal dictionary understood by the UI.
        url = item.get("asset_url")
        if not url:
            output = item.get("output") or {}
            if isinstance(output, list) and output:
                url = output[0].get("url")
            elif isinstance(output, dict):
                url = output.get("url") or output.get("video")
        results.append(
            {
                "title": item.get("title") or item.get("id"),
                "url": url,
                "created_at": item.get("created_at"),
            }
        )
    return results


def trigger_generation(prompt: str, settings: Dict[str, Any]) -> Dict[str, Any]:
    """Trigger a video generation on Runway using the given prompt and settings."""
    data: Dict[str, Any] = {"prompt": prompt}
    if settings:
        data.update(settings)
    resp = requests.post(
        f"{RUNWAY_API_BASE}/videos",
        json=data,
        headers=_auth_headers(),
        timeout=10,
    )
    # If the request fails, propagate the exception to the caller.
    resp.raise_for_status()
    return resp.json()
