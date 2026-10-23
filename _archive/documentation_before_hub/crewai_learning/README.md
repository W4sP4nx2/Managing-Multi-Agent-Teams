# CrewAI learning bridge: Manager, Coder, QA

[Open the notebook](01_Bridge_Sequential_Crew.ipynb) · [Setup and verification](SETUP_AND_LEARNING_EXPERIENCE.md) · [Course learner paths](../README.md#learner-paths) · [Slide index](../README.md#main-deck-slide-index)

Run a three-agent coding team with real CrewAI execution and deterministic local model responses. The example proves that malformed output is rejected and three failed attempts produce a typed escalation instead of continuing indefinitely.

**Course learning bridge. No separate point scale.** Start with [Lab 2](../notebooks/02_lab_crewai.ipynb); use this notebook for [Lecture 8: Debugging and SDLC](../assignments/assignment_08_debugging_sdlc.md) and [Assignment 09: Framework Comparison](../assignments/assignment_09_framework_comparison.md).

## Learner path

1. Use the existing [Python 3.12 course environment](../SETUP.md). No extra framework package or API key is needed.
2. Open [01_Bridge_Sequential_Crew.ipynb](01_Bridge_Sequential_Crew.ipynb) in JupyterLab and run all cells in order.
3. Inspect the three roles and four tasks: **Manager brief → Coder patch → QA evidence → Manager review**.
4. Observe `ValidationError` for garbage output; QA must not run afterward.
5. Observe **3 tool failures, 3 kickoffs, 1 EscalationReport**, then a successful fixture that stops after one attempt.
6. Return to [Lecture 8](../assignments/assignment_08_debugging_sdlc.md) or the [framework comparison](../assignments/assignment_09_framework_comparison.md) to explain which controls are supplied by CrewAI and which are enforced by the application.

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
| [Verification record](VERIFICATION.md) | Checked requirements, observed notebook results, and full readiness evidence |
| [Editable notebook source](../tools/notebook_sources/01_Bridge_Sequential_Crew.py) | Regenerate with `python tools/build_core_notebooks.py` |
| [Lecture 8](../assignments/assignment_08_debugging_sdlc.md) | Trace failures, evidence, and stopping behavior |
| [Assignment 09](../assignments/assignment_09_framework_comparison.md) | Ungraded framework comparison using the working example |
| [Archived seven-agent material](../_archive/crewai_learning/README.md) | Historical research crew and superseded superseded Homework G material |

## Evidence limits

The notebook uses `Process.sequential`. Manager/Coder/QA demonstrate a hierarchy of responsibilities, not dynamic hierarchical delegation. `FixtureLLM` replaces model responses while the real Agent, Task, guardrail, context, and Crew executors run. Its Coder response invokes the injected tool once; autonomous tool selection and native tool-repair behavior are outside this proof.

QA checks an exact supplied code fixture; it does not execute generated code. The example demonstrates production-oriented control patterns, not production certification, model reliability, process isolation, or deployment readiness. The course factory also stays deterministic and uses no provider API.

The [earlier audit](../_archive/crewai_learning/CURRICULUM_DELIVERY_AUDIT.md) describes the archived project's pre-fix state. This focused reference replaces that active teaching route under the agreed three-agent scope.

[Return to course home](../README.md) · [Required practical sequence](../README.md#required-practical-sequence)

## Continue into the factory

Open [05 · Software Factory Simulation](../notebooks/05_live_software_factory.ipynb), then [06 · Local CI/CD](../notebooks/06_local_cicd.ipynb). The bridge executes real CrewAI task machinery with fixture LLMs. The factory presents pre-generated role collaboration and performs actual local artifact, review, Git, and publication operations. Historical model labels are illustrative and actual API cost is $0.00. Read [the factory guide](../extensions/live_software_factory.md) for human gates and simulated cost accounting.
