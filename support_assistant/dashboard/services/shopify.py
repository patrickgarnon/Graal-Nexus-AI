import os
import requests

API_BASE = os.getenv("SHOPIFY_API_URL", "").rstrip("/")
API_TOKEN = os.getenv("SHOPIFY_API_TOKEN")


def fetch_recent_sales(limit: int = 5):
    """Fetch recent sales orders from Shopify.

    Args:
        limit: Number of orders to retrieve.

    Returns:
        List of order dictionaries.
    """
    if not API_BASE or not API_TOKEN:
        raise RuntimeError("Missing Shopify API configuration")

    url = f"{API_BASE}/orders.json"
    headers = {"X-Shopify-Access-Token": API_TOKEN}
    params = {"limit": limit, "status": "any", "order": "created_at desc"}
    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return response.json().get("orders", [])
