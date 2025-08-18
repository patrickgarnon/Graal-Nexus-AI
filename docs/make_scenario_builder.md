# Make Scenario Builder

Utilities for constructing and running [Make.com](https://www.make.com/) scenarios.

## Installation

```bash
pip install -r requirements.txt  # if a requirements file exists
```

The modules live under `scripts/make_scenario_builder` and can be imported in
Python via:

```python
from scripts.make_scenario_builder import (
    MakeAPI,
    create_scenario,
    clone_scenario,
    update_scenario,
    run_scenario,
    chain_http_modules,
    OpenRouterClient,
    RunwayClient,
    ElevenLabsClient,
    run_autopilot,
)
```

## Usage

### Managing Scenarios

```python
api = MakeAPI("<api-key>")
scenario = create_scenario(api, "demo", modules=[{"type": "http", "url": "https://example.com"}])
clone = clone_scenario(api, scenario["id"])
update_scenario(api, clone["id"], {"name": "updated"})
run_scenario(api, clone["id"])
```

### Chaining HTTP Modules

```python
chain_http_modules(api, clone["id"], ["https://a.com", "https://b.com"])
```

### Provider Clients

```python
orc = OpenRouterClient("<key>")
orc.invoke("Hello, world!")
```

### Autopilot

```python
result = run_autopilot(api, clone["id"], [{"name": "tuned"}])
```

This will run the scenario and apply adjustments if the execution fails.
