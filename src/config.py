from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Directories containing JSON definitions
AGENTS_DIR = BASE_DIR / "data" / "agents"
SCENARIOS_DIR = BASE_DIR / "data" / "scenarios"
