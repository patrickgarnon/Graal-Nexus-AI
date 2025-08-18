from flask import Flask, request, render_template
import asyncio

from agents import run_scenarios

app = Flask(__name__)

OWNER_EMAIL = "patrickgarnon09@gmail.com"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/install", methods=["POST"])
def install():
    api_token = request.form.get("api_token")
    scenario_ids_raw = request.form.get("scenario_id")
    if not api_token or not scenario_ids_raw:
        return "Missing credentials", 400
    scenario_ids = [sid.strip() for sid in scenario_ids_raw.split(",")]
    results = asyncio.run(run_scenarios(api_token, scenario_ids))
    messages = [
        f"Scenario {res['scenario']} triggered with status {res['status']}"
        for res in results
    ]
    return "<br>".join(messages)


if __name__ == "__main__":
    app.run(debug=True)
