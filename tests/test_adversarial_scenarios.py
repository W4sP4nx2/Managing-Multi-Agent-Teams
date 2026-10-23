from __future__ import annotations

import pytest
from pydantic import ValidationError

import assignments.starter_code.ex5_capstone_starter as capstone

pytestmark = pytest.mark.integration


def test_hallucinating_coder_payload_is_rejected_before_handoff() -> None:
    """Unknown model fields, including fabricated authority, fail the contract."""

    payload = {
        "files": {"slugify.py": "def slugify(text): return text.lower()"},
        "rationale": "Implement the requested function safely.",
        "tests_to_run": ["test_slugify"],
        "confidence": 150,
        "secret_key": "synthetic-secret",
    }

    with pytest.raises(ValidationError) as exc_info:
        capstone.CodePatch.model_validate(payload)

    rejected_fields = {str(error["loc"][0]) for error in exc_info.value.errors()}
    assert {"confidence", "secret_key"}.issubset(rejected_fields)


def test_infinite_coder_loop_stops_after_three_calls_and_escalates(monkeypatch) -> None:
    """A permanently failing deterministic coder cannot outlive its repair cap."""

    attempts: list[int] = []

    def always_failing_coder(task: capstone.TaskSpec, feedback: list[str]) -> capstone.CodePatch:
        attempts.append(len(feedback))
        return capstone.CodePatch(
            files={"slugify.py": "def slugify(text): return text.lower()"},
            rationale="Intentionally fails the whitespace contract.",
            tests_to_run=["test_slugify_spaces"],
        )

    monkeypatch.setattr(capstone, "code", always_failing_coder)
    summary = capstone.run_company("Create slugify(text) utility with tests.", max_repairs=2)

    assert len(attempts) == 3
    assert summary.status == "ESCALATED_TO_HUMAN"
    assert any("Repair budget exhausted" in event for event in summary.audit_trail)
    assert len(summary.tests) == 1


def test_sql_like_prompt_payload_is_rejected_by_typed_tool_boundary() -> None:
    """The lab's SQL-like string cannot smuggle an unmodeled field through a patch."""

    coder = capstone.AgentIdentity(
        role=capstone.Role.CODER,
        allowed_tools={capstone.Tool.WRITE_PATCH},
        trust_tier="confidential",
    )
    request = capstone.ToolRequest(
        caller=coder,
        tool=capstone.Tool.WRITE_PATCH,
        args={
            "patch": {
                "files": {"slugify.py": "def slugify(text): return text.lower()"},
                "rationale": "Implement the requested function safely.",
                "tests_to_run": ["test_slugify"],
                "user_id": "123; DROP TABLE users; --",
            }
        },
        sensitivity="confidential",
    )

    with pytest.raises(ValidationError, match="user_id"):
        capstone.ToolGateway().call(request)


def test_manager_role_cannot_write_code_even_if_scope_is_misconfigured() -> None:
    """Role-level separation of duties catches an overbroad Manager scope."""

    manager = capstone.AgentIdentity(
        role=capstone.Role.PM,
        allowed_tools={capstone.Tool.WRITE_PATCH},
        trust_tier="confidential",
    )
    request = capstone.ToolRequest(
        caller=manager,
        tool=capstone.Tool.WRITE_PATCH,
        args={
            "patch": {
                "files": {"slugify.py": "def slugify(text): return text.lower()"},
                "rationale": "Attempt to bypass separation of duties.",
                "tests_to_run": ["test_slugify"],
            }
        },
        sensitivity="confidential",
    )

    with pytest.raises(PermissionError, match="Only the coder"):
        capstone.ToolGateway().call(request)
