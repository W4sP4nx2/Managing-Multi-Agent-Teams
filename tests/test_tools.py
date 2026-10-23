from __future__ import annotations

import pytest

from src.enterprise_agent_team import (
    AgentIdentity,
    AgentRole,
    TeamCommitment,
    ToolName,
    ToolPolicy,
    ToolRequest,
    TrustTier,
    check_teamlog_commitments,
)

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("clearance", list(TrustTier))
@pytest.mark.parametrize("sensitivity", list(TrustTier))
def test_tool_policy_enforces_the_complete_clearance_order(clearance, sensitivity):
    order = [TrustTier.PUBLIC, TrustTier.CONFIDENTIAL, TrustTier.RESTRICTED]
    caller = AgentIdentity(agent_id="reader", role=AgentRole.CODER, org_id="training",
                           scopes={ToolName.SEARCH_MEMORY}, clearance=clearance)
    request = ToolRequest(caller=caller, tool=ToolName.SEARCH_MEMORY,
                          args={"query": "task"}, data_sensitivity=sensitivity)
    if order.index(clearance) < order.index(sensitivity):
        with pytest.raises(PermissionError):
            ToolPolicy().authorize(request)
    else:
        ToolPolicy().authorize(request)


def test_tool_policy_allows_scoped_confidential_request() -> None:
    policy = ToolPolicy()
    coder = AgentIdentity(
        agent_id="coder-001",
        role=AgentRole.CODER,
        org_id="training",
        scopes={ToolName.SEARCH_MEMORY},
        clearance=TrustTier.CONFIDENTIAL,
    )

    policy.authorize(
        ToolRequest(
            caller=coder,
            tool=ToolName.SEARCH_MEMORY,
            args={"query": "task"},
            data_sensitivity=TrustTier.CONFIDENTIAL,
        )
    )


def test_tool_policy_blocks_unscoped_tool() -> None:
    policy = ToolPolicy()
    coder = AgentIdentity(
        agent_id="coder-001",
        role=AgentRole.CODER,
        org_id="training",
        scopes={ToolName.SEARCH_MEMORY},
        clearance=TrustTier.CONFIDENTIAL,
    )

    with pytest.raises(PermissionError):
        policy.authorize(
            ToolRequest(
                caller=coder,
                tool=ToolName.EXECUTE_TESTS,
                args={"patch": {}},
                data_sensitivity=TrustTier.CONFIDENTIAL,
            )
        )


def test_tool_policy_blocks_restricted_data_without_clearance() -> None:
    policy = ToolPolicy()
    coder = AgentIdentity(
        agent_id="coder-001",
        role=AgentRole.CODER,
        org_id="training",
        scopes={ToolName.SEARCH_MEMORY},
        clearance=TrustTier.CONFIDENTIAL,
    )

    with pytest.raises(PermissionError):
        policy.authorize(
            ToolRequest(
                caller=coder,
                tool=ToolName.SEARCH_MEMORY,
                args={"query": "secret"},
                data_sensitivity=TrustTier.RESTRICTED,
            )
        )


def test_teamlog_commitment_blocks_external_api_call() -> None:
    coder = AgentIdentity(
        agent_id="coder-001",
        role=AgentRole.CODER,
        org_id="training",
        scopes={ToolName.CALL_EXTERNAL_API},
        clearance=TrustTier.CONFIDENTIAL,
    )
    commitment = TeamCommitment(
        owner=AgentRole.PRODUCT_MANAGER,
        commitment="All code must run offline. No external network calls.",
        visible_to={AgentRole.CODER},
        sensitivity=TrustTier.CONFIDENTIAL,
    )

    with pytest.raises(PermissionError, match="TeamLog commitment"):
        check_teamlog_commitments(
            ToolRequest(
                caller=coder,
                tool=ToolName.CALL_EXTERNAL_API,
                args={"url": "https://api.example.com"},
                data_sensitivity=TrustTier.CONFIDENTIAL,
            ),
            [commitment],
        )
