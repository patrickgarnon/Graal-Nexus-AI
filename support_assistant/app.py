from flask import Flask, request, render_template
import requests
import argparse
import os

from nexus.logging import get_logger, setup_logging

app = Flask(__name__)
logger = get_logger(__name__)

OWNER_EMAIL = "patrickgarnon09@gmail.com"
MAKE_API_BASE = "https://api.make.com/v2"  # Placeholder base URL


def connect_to_make(api_token: str, scenario_id: str) -> dict:
    """Simulate triggering a Make scenario using the provided API token.
    The real implementation should handle errors and actual API calls.
    """

    logger.debug("Connecting to Make scenario %s", scenario_id)
    headers = {"Authorization": f"Token {api_token}", "Content-Type": "application/json"}
    # Example request (commented out as this environment has no external access)
    # response = requests.post(f"{MAKE_API_BASE}/scenarios/{scenario_id}/run", headers=headers)
    # logger.debug("Make API response: %s", response.text)
    # return response.json()
    logger.info("Simulated Make scenario %s triggered", scenario_id)
    return {"status": "connected", "scenario": scenario_id}


@app.route("/", methods=["GET"])
def index():
    logger.info("Rendering index page")
    return render_template("index.html")


@app.route("/install", methods=["POST"])
def install():
    logger.info("Install endpoint called")
    api_token = request.form.get("api_token")
    scenario_id = request.form.get("scenario_id")
    if not api_token or not scenario_id:
        logger.error("Missing credentials: api_token=%s scenario_id=%s", bool(api_token), bool(scenario_id))
        return "Missing credentials", 400
    logger.debug("Triggering Make scenario %s", scenario_id)
    result = connect_to_make(api_token, scenario_id)
    logger.info("Scenario %s triggered with status %s", result['scenario'], result['status'])
    return f"Scenario {result['scenario']} triggered with status {result['status']}."


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Support assistant service")
    parser.add_argument(
        "--log-level",
        default=None,
        help="Logging level (e.g. INFO, DEBUG, ERROR). Overrides LOG_LEVEL env var.",
    )
    args = parser.parse_args()
    setup_logging(args.log_level)
    logger.debug("Starting Flask app with log level %s", args.log_level or os.getenv("LOG_LEVEL", "INFO"))
    app.run(debug=True)
