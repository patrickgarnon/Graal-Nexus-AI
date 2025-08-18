from flask import Flask, request, render_template
import logging
import requests

from src.utils.retry import retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

OWNER_EMAIL = "patrickgarnon09@gmail.com"
MAKE_API_BASE = "https://api.make.com/v2"  # Placeholder base URL


@retry(max_attempts=3, base_delay=1, jitter=0.5, exceptions=(requests.RequestException,), logger=logger)
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
    result = connect_to_make(api_token, scenario_id)
    return f"Scenario {result['scenario']} triggered with status {result['status']}."


if __name__ == "__main__":
    app.run(debug=True)
