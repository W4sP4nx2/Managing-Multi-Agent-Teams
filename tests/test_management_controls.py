"""Regression tests for the manually rehearsed Manager audit and oversight."""
from __future__ import annotations

from types import SimpleNamespace as Obj

import pytest

from tests.workshop_support import notebook_definitions, workshop_paths

pytestmark = pytest.mark.unit


@pytest.fixture
def audit(repo_root):
    names = {"StrictContract", "CodePatch", "QAReport", "manager_audit_gate"}
    with notebook_definitions(workshop_paths(repo_root)["lab2"], "lab2", names) as ns:
        yield ns


def team(ns):
    manager = Obj(tools=[Obj(name="approve_code_tool")], allow_delegation=True)
    coder = Obj(tools=[Obj(name="write_code_tool")])
    qa = Obj(tools=[Obj(name="run_tests_tool")])
    brief = Obj()
    implementation = Obj(agent=coder, context=[brief], output_pydantic=ns["CodePatch"])
    review = Obj(agent=qa, context=[implementation], output_pydantic=ns["QAReport"])
    return [manager, coder, qa, brief, implementation, review]


def test_manager_admits_one_typed_proposal(audit):
    result, patch = audit["manager_audit_gate"](*team(audit), {"user_id": "101", "operation": "create"})
    assert result["decision"] == "PASS_TO_QA"
    assert all(result["checks"].values())
    assert isinstance(patch, audit["CodePatch"])
    assert patch.user_id == "101"


@pytest.mark.parametrize("fault", [
    "manager_write", "manager_no_delegation", "coder_approval", "qa_write",
    "wrong_owner", "wrong_qa_owner", "lost_architect_context", "lost_qa_context", "untyped_coder", "untyped_qa",
])
def test_manager_blocks_independent_permission_and_handoff_faults(audit, fault):
    agents = team(audit)
    manager, coder, qa, _, implementation, review = agents
    if fault == "manager_write": manager.tools.append(Obj(name="write_code_tool"))
    elif fault == "manager_no_delegation": manager.allow_delegation = False
    elif fault == "coder_approval": coder.tools.append(Obj(name="approve_code_tool"))
    elif fault == "qa_write": qa.tools.append(Obj(name="write_code_tool"))
    elif fault == "wrong_owner": implementation.agent = qa
    elif fault == "wrong_qa_owner": review.agent = coder
    elif fault == "lost_architect_context": implementation.context = []
    elif fault == "lost_qa_context": review.context = []
    elif fault == "untyped_coder": implementation.output_pydantic = None
    elif fault == "untyped_qa": review.output_pydantic = None
    result, patch = audit["manager_audit_gate"](*agents, {"user_id": "101", "operation": "create"})
    assert result["decision"] == "BLOCK"
    assert not all(result["checks"].values())
    assert patch is None


@pytest.mark.parametrize("payload", [
    {"user_id": 101, "operation": "create"},
    {"user_id": "101", "operation": "create", "approved": True},
    {"operation": "create"},
])
def test_manager_rejects_malformed_candidate_even_with_valid_roles(audit, payload):
    result, patch = audit["manager_audit_gate"](*team(audit), payload)
    assert result["decision"] == "BLOCK" and patch is None
    assert result["checks"]["Current Coder payload validates"] is False


@pytest.mark.filterwarnings("ignore:Pydantic serializer warnings:UserWarning")
def test_manager_revalidates_a_model_constructed_without_validation(audit):
    candidate = audit["CodePatch"].model_construct(user_id=101, operation="create")
    result, patch = audit["manager_audit_gate"](*team(audit), candidate)
    assert result["decision"] == "BLOCK" and patch is None
    assert result["checks"]["Current Coder payload validates"] is False


@pytest.fixture
def oversight(repo_root):
    names = {"SecureToolInput", "malicious_tool_input", "MAX_RETRIES", "MOCK_COST_PER_CALL",
             "always_failing_mock", "run_repair_loop", "management_oversight"}
    with notebook_definitions(workshop_paths(repo_root)["lab3"], "lab3", names, "fixed") as ns:
        yield ns


def test_failed_worker_has_four_calls_and_explicit_escalation(oversight):
    state = oversight["run_repair_loop"](3)
    assert state == {"calls": 4, "cost": 0.20, "escalated": True}
    result = oversight["management_oversight"](state, ["123"])
    assert result["decision"] == "ESCALATE_TO_HUMAN"
    assert result["release_approved"] is False


def test_repair_stops_immediately_when_worker_succeeds(oversight, monkeypatch):
    outcomes = iter([False, True])
    monkeypatch.setitem(oversight, "always_failing_mock", lambda: next(outcomes))
    assert oversight["run_repair_loop"](3) == {"calls": 2, "cost": 0.10, "escalated": False}


@pytest.mark.parametrize("field,value", [
    ("calls", True), ("calls", 3), ("calls", 5), ("calls", "4"),
    ("cost", -0.05), ("cost", 0.15), ("cost", 0.25), ("cost", None),
    ("escalated", False), ("escalated", 1),
])
def test_oversight_blocks_forged_or_incomplete_execution_evidence(oversight, field, value):
    state = {"calls": 4, "cost": 0.20, "escalated": True, field: value}
    result = oversight["management_oversight"](state, ["123"])
    assert result["decision"] == "BLOCK_AND_REPAIR_CONTROLS"
    assert result["release_approved"] is False


def test_oversight_detects_unsafe_call_in_history(oversight):
    state = oversight["run_repair_loop"](3)
    result = oversight["management_oversight"](state, ["123", oversight["malicious_tool_input"]["user_id"]])
    assert result["decision"] == "BLOCK_AND_REPAIR_CONTROLS"
    assert result["checks"]["Unsafe value absent from tool calls"] is False


@pytest.mark.parametrize("user_id", ["", "1234567890123", "123; DROP TABLE users; --", " 123", "123\n"])
def test_input_gate_rejects_values_outside_documented_id_contract(oversight, user_id):
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        oversight["SecureToolInput"].model_validate({"user_id": user_id})


@pytest.mark.parametrize("user_id", ["0", "123456789012"])
def test_input_gate_accepts_boundary_length_ids(oversight, user_id):
    assert oversight["SecureToolInput"].model_validate({"user_id": user_id}).user_id == user_id
