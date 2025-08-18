from flask import Flask, request, render_template, jsonify
import os
import requests

from integrations.runway import init_db, get_history, sync_jobs

app = Flask(__name__)
init_db()

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


@app.route("/runway/history", methods=["GET"])
def runway_history():
    api_key = os.environ.get("RUNWAY_API_KEY")
    if api_key:
        try:
            sync_jobs(api_key)
        except requests.RequestException:
            pass
    videos = get_history()
    return jsonify(videos)


@app.route("/runway/history/ui", methods=["GET"])
def runway_history_ui():
    videos = get_history()
    return render_template("runway_history.html", videos=videos)


if __name__ == "__main__":
    app.run(debug=True)
