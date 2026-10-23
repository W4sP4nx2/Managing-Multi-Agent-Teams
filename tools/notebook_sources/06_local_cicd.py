# %% {"id": "cicd-intro", "type": "markdown"}
# # Local CI/CD · prove that release gates stop publication
#
# [Course dashboard](../README.md#navigation-dashboard) · [Factory lab](05_live_software_factory.ipynb) · [Execution guide](../extensions/live_software_factory.md) · [Capstone ERD](../resources/diagrams/capstone_factory_erd.md)
#
# You are running Python/CLI checks against temporary local workspaces. The orchestrator uses checked-in outputs and scripted `notebook-fixture` decisions. Git operations, file changes, hashes, and publication checks run locally; no provider or remote deployment is involved.
#
# | Action | What you do in this notebook |
# | --- | --- |
# | **Run** | Run all cells unchanged to observe publication denial, stale-candidate blocking, and `--no-input` refusal. |
# | **Edit** | Temporarily change the denied stage from `publish` to `qa` and its expected teaching total from `0.45` to `0.40`, following the experiment instructions below. Restore both values afterwards. |
# | **Inspect** | Check each `BLOCKED` result, the preserved previous page, candidate hash/commit evidence, and the final `cicd_evidence` summary. |
# | **Finish** | Restart the kernel and run all cells with the original publication-denial case restored. Explain why approval and evidence must match the current artifact. |
#
# All cases use temporary files and actual API cost **$0.00**. Simulated costs count completed example work; they are not payments and require no manual profile or budget setup.

# %% {"id": "cicd-exercise-flow", "type": "markdown", "diagram": "resources/diagrams/notebook-cicd-flow.svg"}
# ## Exercise flow
#
# ![Local CI/CD exercise flow: run local checks, then verify publication denial preserves the previous page, a changed candidate invalidates review evidence, and unattended input cannot approve publication.](attachment:notebook-cicd-flow.svg)
#
# Each branch is a separate temporary run. Read its result and assertions before changing the denied stage. A successful check report, a scripted approval, and a current artifact hash are separate facts; the release policy verifies the facts it requires before copying a page.

# %% {"id": "cicd-setup", "type": "code"}
USE_LIVE_LLM = False

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from orchestrator import main as factory_cli
from software_factory.workflow import FactoryOrchestrator, MALICIOUS_REQUEST

cicd_scratch = TemporaryDirectory(prefix="course-cicd-")
cicd_root = Path(cicd_scratch.name)
assert factory_cli(["--check-only"]) == 0
assert factory_cli(["--security-demo"]) == 0

# %% {"id": "cicd-denial-instructions", "type": "markdown"}
# ## 1 · Deny publication and inspect the previous page
#
# Run the next cell unchanged first. Its lambda approves every stage except `publish`. Expect a new candidate to be created, publication to be `BLOCKED`, simulated total **$0.45**, and the previous page's text to remain unchanged. Earlier checks do not grant publication permission.
#
# For the edit experiment, follow section 4 after observing the baseline. This cell creates a directory once, so use **Restart Kernel**, then run from the top when repeating it.

# %% {"id": "cicd-publication-denied", "type": "code"}
previous_page = cicd_root / "previous" / "index.html"
previous_page.parent.mkdir()
previous_page.write_text("Previously approved local page", encoding="utf-8")
denied_runner = FactoryOrchestrator(
    cicd_root / "denied", publish_path=previous_page,
    approval=lambda request: request.stage != "publish",
    actor="notebook-fixture", delay_seconds=0, emit=lambda line: None,
)
denied_result = denied_runner.run()
assert denied_result.status == "BLOCKED"
assert denied_result.costs["simulated_total"] == "0.45"
assert previous_page.read_text() == "Previously approved local page"
print(denied_result.model_dump_json(indent=2))

# %% {"id": "cicd-stale-instructions", "type": "markdown"}
# ## 2 · Change the candidate after review
#
# The next fixture mutates the HTML during final approval. The approval still returns `True`, but the candidate hash has changed. Observe the independent stale-evidence gate blocking publication. Explain why a boolean `approved=True` alone is insufficient.

# %% {"id": "cicd-stale-proof", "type": "code"}
stale_runner = None

def change_candidate_at_final_gate(request):
    if request.stage == "publish":
        with stale_runner.candidate.open("a", encoding="utf-8") as candidate:
            candidate.write("\n<!-- changed after independent review -->\n")
    return True

stale_target = cicd_root / "stale-page" / "index.html"
stale_runner = FactoryOrchestrator(
    cicd_root / "stale", publish_path=stale_target,
    approval=change_candidate_at_final_gate, actor="notebook-fixture", delay_seconds=0,
    emit=lambda line: None,
)
stale_result = stale_runner.run()
assert stale_result.status == "BLOCKED" and "stale" in stale_result.reason
assert not stale_target.exists()
print(stale_result.model_dump_json(indent=2))

# %% {"id": "cicd-unattended-instructions", "type": "markdown"}
# ## 3 · Prove unattended execution cannot approve itself
#
# The CLI's `--no-input` route denies approvals. It has no auto-approval flag. A CI job verifies the release policy; it does not impersonate a human to publish the course page.

# %% {"id": "cicd-unattended-proof", "type": "code"}
unattended_target = cicd_root / "unattended" / "index.html"
unattended_status = factory_cli([
    "--workspace", str(cicd_root / "unattended-run"),
    "--output", str(unattended_target), "--no-input", "--delay-seconds", "0",
])
assert unattended_status == 2 and not unattended_target.exists()
cicd_evidence = {
    "local_checks_passed": True,
    "denied_publication_blocked": denied_result.status == "BLOCKED",
    "previous_page_preserved": previous_page.read_text() == "Previously approved local page",
    "stale_evidence_blocked": stale_result.status == "BLOCKED",
    "unattended_publication_blocked": unattended_status == 2,
    "actual_cost": "0.00",
}
print(json.dumps(cicd_evidence, indent=2))

# %% {"id": "cicd-exercise-and-submit", "type": "markdown"}
# ## 4 · Change the denied stage, restore, and finish
#
# After running the baseline, perform this temporary edit in the **Deny publication** code cell:
#
# 1. Change `request.stage != "publish"` to `request.stage != "qa"`.
# 2. Change that cell's expected simulated total from `"0.45"` to `"0.40"`. Predict why the denied QA stage contributes no cost.
# 3. Restart the kernel and run from the top through the edited denial cell. Inspect where the run stopped and verify that the previous page is preserved.
# 4. Restore both original values (`"publish"` and `"0.45"`), restart the kernel, then run all cells. The final evidence summary must show all three blocking cases.
#
# For the stale-candidate case, explain the repair: review the changed candidate again and create fresh matching evidence. Changing an approval boolean does not repair the hash mismatch. Save the observed cases, hashes/commits, teaching ledger, and reasoning with your [Capstone ADR](../ASSIGNMENTS.md#ex5-capstone-virtual-software-company); use the [submission checklist](../README.md#submission-checklist).
#
# The separate [Git hook exercise](../extensions/live_software_factory.md#exercise-fix-the-broken-pipeline) covers `commit-msg` receiving its message file as `$1`, staged-source scanning, and nonzero scanner failures. This notebook needs no external scanner. The [CI workflow](../.github/workflows/readiness.yml) runs repository checks; this local exercise does not prove that a remote CI job ran.

