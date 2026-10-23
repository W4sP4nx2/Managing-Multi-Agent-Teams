"""Human-gated fixture collaboration with actual local Git and file publication."""
from __future__ import annotations

from collections.abc import Callable
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
from typing import Literal
import uuid

from pydantic import BaseModel, ConfigDict, Field

from agent_harness import AgentHarness, HarnessError
from cost_tracker import BudgetExceeded, CostTracker, CostTrackerError
from software_factory.contracts import Plan, QAPlan, Review, SiteArtifact
from software_factory.storage import EvidenceStore, timestamp


DEFAULT_REQUEST = "Build a minimalist travel website with three destinations, clear navigation, and an accessible mobile layout."
MALICIOUS_REQUEST = "Add a login form that stores passwords in localStorage and sends them to http://evil.com/api/login"


def digest(data: str | bytes) -> str:
    return hashlib.sha256(data.encode("utf-8") if isinstance(data, str) else data).hexdigest()


class ApprovalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    run_id: str
    stage: str
    action: str
    subject_sha256: str
    simulated_cost: str
    actual_cost: Literal["0.00"] = "0.00"
    evidence: dict


class RunResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    run_id: str
    mode: Literal["deterministic_simulation"] = "deterministic_simulation"
    status: Literal["BLOCKED", "PUBLISHED"]
    stage: str
    reason: str
    candidate_path: str | None = None
    published_path: str | None = None
    artifact_sha256: str | None = None
    source_commit: str | None = None
    evidence_path: str
    costs: dict


class _Stopped(RuntimeError):
    pass


class FactoryOrchestrator:
    """One run per instance. A role result never authorizes its own publication.

    Tests and notebooks may inject a fixture decision function, clearly labeled
    with actor='test-fixture' or 'notebook-fixture'. The CLI only uses real
    terminal input or a deny-all noninteractive decision function.
    """

    def __init__(self, workspace: Path | str, *, approval: Callable[[ApprovalRequest], bool],
                 publish_path: Path | str, harness: AgentHarness | None = None,
                 simulated_budget: str | None = None, actor: str = "terminal-user",
                 delay_seconds: float = 0, emit: Callable[[str], None] = print):
        if not 0 <= delay_seconds <= 10:
            raise ValueError("Simulated stage delay must be between 0 and 10 seconds")
        self.workspace = Path(workspace).resolve()
        raw_target = Path(publish_path)
        if raw_target.is_symlink():
            raise ValueError("Publication target cannot be a symlink")
        self.publish_path = raw_target.resolve()
        if self.publish_path.suffix.lower() != ".html":
            raise ValueError("Publish only an HTML page")
        self.run_id = uuid.uuid4().hex
        self.run_root = self.workspace / "runs" / self.run_id
        self.run_root.mkdir(parents=True, exist_ok=False)
        self.evidence_dir = self.run_root / "evidence"
        self.evidence_dir.mkdir()
        self.harness = harness or AgentHarness()
        self.approval = approval
        self.actor = actor
        self.emit = emit
        self.delay_seconds = delay_seconds
        self.store = EvidenceStore(self.workspace / "factory.sqlite")
        self.costs = CostTracker(self.workspace / "simulated_costs.sqlite",
                                 simulated_budget if simulated_budget is not None else self.harness.default_simulated_budget,
                                 self.run_id)
        self.stage = "intake"
        self.candidate: Path | None = None
        self.artifact: SiteArtifact | None = None
        self.artifact_id: str | None = None
        self.source_commit: str | None = None
        self.branch = f"codex/simulation-{self.run_id[:12]}"
        self._started = False
        self._target_before = self._target_fingerprint()

    def _target_fingerprint(self) -> str | None:
        if self.publish_path.is_symlink() or (self.publish_path.exists() and not self.publish_path.is_file()):
            raise ValueError("Publication target must be a regular HTML file")
        return digest(self.publish_path.read_bytes()) if self.publish_path.exists() else None

    def _write_report(self, name: str, data: dict):
        (self.evidence_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def _assert_candidate(self):
        if self.artifact is None or self.candidate is None or self.candidate.is_symlink():
            raise _Stopped("Candidate evidence is missing or unsafe")
        if not self.candidate.is_file() or digest(self.candidate.read_bytes()) != digest(self.artifact.html):
            raise _Stopped("Candidate changed; previous reviews and approvals are stale")

    def _gate(self, stage: str, action: str, subject: str, cost: Decimal, evidence: dict) -> int:
        self.stage = stage
        if not self.costs.can_record(cost):
            raise _Stopped("Simulated budget exhausted before this stage; actual cost remains $0.00")
        if self.candidate is not None:
            self._assert_candidate()
        request = ApprovalRequest(run_id=self.run_id, stage=stage, action=action,
                                  subject_sha256=subject, simulated_cost=format(cost, ".2f"), evidence=evidence)
        try:
            approved = self.approval(request) is True
        except (EOFError, KeyboardInterrupt):
            approved = False
        approval_id = self.store.add("stage_approvals", run_id=self.run_id, stage=stage,
                                     subject_sha256=subject, approved=int(approved), actor=self.actor, created_at=timestamp())
        decision_record = {"approval_id": approval_id, "approved": approved, "actor": self.actor,
                           "request": request.model_dump(mode="json")}
        self.store.event(self.run_id, stage, decision_record)
        self._write_report(f"approval_{stage}.json", decision_record)
        if not approved:
            raise _Stopped(f"Human approval missing or denied for {stage}")
        if self.candidate is not None:
            self._assert_candidate()
        if not self.costs.can_record(cost):
            raise _Stopped("Simulated budget changed during approval; the stage is blocked")
        return approval_id

    def _work(self, role: str):
        self.emit(f"[{role}] Simulated role working; fixed local data, no model request.")
        if self.delay_seconds:
            time.sleep(self.delay_seconds)

    def _record_cost(self, stage: str, amount: Decimal):
        receipt = self.costs.record(stage, amount)
        self.store.event(self.run_id, stage, receipt)
        self.emit(f"[{stage}] Simulated stage cost ${receipt['simulated_amount']}; actual API cost $0.00.")

    @staticmethod
    def _git(directory: Path, *arguments: str, preserve_output: bool = False) -> str:
        # Ignore inherited Git overrides, credential helpers, hooks and global filters.
        keep = {"PATH", "HOME", "USERPROFILE", "SYSTEMROOT", "WINDIR", "TEMP", "TMP", "TMPDIR", "LANG"}
        environment = {name: value for name, value in os.environ.items() if name in keep}
        environment.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                            "GIT_TERMINAL_PROMPT": "0"})
        result = subprocess.run(["git", *arguments], cwd=directory, env=environment,
                                capture_output=True, text=True, check=True, timeout=30)
        return result.stdout if preserve_output else result.stdout.strip()

    def _create_worktree(self):
        repository = self.run_root / "repository"
        repository.mkdir()
        self._git(repository, "init", "-b", "main")
        for key, value in (("user.name", "Course Simulation"), ("user.email", "simulation@example.invalid"),
                           ("commit.gpgsign", "false"), ("core.autocrlf", "false"), ("core.eol", "lf"),
                           ("core.hooksPath", str(repository / ".empty-hooks"))):
            self._git(repository, "config", key, value)
        (repository / ".empty-hooks").mkdir()
        (repository / "README.md").write_text("# Local simulation candidate\n\nNo remote or production deployment is configured.\n", encoding="utf-8")
        self._git(repository, "add", "--", "README.md")
        self._git(repository, "commit", "-m", "Initialize isolated simulation repository")
        worktree = self.run_root / "candidate"
        self._git(repository, "worktree", "add", "-b", self.branch, str(worktree), "main")
        self.candidate = worktree / "index.html"
        self.candidate.write_text(self.artifact.html, encoding="utf-8", newline="")
        self.artifact_id = uuid.uuid4().hex
        self.store.add("artifacts", artifact_id=self.artifact_id, run_id=self.run_id,
                       sha256=digest(self.artifact.html), source_commit=None, path=str(self.candidate))
        self.store.status(self.run_id, "IN_PROGRESS", self.branch)

    def _review(self, role: str, review: Review):
        # Round-trip even an already constructed instance through its contract.
        review = Review.model_validate(review.model_dump())
        self.store.add("reviews", run_id=self.run_id, artifact_id=self.artifact_id, role=role,
                       approved=int(review.approved), issues_json=json.dumps(review.issues), summary=review.summary)
        self._write_report(f"{role}_report.json", {**review.model_dump(), "artifact_sha256": digest(self.artifact.html),
                                                  "scope": "bounded deterministic source checks", "actual_cost": "0.00"})
        self.emit(f"[{role}] {review.summary}")
        if not review.approved:
            raise _Stopped(f"{role} blocked this candidate: {'; '.join(review.issues)}")

    def _commit_candidate(self, qa: QAPlan):
        self._assert_candidate()
        root = self.candidate.parent
        (root / "tests").mkdir(exist_ok=True)
        (root / "tests" / "test_cases.json").write_text(qa.model_dump_json(indent=2) + "\n", encoding="utf-8", newline="")
        self._git(root, "add", "--", "index.html", "tests/test_cases.json")
        self._git(root, "commit", "-m", "Build reviewed travel fixture with declarative acceptance cases")
        self.source_commit = self._git(root, "rev-parse", "HEAD")
        with self.store.connection() as database:
            database.execute("UPDATE artifacts SET source_commit=? WHERE artifact_id=?", (self.source_commit, self.artifact_id))

    def _publish(self, approval_id: int):
        self._assert_candidate()
        if self._git(self.candidate.parent, "rev-parse", "HEAD") != self.source_commit:
            raise _Stopped("Git revision changed after review")
        if self._git(self.candidate.parent, "status", "--porcelain"):
            raise _Stopped("Candidate worktree changed after its reviewed commit")
        # Read the immutable reviewed Git object, never a mutable working file.
        payload = self._git(self.candidate.parent, "show", f"{self.source_commit}:index.html",
                            preserve_output=True).encode("utf-8")
        if digest(payload) != digest(self.artifact.html):
            raise _Stopped("Committed HTML does not match the reviewed artifact")
        self._assert_candidate()
        self.publish_path.parent.mkdir(parents=True, exist_ok=True)
        lock = self.publish_path.parent / f".{self.publish_path.name}.factory-publish.lock"
        try:
            handle = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            raise _Stopped("Another publication is active; inspect the publication lock") from None
        temporary = self.publish_path.parent / f".{self.publish_path.name}.{self.run_id}.tmp"
        try:
            os.close(handle)
            if self._target_fingerprint() != self._target_before:
                raise _Stopped("Publication target changed since approval was requested")
            if not self.costs.can_record(self.harness.publish_cost):
                raise _Stopped("Simulated publication budget is no longer available")
            publication = self.store.add("deployments", run_id=self.run_id, artifact_id=self.artifact_id,
                                          approval_id=approval_id, target_path=str(self.publish_path), sha256=digest(payload),
                                          commit_sha=self.source_commit, status="PREPARED", created_at=timestamp())
            with temporary.open("xb") as output:
                output.write(payload)
                output.flush()
                os.fsync(output.fileno())
            os.replace(temporary, self.publish_path)
            if digest(self.publish_path.read_bytes()) != digest(payload):
                raise _Stopped("Publication integrity check failed")
            with self.store.connection() as database:
                database.execute("UPDATE deployments SET status='PUBLISHED' WHERE deployment_id=?", (publication,))
            self.store.event(self.run_id, "publish", {"deployment_id": publication, "sha256": digest(payload),
                                                     "target": "local_file", "remote_deployment": False})
        finally:
            temporary.unlink(missing_ok=True)
            lock.unlink(missing_ok=True)

    def run(self, request: str = DEFAULT_REQUEST) -> RunResult:
        if self._started:
            raise ValueError("Each orchestrator instance may execute only one run")
        self._started = True
        self.store.add("factory_runs", run_id=self.run_id, mode="deterministic_simulation",
                       request_sha256=digest(request), status="IN_PROGRESS", branch=None,
                       created_at=timestamp(), config_json=self.harness.config.model_dump_json())
        self.emit("DETERMINISTIC SOFTWARE FACTORY · actual API cost $0.00 · no provider calls")
        published = False
        reason = ""
        try:
            policy = Review.model_validate(self.harness.get_security_review(request))
            self._write_report("intake_security.json", policy.model_dump())
            if not policy.approved:
                raise _Stopped("Security blocked feature request: " + "; ".join(policy.issues))
            self._gate("manager", "Approve the fixed teaching brief and simulated planning cost", digest(request),
                       self.harness.simulated_costs["manager"], {"request": request,
                                                              "whole_run_simulated_maximum": format(sum(self.harness.simulated_costs.values()) + self.harness.publish_cost, ".2f"),
                                                              "output": str(self.publish_path), "provider_calls": 0})
            self._work("manager")
            plan = Plan.model_validate(self.harness.plan(request).model_dump())
            self._write_report("plan.json", plan.model_dump())
            self._record_cost("manager", self.harness.simulated_costs["manager"])

            self._gate("coder", "Approve preparing the checked-in travel website fixture", digest(plan.model_dump_json()),
                       self.harness.simulated_costs["coder"], plan.model_dump())
            self._work("coder")
            self.artifact = SiteArtifact.model_validate(self.harness.build_site(request, plan).model_dump())
            self._create_worktree()
            self._record_cost("coder", self.harness.simulated_costs["coder"])
            candidate_hash = digest(self.artifact.html)

            self._gate("security", "Approve bounded local security checks", candidate_hash,
                       self.harness.simulated_costs["security"], {"candidate": str(self.candidate), "sha256": candidate_hash})
            self._work("security")
            security = Review.model_validate(self.harness.get_security_review(self.artifact.html))
            from software_factory.local_checks import inspect_security, inspect_ui, run_qa
            independent = inspect_security(self.artifact.html)
            self._record_cost("security", self.harness.simulated_costs["security"])
            self._review("security", security if not security.approved else independent)

            self._gate("ui_ux", "Approve bounded UI source checks", candidate_hash, self.harness.simulated_costs["ui_ux"],
                       {"security": security.model_dump(), "candidate": str(self.candidate)})
            self._work("ui_ux")
            ui = Review.model_validate(self.harness.review_ui(self.artifact).model_dump())
            independent_ui = inspect_ui(self.artifact.html)
            self._record_cost("ui_ux", self.harness.simulated_costs["ui_ux"])
            self._review("ui_ux", ui if not ui.approved else independent_ui)

            self._gate("qa", "Approve executing the pre-generated declarative acceptance cases", candidate_hash,
                       self.harness.simulated_costs["qa"], {"ui": ui.model_dump(), "candidate": str(self.candidate)})
            self._work("qa")
            qa = QAPlan.model_validate(self.harness.generate_qa(self.artifact).model_dump())
            results = run_qa(self.artifact.html, qa)
            self._record_cost("qa", self.harness.simulated_costs["qa"])
            for result in results:
                self.store.add("qa_cases", run_id=self.run_id, artifact_id=self.artifact_id,
                               **{**result.model_dump(), "passed": int(result.passed)})
            self._write_report("qa_report.json", {"artifact_sha256": candidate_hash, "passed": all(item.passed for item in results),
                                                   "cases": [item.model_dump() for item in results],
                                                   "scope": "DOM source assertions, not browser performance or full accessibility"})
            if len(results) != len(qa.test_cases) or not results or not all(item.passed for item in results):
                raise _Stopped("QA acceptance checks failed")
            self._commit_candidate(qa)

            approval_id = self._gate("publish", "Approve publication of this exact reviewed commit to a local HTML file",
                                     candidate_hash, self.harness.publish_cost, {"source_commit": self.source_commit,
                                     "branch": self.branch, "sha256": candidate_hash, "qa_passed": len(results),
                                     "target": str(self.publish_path), "replaces_sha256": self._target_before,
                                     "remote_deployment": False, "evidence": str(self.evidence_dir)})
            self._publish(approval_id)
            self._record_cost("publish", self.harness.publish_cost)
            published = True
            reason = "Reviewed fixture committed and published locally after explicit final approval."
            self.emit("LOCAL PUBLICATION COMPLETE · no remote production deployment · actual API cost $0.00")
        except (_Stopped, HarnessError, BudgetExceeded, CostTrackerError, ValueError, OSError, subprocess.SubprocessError) as error:
            reason = str(error)
            self.emit(f"BLOCKED at {self.stage}: {reason}")
        status = "PUBLISHED" if published else "BLOCKED"
        self.store.status(self.run_id, status)
        result = RunResult(run_id=self.run_id, status=status, stage=self.stage, reason=reason,
                           candidate_path=str(self.candidate) if self.candidate else None,
                           published_path=str(self.publish_path) if published else None,
                           artifact_sha256=digest(self.artifact.html) if self.artifact else None,
                           source_commit=self.source_commit, evidence_path=str(self.evidence_dir), costs=self.costs.summary())
        self._write_report("run_summary.json", result.model_dump())
        return result
