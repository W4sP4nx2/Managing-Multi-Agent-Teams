"""Agent results are data, never executable instructions or deployment authority."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class AgentOutput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class Plan(AgentOutput):
    goal: Text
    acceptance_criteria: list[Text] = Field(min_length=1, max_length=20)


class SiteArtifact(AgentOutput):
    html: str = Field(min_length=1, max_length=200_000)
    title: Text


class Review(AgentOutput):
    approved: bool
    issues: list[Text] = Field(max_length=30)
    summary: Text

    @model_validator(mode="after")
    def approval_matches_findings(self) -> "Review":
        if self.approved and self.issues:
            raise ValueError("A review with unresolved issues cannot approve the artifact")
        if not self.approved and not self.issues:
            raise ValueError("A blocked review must explain at least one issue")
        return self


class QATest(AgentOutput):
    """A bounded declarative browser assertion; no Python, shell, or JavaScript."""

    name: Text
    selector: str = Field(min_length=1, max_length=200)
    assertion: Literal["visible", "text", "count", "attribute"]
    expected: str = Field(max_length=500)


class QAPlan(AgentOutput):
    test_cases: list[QATest] = Field(min_length=1, max_length=20)
