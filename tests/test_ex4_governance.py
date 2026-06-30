from __future__ import annotations

from assignments.starter_code.ex4_governance_matrix_starter import (
    AgentIdentity,
    Tool,
    ToolGateway,
    ToolRequest,
    TrustTier,
)


def test_vendor_cannot_export_restricted_report() -> None:
    """The rogue-agent test: external vendor is denied restricted data export."""

    vendor = AgentIdentity(
        agent_id="vendor-test",
        organization="external_vendor",
        role="vendor_reporter",
        trust_tier=TrustTier.PUBLIC,
        allowed_tools={Tool.EXPORT_REPORT},
        public_key_ref="did:example:vendor",
    )
    gateway = ToolGateway()

    result = gateway.call(
        ToolRequest(
            caller=vendor,
            tool=Tool.EXPORT_REPORT,
            args={"name": "restricted_audit"},
            data_sensitivity=TrustTier.RESTRICTED,
        )
    )

    assert result.success is False
    assert result.output is None
    assert gateway.audit_log[-1].allowed is False
    assert "denied" in gateway.audit_log[-1].reason.lower()
