from flask import Flask, request, render_template
import requests
from flask_socketio import SocketIO

from integrations.shopify import client_from_env

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

OWNER_EMAIL = "patrickgarnon09@gmail.com"
MAKE_API_BASE = "https://api.make.com/v2"  # Placeholder base URL

# Shopify client (optional if env vars not provided)
try:
    shopify_client = client_from_env()
except Exception:
    shopify_client = None


def poll_orders() -> None:
    """Background task polling Shopify for new orders and emitting them."""
    if not shopify_client:
        return
    last_id = None
    while True:
        try:
            orders = shopify_client.get_orders(since_id=last_id)
            for order in orders:
                socketio.emit("order", order, namespace="/shopify-stream")
                order_id = order.get("id")
                if order_id:
                    last_id = max(last_id or 0, order_id)
        except Exception:
            pass
        socketio.sleep(10)


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


@socketio.on("connect", namespace="/shopify-stream")
def shopify_stream_connect():
    # Connection event placeholder
    pass


@app.route("/install", methods=["POST"])
def install():
    api_token = request.form.get("api_token")
    scenario_id = request.form.get("scenario_id")
    if not api_token or not scenario_id:
        return "Missing credentials", 400
    result = connect_to_make(api_token, scenario_id)
    return f"Scenario {result['scenario']} triggered with status {result['status']}."


if __name__ == "__main__":
    if shopify_client:
        socketio.start_background_task(poll_orders)
    socketio.run(app, debug=True)
