"""Tests PyTest — microservice Graal Health Leads."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from health_leads import brevo_client, sheets_client
from health_leads.main import app, limiter

client = TestClient(app)

VALID_PAYLOAD = {
    "email": "patrick.garnon@sanoja.ai",
    "first_name": "Patrick",
    "consent_given": True,
}


@pytest.fixture(autouse=True)
def _reset_rate_limiter():
    limiter.reset()
    yield
    limiter.reset()


@pytest.fixture(autouse=True)
def _mock_external_calls(monkeypatch):
    async def _fake_send_email(**kwargs):
        return {"messageId": "test-message-id"}

    async def _fake_push_to_sheet(**kwargs):
        return None

    monkeypatch.setattr(brevo_client, "send_transactional_email", _fake_send_email)
    monkeypatch.setattr(sheets_client, "push_lead_to_sheet", _fake_push_to_sheet)


def test_health_check_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "graal-health-leads"


def test_valid_signup_with_consent_returns_201():
    response = client.post("/api/v1/graal/lead-capture", json=VALID_PAYLOAD)
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "accepted"
    assert len(body["lead_id"]) > 0


def test_reject_missing_consent_returns_400():
    payload = {**VALID_PAYLOAD, "consent_given": False}
    response = client.post("/api/v1/graal/lead-capture", json=payload)
    assert response.status_code == 400
    assert "consentement" in response.json()["detail"].lower()


def test_invalid_email_regex_returns_422():
    payload = {**VALID_PAYLOAD, "email": "pas-un-email"}
    response = client.post("/api/v1/graal/lead-capture", json=payload)
    assert response.status_code == 422


def test_missing_required_field_returns_422():
    payload = {**VALID_PAYLOAD}
    del payload["consent_given"]
    response = client.post("/api/v1/graal/lead-capture", json=payload)
    assert response.status_code == 422


def test_rate_limiter_blocks_after_threshold():
    for _ in range(5):
        response = client.post("/api/v1/graal/lead-capture", json=VALID_PAYLOAD)
        assert response.status_code == 201

    response = client.post("/api/v1/graal/lead-capture", json=VALID_PAYLOAD)
    assert response.status_code == 429
