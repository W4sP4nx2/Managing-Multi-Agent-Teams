"""Starter code for Homework F: Advanced Fugu Discussion."""

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


class RoutingHistory(StrictModel):
    task_description: str
    task_features: dict[str, float]
    chosen_model: ModelClass
    actual_cost_usd: float
    actual_latency_seconds: float
    success_score: float = Field(ge=0.0, le=1.0)


class WorkflowScaffold(StrictModel):
    agents_needed: list[str]
    execution_order: list[tuple[str, str]]
    parallel_groups: list[list[str]]
    estimated_total_cost: float
    estimated_total_latency: float


class DebateRecord(StrictModel):
    topic: str
    agent_a_position: str
    agent_b_position: str
    points_of_agreement: list[str]
    points_of_contention: list[str]
    final_decision: str
    escalation_required: bool = False


class DelegationDecision(StrictModel):
    action: Literal["delegate", "escalate", "review"]
    target_agent: str
    payload: dict
    rationale: str


class SimpleLearner:
    def analyze_history(self, history: list[RoutingHistory]) -> dict[ModelClass, list[str]]:
        """TODO: identify features correlated with model success."""
        raise NotImplementedError


class ScaffoldGenerator:
    def generate(self, task: str) -> WorkflowScaffold:
        """TODO: create workflow topology from task complexity."""
        raise NotImplementedError


class DebateModerator:
    def moderate(self, topic: str, position_a: str, position_b: str) -> DebateRecord:
        """TODO: preserve disagreement and synthesize or escalate."""
        raise NotImplementedError
