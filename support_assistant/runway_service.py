from dataclasses import dataclass
from datetime import datetime
from typing import Dict

import requests

RUNWAY_API_BASE = "https://api.runwayml.com/v1"  # Placeholder base URL


@dataclass
class RunwayVideo:
    id: str
    title: str
    url: str
    date: datetime
    status: str


def create_video(prompt: str, params: Dict[str, str], api_key: str) -> RunwayVideo:
    """Create a video via the Runway API."""
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"prompt": prompt, **params}
    # response = requests.post(f"{RUNWAY_API_BASE}/videos", json=payload, headers=headers)
    # data = response.json()
    # Mocked response for offline environment
    data = {
        "id": f"vid_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "title": prompt,
        "url": "",
        "status": "processing",
        "created_at": datetime.utcnow().isoformat(),
    }
    return RunwayVideo(
        id=data["id"],
        title=data["title"],
        url=data["url"],
        date=datetime.fromisoformat(data["created_at"]),
        status=data["status"],
    )


def get_video_status(video_id: str, api_key: str) -> RunwayVideo:
    """Retrieve the status of a Runway video."""
    headers = {"Authorization": f"Bearer {api_key}"}
    # response = requests.get(f"{RUNWAY_API_BASE}/videos/{video_id}", headers=headers)
    # data = response.json()
    # Mocked response for offline environment
    data = {
        "id": video_id,
        "title": "Sample",
        "url": "https://example.com/video.mp4",
        "status": "completed",
        "created_at": datetime.utcnow().isoformat(),
    }
    return RunwayVideo(
        id=data["id"],
        title=data["title"],
        url=data["url"],
        date=datetime.fromisoformat(data["created_at"]),
        status=data["status"],
    )
