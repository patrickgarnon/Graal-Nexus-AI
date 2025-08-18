import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import MagicMock, patch

from scripts.make_scenario_builder.api import MakeAPI
from scripts.make_scenario_builder import builder
from scripts.make_scenario_builder.providers import (
    OpenRouterClient,
    RunwayClient,
    ElevenLabsClient,
)
from scripts.make_scenario_builder.autopilot import run_autopilot


# ---------------------------------------------------------------------------
# API wrapper tests
# ---------------------------------------------------------------------------

def test_makeapi_crud_and_run():
    api = MakeAPI("token")
    with patch("scripts.make_scenario_builder.api.requests.post") as post, \
         patch("scripts.make_scenario_builder.api.requests.get") as get, \
         patch("scripts.make_scenario_builder.api.requests.put") as put:

        post.return_value.json.return_value = {"id": 1}
        post.return_value.raise_for_status.return_value = None
        assert api.create_scenario({"name": "demo"}) == {"id": 1}
        post.assert_called_with(
            "https://api.make.com/v2/scenarios",
            headers={"Authorization": "Bearer token"},
            json={"name": "demo"},
        )

        post.reset_mock()
        post.return_value.json.return_value = {"status": "success"}
        api.run_scenario(1)
        post.assert_called_with(
            "https://api.make.com/v2/scenarios/1/run",
            headers={"Authorization": "Bearer token"},
        )

        get.return_value.json.return_value = {"id": 1}
        get.return_value.raise_for_status.return_value = None
        api.read_scenario(1)
        get.assert_called_with(
            "https://api.make.com/v2/scenarios/1",
            headers={"Authorization": "Bearer token"},
        )

        put.return_value.json.return_value = {"ok": True}
        put.return_value.raise_for_status.return_value = None
        api.update_scenario(1, {"name": "x"})
        put.assert_called_with(
            "https://api.make.com/v2/scenarios/1",
            headers={"Authorization": "Bearer token"},
            json={"name": "x"},
        )


# ---------------------------------------------------------------------------
# Builder tests
# ---------------------------------------------------------------------------

def test_builder_functions():
    api = MagicMock(spec=MakeAPI)
    api.read_scenario.return_value = {"id": 1, "name": "orig"}

    builder.create_scenario(api, "new", [1])
    api.create_scenario.assert_called_with({"name": "new", "modules": [1]})

    builder.clone_scenario(api, 1)
    api.read_scenario.assert_called_with(1)
    api.create_scenario.assert_called_with({"name": "orig (clone)"})

    builder.update_scenario(api, 1, {"x": 2})
    api.update_scenario.assert_called_with(1, {"x": 2})

    builder.run_scenario(api, 1)
    api.run_scenario.assert_called_with(1)

    builder.chain_http_modules(api, 1, ["u1", "u2"])
    api.update_scenario.assert_called_with(
        1,
        {
            "modules": [
                {"type": "http", "url": "u1"},
                {"type": "http", "url": "u2"},
            ]
        },
    )


# ---------------------------------------------------------------------------
# Provider tests
# ---------------------------------------------------------------------------

def test_provider_clients():
    with patch("scripts.make_scenario_builder.providers.requests.post") as post:
        post.return_value.json.return_value = {"result": 1}
        post.return_value.raise_for_status.return_value = None

        orc = OpenRouterClient("k")
        assert orc.invoke("hi") == {"result": 1}
        url, kwargs = post.call_args
        assert url[0] == "https://openrouter.ai/api/v1/chat/completions"
        assert kwargs["headers"] == {"Authorization": "Bearer k"}

        rc = RunwayClient("k")
        rc.invoke("model", {"a": 1})
        url, kwargs = post.call_args
        assert url[0] == "https://api.runwayml.com/v1/models/model/invoke"
        assert kwargs["json"] == {"input": {"a": 1}}

        el = ElevenLabsClient("k")
        el.invoke("text")
        url, kwargs = post.call_args
        assert url[0] == "https://api.elevenlabs.io/v1/text-to-speech/default"
        assert kwargs["headers"] == {"xi-api-key": "k"}


# ---------------------------------------------------------------------------
# Autopilot tests
# ---------------------------------------------------------------------------

def test_run_autopilot_updates_on_failure():
    api = object()
    with patch("scripts.make_scenario_builder.autopilot.run_scenario") as run, \
         patch("scripts.make_scenario_builder.autopilot.update_scenario") as upd:
        run.side_effect = [
            {"status": "error"},
            {"status": "success"},
        ]
        result = run_autopilot(api, 1, [{"modules": []}])
        assert result["status"] == "success"
        upd.assert_called_once_with(api, 1, {"modules": []})
        assert run.call_count == 2
