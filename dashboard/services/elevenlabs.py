import os
import requests

ELEVENLABS_BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech"


def generate_audio(text: str, voice_id: str) -> bytes:
    """Generate speech audio from text using the ElevenLabs API.

    Args:
        text: The text to convert to speech.
        voice_id: Identifier of the voice to use.

    Returns:
        Raw audio bytes in MP3 format.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY environment variable is not set.")

    url = f"{ELEVENLABS_BASE_URL}/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {"text": text}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.content
