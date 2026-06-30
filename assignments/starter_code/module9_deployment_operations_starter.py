"""Starter code for Homework C: Deployment & Operations."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ExecutionRequest(StrictModel):
    code: str
    timeout_seconds: int = Field(default=5, ge=1, le=60)
    network_allowed: bool = False


class ExecutionResult(StrictModel):
    ok: bool
    stdout: str = ""
    stderr: str = ""
    timed_out: bool = False


class AgentConfig(StrictModel):
    agent_id: str
    system_prompt: str
    tools: set[str]
    model_name: str
    policy_version: str


class AgentObservability:
    def log_agent_action(self, agent_id: str, action: str, result: dict) -> None:
        """TODO: emit structured logs without secrets."""
        raise NotImplementedError


class SecureSandbox:
    def execute_untrusted_code(self, request: ExecutionRequest) -> ExecutionResult:
        """TODO: execute code in an isolated, resource-bounded environment."""
        raise NotImplementedError


class AgentVersionControl:
    def save_agent_version(self, config: AgentConfig) -> str:
        """TODO: hash and store versioned agent configuration."""
        raise NotImplementedError

    def rollback_agent(self, agent_id: str, version: str) -> AgentConfig:
        """TODO: restore and validate a previous configuration."""
        raise NotImplementedError
