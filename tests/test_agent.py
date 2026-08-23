from pathlib import Path

import yaml

from workflow.graph import run_scenario


def scenarios() -> list[dict]:
    return yaml.safe_load(Path("scenarios/golden.yaml").read_text())["scenarios"]


def test_database_issue_is_escalated() -> None:
    result = run_scenario(scenarios()[0])
    assert result["recommendation"] == "incident.escalate"
    assert result["verified"] is False


def test_deployment_regression_can_recommend_rollback() -> None:
    result = run_scenario(scenarios()[1])
    assert result["recommendation"] == "application.rollback_deployment"
    assert result["confidence"] >= 0.70
    assert result["verified"] is True