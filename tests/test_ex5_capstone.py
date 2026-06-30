from __future__ import annotations

from assignments.starter_code.ex5_capstone_starter import run_company


def test_capstone_baseline_returns_pull_request_summary() -> None:
    """The capstone starter should be executable before learners extend it."""

    result = run_company("Create slugify(text) utility with tests.", max_repairs=2)

    assert result.status == "SHIPPED"
    assert result.title
    assert result.tests
    assert result.audit_trail


def test_capstone_escalates_when_repair_budget_is_exhausted() -> None:
    """The capstone starter should model human escalation."""

    result = run_company("Create slugify(text) utility with tests.", max_repairs=0)

    assert result.status == "ESCALATED_TO_HUMAN"
    assert "Repair budget exhausted" in result.body
