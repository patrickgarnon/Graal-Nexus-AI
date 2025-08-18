from flask import Flask, request, render_template, jsonify
import requests

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


def make_service(scenario_id: str) -> dict:
    """Stub for running a Make scenario.
    Replace this with real implementation when available.
    """
    # Example service call (commented out)
    # response = requests.post(f"{MAKE_API_BASE}/scenarios/{scenario_id}/run")
    # return response.json()
    return {"status": "started", "scenario": scenario_id}


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


@app.route("/make/run-scenario", methods=["POST"])
def run_scenario():
    data = request.get_json()
    scenario_id = data.get("scenario_id") if data else None
    if not scenario_id:
        return jsonify({"error": "Missing scenario_id"}), 400
    result = make_service(scenario_id)
    return jsonify(result)


def runway_generate_service(prompt: str, model: str) -> dict:
    """Stub for generating content with Runway model."""
    # Example API call would go here
    return {"status": "generated", "model": model, "prompt": prompt}


@app.route("/runway/generate", methods=["POST"])
def runway_generate():
    data = request.get_json()
    prompt = data.get("prompt") if data else None
    model = data.get("model") if data else None
    if not prompt or not model:
        return jsonify({"error": "Missing prompt or model"}), 400
    result = runway_generate_service(prompt, model)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
