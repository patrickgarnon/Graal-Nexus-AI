from pathlib import Path

from flask import Flask, request, render_template
import requests

from src.core.retry import retry_on_exception, load_json

app = Flask(__name__)

OWNER_EMAIL = "patrickgarnon09@gmail.com"
CONFIG = load_json(Path(__file__).with_name("config.json"))
MAKE_API_BASE = CONFIG.get("MAKE_API_BASE", "https://api.make.com/v2")


@retry_on_exception(max_attempts=5, base=2)
def connect_to_make(api_token: str, scenario_id: str) -> dict:
    """Trigger a Make scenario using the provided API token."""
    headers = {"Authorization": f"Token {api_token}", "Content-Type": "application/json"}
    response = requests.post(f"{MAKE_API_BASE}/scenarios/{scenario_id}/run", headers=headers)
    response.raise_for_status()
    return response.json()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/install", methods=["POST"])
def install():
    api_token = request.form.get("api_token")
    scenario_id = request.form.get("scenario_id")
    if not api_token or not scenario_id:
        return "Missing credentials", 400
    try:
        result = connect_to_make(api_token, scenario_id)
    except requests.RequestException as exc:
        return f"Error triggering scenario: {exc}", 502
    return f"Scenario {result['scenario']} triggered with status {result['status']}."


if __name__ == "__main__":
    app.run(debug=True)
