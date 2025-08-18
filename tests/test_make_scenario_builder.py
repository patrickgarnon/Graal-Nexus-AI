import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from make_scenario_builder import MakeScenarioBuilder


def test_chain_http_modules_and_helpers():
    builder = MakeScenarioBuilder()
    steps = [
        builder.build_openrouter_call("Hello"),
        builder.build_runway_call("https://example.com/video.mp4"),
        builder.build_elevenlabs_call("Hi", "voice-id"),
    ]

    modules = builder.chain_http_modules(steps)

    assert len(modules) == 3
    assert all(m["type"] == "http" for m in modules)
    assert modules[0]["next"] == modules[1]["id"]
    assert modules[1]["next"] == modules[2]["id"]
    assert "next" not in modules[-1]


def test_create_scenario_embeds_modules():
    builder = MakeScenarioBuilder()
    steps = [builder.build_openrouter_call("Test")]
    scenario = builder.create_scenario(steps)
    assert "modules" in scenario
    assert len(scenario["modules"]) == 1
