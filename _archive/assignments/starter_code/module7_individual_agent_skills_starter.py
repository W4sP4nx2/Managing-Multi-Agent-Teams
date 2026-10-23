"""Starter code for Homework A: Specialist Agent Skills."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodePatch(StrictModel):
    files: dict[str, str]
    rationale: str
    tests_to_run: list[str] = Field(default_factory=list)


class CodeQualityReport(StrictModel):
    security_score: float = Field(ge=0.0, le=1.0)
    testability_score: float = Field(ge=0.0, le=1.0)
    documentation_score: float = Field(ge=0.0, le=1.0)
    style_score: float = Field(ge=0.0, le=1.0)
    edge_case_score: float = Field(ge=0.0, le=1.0)
    findings: list[str] = Field(default_factory=list)


class TestSuite(StrictModel):
    unit_tests: list[str] = Field(default_factory=list)
    integration_tests: list[str] = Field(default_factory=list)
    edge_case_tests: list[str] = Field(default_factory=list)
    performance_tests: list[str] = Field(default_factory=list)


class SecurityReport(StrictModel):
    critical: int = Field(ge=0)
    medium: int = Field(ge=0)
    low: int = Field(ge=0)
    findings: list[str] = Field(default_factory=list)


class DocumentationBundle(StrictModel):
    readme: str
    api_docs: str
    inline_comment_suggestions: list[str] = Field(default_factory=list)
    changelog: str


def assess_code_quality(patch: CodePatch) -> CodeQualityReport:
    """TODO: inspect patch contents and return typed quality scores."""
    raise NotImplementedError


def generate_test_suite(patch: CodePatch) -> TestSuite:
    """TODO: generate typed unit, integration, edge, and performance tests."""
    raise NotImplementedError


def security_scan(patch: CodePatch) -> SecurityReport:
    """TODO: scan patch contents for unsafe patterns and severity counts."""
    raise NotImplementedError


def generate_documentation(patch: CodePatch) -> DocumentationBundle:
    """TODO: generate docs from patch contents without inventing APIs."""
    raise NotImplementedError
