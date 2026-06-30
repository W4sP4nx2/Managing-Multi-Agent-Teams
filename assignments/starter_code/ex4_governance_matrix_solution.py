"""Instructor solution for Ex4: Trust & Governance Matrix.

Run:
    python3 assignments/starter_code/ex4_governance_matrix_solution.py
"""

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Tool(str, Enum):
    READ_CODE = "read_code"
    READ_TICKETS = "read_tickets"
    READ_DEPLOYMENT_LOGS = "read_deployment_logs"
    EXPORT_REPORT = "export_report"


class TrustTier(str, Enum):
    PUBLIC = "public"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AgentIdentity(StrictModel):
    agent_id: str
    organization: str
    role: str
    trust_tier: TrustTier
    allowed_tools: set[Tool]
    public_key_ref: str


class ToolRequest(StrictModel):
    caller: AgentIdentity
    tool: Tool
    args: dict[str, Any] = Field(default_factory=dict)
    data_sensitivity: TrustTier


class A2AMessage(StrictModel):
    sender_id: str
    receiver_id: str
    schema_name: str
    payload: dict[str, Any]
    sensitivity: TrustTier


class GovernancePolicy:
    LEVELS = {
        TrustTier.PUBLIC: 0,
        TrustTier.CONFIDENTIAL: 1,
        TrustTier.RESTRICTED: 2,
    }

    def authorize(self, request: ToolRequest) -> bool:
        if request.tool not in request.caller.allowed_tools:
            return False
        if self.LEVELS[request.caller.trust_tier] < self.LEVELS[request.data_sensitivity]:
            return False
        if request.caller.organization != "internal" and request.data_sensitivity == TrustTier.RESTRICTED:
            return False
        return True


def build_governance_matrix() -> list[AgentIdentity]:
    return [
        AgentIdentity(
            agent_id="internal-data-analyst",
            organization="internal",
            role="data_analyst",
            trust_tier=TrustTier.CONFIDENTIAL,
            allowed_tools={Tool.READ_TICKETS, Tool.READ_CODE},
            public_key_ref="did:example:internal-data-analyst",
        ),
        AgentIdentity(
            agent_id="internal-security-reviewer",
            organization="internal",
            role="security_reviewer",
            trust_tier=TrustTier.RESTRICTED,
            allowed_tools={Tool.READ_CODE, Tool.READ_DEPLOYMENT_LOGS, Tool.EXPORT_REPORT},
            public_key_ref="did:example:internal-security-reviewer",
        ),
        AgentIdentity(
            agent_id="vendor-report-agent",
            organization="external_vendor",
            role="vendor_reporter",
            trust_tier=TrustTier.CONFIDENTIAL,
            allowed_tools={Tool.EXPORT_REPORT},
            public_key_ref="did:example:vendor-report-agent",
        ),
    ]


def demo_policy() -> None:
    policy = GovernancePolicy()
    data_analyst, security, vendor = build_governance_matrix()

    allowed = ToolRequest(
        caller=security,
        tool=Tool.READ_DEPLOYMENT_LOGS,
        args={"service": "payments"},
        data_sensitivity=TrustTier.RESTRICTED,
    )
    denied_vendor_logs = ToolRequest(
        caller=vendor,
        tool=Tool.READ_DEPLOYMENT_LOGS,
        args={"service": "payments"},
        data_sensitivity=TrustTier.RESTRICTED,
    )
    denied_analyst_export = ToolRequest(
        caller=data_analyst,
        tool=Tool.EXPORT_REPORT,
        args={"name": "compliance"},
        data_sensitivity=TrustTier.CONFIDENTIAL,
    )

    assert policy.authorize(allowed) is True
    assert policy.authorize(denied_vendor_logs) is False
    assert policy.authorize(denied_analyst_export) is False

    print("Security can read restricted logs:", policy.authorize(allowed))
    print("Vendor can read restricted logs:", policy.authorize(denied_vendor_logs))
    print("Analyst can export report:", policy.authorize(denied_analyst_export))


if __name__ == "__main__":
    demo_policy()
