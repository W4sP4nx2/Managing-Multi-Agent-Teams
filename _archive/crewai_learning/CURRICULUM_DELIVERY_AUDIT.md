# CrewAI curriculum delivery audit

> **Historical baseline audit.** The findings below describe the seven-agent research project before the three-agent refactor. That project is now [archived](README.md). Use the [active reference](../../crewai_learning/README.md) and [verification instructions](../../crewai_learning/SETUP_AND_LEARNING_EXPERIENCE.md) for current delivery. The original research-pipeline feature requests below are not requirements of the agreed three-agent reference.

Reviewed **19 October 2026** against the current files, the installed nested-project environment, and the promises in the [learning guide](../../crewai_learning/README.md), [setup guide](../../crewai_learning/SETUP_AND_LEARNING_EXPERIENCE.md), and [Homework G](../../assignments/module14_crewai_orchestration_patterns.md).

**Finding:** this folder supports reading and auditing a seven-agent research crew. It does not yet supply the enforced governance, recovery behavior, saved report, or reusable offline coding-team template described in the curriculum. Delivering those promises requires working code, exercises, and evidence in addition to documentation corrections.

The core two-day workshop remains a separate, deterministic route. Homework G is explicitly optional post-course work. Keep both promised extension outcomes: a governed research pipeline and a personal coding-team template. Do not treat changing the wording to “discussion only” as completion of either build outcome.

This is an audit and implementation plan. The extracted research project's source and dependency files were not changed.

## What is already present

- Seven agents and seven tasks construct successfully with the installed CrewAI **1.15.0**, crewai-tools **1.15.0**, and Pydantic **2.12.5**.
- The sequential context graph is wired correctly, including the compiler's direct access to article, evaluation, gate, and manager outputs.
- Tools are assigned by role, and all agents disable delegation. These are useful configuration examples, not a complete execution authorization system.
- Six project Python files parse successfully.
- The six-week outline, four C1–C4 audit activities, twelve Homework G exercises, and rubrics provide substantial teaching material.

## Delivery blockers, in repair order

### 1. Supply the promised offline coding-team starter

**Evidence:** [historical README learning outcomes](historical_README.md#learning-outcomes) promise a Coder–QA–Review team, bounded feedback loop, reusable template, and showcase. [historical Exercises 14.6–14.8](historical_homework_g.md#exercise-146-build-your-coding-agent-roster) require these artifacts. The supplied executable project instead contains research, writing, evaluation, gate, manager, compiler, and delivery roles. There is no coding-team project, offline showcase, or fixture suite in this folder.

**Fix:** add a separate `coding_team_starter/` with explicit learner TODOs, deterministic Coder/QA/Review adapters, fixtures, setup instructions, and tests. Include strict `CodingTask`, `CodePatch`, `TestResult`, `ReviewDecision`, `TeamState`, and `EscalationTicket` contracts. Keep instructor repairs separate from the learner starter. Review and adapt the existing [course models](../../src/enterprise_agent_team.py) rather than copying incompatible schemas without checking their semantics.

**Acceptance:** a learner can run a passing case, a needs-changes case that repairs successfully, and an exhausted-budget case without credentials or network access. Each transition records the artifact and decision; unauthorized role actions are rejected. The showcase includes failure and escalation, not only success.

### 2. Turn output descriptions into enforced contracts

**Evidence:** all seven constructed tasks have `guardrail=None`, no active `guardrails`, `output_pydantic=None`, and `output_json=None`. The [task factory methods](academic_research_crewai_project/src/academic_research_writer_evaluator/crew.py) pass only config and `markdown=False`. The YAML's `expected_output` fields describe desired results; they do not validate them. C3 currently asks learners to improve this prose while calling the activity a “Guardrail Upgrade.”

**Fix:** in a maintained teaching copy, add output models and application-side validation for research, article, evaluation, routing, and manager decisions. Attach callable task guardrails for required fields, ranges, counts, allowed decisions, and consistency. Validate the final artifact too. Make C3 require an executable rejection case. Configure task-validation retries explicitly; a default retry limit does nothing when no guardrail is attached.

**Acceptance:** malformed output cannot reach its consumer. Tests reject missing fields, extra fields, out-of-range scores, unknown decisions, missing article/source IDs, and score totals inconsistent with their components. Tests should distinguish structural validity from the truth of a claim. CrewAI documents `expected_output`, structured output, and guardrails as separate task features. [Official task reference](https://docs.crewai.com/en/concepts/tasks).

### 3. Implement actual routing and bounded recovery

**Evidence:** [crew.py](academic_research_crewai_project/src/academic_research_writer_evaluator/crew.py) runs one `Process.sequential` list. No Flow, conditional task, or Python controller consumes gate/manager decisions. The evaluator prompt sets `retry_count = 0`; the manager prompt says “Never loop.” All agents use `max_iter=25`, which is not the promised five-round research policy or the stage retry budgets.

**Observed:** with agent execution replaced by fixed responses, the real CrewAI scheduler ran all seven tasks after each of these results:

| Injected gate / manager result | Observed scheduler behavior |
| --- | --- |
| `RETRY_NEEDED` / `REJECT_AND_RETRY` | Compiler and delivery still ran; no earlier task was retried. |
| `PIPELINE_ERROR` / `ERROR` | Compiler and delivery still ran. |
| `PROCEED_TO_DELIVERY` / `HARD_STOP` | Compiler and delivery still ran. |

**Fix:** retain sequential order inside each pass, but put an explicit controller around the passes. A typed Python state machine or CrewAI Flow can own counters, feedback, routing, stopping, and escalation. Distinguish agent reasoning iterations, tool retries, task guardrail retries, and whole-stage retries. Decide how the documented research 2 / writing 2 / evaluation 1 budgets interact and prevent nested retry multiplication. Set an overall call/time/spend policy for optional live runs.

**Acceptance:** a retry re-enters the intended stage with typed feedback and an incremented counter; success stops early; exhaustion returns an escalation; infrastructure failure and hard stop make zero downstream delivery calls. Test exact call counts. CrewAI Flows offer explicit state and conditional routing; returning the word `RETRY_NEEDED` from an ordinary task is not such a controller. [Official Flow reference](https://docs.crewai.com/en/concepts/flows).

### 4. Define one approval policy and preserve failures

**Evidence:** `quality_gate_check` explicitly sends missing/malformed evaluation and `ERROR` to `PROCEED_TO_DELIVERY`. The manager task says its quality score “ALWAYS wins” and can override retries; its agent backstory instead says `PIPELINE_ERROR` must produce `ERROR`. The compiler's stop instructions are prompt text. The delivery task strips error tags and diagnostic fields. See [tasks.yaml](academic_research_crewai_project/src/academic_research_writer_evaluator/config/tasks.yaml) and [agents.yaml](academic_research_crewai_project/src/academic_research_writer_evaluator/config/agents.yaml).

**Fix:** publish and implement a single decision table shared by prompts and tests. Invalid contracts, missing required evidence, infrastructure failure, and exhausted budgets must not be turned into approval by a score. Allow best-effort output only under a defined policy: validated partial content, explicit unresolved issues, and a recorded approval where required. A model's manager role is not a human approval channel.

**Acceptance:** hard failures take precedence over scores. Conflicting decisions reject or escalate deterministically. A best-effort report retains its warning. Failed runs produce a separate failure artifact; they cannot become successful-looking reports by stripping error markers.

### 5. Produce and verify the promised document

**Evidence:** the nested [project README](academic_research_crewai_project/README.md#running-the-project) promises `report.md`. None of the seven tasks sets `output_file`, and [main.py](academic_research_crewai_project/src/academic_research_writer_evaluator/main.py) discards the kickoff result. The mocked runs created no `report.md`. The writer produces “References,” while the compiler first asks for “## Sources”; the compiler also mixes character-for-character copying, ±5 words, and a 5% mismatch threshold.

**Fix:** define a typed article artifact with stable fields, then render the approved result deterministically. Save it through a named output path, along with a separate audit record and an explicit return value/status. Use exact equality or a content hash for content promised to be verbatim. Resolve the source-section and tolerance contradictions.

**Acceptance:** an approved run creates a nonempty Markdown file at the documented path with expected sections, unchanged article/citations/scores, and retained warnings. A rejected run creates no success report. A temporary-directory test proves both behaviors.

### 6. Add a release gate for this extension

**Evidence:** the extracted `tests/` directory contains no test files, and pytest is absent from its installed environment. The [core development guide](../../DEVELOPMENT.md) explicitly excludes the nested project from the core execution gate. A Crew graph construction check verifies wiring, not governance or a complete report.

**Fix:** provide a documented offline verification command with fixture-driven contract, controller, role-policy, tool, and artifact tests. Pin its test dependencies. Add a separate CI job for this extension so core workshop success cannot mask extension failures. Keep paid model evaluation separate; the generated `test` entry point is a CrewAI evaluation command, not a replacement for unit tests.

**Acceptance:** one documented command passes with keys removed and outbound connections blocked. It covers malformed handoffs, denied tools, fail-then-pass recovery, exact retry exhaustion, failure precedence, source verification failures, approved delivery, and rejected delivery. Preserve an executed example and instructor answer guide. Optional live smoke testing remains separately reported.

## Setup and content corrections before distribution

| Area | Current problem | Required correction and check |
| --- | --- | --- |
| Learner navigation | The first Lab 2 link targets removed `02_lab_crewai_team_handoff.ipynb`. | Point to [current Lab 2](../../notebooks/02_lab_crewai.ipynb); link the current course map, required sequence, and separate extension paths. Run local link checks. |
| Reference archive | Both guides advertise `academic_research_crewai-project.zip`, which is absent. | Supply the intended archive or remove the nonexistent-download claim and identify a reproducible baseline snapshot. |
| Sandbox command | The first copy example omits `mkdir -p experiments`; a later example includes it. | Give one tested copy procedure. Exclude virtual environments, local credentials, and generated outputs from a reusable student package. |
| Run inputs | `research_topic` is `sample_value`; the model is hard-coded eight times, including chat. | Expose validated topic, output location, and optional live model configuration. Provide a concrete offline example and document configuration precedence. |
| Entry points | `pyproject.toml` advertises `run_with_trigger`, but `main.py` has no such function. | Implement it if teaching triggers, or remove that entry point. Check every advertised command without making a provider call. |
| Key/setup instructions | The nested README mentions only OpenAI, while constructors also need Exa, Brave, and Serply keys. No `.env.example` is supplied. | Separate offline and live setup; provide a secret-free example and a preflight that names missing configuration without revealing values. |
| CLI version | Nested dependencies pin CrewAI 1.15.0, but `uv tool install crewai` is unpinned. | Choose and rehearse one CLI/project version pair. Current official docs describe JSONC scaffolding by default and `--classic` for Python/YAML; do not mix those instructions into the 1.15.0 lab without checking support. [Official task/scaffold reference](https://docs.crewai.com/en/concepts/tasks). |
| Confidence calculation | `(num_sources/9)` is uncapped, and `sources_with_url/num_sources` divides by zero for an empty result. | Handle zero sources; define/deduplicate verified sources; bound components and the result to 0–1. Test 0, 1, 9, and more than 9 sources. Label credibility as a heuristic with an evidence basis. |
| Source policy | Research/writer allow arXiv, Semantic Scholar, and `.edu`; compiler additionally permits ACL; the search tool can return DOI links. | Centralize hostname and provenance policy. Test permitted hosts, subdomains, deceptive suffixes, placeholders, duplicates, missing metadata, and inaccessible URLs. A permitted domain alone does not prove factual support or peer review. |
| Tool failures | The Semantic Scholar tool accepts a blank query and raises `AttributeError` for a valid JSON response with an unexpected top-level shape. HTTP errors return free-form strings. | Validate query/result shape; return a structured success/error result with retryability and a supported next action. Add mocked timeout, 429, malformed JSON, unexpected shape, empty, and success cases. |
| Context/knowledge claims | The knowledge file contains sample personal preferences, but no knowledge source is wired into the Crew. Shared memory, MCP authorization, and API perimeters are discussed rather than implemented here. | Label the baseline accurately, and link each implemented extension to its code and evidence. Do not count a file's presence or a tool list as proof of those controls. |
| Readiness language | A 90–100 design score is labeled ready for live keys, without a live-run gate. | Keep it a learning rubric. Add separate configuration, behavior, budget, and deployment evidence before asserting operational readiness. |

The installed 1.15.0 project is behind the version served by the current documentation (1.15.28 during this audit). An upgrade alone will not add the missing contracts or controller. Keep a rehearsed version pin and test any upgrade separately.

## Connect every promised learning activity to evidence

Use one track map instead of leaving learners to reconcile overlapping outlines. Each row needs a starting artifact, learner action, expected evidence, and instructor check. Completed solutions belong in the instructor materials; students still perform the assigned work.

| Existing activity | Evidence needed to deliver it |
| --- | --- |
| C1 / Week 1 / 14.5–14.6: roles and basics | Annotated roster, least-privilege table, working setup, and coding-team starter with clear TODOs. |
| C2 / Week 2 / 14.1: context and contracts | DAG plus a fixture showing both upstream inputs are consumed; a missing-context failure and typed rejection. |
| Week 3 / C4 / 14.10: process choice and hierarchy | Fixed sequential example and separate hierarchical/manager-adapter exercise, with two ticket fixtures and auditable delegation. The research manager is a sequential reviewer, not proof of hierarchical execution. |
| C3 / Week 4 / 14.4: guardrails and governed tools | Invalid/valid output cases; allowed/denied tool calls; proof that denied calls never invoke the backend. SQL shape checks must state their limits. |
| Week 5 / 14.7: recovery | Typed state, measured retry counts, feedback propagation, early success, and exhaustion/escalation traces. |
| Week 6 / 14.3 / 14.8: delivery and packaging | Saved document, content-preservation test, setup from a clean directory, and a failure-inclusive showcase. |
| 14.2: parallel work | Independent-task fixture, join-before-consume check, and sequential/parallel timing evidence; no speedup claim without measurements. |
| 14.9: research–write–edit | Small source fixture, explicit context, typed article, and a missing-context comparison before using the seven-role case. |
| 14.11: LangGraph comparison | Separate optional graph/state-machine exercise with passing and escalation evidence. It is not implemented by the sequential research crew. |
| 14.12: framework translation | One governance behavior implemented as an offline adapter and expressed in framework form; explain configured behavior versus actual execution. |

The research Capstone's eight requirements also need explicit checks:

| Promised requirement | Current evidence | Completion check |
| --- | --- | --- |
| At least five agents | Seven exist. | Preserve purposeful roles and explain each boundary. |
| Sequential process when order is known | Configured and constructed. | Preserve fixed order within a pass; controller owns recovery. |
| Guardrail per task | None configured. | Reject a malformed fixture at every task boundary. |
| Correct context chain | Explicit dependencies construct correctly. | Test both context consumption and missing-input behavior. |
| Recovery for three failure modes | Described in prompts. | Execute three bounded recovery/escalation cases. |
| Clean `.md` delivery | No configured file writer. | Verify an approved artifact and failure suppression. |
| Documented required inputs | Listed, but executable defaults/setup disagree. | Validate inputs and rehearse the documented command. |
| Gate routes without changing content | Text instructions only. | Verify executed branch, unchanged artifact hash, and stop precedence. |

Keep the main workshop's three labs and Capstone marks separate from Homework G's readiness rubric and the six-week research Capstone's /100 rubric. Add durations, prerequisites, and submission paths to the extension map; do not silently add these builds to the two-day assessed route. The main deck's desktop/video/cloud helper and tool-discovery discussions remain formative design topics, not additional implemented capabilities promised by this folder.

## Suggested implementation sequence

1. Fix the broken link, setup/entry-point claims, and track map; preserve the extracted project as the baseline case study.
2. Deliver the offline coding-team starter and evidence for exercises 14.6–14.8.
3. Build a maintained research-project copy with strict contracts and one decision table.
4. Add controller-owned retries and stopping, then deterministic approved-report rendering.
5. Add negative-path tests, instructor examples, and an independent extension verification command.
6. Rehearse a clean learner setup. Run optional live evaluation only after the offline release gate passes and its provider/budget configuration is ready.

## Audit evidence and limits

[Runtime evidence](../../crewai_learning/audit_evidence/2026-10-19-runtime.json) records versions, task fields, scenario traces, and source hashes. The probe used the installed project's actual CrewAI `kickoff` scheduler and task processing, replacing `Agent.execute_task` with deterministic fixture responses. Outbound connections were blocked; **zero network attempts** occurred. The three scenarios each supplied malformed research, an uncited short article, and an empty evaluation, then the gate/manager result shown above. All reached delivery with no typed outputs and no `report.md`.

This proves absent application enforcement for the injected responses. It does not claim that a particular live model would always return those responses, or assess live search quality. No dependency sync, paid provider execution, or fresh cross-platform installation was performed. The installed graph, six syntax parses, local file inventory, broken-link check, and custom-tool response-shape probe are current observations; older “verified” tables in the guide were not treated as current test results.

[Course home](../../README.md) · [CrewAI study guide](../../crewai_learning/README.md) · [Homework G](../../assignments/module14_crewai_orchestration_patterns.md)
