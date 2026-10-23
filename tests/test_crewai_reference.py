"""Actual CrewAI execution under local fixtures; no provider or external network."""
import json
from unittest.mock import Mock

import nbformat
import pytest
from nbclient.exceptions import CellExecutionError

from crewai_learning.offline import blocked_network
from tests.notebook_runtime import execute_notebook


@pytest.fixture
def reference(monkeypatch, tmp_path):
    monkeypatch.setenv("CREWAI_STORAGE_DIR", str(tmp_path / "crewai"))
    monkeypatch.setenv("OTEL_SDK_DISABLED", "true")
    monkeypatch.setenv("CREWAI_TRACING_ENABLED", "false")
    monkeypatch.setenv("CREWAI_TELEMETRY_ENABLED", "false")
    with blocked_network() as network:
        from crewai_learning import coding_team as ref
        yield ref
    assert network == []


def order(ref):
    return ref.WorkOrder(task_id="test-add", spec="Add two numbers")


@pytest.mark.unit
def test_three_roles_and_all_task_boundaries_are_enforced(reference):
    crew = reference.build_crew(order(reference), reference.FixtureState(), 1)
    assert [a.role for a in crew.agents] == ["Manager", "Coder", "QA"]
    assert [t.output_pydantic for t in crew.tasks] == [reference.WorkOrder, reference.CodePatch,
                                                       reference.QAReport, reference.ManagerDecision]
    assert all(t.guardrail is not None and t.guardrail_max_retries == 0 for t in crew.tasks)
    assert all(a.max_retry_limit == 0 and not a.allow_delegation for a in crew.agents)
    assert crew.tasks[-1].agent is crew.tasks[0].agent
    assert crew.memory is False and crew.cache is False
    assert crew.verbose is False


@pytest.mark.unit
def test_direct_kickoff_returns_renderable_final_task_text(reference):
    from IPython.display import Markdown

    state = reference.FixtureState()
    crew = reference.build_crew(order(reference), state, 1)
    result = crew.kickoff(inputs={"task_id": "test-add"})
    assert [name for _, name in state.trace] == ["brief", "code", "qa", "review"]
    assert len(result.tasks_output) == 4
    assert isinstance(result.pydantic, reference.ManagerDecision)
    assert result.pydantic == reference.ManagerDecision.model_validate_json(result.raw)
    rendered = Markdown("### Final Crew task: Manager decision\n\n```json\n" + result.raw + "\n```")
    assert json.loads(result.raw)["status"] == "approved"
    assert result.raw in rendered.data


@pytest.mark.unit
@pytest.mark.parametrize("stage", ["brief", "code", "qa", "review"])
def test_garbage_raises_validation_error_before_the_next_task(reference, stage):
    state = reference.FixtureState(overrides={stage: "not JSON"})
    with pytest.raises(reference.ValidationError):
        reference.build_crew(order(reference), state, 1).kickoff()
    stages = ["brief", "code", "qa", "review"]
    assert [name for _, name in state.trace] == stages[:stages.index(stage) + 1]


@pytest.mark.unit
@pytest.mark.parametrize("payload", [
    '{"task_id":"test-add","code":123}',
    '{"task_id":"test-add","code":"valid","approved":true}',
    '{"task_id":"test-add"}',
])
def test_coder_contract_rejects_wrong_types_extra_and_missing_fields(reference, payload):
    state = reference.FixtureState(overrides={"code": payload})
    with pytest.raises(reference.ValidationError):
        reference.build_crew(order(reference), state, 1).kickoff()
    assert state.trace == [(1, "brief"), (1, "code")]


@pytest.mark.unit
def test_three_tool_failures_escalate_once_and_never_reach_qa(reference, monkeypatch):
    from crewai.tools import tool
    calls = []

    @tool("failing_code_tool")
    def failing_code_tool(spec: str) -> str:
        """Fail every call, including the third."""
        calls.append(spec)
        raise reference.SimulatedInfrastructureError("Simulated infrastructure error")

    escalate = Mock(wraps=reference.escalate_to_human)
    monkeypatch.setattr(reference, "escalate_to_human", escalate)
    state = reference.FixtureState(code_tool=failing_code_tool)
    result = reference.run_team(order(reference), state)
    assert isinstance(result, reference.EscalationReport)
    assert len(calls) == state.kickoffs == result.attempts == 3
    assert [failure.attempt for failure in result.failures] == [1, 2, 3]
    assert {failure.error_type for failure in result.failures} == {"SimulatedInfrastructureError"}
    assert state.trace == [(i, stage) for i in range(1, 4) for stage in ("brief", "code")]
    escalate.assert_called_once()


@pytest.mark.unit
def test_transient_failures_recover_on_third_attempt_with_feedback(reference):
    from crewai.tools import tool
    calls = []

    @tool("transient_code_tool")
    def transient_code_tool(spec: str) -> str:
        """Fail twice, then return the supplied successful code fixture."""
        calls.append(spec)
        if len(calls) < 3:
            raise reference.SimulatedInfrastructureError("Try the next bounded attempt")
        return reference.FIXTURE_CODE

    state = reference.FixtureState(code_tool=transient_code_tool)
    result = reference.run_team(order(reference), state)
    assert isinstance(result, reference.ApprovedResult)
    assert len(calls) == state.kickoffs == result.attempts == 3
    assert [len(items) for items in state.feedback_received] == [0, 1, 2]
    assert state.feedback_received[-1][-1]["error_type"] == "SimulatedInfrastructureError"


@pytest.mark.unit
def test_valid_fixture_stops_after_one_attempt(reference):
    state = reference.FixtureState()
    result = reference.run_team(order(reference), state)
    assert isinstance(result, reference.ApprovedResult)
    assert result.attempts == state.kickoffs == 1
    assert result.patch.code == reference.FIXTURE_CODE
    assert result.qa.passed and result.decision.status == "approved"


@pytest.mark.unit
def test_validation_failures_are_bounded_too(reference):
    state = reference.FixtureState(overrides={"code": "garbage"})
    result = reference.run_team(order(reference), state)
    assert isinstance(result, reference.EscalationReport)
    assert state.kickoffs == 3
    assert {f.error_type for f in result.failures} == {"ValidationError"}
    assert all(name in {"brief", "code"} for _, name in state.trace)


@pytest.mark.unit
@pytest.mark.parametrize("fault", ["failed_qa", "stale_hash", "wrong_task", "manager_reject"])
def test_approval_requires_matching_evidence_and_both_decisions(reference, fault):
    from hashlib import sha256
    qa = {"task_id":"test-add", "passed":True,
          "patch_sha256":sha256(reference.FIXTURE_CODE.encode()).hexdigest(), "checks":["fixture"]}
    decision = {"task_id":"test-add", "status":"approved", "reason":"fixture"}
    if fault == "failed_qa": qa["passed"] = False
    if fault == "stale_hash": qa["patch_sha256"] = "0" * 64
    if fault == "wrong_task": qa["task_id"] = "another-task"
    if fault == "manager_reject": decision["status"] = "needs_changes"
    state = reference.FixtureState(overrides={"qa":json.dumps(qa), "review":json.dumps(decision)})
    result = reference.run_team(order(reference), state)
    assert isinstance(result, reference.EscalationReport)
    assert state.kickoffs == 3


@pytest.mark.unit
def test_unexpected_programming_error_is_not_retried_as_infrastructure(reference, monkeypatch):
    monkeypatch.setattr(reference, "build_crew", Mock(side_effect=TypeError("implementation defect")))
    state = reference.FixtureState()
    with pytest.raises(TypeError, match="implementation defect"):
        reference.run_team(order(reference), state)
    assert state.kickoffs == 0


@pytest.mark.unit
def test_unexpected_error_during_kickoff_stops_without_retry_or_escalation(reference, monkeypatch):
    crew = Mock()
    crew.kickoff.side_effect = TypeError("unexpected executor defect")
    builder = Mock(return_value=crew)
    escalation = Mock(wraps=reference.escalate_to_human)
    monkeypatch.setattr(reference, "build_crew", builder)
    monkeypatch.setattr(reference, "escalate_to_human", escalation)
    state = reference.FixtureState()
    with pytest.raises(TypeError, match="unexpected executor defect"):
        reference.run_team(order(reference), state)
    assert state.kickoffs == 1
    builder.assert_called_once()
    crew.kickoff.assert_called_once_with(inputs={"task_id": "test-add"})
    escalation.assert_not_called()


@pytest.mark.integration
@pytest.mark.notebook
def test_reference_notebook_proves_three_failures_in_a_real_kernel(repo_root, tmp_path, request):
    path = repo_root / "crewai_learning/01_Bridge_Sequential_Crew.ipynb"
    notebook = json.loads(path.read_text())
    artifact_base = request.config.getoption("--notebook-artifacts")
    from pathlib import Path
    artifacts = Path(artifact_base) / "crewai-reference" if artifact_base else None
    result = execute_notebook(notebook, tmp_path, repo_root, fixture_crews=True, artifact_dir=artifacts,
        assertions='''
assert attempt_count == failing_state.kickoffs == 3
assert isinstance(escalation, EscalationReport)
assert escalation.code == "ESCALATION_TRIGGERED"
assert validation_error_name == "ValidationError"
assert successful_state.kickoffs == 1
assert [name for _, name in kickoff_state.trace] == ["brief", "code", "qa", "review"]
assert len(result.tasks_output) == 4
assert result.pydantic.status == "approved"
assert recovering_state.kickoffs == recovered.attempts == recovery_count == 3
assert [len(items) for items in recovering_state.feedback_received] == [0, 1, 2]
assert [a.role for a in example.agents] == ["Manager", "Coder", "QA"]
''')
    assert not any(out.get("output_type") == "error" for cell in result.cells
                   for out in cell.get("outputs", []))


@pytest.mark.integration
def test_fixture_kernel_still_blocks_external_network(repo_root, tmp_path):
    notebook = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(
        "import socket; socket.getaddrinfo('api.invalid', 443)")])
    with pytest.raises(CellExecutionError, match="OFFLINE_TRIPWIRE"):
        execute_notebook(notebook, tmp_path, repo_root, fixture_crews=True)
