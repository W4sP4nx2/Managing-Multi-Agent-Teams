"""Starter code for Homework D: HR Governance Track."""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ToolName(str, Enum):
    REDACT_PII = "redact_pii"
    EVALUATE_CANDIDATE = "evaluate_candidate"
    UPDATE_PAYROLL = "update_payroll"


class CandidateProfile(StrictModel):
    candidate_id: str
    anonymized_skills: list[str]
    pii_quarantine: dict[str, str] = Field(default_factory=dict)
    redaction_complete: bool = False


class ToolRequest(StrictModel):
    tool: ToolName
    args: dict


class HumanApprovalRequest(StrictModel):
    request_id: str
    employee_id: str
    proposed_action: Literal["promote", "compensation_change"]
    rationale: str
    risk_level: Literal["medium", "high"]
    requested_by_agent: str
    status: Literal["pending", "approved", "rejected"] = "pending"


class ToolPolicy:
    def authorize(self, request: ToolRequest) -> bool:
        """TODO: block candidate evaluation when PII is unredacted."""
        raise NotImplementedError


def redact_pii(raw_profile: CandidateProfile) -> CandidateProfile:
    """TODO: move name, email, phone, address, and graduation year to quarantine."""
    raise NotImplementedError


def handle_human_webhook(
    approval: HumanApprovalRequest,
    status: Literal["approved", "rejected"],
) -> HumanApprovalRequest:
    """TODO: update approval state and unblock or terminate payroll path."""
    raise NotImplementedError
