from __future__ import annotations

"""Utility for building Make.com scenarios.

This module exposes :class:`MakeScenarioBuilder` which helps assemble a chain
of HTTP modules and insert them inside a scenario definition compatible with
Make (formerly Integromat).

The builder focuses on simplicity and does not aim to cover every feature of
Make.  It is sufficient for unit tests and for composing requests to common AI
APIs such as OpenRouter, Runway and ElevenLabs.
"""

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional


@dataclass
class HTTPModuleConfig:
    """Configuration for a single HTTP request step.

    Attributes
    ----------
    url:
        Endpoint to call.
    method:
        HTTP method to use. Defaults to ``"GET"``.
    headers:
        HTTP headers for the request.
    body:
        Optional body payload.
    name:
        Optional module name; if omitted a generic one is generated.
    """

    url: str
    method: str = "GET"
    headers: Dict[str, str] = field(default_factory=dict)
    body: Optional[Dict] = None
    name: Optional[str] = None


class MakeScenarioBuilder:
    """Helper object used to assemble Make scenarios."""

    def __init__(self) -> None:
        self._id_counter = 1

    # ------------------------------------------------------------------
    # Public helper constructors
    def build_openrouter_call(self, prompt: str) -> HTTPModuleConfig:
        """Return configuration for an OpenRouter completion call."""
        body = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt},
            ],
        }
        return HTTPModuleConfig(
            url="https://openrouter.ai/api/v1/chat/completions",
            method="POST",
            headers={"Content-Type": "application/json"},
            body=body,
            name="OpenRouter call",
        )

    def build_runway_call(self, media_url: str) -> HTTPModuleConfig:
        """Return configuration for a Runway media processing call."""
        return HTTPModuleConfig(
            url="https://api.runwayml.com/v1/tasks",
            method="POST",
            headers={"Content-Type": "application/json"},
            body={"media_url": media_url},
            name="Runway call",
        )

    def build_elevenlabs_call(self, text: str, voice: str) -> HTTPModuleConfig:
        """Return configuration for an ElevenLabs text-to-speech call."""
        return HTTPModuleConfig(
            url=f"https://api.elevenlabs.io/v1/text-to-speech/{voice}",
            method="POST",
            headers={"Content-Type": "application/json"},
            body={"text": text},
            name="ElevenLabs call",
        )

    # ------------------------------------------------------------------
    def chain_http_modules(self, step_configs: Iterable[HTTPModuleConfig]) -> List[Dict]:
        """Build a list of Make HTTP modules chained sequentially.

        Parameters
        ----------
        step_configs:
            Iterable of :class:`HTTPModuleConfig` describing each HTTP request.

        Returns
        -------
        list of dict
            The Make modules specification.  Each module contains an ``id`` and
            a reference to the next module to execute via the ``next`` field.
        """

        modules: List[Dict] = []
        step_configs = list(step_configs)
        for index, cfg in enumerate(step_configs, start=1):
            module: Dict = {
                "id": self._id_counter,
                "type": "http",
                "name": cfg.name or f"HTTP {self._id_counter}",
                "operation": {
                    "url": cfg.url,
                    "method": cfg.method,
                    "headers": cfg.headers,
                    "body": cfg.body,
                },
            }
            self._id_counter += 1
            if index < len(step_configs):
                module["next"] = self._id_counter
            modules.append(module)
        return modules

    def create_scenario(self, step_configs: Iterable[HTTPModuleConfig]) -> Dict:
        """Create a complete Make scenario definition.

        The scenario currently consists solely of the chained HTTP modules, but
        the method is designed so additional scenario-level metadata can easily
        be added in the future.
        """

        modules = self.chain_http_modules(step_configs)
        return {"modules": modules}
