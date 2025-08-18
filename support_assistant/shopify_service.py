import os
import sqlite3
from typing import List, Dict

import requests


class ShopifyService:
    """Service to interact with Shopify API and store sales history."""

    def __init__(self, api_key: str, password: str, shop_name: str, db_path: str = "sales.db"):
        self.api_key = api_key
        self.password = password
        self.shop_name = shop_name
        self.base_url = f"https://{shop_name}.myshopify.com/admin/api/2023-10"
        self.db_path = os.path.join(os.path.dirname(__file__), db_path)
        self._init_db()

    def _init_db(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                id TEXT PRIMARY KEY,
                amount REAL,
                created_at TEXT
            )
            """
        )
        conn.commit()
        conn.close()

    def fetch_orders(self) -> List[Dict]:
        """Fetch orders from Shopify."""
        url = f"{self.base_url}/orders.json?status=any"
        response = requests.get(url, auth=(self.api_key, self.password))
        response.raise_for_status()
        return response.json().get("orders", [])

    def sync_orders(self) -> List[Dict]:
        """Sync new orders and store them in SQLite."""
        orders = self.fetch_orders()
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        new_sales = []
        for order in orders:
            order_id = str(order["id"])
            amount = float(order["total_price"])
            created_at = order["created_at"]
            cur.execute("SELECT 1 FROM sales WHERE id=?", (order_id,))
            if not cur.fetchone():
                cur.execute(
                    "INSERT INTO sales (id, amount, created_at) VALUES (?, ?, ?)",
                    (order_id, amount, created_at),
                )
                new_sales.append({"id": order_id, "amount": amount, "created_at": created_at})
        conn.commit()
        conn.close()
        return new_sales

    def get_total_sales(self) -> float:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT SUM(amount) FROM sales")
        total = cur.fetchone()[0] or 0.0
        conn.close()
        return total


# Helper factory using environment variables

def service_from_env() -> ShopifyService:
    return ShopifyService(
        api_key=os.getenv("SHOPIFY_API_KEY", ""),
        password=os.getenv("SHOPIFY_PASSWORD", ""),
        shop_name=os.getenv("SHOPIFY_SHOP_NAME", ""),
    )

