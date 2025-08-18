from flask import Flask, request, render_template, jsonify
import requests
from integrations.make import get_scenario_stats

app = Flask(__name__)

OWNER_EMAIL = "patrickgarnon09@gmail.com"
MAKE_API_BASE = "https://api.make.com/v2"  # Placeholder base URL


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


@app.route("/make/stats", methods=["GET"])
def make_stats():
    api_token = request.args.get("api_token")
    scenario_id = request.args.get("scenario_id")
    if not api_token or not scenario_id:
        return jsonify({"error": "Missing credentials"}), 400
    stats = get_scenario_stats(api_token, scenario_id)
    return jsonify(stats)


@app.route("/make/dashboard", methods=["GET"])
def make_dashboard():
    return render_template("make_stats.html")


if __name__ == "__main__":
    app.run(debug=True)
