from flask import Flask, request, render_template, send_file
import requests

from dashboard.elevenlabs import ensure_sample_audio, get_audio_path

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
    audio_id = ensure_sample_audio()
    return render_template("index.html", audio_id=audio_id)


@app.route("/install", methods=["POST"])
def install():
    api_token = request.form.get("api_token")
    scenario_id = request.form.get("scenario_id")
    if not api_token or not scenario_id:
        return "Missing credentials", 400
    result = connect_to_make(api_token, scenario_id)
    return f"Scenario {result['scenario']} triggered with status {result['status']}."


@app.route("/elevenlabs/audio/<audio_id>", methods=["GET"])
def elevenlabs_audio(audio_id: str):
    path = get_audio_path(audio_id)
    if path is None:
        return "Audio not found", 404
    mimetype = "audio/mpeg" if path.suffix == ".mp3" else "audio/wav"
    return send_file(path, mimetype=mimetype)


if __name__ == "__main__":
    app.run(debug=True)
