import os
import sys
import json
import time

from flask import Flask, request, render_template, jsonify, Response, stream_with_context
import requests

# Allow imports from parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dashboard.shopify import ShopifyClient

app = Flask(__name__)

OWNER_EMAIL = "patrickgarnon09@gmail.com"
MAKE_API_BASE = "https://api.make.com/v2"  # Placeholder base URL

# Initialize Shopify client using environment variables as defaults
shopify_client = ShopifyClient(
    shop_name=os.environ.get("SHOPIFY_SHOP_NAME", "demo"),
    access_token=os.environ.get("SHOPIFY_ACCESS_TOKEN", "demo"),
)


def connect_to_make(api_token: str, scenario_id: str) -> dict:
    """Simulate triggering a Make scenario using the provided API token.
    The real implementation should handle errors and actual API calls.
    """
    headers = {"Authorization": f"Token {api_token}", "Content-Type": "application/json"}
    # Example request (commented out as this environment has no external access)
    # response = requests.post(f"{MAKE_API_BASE}/scenarios/{scenario_id}/run", headers=headers)
    # return response.json()
    return {"status": "connected", "scenario": scenario_id}


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/install", methods=["POST"])
def install():
    api_token = request.form.get("api_token")
    scenario_id = request.form.get("scenario_id")
    if not api_token or not scenario_id:
        return "Missing credentials", 400
    result = connect_to_make(api_token, scenario_id)
    return f"Scenario {result['scenario']} triggered with status {result['status']}."


@app.route("/shopify/sales", methods=["GET"])
def shopify_sales():
    """Return a batch of Shopify sales."""
    try:
        orders = shopify_client.get_orders()
        return jsonify(orders)
    except Exception as exc:  # pragma: no cover - simple error propagation
        return jsonify({"error": str(exc)}), 500


def _sales_stream():
    """Yield new sales as Server-Sent Events."""
    seen = set()
    while True:
        orders = shopify_client.get_orders().get("orders", [])
        for order in orders:
            oid = order.get("id")
            if oid not in seen:
                seen.add(oid)
                data = json.dumps(order)
                yield f"data: {data}\n\n"
        time.sleep(5)


@app.route("/shopify/sales/stream")
def stream_sales():
    """Stream sales updates to the client using EventSource."""
    return Response(stream_with_context(_sales_stream()), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True)
