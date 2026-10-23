"""Deterministic specialist fixtures for a live-feeling, offline software factory.

There are no model requests, credentials, provider dependencies, or actual API
charges. Model names are illustrative role labels. Local checks inspect the
actual candidate; fixture reports cannot approve a different HTML document.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from decimal import Decimal
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from software_factory.contracts import Plan, QAPlan, Review, SiteArtifact

Role = Literal["manager", "coder", "security", "ui_ux", "qa"]
ROLES = ("manager", "coder", "security", "ui_ux", "qa")
FIXTURE_DIR = Path(__file__).parent / "software_factory" / "fixtures"
FIXTURE_HTML = (FIXTURE_DIR / "index.html").read_text(encoding="utf-8")
FIXTURE_SHA256 = hashlib.sha256(FIXTURE_HTML.encode("utf-8")).hexdigest()
DEFAULT_CONFIG = Path(__file__).parent / "software_factory" / "simulation_config.json"


class HarnessError(RuntimeError):
    """Fail-closed fixture, schema, or unsupported-mode error."""


class SimulatedRoute(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    provider: Literal["offline"] = "offline"
    model: str = Field(min_length=1, max_length=160)
    purpose: str = Field(min_length=1, max_length=300)
    simulated_cost: Decimal = Field(ge=0, le="92233720368547758.07", allow_inf_nan=False)

    @field_validator("simulated_cost", mode="before")
    @classmethod
    def exact_teaching_cost(cls, value: Any) -> Any:
        return _money(value)


def _money(value: Any) -> Decimal:
    if not isinstance(value, (str, Decimal)):
        raise ValueError("Teaching amounts must be exact decimal strings or Decimal values")
    try:
        parsed = Decimal(value)
    except ArithmeticError:
        raise ValueError("Teaching amounts must be valid decimal values") from None
    if not parsed.is_finite() or parsed < 0 or parsed > Decimal("92233720368547758.07"):
        raise ValueError("Teaching amounts must be finite, nonnegative, and inside the local ledger range")
    numerator, denominator = parsed.as_integer_ratio()
    if (numerator * 100) % denominator:
        raise ValueError("Teaching amounts cannot contain fractional cents")
    return parsed


class SimulationConfig(BaseModel):
    """Teaching controls only; configuration cannot activate a provider route."""

    model_config = ConfigDict(extra="forbid", frozen=True)
    mode: Literal["simulation"]
    actual_cost: Decimal
    provider_calls: Literal[0]
    default_simulated_budget: Decimal = Field(ge=0, le="92233720368547758.07", allow_inf_nan=False)
    local_publish_cost: Decimal = Field(ge=0, le="92233720368547758.07", allow_inf_nan=False)
    notes: str = Field(min_length=1)
    roles: dict[str, SimulatedRoute]

    @field_validator("actual_cost", "default_simulated_budget", "local_publish_cost", mode="before")
    @classmethod
    def exact_amount(cls, value: Any) -> Decimal:
        return _money(value)

    @field_validator("actual_cost")
    @classmethod
    def actual_charges_are_impossible(cls, value: Decimal) -> Decimal:
        if value != 0:
            raise ValueError("Actual cost is fixed at 0.00; paid mode is disabled")
        return Decimal("0.00")

    @field_validator("provider_calls", mode="before")
    @classmethod
    def no_provider_calls(cls, value: Any) -> int:
        if type(value) is not int or value != 0:
            raise ValueError("Provider calls must be the integer zero")
        return value

    @model_validator(mode="after")
    def roles_are_complete(self) -> "SimulationConfig":
        if set(self.roles) != set(ROLES):
            raise ValueError("Exactly manager, coder, security, ui_ux, and qa roles are required")
        return self


def load_config(config: SimulationConfig | Mapping[str, Any] | str | Path | None = None) -> SimulationConfig:
    """Read JSON data only. Config cannot specify imports, endpoints, or keys."""
    try:
        if isinstance(config, SimulationConfig):
            return SimulationConfig.model_validate(config.model_dump())
        if isinstance(config, Mapping):
            return SimulationConfig.model_validate(dict(config))
        path = Path(config) if config is not None else DEFAULT_CONFIG
        return SimulationConfig.model_validate_json(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValidationError):
        raise HarnessError("Simulation configuration is missing or invalid; only offline roles and exact nonnegative teaching costs are allowed") from None


class FixtureRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    artifact_sha256: str
    review: Review


class QARecord(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    artifact_sha256: str
    plan: QAPlan


def security_policy(text: str) -> Review:
    """Small local deny rules, with no model override or claim of completeness."""
    normalized = text.casefold()
    issues = []
    if re.search(r"http\s*:\s*//", normalized):
        issues.append("Insecure HTTP endpoint")
    if "password" in normalized and "localstorage" in normalized:
        issues.append("Passwords in localStorage")
    if "evil.com" in normalized or re.search(r"\bexfiltrat\w*\b", normalized):
        issues.append("Potential data exfiltration")
    return Review(
        approved=not issues,
        issues=issues,
        summary="Local policy blocked this request." if issues else "No local request deny rule matched; candidate source checks and human review remain required.",
    )


class AgentHarness:
    """Same typed specialist interfaces as the labs; every output is local data.

    ``simulation`` and the compatibility alias ``replay`` perform identical
    deterministic work. ``live`` is explicitly disabled before any operation.
    Human approvals, terminal animation, the simulated ledger, git, file writes,
    and local publication belong to the trusted orchestrator.
    """

    def __init__(self, mode: str = "simulation", config: SimulationConfig | Mapping[str, Any] | str | Path | None = None):
        if mode not in ("simulation", "replay"):
            raise HarnessError("Live API mode is disabled. Use simulation or replay; no API keys or paid calls are needed.")
        self.mode = mode
        self.config = load_config(config)
        self.routes = dict(self.config.roles)
        self.simulated_costs = {role: route.simulated_cost for role, route in self.routes.items()}
        self.publish_cost = self.config.local_publish_cost
        self.default_simulated_budget = str(self.config.default_simulated_budget)

    @property
    def actual_cost(self) -> Decimal:
        return self.config.actual_cost

    def quote_role(self, role: str) -> Decimal:
        """Actual API quote is always zero; see simulated_costs for teaching units."""
        if role not in ROLES:
            raise ValueError("Unknown agent role")
        return Decimal("0.00")

    def plan(self, request: str) -> Plan:
        if not isinstance(request, str) or not request.strip():
            raise HarnessError("A nonempty feature request is required")
        return Plan(
            goal="Build Wanderlight, a responsive travel landing page from the fixed teaching fixture",
            acceptance_criteria=[
                "Show semantic navigation, exactly one primary heading, and three destination cards.",
                "Provide destinations, approach, and contact sections connected by local links.",
                "Include mobile CSS, visible keyboard focus, a skip link, and reduced-motion handling.",
                "Use self-contained HTML/CSS without scripts, forms, external resources, or credential storage.",
                "Pass the local security, source UI, and declarative QA checks before human-approved local publication.",
            ],
        )

    def build_site(self, request: str, plan: Plan) -> SiteArtifact:
        if not isinstance(request, str) or not request.strip():
            raise HarnessError("A nonempty feature request is required")
        Plan.model_validate(plan)
        # No text interpolation: untrusted intake can never inject executable HTML.
        return SiteArtifact(html=FIXTURE_HTML, title="Wanderlight | Travel slowly")

    def get_security_review(self, request_or_html: str) -> dict[str, Any]:
        policy = security_policy(request_or_html)
        if not policy.approved:
            return policy.model_dump()
        if "<" not in request_or_html:
            return policy.model_dump()
        from software_factory.local_checks import inspect_security
        local = inspect_security(request_or_html)
        if not local.approved:
            return local.model_dump()
        if self._digest(request_or_html) != FIXTURE_SHA256:
            return Review(approved=False, issues=["Candidate differs from the pre-reviewed teaching fixture"], summary="A fixture review cannot approve changed HTML; review and replace the fixture evidence first.").model_dump()
        return self._fixture_review("security_review.json", request_or_html).model_dump()

    def review_ui(self, artifact: SiteArtifact) -> Review:
        artifact = SiteArtifact.model_validate(artifact)
        from software_factory.local_checks import inspect_ui
        local = inspect_ui(artifact.html)
        if not local.approved:
            return local
        if self._digest(artifact.html) != FIXTURE_SHA256:
            return Review(approved=False, issues=["Candidate differs from the pre-reviewed teaching fixture"], summary="The pre-generated UI review applies only to its recorded HTML hash.")
        return self._fixture_review("ui_review.json", artifact.html)

    def generate_qa(self, artifact: SiteArtifact) -> QAPlan:
        artifact = SiteArtifact.model_validate(artifact)
        try:
            record = QARecord.model_validate_json((FIXTURE_DIR / "qa_plan.json").read_text(encoding="utf-8"))
        except (OSError, ValidationError):
            raise HarnessError("QA fixture is missing or violates the typed contract") from None
        if record.artifact_sha256 != self._digest(artifact.html):
            raise HarnessError("QA fixture evidence does not match this candidate HTML")
        return record.plan

    def call_role(self, role: Role, data: dict[str, Any]) -> Plan | SiteArtifact | Review | QAPlan:
        """Small explicit router; results never grant execution permissions."""
        if role not in ROLES:
            raise ValueError("Unknown agent role")
        if role == "manager":
            return self.plan(data["request"])
        if role == "coder":
            return self.build_site(data["request"], Plan.model_validate(data["plan"]))
        if role == "security":
            return Review.model_validate(self.get_security_review(data["untrusted_input"]))
        artifact = SiteArtifact.model_validate(data)
        if role == "ui_ux":
            return self.review_ui(artifact)
        if role == "qa":
            return self.generate_qa(artifact)
        raise ValueError("Unknown agent role")

    @staticmethod
    def _digest(html: str) -> str:
        return hashlib.sha256(html.encode("utf-8")).hexdigest()

    def _fixture_review(self, name: str, html: str) -> Review:
        try:
            record = FixtureRecord.model_validate_json((FIXTURE_DIR / name).read_text(encoding="utf-8"))
        except (OSError, ValidationError):
            raise HarnessError("Review fixture is missing or violates the typed contract") from None
        if record.artifact_sha256 != self._digest(html):
            raise HarnessError("Pre-generated review evidence does not match this candidate HTML")
        return record.review
