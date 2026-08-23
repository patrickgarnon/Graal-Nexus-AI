import os

from flask import Flask, request, render_template, redirect, url_for
import requests

from dashboard.services.make import fetch_campaign_stats, trigger_scenario

app = Flask(__name__)

OWNER_EMAIL = "patrickgarnon09@gmail.com"
MAKE_API_BASE = "https://api.make.com/v2"  # Placeholder base URL


def connect_to_make(api_token: str, scenario_id: str) -> dict:
    """Trigger a Make scenario using the provided API token."""
    return trigger_scenario(api_token, scenario_id)


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


@app.route("/make", methods=["GET"])
def make_dashboard():
    api_token = request.args.get("api_token")
    scenario_id = request.args.get("scenario_id")
    status = request.args.get("status")
    stats = None
    if api_token and scenario_id:
        stats = fetch_campaign_stats(api_token, scenario_id)
    return render_template(
        "make.html",
        stats=stats,
        api_token=api_token,
        scenario_id=scenario_id,
        status=status,
    )


@app.route("/make/trigger/<scenario_id>", methods=["POST"])
def trigger_make(scenario_id):
    api_token = request.form.get("api_token")
    if not api_token:
        return "Missing API token", 400
    result = trigger_scenario(api_token, scenario_id)
    status = "success" if result.get("status") == "success" else "error"
    return redirect(
        url_for(
            "make_dashboard",
            api_token=api_token,
            scenario_id=scenario_id,
            status=status,
        )
    )


if __name__ == "__main__":
    # Voir dashboard/app.py pour la justification : debug=True est un
    # risque d'exécution de code arbitraire si ce port est jamais exposé
    # au-delà de localhost. Désactivé par défaut.
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug_mode)
