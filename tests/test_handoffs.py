from __future__ import annotations

import json

from src.enterprise_agent_team import (
    AgentRole,
    CodeFile,
    CodePatch,
    MemoryRecord,
    SharedAgenticMemory,
    TrustTier,
    coder_generate_patch,
    product_manager_parse_issue,
    run_python_patch_tests,
)


def test_pm_to_coder_handoff() -> None:
    """Verify the PM's typed TaskSpec becomes a valid coder input."""

    task = product_manager_parse_issue("Create safe add function")
    assert task.goal
    assert len(task.acceptance_criteria) >= 1

    memory = SharedAgenticMemory()
    memory.add(
        MemoryRecord(
            text=json.dumps(task.model_dump(mode="json")),
            tags={"task", "acceptance"},
            sensitivity=TrustTier.CONFIDENTIAL,
            author=AgentRole.PRODUCT_MANAGER,
        )
    )

    patch = coder_generate_patch(task, repair_attempts=0, memories=[])
    assert len(patch.files) >= 1
    assert patch.files[0].path.endswith(".py")
    assert patch.tests_to_run == ["test_addition_contract"]


def test_qa_test_execution_accepts_valid_patch() -> None:
    """Verify QA can execute tests against a typed CodePatch."""

    patch = CodePatch(
        files=[CodeFile(path="math.py", content="def add(a, b): return a + b")],
        rationale="Valid addition patch",
        tests_to_run=["test_addition_contract"],
    )

    result = run_python_patch_tests(patch)
    assert result.passed is True


def test_qa_test_execution_rejects_invalid_patch() -> None:
    """Verify QA failure returns a typed TestResult instead of crashing."""

    patch = CodePatch(
        files=[CodeFile(path="math.py", content="def add(a, b): return a - b")],
        rationale="Invalid addition patch",
        tests_to_run=["test_addition_contract"],
    )

    result = run_python_patch_tests(patch)
    assert result.passed is False
    assert result.failing_tests == ["test_addition_contract"]
