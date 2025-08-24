import os
from typing import Dict, List, Optional

import requests


class ShopifyClient:
    """Minimal client for querying the Shopify Orders API."""

    def __init__(self, store: str, access_token: str, api_version: str = "2023-07") -> None:
        self.store = store
        self.access_token = access_token
        self.api_version = api_version
        self.base_url = f"https://{store}/admin/api/{api_version}"

    def get_orders(self, since_id: Optional[int] = None) -> List[Dict]:
        """Return a list of orders newer than ``since_id``."""
        params = {"status": "any", "limit": 50}
        if since_id:
            params["since_id"] = since_id
        headers = {"X-Shopify-Access-Token": self.access_token}
        response = requests.get(f"{self.base_url}/orders.json", headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("orders", [])


def client_from_env() -> ShopifyClient:
    """Create a :class:`ShopifyClient` using environment variables.

    Required variables::

        SHOPIFY_STORE -- e.g. ``myshop.myshopify.com``
        SHOPIFY_ACCESS_TOKEN -- private app access token
    """
    store = os.getenv("SHOPIFY_STORE")
    token = os.getenv("SHOPIFY_ACCESS_TOKEN")
    if not store or not token:
        raise ValueError("Missing Shopify credentials")
    return ShopifyClient(store, token)
