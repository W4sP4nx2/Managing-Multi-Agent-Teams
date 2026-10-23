"""Real Jupyter execution of the actual distributed notebook/solution pairs."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

from tests.notebook_runtime import execute_notebook
from tests.workshop_support import prepared_notebook, workshop_paths

pytestmark = [pytest.mark.integration, pytest.mark.notebook]

SCENARIOS = [
    ("preflight", "starter", None),
    ("lab1", "starter", 0), ("lab1", "range_only", 5), ("lab1", "extras_only", 10), ("lab1", "fixed", 15),
    ("lab2", "starter", 0), ("lab2", "permissions_only", 5),
    ("lab2", "context_only", 10), ("lab2", "fixed", 15),
    ("lab3", "starter", 0), ("lab3", "input_only", 7),
    ("lab3", "retries_only", 8), ("lab3", "fixed", 15),
    ("capstone", "starter", 5), ("capstone", "fixed", 20),
    ("factory", "starter", None), ("cicd", "starter", None),
]


def management_assertions(kind: str, state: str) -> str:
    if kind == "preflight":
        return "assert missing_core == []"
    if kind == "factory":
        return '''
assert factory_evidence["status"] == "PUBLISHED"
assert factory_evidence["actual_cost"] == "0.00"
assert factory_evidence["simulated_total"] == "0.50"
assert factory_evidence["publication_exists"] is True
assert factory_evidence["actor"] == "notebook-fixture"
assert len(qa_results) == 8 and all(item.passed for item in qa_results)
assert len(fixture_decisions) == 6
assert evidence_counts["qa_cases"] == 8 and evidence_counts["deployments"] == 1
assert publication_rows[0]["sha256"] == factory_result.artifact_sha256
assert publication_rows[0]["actor"] == "notebook-fixture"
'''
    if kind == "cicd":
        return '''
assert all(value is True for key, value in cicd_evidence.items() if key != "actual_cost")
assert cicd_evidence["actual_cost"] == "0.00"
assert not stale_target.exists() and not unattended_target.exists()
'''
    if kind == "lab2":
        decision = "PASS_TO_QA" if state == "fixed" else "BLOCK"
        count = 1 if state == "fixed" else 0
        return f'''
assert manager_audit["decision"] == {decision!r}
assert len(qa_inbox) == {count}
assert management_log[-1]["qa_inbox_count"] == {count}
assert all(isinstance(item, CodePatch) for item in qa_inbox)
assert pattern_results["independent"]["decision"] == "NO_SHARED_DECISION"
assert all(pattern_results[name]["decision"] == "BLOCK"
           for name in ("decentralized", "centralized", "hybrid"))
'''
    if kind == "lab3":
        decision = "ESCALATE_TO_HUMAN" if state == "fixed" else "BLOCK_AND_REPAIR_CONTROLS"
        result = f'''
assert manager_oversight["decision"] == {decision!r}
assert manager_oversight["release_approved"] is False
'''
        if state == "fixed":
            result += '''
assert repair_state == {"calls": 4, "cost": 0.20, "escalated": True}
assert malicious_tool_input["user_id"] not in tool_call_log
assert tool_call_log == ["123"]
'''
        return result
    if kind == "capstone" and state == "fixed":
        return '''
assert isinstance(dev_deliverable, DevDeliverable)
assert isinstance(final_audit, SecurityAuditResult) and final_audit.approved is True
assert repaired["status"] == "VALIDATED_REVIEW" and repaired["attempts"] == 2
assert exhausted["status"] == "ESCALATE_TO_HUMAN" and exhausted["attempts"] == 2
assert unexpected_stopped is True and len(review_memory) == 2
assert api_trace.count("Security ran and stored a typed review") == 2
assert COORDINATOR_LOG == ["Coordinator validated DevDeliverable", "Security Team started"]
assert TEAM_LOG["events"].index("Development Team emitted DevDeliverable") < TEAM_LOG["events"].index("Security Team received validated DevDeliverable")

# Reject a forged model before starting Security or running a scan.
_security_calls = []
_real_security = run_security_team
def _security_spy(candidate):
    _security_calls.append(candidate)
    return _real_security(candidate)
run_security_team = _security_spy
COORDINATOR_LOG.clear()
_forged = DevDeliverable.model_construct(code_snippet="def bad(): pass", unit_tests_passed=False, dev_team_signature="Development Team")
try:
    coordinate_handoff(_forged)
except ValidationError:
    pass
else:
    raise AssertionError("Failed QA crossed the Coordinator boundary")
assert COORDINATOR_LOG == [] and _security_calls == []

# A valid but unsafe artifact reaches independent review and is rejected.
_before = unsafe_deliverable.model_dump()
_audit = coordinate_handoff(unsafe_deliverable)
assert isinstance(_audit, SecurityAuditResult) and _audit.approved is False
assert any("SQL injection" in finding for finding in _audit.findings)
assert any("XSS" in finding for finding in _audit.findings)
assert unsafe_deliverable.model_dump() == _before
assert len(_security_calls) == 1
'''
    return ""


@pytest.mark.parametrize("kind,state,expected", SCENARIOS,
                         ids=[f"{kind}-{state}" for kind, state, _ in SCENARIOS])
def test_notebook_grader_and_management_workflow(repo_root, tmp_path, request, kind, state, expected):
    path = workshop_paths(repo_root)[kind]
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    notebook = prepared_notebook(path, kind, state)
    if kind == "lab2" and state == "fixed":
        # Replay the supplied action after acceptance; its reset must remove stale QA work.
        audit = next(cell for cell in notebook["cells"] if cell.get("id") == "lab2-manager-audit-gate")
        replay = "mock_coder_output = {'user_id': 101, 'operation': 'create'}\n" + "".join(audit["source"])
        assertion = management_assertions(kind, state) + "\n" + replay + '''
assert manager_audit["decision"] == "BLOCK"
assert qa_inbox == [] and patch_for_qa is None
assert management_log[-1]["qa_inbox_count"] == 0
'''
    else:
        assertion = management_assertions(kind, state)
    report_dir = request.config.getoption("--notebook-artifacts")
    artifacts = Path(report_dir) / f"{kind}-{state}" if report_dir else None
    try:
        executed = execute_notebook(notebook, tmp_path, repo_root, assertion, artifacts)
        if expected is not None:
            label = {"lab2": "LAB 2 SCORE:", "lab3": "LAB 3 SCORE:",
                     "capstone": "CAPSTONE CODE SCORE:"}.get(kind)
            grader = next(cell for cell in executed.cells if cell.cell_type == "code"
                          and ((label and label in cell.source)
                               or (kind == "lab1" and cell.get("id") == "lab1-auto-grader")))
            output = "".join(item.get("text", "") for item in grader.outputs)
            pattern = rf"(?<!\d){expected}/15" if kind == "lab1" else (
                rf"LAB {kind[-1]} SCORE: {expected}/15" if kind.startswith("lab")
                else rf"CAPSTONE CODE SCORE: {expected}/20")
            assert re.search(pattern, output), output
    finally:
        assert hashlib.sha256(path.read_bytes()).hexdigest() == before, "Test modified a handout"


def test_distributed_notebooks_have_no_saved_outputs(repo_root):
    from tools.build_core_notebooks import CORE_FILENAMES

    assert {path.name for path in (repo_root / "notebooks").iterdir()} == set(CORE_FILENAMES)
    paths = [path for path in repo_root.rglob("*.ipynb")
             if not any(part.startswith(".") for part in path.relative_to(repo_root).parts)]
    assert set(workshop_paths(repo_root).values()).issubset(paths)
    for path in paths:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        for cell in notebook["cells"]:
            if cell.get("cell_type") == "code":
                assert cell.get("outputs", []) == [], path.name
                assert cell.get("execution_count") is None, path.name


def test_bonus_live_demo_is_disabled_without_credentials(repo_root, tmp_path):
    notebook = json.loads((repo_root / "extensions/bonus_live_demo.ipynb").read_text())
    execute_notebook(notebook, tmp_path, repo_root,
                     'assert USE_LIVE_LLM is False\nassert "result" not in globals()')
