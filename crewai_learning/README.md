# CrewAI learning bridge: Manager, Coder, QA

[Open the notebook](01_Bridge_Sequential_Crew.ipynb) · [Setup and verification](#run-and-verify) · [Course learner paths](../README.md#learner-paths) · [Slide index](../README.md#main-deck-slide-index)

Run a three-agent coding team with real CrewAI execution and deterministic local fixture responses. No trained language model, reasoning model, provider API, or API key is used. The example proves that malformed output is rejected and three failed attempts produce a typed escalation instead of continuing indefinitely.

**Course learning bridge. No separate point scale.** Start with [Lab 2](../notebooks/02_lab_crewai.ipynb); use this notebook for [Lecture 8: Debugging and SDLC](../ASSIGNMENTS.md#assignment-08-debugging-sdlc) and [Assignment 09: Framework Comparison](../ASSIGNMENTS.md#assignment-09-framework-comparison).

## How coding_team.py teaches

[`coding_team.py`](coding_team.py) is the reusable implementation imported by the notebook's `bridge-setup` cell. Open [the notebook](01_Bridge_Sequential_Crew.ipynb) in JupyterLab to run the lesson. Running the Python file alone defines its classes and functions but starts no demonstration.

| Read in the module | Run in the notebook | Explain from the output |
| --- | --- | --- |
| Contracts, `strict_guardrail`, and `build_crew` | Create a crew, run `kickoff`, and display the final task as Markdown | Which controls CrewAI executes and why final-task text alone is not application approval |
| Strict guardrail and `run_team` exception policy | Reject malformed output, then compare stopping with bounded recovery | Which handoff fails, and why QA never consumes it |
| `run_team` and `escalate_to_human` | Run the always-failing tool | Why three total attempts produce one typed escalation |
| Matching task IDs, patch hash, QA, and Manager checks | Run the successful fixture | Why valid evidence permits approval after one attempt |

Follow the [guided read/run/explain exercise](../ASSIGNMENTS.md#assignment-09-guided-bridge-exercise). Lab 2 teaches the configuration and fixture boundary; this optional follow-up executes real CrewAI tasks with local fixture responses. It adds no marks or submission.

## Learner path

1. Use the existing [Python 3.12 course environment](../SETUP.md). No extra framework package or API key is needed.
2. Open [01_Bridge_Sequential_Crew.ipynb](01_Bridge_Sequential_Crew.ipynb) in JupyterLab and run all cells in order.
3. Inspect the three roles and four tasks: **Manager brief → Coder patch → QA evidence → Manager review**.
4. Run the direct `Crew.kickoff` cell; inspect the four-task trace and the final Manager task displayed with `Markdown(result.raw)` inside a fenced JSON block.
5. Observe `ValidationError` for garbage output; QA must not run afterward.
6. Compare **3 tool failures, 3 kickoffs, 1 EscalationReport** with a tool that recovers on attempt three and a valid fixture that succeeds on attempt one.
7. Return to [Lecture 8](../ASSIGNMENTS.md#assignment-08-debugging-sdlc) or the [framework comparison](../ASSIGNMENTS.md#assignment-09-framework-comparison) to explain which controls are supplied by CrewAI and which are enforced by the application.

## Creating and running the crew

The notebook's **Creating the Crew** section shows the `Crew(...)` constructor used by `build_crew`. For pinned CrewAI 1.15.23, `verbose` is Boolean. `memory=False` keeps this exercise on explicit `Task.context` and typed failure feedback; no embedding service or persistent memory setup is required.

The **Running the Crew** cell creates a fresh crew and actually executes it:

```python
crew = build_crew(order, kickoff_state, attempt=1)
result = await asyncio.to_thread(crew.kickoff, inputs={"task_id": order.task_id})
display(Markdown("### Final Crew task: Manager decision\n\n```json\n" + result.raw + "\n```"))
```

Run the notebook setup first; it supplies these names and wraps execution in `blocked_network`. `result` is a `CrewOutput`; `.raw` supplies the final task's text for Markdown. That final task is the Manager decision. The separate `run_team` wrapper checks all four typed outputs, task identity, patch hash, QA, and approval before returning `ApprovedResult`.

The course does not choose between video or platform GPT models. `FixtureLLM` supplies scripted local responses, so unchanged fixtures repeat the same output. An actual language-model integration could return different outputs for the same input; that would require separate provider setup and tests.

## Exception handling: stop or bounded recovery

The malformed-output example directly calls `kickoff`. Its strict guardrail raises `ValidationError`, stopping that task chain before QA. The notebook catches the expected error to inspect the trace and continue the lesson.

For governed recovery, `run_team` catches only `ValidationError`, `SimulatedInfrastructureError`, and `ReviewNeedsChanges`. Each recognized failure is recorded; a fresh crew can retry, with a maximum of three total attempts. The notebook demonstrates both recovery on attempt three and escalation after three failures. An unexpected programming exception propagates immediately. These are tested application policies, rather than a blanket rule that CrewAI continues after every exception.

## What the code enforces

| Control | Implementation | Visible proof |
| --- | --- | --- |
| Strict task output | Every task has `output_pydantic` plus a callable strict Pydantic guardrail. | Invalid JSON, fields, or types raise `ValidationError` before the next task. |
| Bounded recovery | Python owns `max_attempts = 3`; native agent/guardrail retries are disabled. | Three total failed kickoffs, followed by a typed escalation. |
| Approval boundary | Task IDs, current-patch hash, QA pass, and Manager approval are checked. | Failed or stale evidence cannot produce an approved result. |
| Offline execution | Local fixture LLMs and a temporary external-network block. | No model-provider credentials or network calls are needed. |
| Early success | The wrapper returns immediately after validated approval. | Valid fixture completes in one attempt. |

The failing tool raises on its third call too. Returning an escalation string from the tool would count as a successful tool response; the Python wrapper must produce the escalation after catching the third failure. `escalate_to_human()` creates a local report and sends no message.

## Files and curriculum connections

| File | Purpose |
| --- | --- |
| [Notebook](01_Bridge_Sequential_Crew.ipynb) | Readable, runnable demonstration with a failing tool and assertions |
| [Reusable coding team](coding_team.py) | Schemas, fixture LLM, three-agent graph, validation, bounded wrapper, and escalation |
| [Offline boundary](offline.py) | Blocks external DNS and connections during the examples |
| [Regression tests](../tests/test_crewai_reference.py) | Negative paths, exact counts, recovery, and real Jupyter-kernel execution |
| [Verification record](#historical-verification) | Checked requirements, observed notebook results, and full readiness evidence |
| [Editable notebook source](../tools/notebook_sources/01_Bridge_Sequential_Crew.py) | Regenerate with `python tools/build_core_notebooks.py` |
| [Lecture 8](../ASSIGNMENTS.md#assignment-08-debugging-sdlc) | Trace failures, evidence, and stopping behavior |
| [Assignment 09](../ASSIGNMENTS.md#assignment-09-framework-comparison) | Ungraded framework comparison using the working example |
| [Archived seven-agent material](../_archive/crewai_learning/README.md) | Historical research crew and superseded Homework G material |

## Evidence limits

The notebook uses `Process.sequential`. Manager/Coder/QA demonstrate a hierarchy of responsibilities, not dynamic hierarchical delegation. `FixtureLLM` replaces model responses while the real Agent, Task, guardrail, context, and Crew executors run. Its Coder response invokes the injected tool once; autonomous tool selection and native tool-repair behavior are outside this proof.

QA checks an exact supplied code fixture; it does not execute generated code. The example demonstrates production-oriented control patterns, not production certification, model reliability, process isolation, or deployment readiness. The course factory also stays deterministic and uses no provider API.

The [earlier audit](../_archive/crewai_learning/CURRICULUM_DELIVERY_AUDIT.md) describes the archived project's pre-fix state. This focused reference replaces that active teaching route under the agreed three-agent scope.

[Return to course home](../README.md) · [Required practical sequence](../README.md#required-practical-sequence)

## Continue into the factory

Open [05 · Software Factory Simulation](../notebooks/05_live_software_factory.ipynb), then [06 · Local CI/CD](../notebooks/06_local_cicd.ipynb). The bridge executes real CrewAI task machinery with fixture LLMs. The factory presents pre-generated role collaboration and performs actual local artifact, review, Git, and publication operations. Historical model labels are illustrative and actual API cost is $0.00. Read [the factory guide](../extensions/live_software_factory.md) for human gates and simulated cost accounting.

## Run and verify

<a id="run-and-verify"></a>

<a id="run-and-verify-run-and-verify-the-crewai-reference"></a>
### Run and verify the CrewAI reference

[Reference home](README.md) · [Notebook](01_Bridge_Sequential_Crew.ipynb) · [Course setup](../SETUP.md)

This learning bridge uses the existing Python 3.12 course environment with CrewAI 1.15.23. The seven-agent research project's older environment is archived and is not used here. Installing dependencies needs internet or a prepared package bundle; executing the reference is offline.

<a id="run-and-verify-run-in-jupyterlab"></a>
#### Run in JupyterLab

From the repository root, activate the environment described in [Setup](../SETUP.md), then run:

```bash
python -m pip install -r requirements.txt
python -m jupyterlab
```

Open `crewai_learning/01_Bridge_Sequential_Crew.ipynb` and run all cells in order. Select the course Python kernel. The notebook creates temporary CrewAI storage, disables telemetry, uses fixture LLMs, and blocks external network access around execution. It never needs a `.env` file or provider key.

Expected results:

- Exactly Manager, Coder, and QA agents; four tasks all declare an output model and callable guardrail.
- Malformed Coder output raises `ValidationError`; QA and review do not run.
- The failing tool raises three times; the wrapper returns `EscalationReport` with `ESCALATION_TRIGGERED`, `attempts: 3`, and three failure records.
- The recovery fixture fails twice, then returns `ApprovedResult` on attempt three with both earlier failures supplied as feedback.
- The valid fixture returns `ApprovedResult` after one attempt.
- The direct kickoff displays the final Manager task as Markdown; this is distinct from the wrapper's approved result.

Restart the kernel and run all cells to repeat the complete demonstration. The failing-tool cell resets its counter before each run.

<a id="run-and-verify-automated-verification"></a>
#### Automated verification

Maintainers use the same pinned environment plus the existing test dependencies:

```bash
python -m pip install -r requirements/maintenance.txt
python tools/build_core_notebooks.py --check
python -m pytest tests/test_crewai_reference.py -q --notebook-artifacts=.test-results/crewai-reference
```

The tests run actual CrewAI tasks with local model fixtures and verify failure at every typed task boundary. They cover direct kickoff and final-task text, exact retry counts, fail-twice-then-pass recovery, early success, invalid QA/approval evidence, unexpected-error propagation, and a real Jupyter-kernel run. Kernel tests remove inherited provider credentials and block outbound networking. Jupyter still needs localhost sockets; a restricted executor must permit those local sockets.

For the full distribution gate, run `python tools/check_readiness.py`. The advanced reference is included in its source fingerprint and test collection while remaining alongside the seven-notebook course route without extra marks.

Executed notebook copies belong under ignored `.test-results/`. Distributed notebooks keep empty outputs and null execution counts. Edit [the source cells](../tools/notebook_sources/01_Bridge_Sequential_Crew.py), then regenerate using `python tools/build_core_notebooks.py`.

<a id="run-and-verify-facilitation"></a>
#### Facilitation

Use the bridge after Lab 2 or during trace-diagnosis discussion. Predict the next task after malformed output, run the failure fixture, inspect the typed report, then explain the early-success case. Use [Assignment 09](../ASSIGNMENTS.md#assignment-09-framework-comparison) to separate role/task orchestration from application-owned retry policy.

The third failure belongs to the tool; escalation belongs to the wrapper. Three attempts means at most three kickoffs, not four. The local escalation stub does not contact a human or grant approval for another run.


<a id="run-and-verify-factory-continuation"></a>
#### Factory continuation

Run `python live_simulation_orchestrator.py` from the course root for paced deterministic collaboration, or add `--mode replay --delay-seconds 0` for fast rehearsal. No API key or provider setup is required. Explicit human gates control the real local publication. See [local factory verification](../SETUP.md#verify-the-local-factory).

## Historical verification receipt

This receipt records its dated source snapshot. Run the current readiness gate for current evidence; historical counts are not the present suite total.

<a id="historical-verification"></a>

<a id="historical-verification-three-agent-reference-verification"></a>
### Three-agent reference verification

Verified **20 October 2026, Asia/Bangkok**. The [notebook](01_Bridge_Sequential_Crew.ipynb) is an optional reference for Lecture 8 and Assignment 09, alongside the seven required notebooks without extra marks.

| Requirement | Verified evidence |
| --- | --- |
| Three agents | Manager, Coder, QA; one Manager handles brief and review tasks. |
| Archive the old example | Seven-agent project moved under `_archive/crewai_learning/`; 14 source/configuration files retain their hashes. |
| Strict output for every task | WorkOrder, CodePatch, QAReport, and ManagerDecision; callable guards reject invalid JSON before the next task. Tests inject garbage at all four boundaries. |
| Hard maximum of three attempts | Python wrapper owns the bound; agent and guardrail retries are disabled. Fresh crew per attempt. |
| Third failure escalates | Actual notebook output: `Tool failures: 3 | kickoffs: 3 | stopped: True`; typed `EscalationReport` contains three failures and `ESCALATION_TRIGGERED`. |
| No downstream work after malformed output | `ValidationError` observed; QA and Manager review call counts remain zero. |
| Useful success path | Valid fixture succeeds after one kickoff; a separate test recovers after two tool failures. |
| Invalid approval cannot pass | Tests reject failed QA, stale patch evidence, mismatched task identity, and Manager rejection. |
| Offline notebook | Executed in a real Jupyter kernel with credentials removed and external network tripwires; zero external attempts and unhandled cell errors. |
| Navigation and scope | Active README paths, Lecture 8, Assignment 09, syllabus, course map, and manifest point to the ungraded reference. |

The full `python tools/check_readiness.py` gate passed: **95 unit + 46 integration = 141 tests**, with zero failures, errors, or skips. Exact requirement pins and `pip check` passed. Python 3.12.3; CrewAI 1.15.23; Pydantic 2.12.5; nbclient 0.10.2; nbformat 5.10.4.

Run ID: `20261019T185734Z-495da39a` (UTC timestamp). Verification source fingerprint: `bc68688ef31f5d4fea2f0f90b0dda356620258c3b58ec6d21288f3f0772f19b7`.

[Recorded evidence and hashes](audit_evidence/2026-10-20-reference.json) identify the checked sources. Local executed copies and detailed logs are under `.test-results/readiness/20261019T185734Z-495da39a/`; they are intentionally excluded from distribution. The handout's code outputs and execution counts remain empty.

These results concern the supplied fixture scenarios. The example uses sequential execution and a hierarchy of responsibilities, not native hierarchical delegation. QA compares the supplied fixture rather than running generated code. Live provider behavior and deployment readiness were not tested. The pinned CrewAI version emits deprecation warnings and an event-pairing diagnostic for intentionally raised validation errors; execution assertions still verify the stop behavior.
