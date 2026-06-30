from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.enterprise_agent_team import CodeFile, CodePatch, TaskSpec


def test_task_spec_validation_accepts_actionable_contract() -> None:
    task = TaskSpec(
        goal="Implement add function",
        acceptance_criteria=[
            "Must handle positive integers",
            "Must handle negative integers",
        ],
        risk_level="low",
    )

    assert task.risk_level == "low"


def test_task_spec_validation_rejects_short_criterion() -> None:
    with pytest.raises(ValidationError):
        TaskSpec(
            goal="Implement add function",
            acceptance_criteria=["x"],
            risk_level="low",
        )


def test_code_patch_blocks_path_traversal() -> None:
    with pytest.raises(ValidationError) as exc:
        CodePatch(
            files=[CodeFile(path="../escape.py", content="bad")],
            rationale="Attempted unsafe patch path",
            tests_to_run=["test_escape"],
        )

    message = str(exc.value).lower()
    assert "escape" in message or "relative" in message


def test_code_patch_rejects_non_python_files() -> None:
    with pytest.raises(ValidationError):
        CodePatch(
            files=[CodeFile(path="README.md", content="bad")],
            rationale="Attempted non-python patch",
            tests_to_run=["test_docs"],
        )

