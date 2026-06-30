"""Starter code for Homework B: Production Controls."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AgentAction(StrictModel):
    action_type: str
    estimated_cost_usd: float = Field(ge=0.0)
    confidence: float = Field(ge=0.0, le=1.0)
    data_sensitivity: Literal["public", "confidential", "restricted"]
    rationale: str


class HumanDecision(StrictModel):
    approved: bool
    reviewer: str
    notes: str


class Metrics(StrictModel):
    accuracy: float = Field(ge=0.0, le=1.0)
    latency_seconds: float = Field(ge=0.0)
    cost_usd: float = Field(ge=0.0)
    hallucination_rate: float = Field(ge=0.0, le=1.0)
    tool_usage_efficiency: float = Field(ge=0.0, le=1.0)


class AgentExperience(StrictModel):
    task: str
    outcome: str
    value_score: float = Field(ge=0.0, le=1.0)
    tags: set[str] = Field(default_factory=set)


class HumanApprovalGateway:
    def requires_human_approval(self, action: AgentAction) -> bool:
        """TODO: gate deletion, high-cost, low-confidence, or restricted actions."""
        raise NotImplementedError


class AgentBenchmark:
    def measure_agent_performance(self, tasks: list[str]) -> Metrics:
        """TODO: calculate deterministic benchmark metrics."""
        raise NotImplementedError


class CostAwareAgent:
    def generate_response(self, prompt: str) -> str:
        """TODO: check cache, enforce budget, call model adapter, cache response."""
        raise NotImplementedError


class LongTermMemory:
    def store(self, experience: AgentExperience) -> None:
        """TODO: store experience with governed metadata."""
        raise NotImplementedError

    def retrieve(self, query: str, top_k: int = 5) -> list[AgentExperience]:
        """TODO: retrieve relevant experiences without leaking restricted data."""
        raise NotImplementedError

    def forget(self, strategy: str = "least_recent") -> None:
        """TODO: remove, compress, or down-rank old memories."""
        raise NotImplementedError
