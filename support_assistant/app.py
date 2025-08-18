import os
from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Configuration from environment variables with sensible defaults
OWNER_EMAIL = os.getenv("OWNER_EMAIL", "patrickgarnon09@gmail.com")
MAKE_API_BASE = os.getenv("MAKE_API_BASE", "https://api.make.com/v2")  # Placeholder base URL


def connect_to_make(api_token: str, scenario_id: str) -> dict:
    """Simulate triggering a Make scenario using the provided API token.
    The real implementation should handle errors and actual API calls.
    """
    headers = {"Authorization": f"Token {api_token}", "Content-Type": "application/json"}
    # Example request (commented out as this environment has no external access)
    # response = requests.post(f"{MAKE_API_BASE}/scenarios/{scenario_id}/run", headers=headers)
    # return response.json()
    return {"status": "connected", "scenario": scenario_id}


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/install", methods=["POST"])
def install():
    api_token = request.form.get("api_token")
    scenario_id = request.form.get("scenario_id")
    if not api_token or not scenario_id:
        return "Missing credentials", 400
    result = connect_to_make(api_token, scenario_id)
    return f"Scenario {result['scenario']} triggered with status {result['status']}."


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("DEBUG", "True").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)
