"""Starter code for Homework E: Marketing Orchestration Track."""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ModelClass(str, Enum):
    FAST_CHEAP = "fast-cheap"
    BALANCED = "balanced"
    REASONING = "reasoning"


class BudgetTracker(StrictModel):
    campaign_id: str
    daily_budget_usd: float = Field(gt=0.0)
    spent_usd: float = Field(default=0.0, ge=0.0)


class RoutingDecision(StrictModel):
    model_class: ModelClass
    estimated_cost_usd: float = Field(ge=0.0)
    rationale: str


class BudgetExhausted(StrictModel):
    campaign_id: str
    requested_cost_usd: float
    remaining_budget_usd: float
    blocked_task: str


class SocialDraft(StrictModel):
    campaign_id: str
    channel: Literal["x", "linkedin", "instagram"]
    text: str
    claims: list[str] = Field(default_factory=list)


class BrandSafetyFinding(StrictModel):
    blocked: bool
    violation_type: Literal["unauthorized_trademark", "false_partnership", "restricted_claim"]
    evidence: str
    repair_instruction: str


class FuguRouter:
    def route(self, task: str) -> RoutingDecision:
        """TODO: route bulk variation, strategy, and compliance tasks by cost/risk."""
        raise NotImplementedError


class BrandSafetyScanner:
    def scan(self, draft: SocialDraft) -> list[BrandSafetyFinding]:
        """TODO: check draft against restricted trademarks and false partnerships."""
        raise NotImplementedError
