"""Minimal Flask-based webhook receiver for Graal Nexus AI.

This server exposes a single /webhook endpoint that accepts POST requests.
When the optional WEBHOOK_SECRET environment variable is set, incoming
requests are validated against the `X-Hub-Signature-256` header (GitHub
style HMAC verification).

Usage::
    export WEBHOOK_SECRET="supersecret"
    python webhook.py

"""
from __future__ import annotations

import hashlib
import hmac
import os

from flask import Flask, abort, request


app = Flask(__name__)


def _verify_signature(payload: bytes, header: str, secret: str) -> bool:
    """Return True if the signature header matches the payload/secret."""
    try:
        sha_name, signature = header.split("=", 1)
    except ValueError:  # pragma: no cover - guard clause
        return False
    if sha_name != "sha256":
        return False
    mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)


@app.post("/webhook")
def handle_webhook():
    """Handle incoming webhook events.

    The raw payload is printed to stdout; depending on the source this could
    be JSON or any other data. If a secret is configured the request will be
    rejected unless the signature matches.
    """
    payload = request.data
    secret = os.environ.get("WEBHOOK_SECRET")
    signature_header = request.headers.get("X-Hub-Signature-256", "")
    if secret and not _verify_signature(payload, signature_header, secret):
        abort(403)
    event = request.headers.get("X-GitHub-Event", "unknown")
    print(f"Received event {event}: {payload.decode(errors='replace')}")
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
