from __future__ import annotations

import pytest

from src.enterprise_agent_team import (
    AgentIdentity,
    AgentRole,
    LocalTrainingMcpGateway,
    SharedAgenticMemory,
    TeamCommitment,
    ToolName,
    ToolPolicy,
    ToolRequest,
    TrustTier,
)


def test_tool_gateway_authorization() -> None:
    """Verify the MCP-shaped gateway enforces zero-trust tool scope."""

    memory = SharedAgenticMemory()
    gateway = LocalTrainingMcpGateway(memory=memory, policy=ToolPolicy())
    coder = AgentIdentity(
        agent_id="coder-001",
        role=AgentRole.CODER,
        org_id="training",
        scopes={ToolName.SEARCH_MEMORY, ToolName.WRITE_PATCH},
        clearance=TrustTier.CONFIDENTIAL,
    )

    allowed = gateway.call_tool(
        ToolRequest(
            caller=coder,
            tool=ToolName.SEARCH_MEMORY,
            args={"query": "test"},
            data_sensitivity=TrustTier.CONFIDENTIAL,
        )
    )
    assert allowed.ok is True

    with pytest.raises(PermissionError):
        gateway.call_tool(
            ToolRequest(
                caller=coder,
                tool=ToolName.EXECUTE_TESTS,
                args={"patch": {}},
                data_sensitivity=TrustTier.CONFIDENTIAL,
            )
        )


def test_teamlog_commitment_blocks_external_network_tool() -> None:
    """Verify visible TeamLog commitments override local tool access."""

    memory = SharedAgenticMemory()
    gateway = LocalTrainingMcpGateway(memory=memory, policy=ToolPolicy())
    coder = AgentIdentity(
        agent_id="coder-001",
        role=AgentRole.CODER,
        org_id="training",
        scopes={ToolName.CALL_EXTERNAL_API},
        clearance=TrustTier.CONFIDENTIAL,
    )
    commitments = [
        TeamCommitment(
            owner=AgentRole.PRODUCT_MANAGER,
            commitment="All code must run offline. No external network calls.",
            visible_to={AgentRole.CODER},
            sensitivity=TrustTier.CONFIDENTIAL,
        )
    ]

    with pytest.raises(PermissionError, match="TeamLog"):
        gateway.call_tool(
            ToolRequest(
                caller=coder,
                tool=ToolName.CALL_EXTERNAL_API,
                args={"url": "https://example.com"},
                data_sensitivity=TrustTier.PUBLIC,
            ),
            commitments=commitments,
        )
