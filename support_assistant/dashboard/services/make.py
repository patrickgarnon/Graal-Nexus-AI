"""Make API service utilities."""

import requests

MAKE_API_BASE = "https://api.make.com/v2"

def trigger_scenario(api_token: str, scenario_id: str) -> dict:
    """Trigger a Make scenario and return the execution status."""
    headers = {"Authorization": f"Token {api_token}", "Content-Type": "application/json"}
    url = f"{MAKE_API_BASE}/scenarios/{scenario_id}/executions"
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return {"status": "success"}
    except requests.RequestException as exc:  # pragma: no cover - network errors
        return {"status": "error", "message": str(exc)}

def fetch_campaign_stats(api_token: str, scenario_id: str) -> dict:
    """Fetch execution statistics for a Make scenario."""
    headers = {"Authorization": f"Token {api_token}", "Content-Type": "application/json"}
    url = f"{MAKE_API_BASE}/scenarios/{scenario_id}/executions"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        executions = response.json().get("data", [])
        execution_count = len(executions)
        success_count = sum(1 for e in executions if e.get("status") == "success")
        success_rate = (success_count / execution_count * 100) if execution_count else 0
        messages = [e.get("message", "") for e in executions[-5:]]
        return {
            "execution_count": execution_count,
            "success_rate": success_rate,
            "messages": messages,
        }
    except requests.RequestException as exc:  # pragma: no cover - network errors
        return {"error": str(exc)}
