import time
from typing import Dict
import requests


class MakeService:
    """Client simple pour l'API Make utilisant un token ou OAuth."""

    def __init__(self, api_token: str, base_url: str = "https://api.make.com/v2") -> None:
        self.api_token = api_token
        self.base_url = base_url.rstrip("/")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Token {self.api_token}",
            "Content-Type": "application/json",
        }

    def get_stats(self) -> Dict[str, float]:
        """Récupère les statistiques principales depuis l'API Make.

        Renvoie un dictionnaire avec les clés:
          - daily_executions: int
          - errors: int
          - average_time: float
        """
        url = f"{self.base_url}/stats"
        response = requests.get(url, headers=self._headers(), timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "daily_executions": data.get("daily_executions", 0),
            "errors": data.get("errors", 0),
            "average_time": data.get("average_time", 0.0),
        }
