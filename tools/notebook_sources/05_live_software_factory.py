# %% {"id": "factory-intro", "type": "markdown"}
# # Software Factory · trace a local release
#
# [Course dashboard](../README.md#navigation-dashboard) · [Execution guide](../extensions/live_software_factory.md) · [Capstone ERD](../resources/diagrams/capstone_factory_erd.md) · [Next: Local CI/CD](06_local_cicd.ipynb)
#
# You are interacting with a Python orchestrator and checked-in specialist fixtures. The fixtures supply the travel-page HTML and review records; no model generates content or calls a provider. Git commits, temporary files, HTML checks, and eight declarative QA checks are real local operations.
#
# | Action | What you do in this notebook |
# | --- | --- |
# | **Run** | Run all cells to inspect role labels, the blocked malicious request, typed fixtures, and a complete temporary release. |
# | **Edit** | In the local rehearsal cell, remove `"publish"` from `scripted_approved_stages`; rerun that cell, inspect the denial, then restore it and rerun. |
# | **Inspect** | Read the six scripted decisions, candidate hash, Git commit, eight QA results, and teaching-cost ledger. Each decision is labelled `notebook-fixture`; it records no human approval. |
# | **Finish** | Save the successful and denied evidence. Use the separate terminal route only when you want to make the six decisions yourself. |
#
# All notebook output stays in a temporary directory. Actual API cost is **$0.00**. The simulated-cost ledger measures the example work; it is not payment, and the supplied defaults require no profile or budget setup.

# %% {"id": "factory-exercise-flow", "type": "markdown", "diagram": "resources/diagrams/notebook-factory-flow.svg"}
# ## Exercise flow
#
# ![Software Factory flow: inspect checked-in fixtures, run the six staged decisions in a temporary Git workspace, and compare an approved publication with a denied publication.](attachment:notebook-factory-flow.svg)
#
# The notebook supplies scripted decisions to the real local orchestrator. Removing `publish` from the decision set stops the final file copy. The optional terminal route replaces that scripted function with six prompts for you; both routes use the same fixtures and local checks.

# %% {"id": "factory-profile", "type": "code"}
USE_LIVE_LLM = False

from agent_harness import AgentHarness
from software_factory.workflow import FactoryOrchestrator, MALICIOUS_REQUEST
from software_factory.local_checks import run_qa
from pathlib import Path
from tempfile import TemporaryDirectory
import json

harness = AgentHarness()
role_profile = {
    role: {"label": route.model, "provider": route.provider,
           "simulated_cost": str(harness.simulated_costs[role]), "actual_cost": "0.00"}
    for role, route in harness.routes.items()
}
print(json.dumps(role_profile, indent=2))
print("Local publication simulated cost:", harness.publish_cost)
print("Actual API cost: $0.00; API keys required: False")

# %% {"id": "factory-security-exercise", "type": "markdown"}
# ## 1 · Inspect the blocked request
#
# Run the next cell and read the three policy findings. `MALICIOUS_REQUEST` asks to store passwords and send them to an insecure endpoint. The policy inspects this string without executing it or sending it anywhere. These bounded deny rules demonstrate one blocking case; passing them does not establish complete security.

# %% {"id": "factory-security-proof", "type": "code"}
security_result = harness.get_security_review(MALICIOUS_REQUEST)
print(f"Blocked: {not security_result['approved']}")
print(f"Issues: {security_result['issues']}")
assert security_result["approved"] is False
assert security_result["issues"] == [
    "Insecure HTTP endpoint", "Passwords in localStorage", "Potential data exfiltration"
]

# %% {"id": "factory-artifact-exercise", "type": "markdown"}
# ## 2 · Trace the pre-generated artifact
#
# Read the model declarations in `software_factory/contracts.py` and the fixture under `software_factory/fixtures/`. The Coder supplies HTML/CSS; Security and UI review records carry its SHA-256. Changed HTML cannot inherit those records. QA supplies test data, never Python, shell commands, or JavaScript to execute.
#
# Explain why an approved schema and a review tied to an old hash cannot authorize a changed page. Compare the eight supplied tests with the real page: there is a static contact section, not a contact form or booking service.

# %% {"id": "factory-typed-artifact", "type": "code"}
plan = harness.plan("Build the course travel website fixture")
artifact = harness.build_site(plan.goal, plan)
qa_plan = harness.generate_qa(artifact)
qa_results = run_qa(artifact.html, qa_plan)
print(plan.model_dump_json(indent=2))
print(json.dumps([case.model_dump() for case in qa_results], indent=2))
assert len(qa_results) == 8 and all(case.passed for case in qa_results)

# %% {"id": "factory-run-instructions", "type": "markdown"}
# ## 3 · Change one scripted decision
#
# `fixture_approve` reads membership in `scripted_approved_stages`. It is a scripted decision function, not a human. The orchestrator records its actor as `notebook-fixture`.
#
# 1. Run the next cell unchanged. Expect `PUBLISHED`, a local publication file, six approved decisions, and simulated total **$0.50**.
# 2. Remove only `"publish"` from the set in that cell, then rerun the whole cell. Expect `BLOCKED`, no publication file in this new temporary run, and simulated total **$0.45** for the completed work.
# 3. Restore `"publish"` and rerun the whole cell. Record the successful candidate hash, Git commit, QA results, and decision trace.
#
# Each execution creates a new temporary workspace; inspect the paths printed for the current run. No root `index.html` is published by this cell.

# %% {"id": "factory-local-rehearsal", "type": "code"}
factory_temporary_workspace = TemporaryDirectory(prefix="course-factory-")
factory_sandbox = Path(factory_temporary_workspace.name)
scripted_approved_stages = {"manager", "coder", "security", "ui_ux", "qa", "publish"}
fixture_decisions = []

def fixture_approve(request):
    fixture_decisions.append({"stage": request.stage, "sha256": request.subject_sha256,
                              "approved": request.stage in scripted_approved_stages})
    return request.stage in scripted_approved_stages

factory_runner = FactoryOrchestrator(
    factory_sandbox / "workspace", publish_path=factory_sandbox / "published" / "index.html",
    harness=harness, approval=fixture_approve, actor="notebook-fixture", delay_seconds=0,
)
factory_result = factory_runner.run()
print(factory_result.model_dump_json(indent=2))
print(json.dumps(fixture_decisions, indent=2))
factory_evidence = {
    "status": factory_result.status,
    "actual_cost": factory_result.costs["actual_cost"],
    "simulated_total": factory_result.costs["simulated_total"],
    "source_commit": factory_result.source_commit,
    "publication_exists": (factory_sandbox / "published" / "index.html").exists(),
    "actor": "notebook-fixture",
}
print(json.dumps(factory_evidence, indent=2))

# %% {"id": "factory-evidence-erd", "type": "markdown", "diagram": "resources/diagrams/capstone_factory_erd.svg"}
# ## Read the evidence database
#
# ![Factory evidence ERD: a run owns artifacts, approvals, reviews, QA cases, events, and local publication receipts; the teaching-cost ledger is a separate database.](attachment:capstone_factory_erd.svg)
#
# Follow `run_id` to the candidate, then `artifact_id` to reviews and QA. A publication receipt also references its final `approval_id`. Solid lines are declared foreign keys; dashed lines are logical associations. The current page is static HTML; this is the factory's evidence model. Read the [field-by-field guide](../resources/diagrams/capstone_factory_erd.md) if needed.
#
# Run the next cell after each rehearsal. It reads this run's SQLite evidence without changing the schema. Compare an approved run with a denied publication: both retain completed checks; only the approved run has a publication receipt. The `notebook-fixture` actor identifies a scripted decision, not a person.

# %% {"id": "factory-evidence-readback", "type": "code"}
with factory_runner.store.connection() as evidence_database:
    evidence_counts = {
        table: evidence_database.execute(
            f"SELECT COUNT(*) FROM {table} WHERE run_id = ?", (factory_runner.run_id,)
        ).fetchone()[0]
        for table in ("factory_runs", "artifacts", "stage_approvals", "reviews", "qa_cases", "deployments")
    }
    publication_rows = [dict(row) for row in evidence_database.execute(
        """SELECT d.status, d.sha256, d.commit_sha, a.actor, a.approved
           FROM deployments AS d
           JOIN stage_approvals AS a ON a.approval_id = d.approval_id
           WHERE d.run_id = ?""", (factory_runner.run_id,)
    )]
    assert evidence_database.execute("PRAGMA foreign_key_check").fetchall() == []
assert evidence_counts["factory_runs"] == evidence_counts["artifacts"] == 1
assert evidence_counts["qa_cases"] == 8
assert bool(publication_rows) == factory_evidence["publication_exists"]
print(json.dumps({"table_counts": evidence_counts, "publication_receipts": publication_rows}, indent=2))

# %% {"id": "factory-terminal-route", "type": "markdown"}
# ## 4 · Optional terminal route: make the decisions yourself
#
# The notebook exercise is complete after restoring the successful scripted run. To review each approval personally, use an activated course terminal at the repository root ([setup verification](../SETUP.md#verify-the-local-factory)):
#
# ```bash
# python live_simulation_orchestrator.py --check-only
# python live_simulation_orchestrator.py --security-demo
# python live_simulation_orchestrator.py
# ```
#
# This separate route prompts for six human decisions. Each prompt shows the action, simulated teaching cost, actual cost, and evidence. Review it before typing `yes`; denial or missing input stops the workflow. After approving local publication, open `index.html` in a browser (`open index.html` on macOS) and compare its hash with this run's receipt. An existing page can belong to an earlier run.
#
# Retain the blocked request, decision trace, QA results, candidate commit, and simulated ledger for your Capstone evidence. State the source-check limits and the manual browser checks still needed. Continue to [Local CI/CD](06_local_cicd.ipynb).

