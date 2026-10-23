from __future__ import annotations

import pytest

from assignments.starter_code.ex5_capstone_starter import (
    AgentIdentity,
    DevDeliverable,
    Role,
    SecurityAuditResult,
    Tool,
    ToolGateway,
    ToolRequest,
    build_agent_identities,
    run_company,
)

pytestmark = pytest.mark.integration


def test_capstone_baseline_returns_pull_request_summary() -> None:
    """The capstone starter should be executable before learners extend it."""

    result = run_company("Create slugify(text) utility with tests.", max_repairs=2)

    assert result.status == "SHIPPED"
    assert result.title
    assert result.tests
    assert result.audit_trail
    assert "Engineering Manager approved delivery" in result.audit_trail


def test_capstone_escalates_when_repair_budget_is_exhausted() -> None:
    """The capstone starter should model human escalation."""

    result = run_company("Create slugify(text) utility with tests.", max_repairs=0)

    assert result.status == "ESCALATED_TO_HUMAN"
    assert "Repair budget exhausted" in result.body
    assert any("Engineering Manager escalated" in entry for entry in result.audit_trail)


def test_capstone_two_team_role_and_tool_boundaries() -> None:
    """The two Capstone teams have distinct roles and tool authority."""

    identities = build_agent_identities()
    assert set(identities) == {
        Role.MANAGER,
        Role.CODER,
        Role.QA,
        Role.SECURITY_MANAGER,
        Role.PEN_TESTER,
    }

    manager = identities[Role.MANAGER]
    coder = identities[Role.CODER]
    qa = identities[Role.QA]
    pen_tester = identities[Role.PEN_TESTER]
    assert manager.allowed_tools == {Tool.APPROVE_CODE, Tool.ESCALATE_TO_HUMAN}
    assert coder.allowed_tools == {Tool.SEARCH_MEMORY, Tool.WRITE_PATCH}
    assert Tool.RUN_TESTS in qa.allowed_tools
    assert Tool.SECURITY_SCAN in qa.allowed_tools
    assert Tool.WRITE_PATCH not in qa.allowed_tools
    assert Tool.APPROVE_CODE not in coder.allowed_tools
    assert pen_tester.allowed_tools == {Tool.AUDIT_DEV_DELIVERABLE}
    assert Tool.WRITE_PATCH not in pen_tester.allowed_tools

    gateway = ToolGateway()
    for tool in (Tool.WRITE_PATCH, Tool.RUN_TESTS):
        with pytest.raises(PermissionError):
            gateway.call(
                ToolRequest(
                    caller=manager,
                    tool=tool,
                    args={},
                    sensitivity="confidential",
                )
            )

    with pytest.raises(PermissionError):
        gateway.call(
            ToolRequest(
                caller=coder,
                tool=Tool.APPROVE_CODE,
                args={"tests_passed": True, "security_approved": True},
                sensitivity="confidential",
            )
        )


def test_dev_deliverable_triggers_security_team_automatically() -> None:
    result = run_company("Create slugify(text) utility with tests.", max_repairs=2)

    assert result.status == "SHIPPED"
    assert isinstance(result.dev_deliverable, DevDeliverable)
    assert result.dev_deliverable.unit_tests_passed is True
    assert result.dev_deliverable.dev_team_signature.startswith("Development Team")
    assert isinstance(result.security_audit, SecurityAuditResult)
    assert result.security_audit.approved is True
    assert "Development Team issued Pydantic DevDeliverable" in result.audit_trail
    assert "Security Team received validated DevDeliverable" in result.audit_trail
    assert "Security Team approved deliverable" in result.audit_trail


def test_security_team_rejects_unsafe_inter_team_payload() -> None:
    from assignments.starter_code.ex5_capstone_starter import security_team_audit

    deliverable = DevDeliverable(
        code_snippet="query = 'SELECT * FROM users'; element.innerHTML = input",
        unit_tests_passed=True,
        dev_team_signature="Development Team",
    )
    result = security_team_audit(deliverable)

    assert result.approved is False
    assert any("sql injection" in finding.lower() for finding in result.findings)
    assert any("cross-site scripting" in finding.lower() for finding in result.findings)


def test_security_team_contract_rejects_unverified_output() -> None:
    with pytest.raises(ValueError, match="only accepts deliverables"):
        DevDeliverable(
            code_snippet="def example(): return True",
            unit_tests_passed=False,
            dev_team_signature="Development Team",
        )
