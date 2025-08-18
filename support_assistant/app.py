from flask import Flask, request, render_template, jsonify
import requests
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)

OWNER_EMAIL = "patrickgarnon09@gmail.com"
MAKE_API_BASE = "https://api.make.com/v2"  # Placeholder base URL


@lru_cache(maxsize=32)
def connect_to_make(api_token: str, scenario_id: str) -> dict:
    """Simulate triggering a Make scenario using the provided API token.
    The real implementation should handle errors and actual API calls.

    Results are cached to avoid repeating identical calls.
    """
    headers = {"Authorization": f"Token {api_token}", "Content-Type": "application/json"}
    # Example request (commented out as this environment has no external access)
    # response = requests.post(f"{MAKE_API_BASE}/scenarios/{scenario_id}/run", headers=headers)
    # return response.json()
    return {"status": "connected", "scenario": scenario_id}


def publish_to_channels(api_token: str, scenario_ids: list[str]) -> dict:
    """Trigger multiple scenarios in parallel."""
    results = {}
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(connect_to_make, api_token, sid.strip()): sid.strip()
            for sid in scenario_ids
        }
        for future in as_completed(futures):
            sid = futures[future]
            try:
                results[sid] = future.result()
            except Exception as exc:  # pragma: no cover - demonstration only
                results[sid] = {"status": "error", "detail": str(exc)}
    return results


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/install", methods=["POST"])
def install():
    api_token = request.form.get("api_token")
    scenario_id = request.form.get("scenario_id")
    if not api_token or not scenario_id:
        return "Missing credentials", 400
    # Allow comma-separated IDs for multichannel publication
    if "," in scenario_id:
        ids = scenario_id.split(",")
        results = publish_to_channels(api_token, ids)
        return jsonify(results)
    result = connect_to_make(api_token, scenario_id.strip())
    return f"Scenario {result['scenario']} triggered with status {result['status']}."


@app.route("/cache/clear", methods=["POST"])
def clear_cache():
    """Endpoint to invalidate cached Make responses."""
    connect_to_make.cache_clear()
    return "Cache cleared", 200


if __name__ == "__main__":
    app.run(debug=True)
