# %% {"id": "mock-cicd-intro", "type": "markdown"}
# # Optional extension — Mock CI/CD Pipeline
#
# **Your role: delivery manager.** Follow three feature requests through Dev/QA, Security, and an explicit simulated Manager decision. Inspect why a critical feature is blocked, then resubmit a corrected request without reusing old evidence.
#
# This is an **offline, sequential batch simulation**. The function name `run_parallel_development` represents a conceptual fan-out; its Python loop starts no parallel workers. QA outcomes and Security outcomes are local fixtures. The marker checks recognize only `DROP TABLE` and `BYPASS_AUTH`; they are not real tests, security scans, or complete injection defenses. `DEPLOYED` changes an in-memory enum only. No service, database, webhook, human notification, or deployment runs.
#
# Use the integrated factory and local CI/CD labs alongside this reference. This extension adds no dependencies, assessed work, or marks. A typed Manager decision models a human decision supplied to a workflow; it does not authenticate a human or request real approval.
#
# **Lifecycle:** REQUESTED → IN_PROGRESS → QA_PASSED → SECURITY_APPROVED → DEPLOYED. A failed gate or denial leads to BLOCKED. An explicit resubmission creates a new REQUESTED revision and clears prior evidence.

# %% {"id": "mock-cicd-contract", "type": "code"}
USE_LIVE_LLM = False

import json
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator


def inspect_state(step: str, data: dict):
    """Inspect synthetic or redacted state; never pass credentials or personal data."""
    print(f"\n🔍 INSPECTING: {step}")
    print(json.dumps(data, indent=2, default=str))
    print("─" * 40)


def safe_validate(schema, data):
    """Return a validated model or None; unexpected exceptions still propagate."""
    try:
        return schema.model_validate(data)
    except ValidationError as error:
        issue = error.errors(include_input=False, include_url=False)[0]
        field = ".".join(str(part) for part in issue["loc"]) or "<model>"
        # Fixed policy messages below contain no rejected input values.
        print(f"🛑 GOVERNANCE BLOCK at {schema.__name__}: {issue['msg']} (Field: {field})")
        return None


class FeatureStatus(str, Enum):
    REQUESTED = "REQUESTED"
    IN_PROGRESS = "IN_PROGRESS"
    QA_PASSED = "QA_PASSED"
    SECURITY_APPROVED = "SECURITY_APPROVED"
    DEPLOYED = "DEPLOYED"
    BLOCKED = "BLOCKED"


class ManagerDecision(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, revalidate_instances="always")
    feature_id: str = Field(strict=True, pattern=r"^FEAT-[0-9]{3}$")
    revision: int = Field(strict=True, ge=1)
    description: str = Field(strict=True, min_length=1)
    approved: bool = Field(strict=True)
    reviewer: str = Field(strict=True, min_length=1)

    @field_validator("description", "reviewer")
    @classmethod
    def require_visible_text(cls, value):
        if not value.strip():
            raise ValueError("Decision description and reviewer must contain text.")
        return value


class FeatureRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, revalidate_instances="always")
    id: str = Field(strict=True, pattern=r"^FEAT-[0-9]{3}$")
    description: str = Field(strict=True, min_length=1)
    status: FeatureStatus = FeatureStatus.REQUESTED
    revision: int = Field(default=1, strict=True, ge=1)
    qa_passed: bool = Field(default=False, strict=True)
    security_cleared: bool = Field(default=False, strict=True)
    reviewed_description: str | None = None
    manager_decision: ManagerDecision | None = None
    block_reason: str | None = None

    @field_validator("description")
    @classmethod
    def require_description(cls, value):
        if not value.strip():
            raise ValueError("Feature description must contain text.")
        return value

    @property
    def is_malicious(self) -> bool:
        return any(marker in self.description.upper() for marker in ("DROP TABLE", "BYPASS_AUTH"))

    @model_validator(mode="after")
    def enforce_gate_evidence(self):
        if self.qa_passed:
            if self.reviewed_description != self.description or self.is_malicious:
                raise ValueError("QA evidence must match the current description and pass teaching marker checks.")
        elif self.reviewed_description is not None:
            raise ValueError("A description snapshot requires passed QA.")
        if self.security_cleared and not self.qa_passed:
            raise ValueError("Security clearance requires passed QA.")
        if self.manager_decision is not None:
            decision = self.manager_decision
            if (decision.feature_id, decision.revision, decision.description) != (
                self.id, self.revision, self.description
            ) or not (self.qa_passed and self.security_cleared):
                raise ValueError("Manager evidence requires both gates and must match this feature revision.")
            expected = FeatureStatus.DEPLOYED if decision.approved else FeatureStatus.BLOCKED
            if self.status != expected:
                raise ValueError("The lifecycle state must agree with the recorded Manager decision.")
        if self.status in (FeatureStatus.REQUESTED, FeatureStatus.IN_PROGRESS):
            if self.qa_passed or self.security_cleared or self.manager_decision is not None:
                raise ValueError("New or in-progress work cannot carry passed gate evidence.")
        elif self.status == FeatureStatus.QA_PASSED:
            if not self.qa_passed or self.security_cleared or self.manager_decision is not None:
                raise ValueError("QA_PASSED requires QA evidence and no later approval.")
        elif self.status == FeatureStatus.SECURITY_APPROVED:
            if not (self.qa_passed and self.security_cleared) or self.manager_decision is not None:
                raise ValueError("SECURITY_APPROVED requires both gates and awaits a Manager decision.")
        elif self.status == FeatureStatus.DEPLOYED:
            if self.manager_decision is None or not self.manager_decision.approved:
                raise ValueError("Simulated DEPLOYED requires explicit current-revision Manager approval.")
        if self.status == FeatureStatus.BLOCKED:
            if self.block_reason is None or not self.block_reason.strip():
                raise ValueError("BLOCKED requires an explanation.")
        elif self.block_reason is not None:
            raise ValueError("Only a BLOCKED feature may carry a block reason.")
        return self

# %% {"id": "mock-cicd-gates-instructions", "type": "markdown"}
# ## Run, inspect, then decide
#
# The models are immutable. Every receiving gate revalidates the whole record; transition helpers validate a complete replacement record. QA evidence contains the reviewed description. A Manager decision names the exact feature, revision, and description. Description changes require resubmission and fresh gates.
#
# These checks enforce consistency of local teaching data. They do not authenticate evidence, prove software correct, or secure a production release. In a real workflow, independently produced test/scan artifacts and authenticated human decisions would be required. `inspect_state` does not redact secrets: all examples here are synthetic.
#
# Predict the state of FEAT-002 after Dev/QA, then explain what evidence a safe feature still needs before it may enter simulated DEPLOYED.

# %% {"id": "mock-cicd-pipeline", "type": "code"}
PIPELINE_LOG = []


def _checked_feature(feature):
    if not isinstance(feature, FeatureRequest):
        raise TypeError("Pipeline input must contain FeatureRequest objects.")
    checked = safe_validate(FeatureRequest, feature.model_dump())
    if checked is None:
        raise ValueError("Invalid feature contract; stop before any further gate.")
    return checked


def _checked_batch(features):
    checked = [_checked_feature(feature) for feature in features]
    if len({feature.id for feature in checked}) != len(checked):
        raise ValueError("Duplicate feature IDs are not allowed in a batch.")
    return checked


def _transition(feature, event, **changes):
    updated = FeatureRequest.model_validate({**feature.model_dump(), **changes})
    PIPELINE_LOG.append({"feature_id": updated.id, "revision": updated.revision,
                         "status": updated.status.value, "event": event})
    return updated


def run_parallel_development(features: list[FeatureRequest], qa_results=None) -> list[FeatureRequest]:
    """Action: simulate Dev/QA for REQUESTED items in a sequential batch.
    Input: typed features and explicit per-ID boolean QA fixture outcomes.
    Output: replacement records at QA_PASSED or BLOCKED; other states retain their evidence.
    Warning: no real workers or tests run; missing/non-True QA outcomes block.
    """
    results = {} if qa_results is None else qa_results
    output = []
    for feature in _checked_batch(features):
        if feature.status == FeatureStatus.REQUESTED:
            feature = _transition(feature, "Simulated development started", status=FeatureStatus.IN_PROGRESS)
            if feature.is_malicious or results.get(feature.id) is not True:
                reason = "Forbidden teaching marker detected" if feature.is_malicious else "QA fixture did not pass"
                feature = _transition(feature, reason, status=FeatureStatus.BLOCKED, block_reason=reason)
            else:
                feature = _transition(feature, "QA fixture passed", status=FeatureStatus.QA_PASSED,
                                      qa_passed=True, reviewed_description=feature.description)
        output.append(feature)
    return output


def security_and_manager_approval(features: list[FeatureRequest], manager_decisions=(),
                                  security_results=None) -> list[FeatureRequest]:
    """Action: apply separate simulated Security and Manager gates.
    Input: typed features, explicit ManagerDecision records, and per-ID Security fixture outcomes.
    Output: BLOCKED, SECURITY_APPROVED while awaiting a decision, or simulated DEPLOYED.
    Warning: never auto-approves a feature; stale decisions cannot authorize a revision.
    No security scanner, identity check, notification, or deployment runs.
    """
    checked = _checked_batch(features)
    decisions = {}
    for candidate in manager_decisions:
        raw = candidate.model_dump() if isinstance(candidate, BaseModel) else candidate
        decision = safe_validate(ManagerDecision, raw)
        if decision is None:
            raise ValueError("Invalid Manager decision; approval stopped.")
        if decision.feature_id in decisions:
            raise ValueError("Duplicate Manager decisions are not allowed.")
        decisions[decision.feature_id] = decision
    results = {} if security_results is None else security_results
    output = []
    for feature in checked:
        if feature.status == FeatureStatus.QA_PASSED:
            if feature.is_malicious or results.get(feature.id) is not True:
                feature = _transition(feature, "Security fixture did not pass", status=FeatureStatus.BLOCKED,
                                      block_reason="Security fixture did not pass")
            else:
                feature = _transition(feature, "Security fixture passed; Manager decision required",
                                      status=FeatureStatus.SECURITY_APPROVED, security_cleared=True)
        if feature.status == FeatureStatus.SECURITY_APPROVED:
            decision = decisions.get(feature.id)
            if decision is not None and (decision.revision, decision.description) == (
                feature.revision, feature.description
            ):
                feature = _transition(
                    feature, "Explicit simulated Manager approval" if decision.approved else "Manager denied revision",
                    status=FeatureStatus.DEPLOYED if decision.approved else FeatureStatus.BLOCKED,
                    manager_decision=decision, block_reason=None if decision.approved else "Manager denied revision",
                )
        output.append(feature)
    return output


def resubmit_feature(feature: FeatureRequest, description: str) -> FeatureRequest:
    """Action: submit a new request revision and discard all previous gate evidence.
    Input: an existing typed feature and the replacement description.
    Output: a fresh REQUESTED record with incremented revision and all gates reset.
    Warning: a description change alone does not unblock work or authorize release.
    """
    previous = _checked_feature(feature)
    fresh = FeatureRequest(id=previous.id, description=description, revision=previous.revision + 1)
    PIPELINE_LOG.append({"feature_id": fresh.id, "revision": fresh.revision,
                         "status": fresh.status.value, "event": "Resubmitted; all previous gate evidence discarded"})
    return fresh

# %% {"id": "mock-cicd-run", "type": "code"}
# Explicit local fixtures stand in for independently produced evidence.
QA_FIXTURES = {"FEAT-001": True, "FEAT-002": True, "FEAT-003": True}
SECURITY_FIXTURES = {"FEAT-001": True, "FEAT-002": True, "FEAT-003": True}
feature_batch = [
    FeatureRequest(id="FEAT-001", description="Add login button"),
    FeatureRequest(id="FEAT-002", description="Refactor database schema; DROP TABLE users;"),
    FeatureRequest(id="FEAT-003", description="Implement 2FA"),
]
inspect_state("Requested feature batch", {"features": [item.model_dump(mode="json") for item in feature_batch]})
feature_batch = run_parallel_development(feature_batch, QA_FIXTURES)
inspect_state("Sequential Dev/QA batch result", {"features": [item.model_dump(mode="json") for item in feature_batch]})

# %% {"id": "mock-cicd-approval-instructions", "type": "markdown"}
# ## Security and explicit simulated Manager decisions
#
# The supplied Manager-decision fixture approves **FEAT-001 and FEAT-003 only**. Security still runs first. A safe feature with no matching decision stays at SECURITY_APPROVED; a denial blocks it. These fixtures represent decisions already supplied by a simulated course manager; safety never creates approval automatically.

# %% {"id": "mock-cicd-approval", "type": "code"}
initial_manager_decisions = [
    ManagerDecision(feature_id="FEAT-001", revision=1, description="Add login button",
                    approved=True, reviewer="Simulated course manager"),
    ManagerDecision(feature_id="FEAT-003", revision=1, description="Implement 2FA",
                    approved=True, reviewer="Simulated course manager"),
]
feature_batch = security_and_manager_approval(feature_batch, initial_manager_decisions, SECURITY_FIXTURES)
initial_states = {item.id: item.status.value for item in feature_batch}
inspect_state("Initial final states (simulation only)", initial_states)
inspect_state("Pipeline transition evidence", {"events": PIPELINE_LOG})

# %% {"id": "mock-cicd-incident", "type": "markdown"}
# ## Exercise — Unblock the Pipeline (ungraded)
#
# FEAT-002 is BLOCKED. The Product Owner says its intended request was **"Refactor database schema safely"**. A critical request still needs every gate.
#
# 1. In the next cell, replace `replacement_description` with that safe request. Call the supplied `resubmit_feature` helper as written: it creates a new REQUESTED revision and discards old QA, Security, and Manager evidence. Editing a BLOCKED record without resubmitting would leave it outside the run phase.
# 2. Run that cell and inspect fresh Dev/QA and Security evidence. The safe revision must stop at SECURITY_APPROVED because no Manager decision has been supplied yet.
# 3. In the following cell, deliberately set `approve_repaired_feature = True` to model the Manager's approval after review, or `False` to model denial. `None` means no decision. This is a local decision fixture, not a real approval request.
# 4. Run the decision and proof cells. Prove the safe revision reaches simulated DEPLOYED with passed QA, Security clearance, and a matching explicit Manager decision. Explain why changing the description or presenting an older approval is insufficient.
#
# The starter deliberately keeps the unsafe description and no decision; it executes cleanly and remains BLOCKED. Change the two learner inputs above, not the gate functions. Rerun the repair cell before the decision cell when trying another description; a new revision always needs a new decision.

# %% {"id": "mock-cicd-repair", "type": "code"}
# LEARNER INPUT 1: replace with "Refactor database schema safely".
replacement_description = "Refactor database schema; DROP TABLE users;"
feature_batch[1] = resubmit_feature(feature_batch[1], replacement_description)
feature_batch = run_parallel_development(feature_batch, QA_FIXTURES)
feature_batch = security_and_manager_approval(feature_batch, (), SECURITY_FIXTURES)
inspect_state("Resubmitted revision awaiting a decision", feature_batch[1].model_dump(mode="json"))

# %% {"id": "mock-cicd-repair-approval", "type": "code"}
# LEARNER INPUT 2: after inspecting the new evidence, choose True, False, or None.
approve_repaired_feature = None
candidate_for_decision = feature_batch[1]
repair_manager_decisions = []
if approve_repaired_feature is not None:
    repair_manager_decisions = [ManagerDecision(
        feature_id=candidate_for_decision.id,
        revision=candidate_for_decision.revision,
        description=candidate_for_decision.description,
        approved=approve_repaired_feature,
        reviewer="Simulated course manager",
    )]
feature_batch = security_and_manager_approval(feature_batch, repair_manager_decisions, SECURITY_FIXTURES)
repaired_feature = feature_batch[1]
inspect_state("Manager decision result (simulation only)", repaired_feature.model_dump(mode="json"))

# %% {"id": "mock-cicd-repair-proof", "type": "code"}
if repaired_feature.status == FeatureStatus.DEPLOYED:
    assert repaired_feature.qa_passed and repaired_feature.security_cleared
    assert repaired_feature.manager_decision is not None and repaired_feature.manager_decision.approved is True
    assert repaired_feature.manager_decision.revision == repaired_feature.revision
    assert repaired_feature.manager_decision.description == repaired_feature.description
    print("✅ SUCCESS: corrected revision passed every gate and reached simulated DEPLOYED.")
else:
    print("Release held:", repaired_feature.status.value)
    print("Inspect the current description, gate evidence, and explicit Manager decision; resubmit before retrying blocked work.")
inspect_state("Final feature states (simulation only)", {item.id: item.status.value for item in feature_batch})
inspect_state("Final transition evidence", {"events": PIPELINE_LOG})

# %% {"id": "mock-cicd-reflection", "type": "markdown"}
# ## Reflect and return
#
# Identify the feature, revision, gate, decision, and next owner from the trace. Which evidence is simulated? What independent evidence and authenticated decision would a real release require? A successful local state transition demonstrates this exercise's governance flow, not production safety.
#
# Return to [optional extensions](../README.md#reference-and-maintenance) or the [Capstone](../notebooks/04_capstone.ipynb). The required course sequence and marks are unchanged.
