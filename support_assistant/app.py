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


def generate_runway_video(prompt: str) -> dict:
    """Simulate a Runway video generation call.
    This placeholder simply returns the prompt back with a dummy status.
    """
    # Example request (commented out as this environment has no external access)
    # response = requests.post("https://api.runwayml.com/v1/generate", json={"prompt": prompt})
    # return response.json()
    return {"status": "generated", "prompt": prompt}


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/make/run", methods=["POST"])
def make_run():
    data = request.get_json(silent=True) or {}
    api_token = data.get("api_token") or request.form.get("api_token")
    scenario_id = data.get("scenario_id") or request.form.get("scenario_id")
    if not api_token or not scenario_id:
        return jsonify({"error": "Missing credentials"}), 400
    result = connect_to_make(api_token, scenario_id)
    return jsonify(result)


@app.route("/runway/generate", methods=["POST"])
def runway_generate():
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt") or request.form.get("prompt")
    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400
    result = generate_runway_video(prompt)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
