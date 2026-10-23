"""Governance checks against the actual optional Mock CI/CD handout definitions."""
from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

pytestmark = pytest.mark.unit


@pytest.fixture
def pipeline(repo_root):
    notebook = json.loads((repo_root / "extensions/11_mock_cicd_pipeline.ipynb").read_text())
    namespace = {"__name__": "mock_cicd_unit"}
    for cell in notebook["cells"]:
        if cell["id"] in {"mock-cicd-contract", "mock-cicd-pipeline"}:
            code = compile("".join(cell["source"]), cell["id"], "exec", dont_inherit=True)
            exec(code, namespace)
    return namespace


def feature(ns, description="Add login button"):
    return ns["FeatureRequest"](id="FEAT-001", description=description)


def decision(ns, candidate, approved=True, **changes):
    values = {"feature_id": candidate.id, "revision": candidate.revision,
              "description": candidate.description, "approved": approved,
              "reviewer": "Workshop manager"}
    return ns["ManagerDecision"](**{**values, **changes})


def run_qa(ns, candidate, outcome=True):
    return ns["run_parallel_development"]([candidate], {candidate.id: outcome})[0]


def approve(ns, candidate, decisions=(), security=True):
    return ns["security_and_manager_approval"](
        [candidate], decisions, {candidate.id: security})[0]


@pytest.mark.parametrize("description", [
    "Refactor database schema; DROP TABLE users;", "try bypass_auth", "drop table records",
])
def test_forbidden_fixture_blocks_before_approval(pipeline, description):
    candidate = run_qa(pipeline, feature(pipeline, description))
    assert candidate.status == pipeline["FeatureStatus"].BLOCKED
    assert candidate.qa_passed is False and candidate.security_cleared is False
    assert approve(pipeline, candidate, [decision(pipeline, candidate)]).status == candidate.status


def test_missing_manager_decision_waits_after_security(pipeline):
    candidate = approve(pipeline, run_qa(pipeline, feature(pipeline)))
    assert candidate.status == pipeline["FeatureStatus"].SECURITY_APPROVED
    assert candidate.qa_passed is True and candidate.security_cleared is True
    assert candidate.manager_decision is None


def test_explicit_approval_deploys_only_after_both_gates(pipeline):
    candidate = feature(pipeline)
    approval = decision(pipeline, candidate)
    assert approve(pipeline, candidate, [approval]).status == pipeline["FeatureStatus"].REQUESTED
    candidate = approve(pipeline, run_qa(pipeline, candidate), [approval])
    assert candidate.status == pipeline["FeatureStatus"].DEPLOYED
    assert candidate.manager_decision == approval


def test_manager_denial_blocks_and_preserves_review_evidence(pipeline):
    candidate = run_qa(pipeline, feature(pipeline))
    candidate = approve(pipeline, candidate, [decision(pipeline, candidate, False)])
    assert candidate.status == pipeline["FeatureStatus"].BLOCKED
    assert candidate.qa_passed is True and candidate.security_cleared is True
    assert candidate.manager_decision.approved is False


@pytest.mark.parametrize("stage", ["qa", "security"])
@pytest.mark.parametrize("outcome", [False, None, "true", 1])
def test_gate_requires_explicit_true_fixture(pipeline, stage, outcome):
    candidate = run_qa(pipeline, feature(pipeline), outcome if stage == "qa" else True)
    candidate = approve(pipeline, candidate, [decision(pipeline, candidate)],
                        outcome if stage == "security" else True)
    assert candidate.status == pipeline["FeatureStatus"].BLOCKED
    assert candidate.manager_decision is None


@pytest.mark.parametrize("change", [
    {"feature_id": "FEAT-999"}, {"revision": 2}, {"description": "Different feature"},
])
def test_stale_or_wrong_feature_approval_cannot_deploy(pipeline, change):
    candidate = run_qa(pipeline, feature(pipeline))
    candidate = approve(pipeline, candidate, [decision(pipeline, candidate, **change)])
    assert candidate.status == pipeline["FeatureStatus"].SECURITY_APPROVED


def test_resubmit_discards_all_evidence_and_requires_new_approval(pipeline):
    original = feature(pipeline)
    old_decision = decision(pipeline, original)
    deployed = approve(pipeline, run_qa(pipeline, original), [old_decision])
    fresh = pipeline["resubmit_feature"](deployed, "Implement 2FA")
    assert fresh.revision == 2 and fresh.status == pipeline["FeatureStatus"].REQUESTED
    assert fresh.qa_passed is False and fresh.security_cleared is False
    assert fresh.reviewed_description is None and fresh.manager_decision is None
    fresh = approve(pipeline, run_qa(pipeline, fresh), [old_decision])
    assert fresh.status == pipeline["FeatureStatus"].SECURITY_APPROVED
    fresh = approve(pipeline, fresh, [decision(pipeline, fresh)])
    assert fresh.status == pipeline["FeatureStatus"].DEPLOYED


def test_stuck_feature_requires_resubmit_and_all_gates(pipeline):
    blocked = run_qa(pipeline, feature(pipeline, "DROP TABLE users"))
    fresh = pipeline["resubmit_feature"](blocked, "Refactor database schema safely")
    assert blocked.status == pipeline["FeatureStatus"].BLOCKED
    fresh = approve(pipeline, run_qa(pipeline, fresh), [decision(pipeline, fresh)])
    assert fresh.status == pipeline["FeatureStatus"].DEPLOYED
    unsafe = pipeline["resubmit_feature"](fresh, "BYPASS_AUTH")
    assert run_qa(pipeline, unsafe).status == pipeline["FeatureStatus"].BLOCKED


@pytest.mark.parametrize("description", ["Changed safe request", "DROP TABLE users"])
def test_changing_description_cannot_reuse_qa_evidence(pipeline, description):
    candidate = run_qa(pipeline, feature(pipeline))
    with pytest.raises(ValidationError):
        candidate.description = description
    # model_copy bypasses Pydantic validation; the receiving gate must revalidate.
    forged = candidate.model_copy(update={"description": description})
    with pytest.raises(ValueError, match="Invalid feature contract"):
        approve(pipeline, forged, [decision(pipeline, forged)])


def test_replaying_pipeline_is_idempotent(pipeline):
    candidate = feature(pipeline)
    candidate = approve(pipeline, run_qa(pipeline, candidate), [decision(pipeline, candidate)])
    before = candidate.model_dump()
    events = list(pipeline["PIPELINE_LOG"])
    replay = approve(pipeline, run_qa(pipeline, candidate), [decision(pipeline, candidate)])
    assert replay.model_dump() == before
    assert pipeline["PIPELINE_LOG"] == events


@pytest.mark.parametrize("values", [
    {"id": 1}, {"id": "wrong"}, {"description": ""}, {"description": "   "},
    {"description": 123}, {"qa_passed": "yes"}, {"security_cleared": 1},
    {"status": "UNKNOWN"}, {"status": "DEPLOYED"}, {"status": "QA_PASSED"},
    {"qa_passed": True}, {"security_cleared": True}, {"revision": True},
    {"revision": 0}, {"extra_field": "untrusted"},
])
def test_feature_contract_rejects_invalid_or_unsubstantiated_state(pipeline, values):
    raw = {"id": "FEAT-001", "description": "Add login button", **values}
    assert pipeline["safe_validate"](pipeline["FeatureRequest"], raw) is None


@pytest.mark.parametrize("values", [
    {"approved": "yes"}, {"approved": 1}, {"reviewer": ""}, {"revision": 0},
    {"description": ""}, {"feature_id": "untyped"}, {"extra_field": True},
])
def test_manager_decision_contract_rejects_ambiguous_input(pipeline, values):
    with pytest.raises(ValidationError):
        decision(pipeline, feature(pipeline), **values)


def test_duplicate_batch_or_decisions_fail_closed(pipeline):
    candidate = feature(pipeline)
    with pytest.raises(ValueError, match="Duplicate feature"):
        pipeline["run_parallel_development"]([candidate, candidate], {candidate.id: True})
    candidate = run_qa(pipeline, candidate)
    approval = decision(pipeline, candidate)
    with pytest.raises(ValueError, match="Duplicate Manager"):
        approve(pipeline, candidate, [approval, approval])


def test_lifecycle_records_every_state(pipeline):
    candidate = feature(pipeline)
    pipeline["resubmit_feature"](candidate, "Add login button")
    approve(pipeline, run_qa(pipeline, candidate), [decision(pipeline, candidate)])
    run_qa(pipeline, feature(pipeline, "DROP TABLE users"))
    assert {item["status"] for item in pipeline["PIPELINE_LOG"]} == {
        state.value for state in pipeline["FeatureStatus"]}
