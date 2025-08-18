from flask import Flask, request, render_template
import requests
import base64
import os
import sys

# Ensure root path is importable for dashboard services
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from dashboard.services.elevenlabs import generate_audio

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


@app.route("/elevenlabs", methods=["GET", "POST"])
def elevenlabs_page():
    """Render form to generate audio using ElevenLabs and play it."""
    audio_url = None
    # Example list of available voices. In production, fetch from API if needed.
    voices = {
        "Rachel": "21m00Tcm4TlvDq8ikWAM",
        "Domi": "AZnzlk1XvdvUeBnXmlld",
    }

    if request.method == "POST":
        text = request.form.get("text")
        voice_id = request.form.get("voice_id")
        if text and voice_id:
            try:
                audio_bytes = generate_audio(text, voice_id)
                audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
                audio_url = f"data:audio/mpeg;base64,{audio_b64}"
            except Exception as exc:
                return f"Erreur lors de la génération audio: {exc}", 500

    return render_template("elevenlabs.html", voices=voices, audio_url=audio_url)


if __name__ == "__main__":
    app.run(debug=True)
