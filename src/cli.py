import argparse
import json
from core.app import App


def main() -> None:
    """Entry point for the command line interface."""
    parser = argparse.ArgumentParser(description="Graal Nexus CLI")
    parser.add_argument("category", choices=["agents", "scenarios", "prompts"], help="Type of resource to load")
    parser.add_argument("--name", help="Specific resource name to display")
    args = parser.parse_args()

    app = App()
    loader = getattr(app, f"load_{args.category}")
    data = loader()

    if args.name:
        item = data.get(args.name)
        if item is None:
            print(f"{args.category[:-1].capitalize()} '{args.name}' not found.")
            return
        if isinstance(item, dict):
            print(json.dumps(item, indent=2, ensure_ascii=False))
        else:
            print(item)
    else:
        for key in data:
            print(key)


if __name__ == "__main__":
    main()
