import os
import uuid
import wave
import struct
from pathlib import Path
from typing import Optional

import requests

ELEVENLABS_BASE_URL = "https://api.elevenlabs.io/v1"
AUDIO_DIR = Path(__file__).resolve().parent.parent / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def text_to_speech(text: str, voice: str, api_key: str) -> str:
    """Generate speech using ElevenLabs API and store it locally.

    Returns the identifier of the stored audio file.
    """
    headers = {"xi-api-key": api_key}
    url = f"{ELEVENLABS_BASE_URL}/text-to-speech/{voice}"
    response = requests.post(url, headers=headers, json={"text": text})
    response.raise_for_status()

    audio_id = str(uuid.uuid4())
    path = AUDIO_DIR / f"{audio_id}.mp3"
    with open(path, "wb") as f:
        f.write(response.content)
    return audio_id


def get_audio_path(audio_id: str) -> Optional[Path]:
    """Return path to a stored audio file if it exists."""
    path = AUDIO_DIR / f"{audio_id}.mp3"
    if path.exists():
        return path
    path = AUDIO_DIR / f"{audio_id}.wav"
    if path.exists():
        return path
    return None


def ensure_sample_audio() -> str:
    """Create a silent sample audio file for demonstration purposes.

    Returns the identifier of the sample file.
    """
    sample_id = "sample"
    sample_path = AUDIO_DIR / f"{sample_id}.wav"
    if not sample_path.exists():
        framerate = 44100
        duration = 1  # seconds
        amplitude = 0
        with wave.open(str(sample_path), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(framerate)
            frames = (struct.pack("<h", amplitude) for _ in range(duration * framerate))
            w.writeframes(b"".join(frames))
    return sample_id
