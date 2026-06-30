"""Exercise 4: Trust & Governance Matrix.

Aligned with Enterprise Agentic Automation Standards (IBM/Anthropic).

In production multi-agent systems, autonomous decision-making poses severe
risks: bias, unauthorized execution, and data leakage. This exercise implements
the mandatory governance layer: a zero-trust MCP-style Tool Gateway that
enforces agent-to-agent monitoring and strict permission boundaries before any
tool is executed.

Run:
    python3 assignments/starter_code/ex4_governance_matrix_starter.py
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class Tool(str, Enum):
    READ_RESUME = "read_resume"
    READ_POLICY = "read_policy"
    RUN_BIAS_CHECK = "run_bias_check"
    ISSUE_OFFER = "issue_offer"
    READ_SECURITY_LOGS = "read_security_logs"
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
    request_id: str = Field(default_factory=lambda: f"tool-{uuid4().hex[:8]}")
    caller: AgentIdentity
    tool: Tool
    args: dict[str, Any] = Field(default_factory=dict)
    data_sensitivity: TrustTier


class ToolResult(StrictModel):
    success: bool
    output: Any = None
    error: str | None = None


class AuditEvent(StrictModel):
    event_id: str = Field(default_factory=lambda: f"audit-{uuid4().hex[:8]}")
    request_id: str
    caller_id: str
    caller_role: str
    organization: str
    tool: Tool
    data_sensitivity: TrustTier
    allowed: bool
    reason: str
    timestamp_utc: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class GovernancePolicy:
    """Zero-trust authorization for every tool call."""

    TIER_HIERARCHY = {
        TrustTier.PUBLIC: 0,
        TrustTier.CONFIDENTIAL: 1,
        TrustTier.RESTRICTED: 2,
    }

    TOOL_REQUIRED_TIER = {
        Tool.READ_RESUME: TrustTier.CONFIDENTIAL,
        Tool.READ_POLICY: TrustTier.PUBLIC,
        Tool.RUN_BIAS_CHECK: TrustTier.CONFIDENTIAL,
        Tool.ISSUE_OFFER: TrustTier.RESTRICTED,
        Tool.READ_SECURITY_LOGS: TrustTier.RESTRICTED,
        Tool.EXPORT_REPORT: TrustTier.CONFIDENTIAL,
    }

    TOOL_ALLOWED_ROLES = {
        Tool.READ_RESUME: {"resume_parser", "hiring_manager"},
        Tool.READ_POLICY: {"resume_parser", "bias_checker", "hiring_manager", "vendor_reporter"},
        Tool.RUN_BIAS_CHECK: {"bias_checker"},
        Tool.ISSUE_OFFER: {"hiring_manager"},
        Tool.READ_SECURITY_LOGS: {"security"},
        Tool.EXPORT_REPORT: {"bias_checker", "hiring_manager", "security", "vendor_reporter"},
    }

    def authorize(self, request: ToolRequest) -> tuple[bool, str]:
        # Check 1: Does this identity have the requested tool in its scope?
        # This prevents a specialized agent, such as a resume parser, from
        # opportunistically calling a high-impact tool such as ISSUE_OFFER.
        if request.tool not in request.caller.allowed_tools:
            reason = f"Scope denied: {request.caller.role} cannot use {request.tool.value}."
            print(reason)
            return False, reason

        caller_level = self.TIER_HIERARCHY[request.caller.trust_tier]
        data_level = self.TIER_HIERARCHY[request.data_sensitivity]
        required_tool_level = self.TIER_HIERARCHY[self.TOOL_REQUIRED_TIER[request.tool]]

        # Check 2: Can this trust tier read the requested data sensitivity?
        # This prevents public/vendor agents from reading confidential resumes
        # or restricted security logs even if they know the tool name.
        if caller_level < data_level:
            reason = (
                f"Denied: {request.caller.trust_tier.value} clearance "
                f"< {request.data_sensitivity.value} data."
            )
            print(reason)
            return False, reason

        # Check 3: Is the tool itself too sensitive for this identity?
        # A caller may have confidential data access but still not be allowed
        # to execute restricted actions such as issuing offers.
        if caller_level < required_tool_level:
            reason = (
                f"Denied: {request.tool.value} requires "
                f"{self.TOOL_REQUIRED_TIER[request.tool].value} clearance."
            )
            print(reason)
            return False, reason

        # Check 4: Is this role allowed to perform this class of work?
        # This is separation of duties: only the bias checker can run bias
        # checks, only security can read security logs, and so on.
        if request.caller.role not in self.TOOL_ALLOWED_ROLES[request.tool]:
            reason = f"Role denied: {request.caller.role} cannot call {request.tool.value}."
            print(reason)
            return False, reason

        # Check 5: Is this crossing an organization boundary?
        # External identities can participate in the workflow, but restricted
        # internal data never leaves the organization through this gateway.
        if (
            request.caller.organization != "internal"
            and request.data_sensitivity == TrustTier.RESTRICTED
        ):
            reason = "Organization denied: external organizations cannot access restricted data."
            print(reason)
            return False, reason

        reason = f"Authorized: {request.caller.role} -> {request.tool.value}."
        print(reason)
        return True, reason


class ToolGateway:
    """Small MCP-shaped gateway: authorize first, execute second."""

    def __init__(self, policy: GovernancePolicy | None = None) -> None:
        self.policy = policy or GovernancePolicy()
        self.audit_log: list[AuditEvent] = []

    def call(self, request: ToolRequest) -> ToolResult:
        allowed, reason = self.policy.authorize(request)
        self.audit_log.append(
            AuditEvent(
                request_id=request.request_id,
                caller_id=request.caller.agent_id,
                caller_role=request.caller.role,
                organization=request.caller.organization,
                tool=request.tool,
                data_sensitivity=request.data_sensitivity,
                allowed=allowed,
                reason=reason,
            )
        )

        if not allowed:
            return ToolResult(
                success=False,
                error=reason,
            )

        handlers = {
            Tool.READ_RESUME: lambda args: {
                "candidate_id": args["candidate_id"],
                "skills": ["python", "data pipelines", "stakeholder communication"],
            },
            Tool.READ_POLICY: lambda args: "Hiring policy: remove protected-class signals before ranking.",
            Tool.RUN_BIAS_CHECK: lambda args: {
                "candidate_id": args["candidate_id"],
                "bias_risk": "low",
                "blocked_features": ["age", "gender", "photo"],
            },
            Tool.ISSUE_OFFER: lambda args: f"Offer queued for candidate {args['candidate_id']}",
            Tool.READ_SECURITY_LOGS: lambda args: ["mcp token rotated", "vendor export denied"],
            Tool.EXPORT_REPORT: lambda args: f"Report exported: {args.get('name', 'hiring_audit')}",
        }
        return ToolResult(success=True, output=handlers[request.tool](request.args))


def demo_tool_gateway() -> None:
    resume_parser = AgentIdentity(
        agent_id="resume-parser-001",
        organization="internal",
        role="resume_parser",
        trust_tier=TrustTier.CONFIDENTIAL,
        allowed_tools={Tool.READ_RESUME, Tool.READ_POLICY},
        public_key_ref="did:example:resume-parser-001",
    )
    bias_checker = AgentIdentity(
        agent_id="bias-checker-001",
        organization="internal",
        role="bias_checker",
        trust_tier=TrustTier.CONFIDENTIAL,
        allowed_tools={Tool.READ_POLICY, Tool.RUN_BIAS_CHECK, Tool.EXPORT_REPORT},
        public_key_ref="did:example:bias-checker-001",
    )
    hiring_manager = AgentIdentity(
        agent_id="hiring-manager-001",
        organization="internal",
        role="hiring_manager",
        trust_tier=TrustTier.CONFIDENTIAL,
        allowed_tools={Tool.READ_RESUME, Tool.EXPORT_REPORT, Tool.ISSUE_OFFER},
        public_key_ref="did:example:hiring-manager-001",
    )
    security = AgentIdentity(
        agent_id="security-001",
        organization="internal",
        role="security",
        trust_tier=TrustTier.RESTRICTED,
        allowed_tools={Tool.READ_SECURITY_LOGS, Tool.EXPORT_REPORT},
        public_key_ref="did:example:security-001",
    )
    vendor = AgentIdentity(
        agent_id="vendor-001",
        organization="external_vendor",
        role="vendor_reporter",
        trust_tier=TrustTier.PUBLIC,
        allowed_tools={Tool.READ_POLICY, Tool.EXPORT_REPORT},
        public_key_ref="did:example:vendor-001",
    )

    gateway = ToolGateway()
    requests = [
        ToolRequest(
            caller=resume_parser,
            tool=Tool.READ_RESUME,
            args={"candidate_id": "C-1024"},
            data_sensitivity=TrustTier.CONFIDENTIAL,
        ),
        ToolRequest(
            caller=resume_parser,
            tool=Tool.EXPORT_REPORT,
            args={"name": "candidate_rank"},
            data_sensitivity=TrustTier.CONFIDENTIAL,
        ),
        ToolRequest(
            caller=bias_checker,
            tool=Tool.RUN_BIAS_CHECK,
            args={"candidate_id": "C-1024"},
            data_sensitivity=TrustTier.CONFIDENTIAL,
        ),
        ToolRequest(
            caller=hiring_manager,
            tool=Tool.ISSUE_OFFER,
            args={"candidate_id": "C-1024"},
            data_sensitivity=TrustTier.RESTRICTED,
        ),
        ToolRequest(
            caller=vendor,
            tool=Tool.EXPORT_REPORT,
            args={"name": "restricted_hiring_audit"},
            data_sensitivity=TrustTier.RESTRICTED,
        ),
        ToolRequest(
            caller=security,
            tool=Tool.READ_SECURITY_LOGS,
            args={},
            data_sensitivity=TrustTier.RESTRICTED,
        ),
    ]

    for request in requests:
        result = gateway.call(request)
        print(result.model_dump())

    print("\nAudit log:")
    for event in gateway.audit_log:
        print(event.model_dump())


if __name__ == "__main__":
    demo_tool_gateway()
