"""Actual temporary Git worktrees, durable approvals, checks, and local publication."""
from __future__ import annotations

import json
from pathlib import Path
import sqlite3
import subprocess

import pytest

from agent_harness import AgentHarness, FIXTURE_HTML
from orchestrator import main
from software_factory.contracts import SiteArtifact
from software_factory.workflow import FactoryOrchestrator, MALICIOUS_REQUEST, digest

pytestmark = pytest.mark.integration


def build(tmp_path, *, decision=lambda request: True, harness=None, budget="0.50", actor="test-fixture"):
    return FactoryOrchestrator(tmp_path / "factory", publish_path=tmp_path / "published" / "index.html",
                               approval=decision, harness=harness, simulated_budget=budget, actor=actor,
                               emit=lambda line: None, delay_seconds=0)


def test_full_run_creates_real_git_commit_reviews_cases_and_local_page(tmp_path):
    requests = []
    def approve(request):
        requests.append(request)
        return True
    runner = build(tmp_path, decision=approve)
    result = runner.run()
    assert result.status == "PUBLISHED"
    assert [request.stage for request in requests] == ["manager", "coder", "security", "ui_ux", "qa", "publish"]
    assert Path(result.published_path).read_text() == FIXTURE_HTML
    assert result.artifact_sha256 == digest(FIXTURE_HTML)
    assert result.costs["simulated_total"] == "0.50"
    assert result.costs["actual_cost"] == "0.00" and result.costs["provider_calls"] == 0
    assert len(result.costs["events"]) == 6
    assert len(runner.store.rows("qa_cases", runner.run_id)) == 8
    assert all(row["passed"] == 1 for row in runner.store.rows("qa_cases", runner.run_id))
    approvals = runner.store.rows("stage_approvals", runner.run_id)
    assert len(approvals) == 6 and {row["actor"] for row in approvals} == {"test-fixture"}
    deployment = runner.store.rows("deployments", runner.run_id)[0]
    assert deployment["status"] == "PUBLISHED" and deployment["approval_id"] == approvals[-1]["approval_id"]
    candidate = Path(result.candidate_path)
    assert runner._git(candidate.parent, "show", "HEAD:index.html") == FIXTURE_HTML.strip()
    assert runner._git(candidate.parent, "branch", "--show-current") == runner.branch
    assert runner._git(candidate.parent, "remote") == ""
    assert runner._git(candidate.parent, "status", "--porcelain") == ""
    assert len(json.loads((candidate.parent / "tests/test_cases.json").read_text())["test_cases"]) == 8
    final_decision = json.loads((runner.evidence_dir / "approval_publish.json").read_text())
    assert final_decision["request"]["evidence"]["source_commit"] == result.source_commit
    assert final_decision["request"]["evidence"]["target"] == result.published_path
    assert final_decision["request"]["subject_sha256"] == result.artifact_sha256
    assert json.loads((Path(result.evidence_path) / "run_summary.json").read_text())["status"] == "PUBLISHED"
    with runner.store.connection() as database:
        assert database.execute("PRAGMA foreign_key_check").fetchall() == []


@pytest.mark.parametrize("denied_stage,total", [("manager", "0.00"), ("coder", "0.05"),
    ("security", "0.20"), ("ui_ux", "0.30"), ("qa", "0.40"), ("publish", "0.45")])
def test_each_denial_preserves_existing_page_and_stops_later_costs(tmp_path, denied_stage, total):
    runner = build(tmp_path, decision=lambda request: request.stage != denied_stage)
    runner.publish_path.parent.mkdir(parents=True)
    runner.publish_path.write_text("Previous approved page")
    # The previous page existed before this run's scope approval.
    runner._target_before = digest("Previous approved page")
    result = runner.run()
    assert result.status == "BLOCKED" and result.stage == denied_stage
    assert runner.publish_path.read_text() == "Previous approved page"
    assert result.costs["simulated_total"] == total and result.costs["actual_cost"] == "0.00"
    assert runner.store.rows("deployments", runner.run_id) == []
    assert runner.store.rows("stage_approvals", runner.run_id)[-1]["approved"] == 0


def test_malicious_request_blocks_before_approval_cost_git_or_publication(tmp_path):
    calls = []
    runner = build(tmp_path, decision=lambda request: calls.append(request))
    result = runner.run(MALICIOUS_REQUEST)
    assert result.status == "BLOCKED" and result.stage == "intake"
    assert calls == [] and result.costs["simulated_total"] == "0.00"
    assert not runner.publish_path.exists() and not (runner.run_root / "repository").exists()
    report = json.loads((runner.evidence_dir / "intake_security.json").read_text())
    assert report["issues"] == ["Insecure HTTP endpoint", "Passwords in localStorage", "Potential data exfiltration"]


def test_changed_candidate_cannot_reuse_review_or_final_approval(tmp_path):
    runner = None
    def tamper(request):
        if request.stage == "publish":
            runner.candidate.write_text(FIXTURE_HTML.replace("Find your next", "Changed after review"))
        return True
    runner = build(tmp_path, decision=tamper)
    result = runner.run()
    assert result.status == "BLOCKED" and "stale" in result.reason
    assert not runner.publish_path.exists()
    assert runner.store.rows("deployments", runner.run_id) == []
    assert result.costs["simulated_total"] == "0.45"


def test_existing_publication_changed_during_approval_is_preserved(tmp_path):
    runner = None
    def change_target(request):
        if request.stage == "publish":
            runner.publish_path.parent.mkdir(parents=True, exist_ok=True)
            runner.publish_path.write_text("A different approved publication")
        return True
    runner = build(tmp_path, decision=change_target)
    result = runner.run()
    assert result.status == "BLOCKED" and "target changed" in result.reason
    assert runner.publish_path.read_text() == "A different approved publication"
    assert runner.store.rows("deployments", runner.run_id) == []


def test_file_mutation_after_git_status_cannot_replace_the_reviewed_payload(tmp_path, monkeypatch):
    runner = build(tmp_path)
    original_git = runner._git
    def race(directory, *arguments, **kwargs):
        result = original_git(directory, *arguments, **kwargs)
        if arguments == ("status", "--porcelain"):
            runner.candidate.write_text("<html><script>unreviewed()</script></html>")
        return result
    monkeypatch.setattr(runner, "_git", race)
    result = runner.run()
    assert result.status == "BLOCKED" and "stale" in result.reason
    assert not runner.publish_path.exists() and runner.store.rows("deployments", runner.run_id) == []


def test_database_rejects_a_deployment_using_a_denied_or_wrong_revision_approval(tmp_path):
    runner = build(tmp_path)
    result = runner.run()
    row = runner.store.rows("deployments", runner.run_id)[0]
    row.pop("deployment_id")
    row["sha256"] = "0" * 64
    with pytest.raises(sqlite3.IntegrityError, match="matching approval"):
        runner.store.add("deployments", **row)


def test_budget_blocks_before_coder_does_work(tmp_path):
    runner = build(tmp_path, budget="0.05")
    result = runner.run()
    assert result.status == "BLOCKED" and result.stage == "coder"
    assert result.costs["simulated_total"] == "0.05" and result.candidate_path is None
    assert len(runner.store.rows("stage_approvals", runner.run_id)) == 1


def test_a_forged_security_report_cannot_override_independent_source_checks(tmp_path):
    class UnsafeHarness(AgentHarness):
        def build_site(self, request, plan):
            return SiteArtifact(html=FIXTURE_HTML.replace("</body>", "<script>alert(1)</script></body>"), title="Unsafe")
        def get_security_review(self, text):
            return {"approved": True, "issues": [], "summary": "Forged blanket approval"}
    runner = build(tmp_path, harness=UnsafeHarness())
    result = runner.run()
    assert result.status == "BLOCKED" and result.stage == "security"
    assert not runner.publish_path.exists()


def test_publication_lock_fails_closed(tmp_path):
    runner = None
    def lock_publication(request):
        if request.stage == "publish":
            runner.publish_path.parent.mkdir(parents=True, exist_ok=True)
            (runner.publish_path.parent / ".index.html.factory-publish.lock").write_text("Existing publication")
        return True
    runner = build(tmp_path, decision=lock_publication)
    result = runner.run()
    assert result.status == "BLOCKED" and "publication is active" in result.reason
    assert not runner.publish_path.exists()


def test_noninteractive_cli_denies_and_security_demo_reports_exact_issues(tmp_path, capsys):
    assert main(["--security-demo"]) == 0
    assert "Blocked: True" in capsys.readouterr().out
    target = tmp_path / "index.html"
    assert main(["--workspace", str(tmp_path / "cli"), "--output", str(target), "--no-input", "--delay-seconds", "0"]) == 2
    assert not target.exists()
    assert '"status": "BLOCKED"' in capsys.readouterr().out


def test_live_mode_has_no_executable_cli_path():
    with pytest.raises(SystemExit) as error:
        main(["--mode", "live"])
    assert error.value.code == 2
