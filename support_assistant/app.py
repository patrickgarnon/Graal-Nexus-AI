from flask import Flask, request, render_template, jsonify

from dashboard.make import MakeClient, get_campaign_stats, run_scenario

app = Flask(__name__)

OWNER_EMAIL = "patrickgarnon09@gmail.com"
MAKE_API_BASE = "https://api.make.com/v2"  # Placeholder base URL


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/install", methods=["POST"])
def install():
    api_token = request.form.get("api_token")
    scenario_id = request.form.get("scenario_id")
    if not api_token or not scenario_id:
        return "Missing credentials", 400
    try:
        result = run_scenario(api_token, scenario_id, base_url=MAKE_API_BASE)
    except Exception as exc:
        return f"Failed to trigger scenario: {exc}", 500
    status = result.get("status", "unknown")
    return f"Scenario {scenario_id} triggered with status {status}."


@app.route("/make/stats", methods=["GET"])
def make_stats():
    """Expose aggregated statistics about Make campaigns."""
    api_token = request.args.get("api_token")
    if not api_token:
        return "Missing api_token", 400
    client = MakeClient(api_token, base_url=MAKE_API_BASE)
    stats = get_campaign_stats(client)
    return jsonify(stats)


if __name__ == "__main__":
    app.run(debug=True)
