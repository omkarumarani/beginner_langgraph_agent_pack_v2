"""Run one safe, local incident rehearsal."""
from pathlib import Path

import yaml

from workflow.graph import run_scenario


def main() -> None:
    scenarios = yaml.safe_load(Path("scenarios/golden.yaml").read_text())["scenarios"]
    result = run_scenario(scenarios[0])
    print("\nStarter Agent Result")
    print("=" * 40)
    for key in ("observation", "hypothesis", "diagnosis", "confidence", "recommendation", "verified"):
        print(f"{key}: {result[key]}")


if __name__ == "__main__":
    main()

