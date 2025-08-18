import requests

ELEVENLABS_API_BASE = "https://api.elevenlabs.io/v1"

def get_voice_audio(api_key: str, voice_id: str, text: str) -> bytes:
    """Generate speech audio using ElevenLabs API.

    Args:
        api_key: ElevenLabs API key.
        voice_id: Identifier of the voice to use.
        text: Text to synthesize.

    Returns:
        Audio content in MPEG format as bytes.
    """
    headers = {
        "xi-api-key": api_key,
        "Accept": "audio/mpeg",
    }
    data = {"text": text}
    response = requests.post(
        f"{ELEVENLABS_API_BASE}/text-to-speech/{voice_id}",
        headers=headers,
        json=data,
    )
    response.raise_for_status()
    return response.content
