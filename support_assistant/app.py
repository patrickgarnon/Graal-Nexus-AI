from flask import Flask, request, render_template, jsonify
import requests
from datetime import datetime, timedelta

from make_service import MakeService

app = Flask(__name__)

OWNER_EMAIL = "patrickgarnon09@gmail.com"
MAKE_API_BASE = "https://api.make.com/v2"  # Placeholder base URL

# Cache simple en mémoire pour les statistiques
CACHE = {}
CACHE_TTL = timedelta(minutes=5)


def connect_to_make(api_token: str, scenario_id: str) -> dict:
    """Simulate triggering a Make scenario using the provided API token.
    The real implementation should handle errors and actual API calls.
    """
    headers = {"Authorization": f"Token {api_token}", "Content-Type": "application/json"}
    # Example request (commented out as this environment has no external access)
    # response = requests.post(f"{MAKE_API_BASE}/scenarios/{scenario_id}/run", headers=headers)
    # return response.json()
    return {"status": "connected", "scenario": scenario_id}


def _get_cached_stats(token: str) -> dict:
    """Retourne les stats depuis le cache ou l'API."""
    cache_key = f"stats:{token}"
    entry = CACHE.get(cache_key)
    if entry:
        data, ts = entry
        if datetime.utcnow() - ts < CACHE_TTL:
            return data
    service = MakeService(token)
    data = service.get_stats()
    CACHE[cache_key] = (data, datetime.utcnow())
    return data


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/stats", methods=["GET"])
def stats_page():
    """Page HTML dédiée aux graphiques."""
    return render_template("stats.html")


@app.route("/install", methods=["POST"])
def install():
    api_token = request.form.get("api_token")
    scenario_id = request.form.get("scenario_id")
    if not api_token or not scenario_id:
        return "Missing credentials", 400
    result = connect_to_make(api_token, scenario_id)
    return f"Scenario {result['scenario']} triggered with status {result['status']}."


@app.route("/make/stats", methods=["GET"])
def make_stats():
    token = request.args.get("api_token") or request.headers.get("X-API-Token")
    if not token:
        return jsonify({"error": "Missing API token"}), 400
    data = _get_cached_stats(token)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
