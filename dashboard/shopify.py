import os
import requests
from typing import Dict, Any


class ShopifyClient:
    """Minimal Shopify Admin REST API client."""

    def __init__(self, shop_name: str, access_token: str, api_version: str = "2023-07") -> None:
        self.base_url = f"https://{shop_name}.myshopify.com/admin/api/{api_version}"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "X-Shopify-Access-Token": access_token,
                "Content-Type": "application/json",
            }
        )

    def get_orders(self, status: str = "open", limit: int = 10) -> Dict[str, Any]:
        """Fetch a batch of orders from Shopify."""
        url = f"{self.base_url}/orders.json"
        params = {"status": status, "limit": limit}
        response = self.session.get(url, params=params)
        if response.ok:
            return response.json()
        return {"error": response.text, "status_code": response.status_code}
