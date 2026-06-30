from __future__ import annotations

import pytest

from assignments.starter_code.ex5_capstone_starter import run_company
from src.enterprise_agent_team import run_virtual_software_company


@pytest.mark.system
def test_virtual_software_company_flow() -> None:
    """Test complete PM -> Coder -> QA -> Review flow."""

    state = run_virtual_software_company("Create safe add function")

    assert state.task is not None
    assert state.patch is not None
    assert state.test_result is not None
    assert state.review is not None
    assert state.test_result.passed is True
    assert state.review.next_action == "ship"
    assert state.repair_attempts <= 2
    assert len(state.route_trace) >= 1
    assert len(state.commitments) >= 1


@pytest.mark.system
def test_capstone_repair_loop_can_ship() -> None:
    """Verify the capstone starter has a working baseline learners can extend."""

    summary = run_company("Create slugify(text) utility with tests.", max_repairs=2)
    assert summary.status == "SHIPPED"
    assert "slugify" in summary.title.lower()
    assert summary.tests
    assert summary.audit_trail


@pytest.mark.system
def test_capstone_repair_loop_terminates_on_budget() -> None:
    """Verify bounded repair stops instead of looping forever."""

    summary = run_company("Create slugify(text) utility with tests.", max_repairs=0)
    assert summary.status == "ESCALATED_TO_HUMAN"
    assert "budget" in summary.body.lower()
