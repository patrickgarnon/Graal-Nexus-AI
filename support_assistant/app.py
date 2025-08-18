from flask import Flask, request, render_template, jsonify
import requests
from typing import List

from runway_service import RunwayVideo, create_video

app = Flask(__name__)

videos: List[RunwayVideo] = []

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


def _video_to_dict(video: RunwayVideo) -> dict:
    return {
        "id": video.id,
        "title": video.title,
        "url": video.url,
        "date": video.date.isoformat(),
        "status": video.status,
    }


@app.route("/runway/videos", methods=["GET"])
def list_runway_videos():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    start = (page - 1) * per_page
    end = start + per_page
    data = [_video_to_dict(v) for v in videos[start:end]]
    return jsonify({"videos": data, "page": page, "total": len(videos)})


@app.route("/runway/generate", methods=["POST"])
def generate_runway_video():
    payload = request.get_json() or {}
    prompt = payload.get("prompt")
    params = payload.get("params", {})
    if not prompt:
        return jsonify({"error": "prompt is required"}), 400
    video = create_video(prompt, params, api_key="")
    videos.append(video)
    return jsonify(_video_to_dict(video)), 201


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
