"""HTTP clients for common AI service providers."""

from __future__ import annotations

from . import _requests as requests


class OpenRouterClient:
    """Client for the OpenRouter API."""

    def __init__(self, api_key: str, base_url: str = "https://openrouter.ai/api/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def invoke(self, prompt: str, model: str = "gpt-3.5-turbo", **kwargs) -> dict:
        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        }
        payload.update(kwargs)
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()


class RunwayClient:
    """Client for the RunwayML API."""

    def __init__(self, api_key: str, base_url: str = "https://api.runwayml.com/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def invoke(self, model: str, inputs: dict) -> dict:
        url = f"{self.base_url}/models/{model}/invoke"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(url, headers=headers, json={"input": inputs})
        response.raise_for_status()
        return response.json()


class ElevenLabsClient:
    """Client for the ElevenLabs API."""

    def __init__(self, api_key: str, base_url: str = "https://api.elevenlabs.io/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def invoke(self, text: str, voice: str = "default") -> dict:
        url = f"{self.base_url}/text-to-speech/{voice}"
        headers = {"xi-api-key": self.api_key}
        response = requests.post(url, headers=headers, json={"text": text})
        response.raise_for_status()
        return response.json()
