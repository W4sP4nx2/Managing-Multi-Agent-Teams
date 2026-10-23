# Course Map: Managing Multi-Agent Teams

[Course home](README.md) · [Learner paths](README.md#learner-paths) · [Slide index](README.md#main-deck-slide-index)

This map connects course concepts, learner actions, notebook tasks, and evidence. The teaching sequence is **connect → predict → practice → respond → explain → transfer**: a meaningful case and open question first, a bounded repair second, then feedback and evidence before the Capstone transfer. The design adapts the Stanford Teaching Commons' AI-literacy and assignment guidance; see the [teaching-design alignment](INSTRUCTOR_PLAYBOOK.md#stanford-teaching-guide-alignment). Start with a **multiagent system (MAS)**: agents interacting with one another and an environment. Explore interaction types, procurement, and an HR/RAG use case before the practical route. Then use **spec-driven development**: define the expected artifact, make relevant context available, limit tools, validate the handoff, and inspect evidence before accepting a result. The course groups nine competency topics into Context Engineering (Lab 1), Multi-Agent Management/Code Auditing (Lab 2), Manager Oversight/Code Validation (Lab 3), and a two-team software Capstone.

The required runtime is deterministic. Learners construct CrewAI roles and task dependencies, then exercise local Python fixtures. Foundation notebooks construct and inspect CrewAI configurations. The learning bridge executes Crew tasks with fixture LLMs. The integrated factory writes and publishes a real local static travel page after explicit human approval. No provider call, login/booking service, remote deployment, or full penetration test runs. The deliverables include workflow evidence, local artifacts, and an Architecture Decision Record (ADR).

## Choose your route

| You need… | Open… |
| --- | --- |
| The environment and four setup commands | [SETUP.md](SETUP.md) |
| The next notebook and the precise learner edits | [Seven-notebook order](#seven-notebook-order), then [control and cell map](#control-and-cell-map) |
| Concepts, simulations, and slides | [README slide dashboard](README.md#click-through-course-journey) · [Course syllabus](README.md#course-topics) · [Simulation walkthroughs](ASSIGNMENTS.md#workshop-simulations) |
| Exercise instructions | [Assignment index](ASSIGNMENTS.md#assignment-index) · [Capstone brief](ASSIGNMENTS.md#ex5-capstone-virtual-software-company) |
| The learner workflow and assessment | [Learner Playbook](README.md#golden-path) |
| Assessment and the Paper ADR route | [Assessment](#assessment-100-course-marks) · [Capstone brief](ASSIGNMENTS.md#ex5-capstone-virtual-software-company) |
| Research context | [Curated academic and technical resources](README.md#readings) |
| Agent-building design prompts | [Design guide](ASSIGNMENTS.md#agent-building-design-guide); optional reading alongside runnable exercises |
| Framework literacy in the written reference | [Framework comparison](README.md#framework-comparison); ungraded reference reading |

## Seven-notebook order

Install [the required course environment](SETUP.md), start JupyterLab from the repository root, and open these notebooks in order. The [manifest](notebook_manifest.yml) records this runtime sequence. The [six-slide main deck](slides/managing_multi_agent_teams_6_slides.pptx) summarizes architecture, execution, typed handoffs, team review, deliverables, and setup/assessment. MAS types, applications, framework comparisons, and formative simulations remain in the written guides and add no runnable notebook, package, or grade. The nine competency topics share the same seven-notebook route.

| Order | Notebook | What the learner does | Completion evidence |
| ---: | --- | --- | --- |
| 0 | [Sandbox preflight](notebooks/00_sandbox_preflight.ipynb) | Run package, mode, workspace, and temporary-write checks. | Required packages are present; deterministic mode and workspace assertions pass. Ungraded. |
| 1 | [Lab 1: Context Engineering — Typed Contracts](notebooks/01_lab_pydantic.ipynb) | Replace the TODO model with declared fields, a confidence range, and forbidden extra fields. | The valid fixture passes; the invalid score and extra field are rejected; grader reports 15/15. |
| 2 | [Lab 2: Multi-Agent Management — Code Auditing and Team Oversight](notebooks/02_lab_crewai.ipynb) | Remove the Manager's writing tool and add the Architect task to the Coder's context. | Audit records `PASS_TO_QA` with one typed local inbox item; management note completed; unchanged grader reports 15/15. |
| 3 | [Lab 3: Manager Oversight — Code Validation and Bounded Repair](notebooks/03_lab_security.ipynb) | Validate a short numeric ID and set three retries after the initial attempt. | Unsafe fixture blocked; four mock calls cost $0.20; oversight records `ESCALATE_TO_HUMAN`; note completed; unchanged grader reports 15/15. |
| 4 | [Capstone: Development to Security](notebooks/04_capstone.ipynb) | Reject failed QA, validate before Security starts, separate approval/scanning tools, and complete the ADR. | Code grader reports 20/20; typed audit result and adversarial fixture are inspected; ADR receives a separate /20 score. |
| 5 | [Software Factory Simulation](notebooks/05_live_software_factory.ipynb) | Inspect fixture roles, simulated budget, human gates, and real local candidate. | Malicious request blocks; candidate and gate records refer to the same digest/revision. |
| 6 | [Local CI/CD](notebooks/06_local_cicd.ipynb) | Run bounded checks and prove publication authorization. | Missing/stale evidence blocks; approved local file matches its receipt. |

Each foundation notebook sets `USE_LIVE_LLM = False`; these are separate notebook settings. The foundation notebooks contain no provider-call branch and run offline after setup without an API key. Initial dependency installation needs internet or a prepared environment/package bundle. Foundation notebooks retain `USE_LIVE_LLM = False`. The integrated factory CLI uses deterministic simulation/replay with pre-generated outputs, no API keys, and actual API cost $0.00. The historical bonus notebook is reference material.

## How to use the notebook exercises

Each required notebook starts with **Run / Edit / Inspect / Finish** instructions and an embedded diagram. Run cells in order, edit the marked controls, and inspect the evidence before continuing. The SVG attachments render inside the notebook without a diagram package or network connection.

| Exercise | Interaction and evidence |
| --- | --- |
| 00 · Preflight | Check packages, course paths, execution settings, and temporary-file access. |
| 01 · Typed contracts | Repair required fields, bounds, and extra-field rejection; run the grader. |
| 02 · Team oversight | Repair role permissions and context; compare collaboration patterns using local rules. |
| 03 · Bounded repair | Reject unsafe input, stop after four mock calls, and record escalation. |
| 04 · Capstone | Validate the handoff; inspect scoped memory, an in-process API, and adversarial proofs; complete the ADR. |
| 05 · Factory | Compare approved and denied local publication; read the evidence database using the embedded ERD. |
| 06 · Local CI/CD | Prove denied, stale, and missing-input cases cannot publish. |
| Optional CrewAI bridge | Create and run a real sequential Crew with scripted responses; display Markdown and inspect stop/retry behavior. |

All exercises use local Python and fixed teaching data. No GPT, other LLM, or reasoning model is called. The optional bridge substitutes a scripted adapter at the model boundary; it still executes CrewAI's task machinery. [The design guide](ASSIGNMENTS.md#agent-building-design-guide) remains optional reading.

## Control and cell map

Use the stable cell IDs below to find the learner edit, audit, and grader; introductory diagrams can move numeric cell positions. Legacy Lab 3 and Capstone numbers count all cells, including Markdown, from 1. The [Lab 1 and Lab 2 diagram guide](README.md#diagram-guide) provides a visual route with text descriptions and standards references.

Implementation references: CrewAI documents [task context and structured output](https://docs.crewai.com/en/concepts/tasks), [agent tool configuration](https://docs.crewai.com/en/concepts/agents), and [reusable custom tools](https://docs.crewai.com/en/learn/create-custom-tools). Pydantic documents the [field validators](https://docs.pydantic.dev/latest/concepts/validators/) used at the Capstone boundary. The table below maps those APIs to the current teaching fixtures.

| Mechanism | Exact notebook location | Learner edit or observation | What the mechanism establishes |
| --- | --- | --- | --- |
| Contract before downstream use | Lab 1: `lab1-broken-state`; `lab1-learner-workspace` | Observe the weak model, then declare `topic`, `confidence_score`, and `findings`; add `Field(ge=0.0, le=1.0)` and `ConfigDict(extra="forbid")`. | Representation, field constraints, and rejection of undeclared fields. This does not establish whether findings are true. |
| Role-aware context / TeamLog | Lab 2: `88df3214` — agents; `lab2-task-configuration` — task context; `38b0ca66` — response | Keep the supplied `team_log`; set `coder_task.context=[architect_task]`. | Makes a prior task's output available in the task graph. The mock chooses a string ID when that dependency exists. Context availability does not prove an LLM read, understood, or followed a rule. |
| Typed intra-team handoff | Lab 2: `lab2-task-configuration`; `38b0ca66` | Inspect `coder_task.output_pydantic=CodePatch`, `qa_task.context=[coder_task]`, and `qa_task.output_pydantic=QAReport`; validate the local response. | Declares the Coder-to-QA dependency and output models. The required demonstration validates the Coder fixture locally; it does not execute a QA task. |
| Reusable skills as tools | Lab 2: `88df3214` — `@tool` functions | Inspect `write_code_tool`, `approve_code_tool`, and `run_tests_tool`. | One named function can be exposed to selected roles. These tools return placeholder strings: they write no files, approve no real code, and run no test commands. |
| Specialized role limits | Lab 2: `88df3214` — Agent tool lists | Change the Manager to `tools=[approve_code_tool]`; retain delegation. Keep Coder `[write_code_tool]` and QA `[run_tests_tool]`. | Restricts which custom tools CrewAI exposes to each role. This is framework-level availability, not OS/process isolation or proof that arbitrary code cannot access resources. |
| Skill Transparency Matrix | Lab 2: `lab2-skill-transparency-guide`; `lab2-skill-transparency` | Compare actual and allowed custom tools, inspect Action/Input/Output/Warning metadata, and rerun after repairing the Manager. | Observes framework tool exposure without running tools or changing permissions; does not establish OS isolation or model understanding. |
| Input gate before a tool | Lab 3, cell 3 `03_guardrails_security_and_repair-02`; safe case cell 5 `03_guardrails_security_and_repair-04` | Add forbidden extra fields and a `user_id` validator accepting 1–12 digits. | Rejects the supplied SQL-like payload before the dry-run function is called. This is an MCP-style boundary exercise, not a running MCP service or comprehensive SQL/prompt-injection defense. |
| Bounded repair and escalation | Lab 3, cell 3 `03_guardrails_security_and_repair-02` — `MAX_RETRIES` and `run_repair_loop` | Set `MAX_RETRIES=3` and rerun the state calculation. | The always-failing mock performs one initial attempt plus three retries, then returns `escalated=True`. The mock cost stops at $0.20; there is no real charge or human notification. |
| Manager's Audit Gate | Lab 2: `lab2-manager-audit-gate`; `lab2-manager-audit-decision` | Run the supplied helper after the fixture; inspect every check and record decision, evidence, and next owner. | Audits all three tool lists, Manager delegation, task owners, context/model declarations, and the current payload. `BLOCK` leaves the local QA inbox empty; `PASS_TO_QA` admits one validated `CodePatch`. It executes no QA task or release. Formative, no extra marks. |
| Management Oversight | Lab 3, cell 7 `lab3-management-oversight`; decision cell 8 `lab3-manager-decision` | Inspect the unsafe-call log, valid/invalid input checks, four-call budget, cost, and escalation; record the next owner. | For the always-failing fixture, corrected controls produce `ESCALATE_TO_HUMAN` and no release approval. Failed checks produce `BLOCK_AND_REPAIR_CONTROLS`. The record adds no calls and sends no notification. Formative, no extra marks. |
| Failed-QA contract gate | Capstone, cell 5 `capstone-04` — `DevDeliverable` | Add a field validator rejecting `unit_tests_passed=False`. | Enforces the supplied QA-status claim. It does not independently run tests or prove that `True` is truthful. |
| Inter-team boundary | Capstone, cell 7 `capstone-06` — `coordinate_handoff`; explanation cell 10 `capstone-09` | Revalidate `candidate.model_dump()` as `DevDeliverable`; record validation before the Security-start event. | Validates the artifact before calling the local Security adapter. A plain Python Coordinator connects the teams; it is not a sixth agent. |
| Reusable Security tool and separate approval | Capstone, cell 13 `capstone-11` — `mock_pen_test_tool`, `approve_audit_tool`, and Security Agents | Remove `mock_pen_test_tool` from the Security Manager; retain it for the Pen Tester. | Repeats Lab 2's named-tool pattern. The scanner detects a short fixed list of SQL/XSS markers; it is not a production security scanner. |
| Historical structured-output reference | Separate [bonus notebook](extensions/bonus_live_demo.ipynb); Capstone cells 14–15 `capstone-12` / `capstone-13` contain navigation only | Historical fixture reference; use the integrated deterministic factory for execution. | The reference illustrates a `ResearchOutput` Pydantic model with fixture data. It does not execute either Crew or the Development-to-Security handoff. No provider calls appear in the course factory or core Capstone. |
| Adversarial inspection and design judgment | Capstone, cell 19 `capstone-17`; cell 20 `capstone-18` | Inspect failed-QA rejection and marker findings; answer risk, controls/evidence, and next-step questions. | Separates structural validation from code review and records the learner's reasoning about what remains unproven. |

## Enterprise DX and AX

Labs 2–3 and the Capstone define two small helpers in their first code cell. `inspect_state(step, data)` displays selected, synthetic workflow evidence as indented JSON. `safe_validate(schema, data)` returns the validated model or prints a concise governance block and returns `None` after an expected Pydantic validation error. Callers must check for `None` before using a result. The helper does not repair an invalid artifact or authorize a handoff. Internal audit, grader, and receiving-boundary checks retain their strict validation behavior.

The **Blind Agent Debug** exercise at the end of Lab 2 asks learners to inspect missing Architect context, identify the numeric `generated_output.user_id`, repair `coder_task.context=[architect_task]`, and rerun the actual demonstration and Manager gate. The historical failing trace stays unchanged. This short task adds no marks.

Agent experience (AX) comes from the tool contract: **Action, Input, Output, Warning**. The docstrings describe when to use a tool, accepted arguments, returned evidence, and boundaries. Lab 3's ID validation still runs before its dry-run lookup; the Capstone still separates scanning from approval. Clear documentation supports tool choice, while code enforces the relevant checks.

The [slide index](README.md#main-deck-slide-index) and companion mind map connect the six-slide overview to the fuller curriculum branches. The Strategy, Policy, and Culture lenses organize the discussion, with human review and escalation across them. Codex / ChatGPT is the course workspace reference; the core runtime remains CrewAI configurations and local Python fixtures. Lab 1's privacy connection is context minimization and rejection of undeclared fields, not an implemented PII detector. Inspector output is a local teaching log, not durable or tamper-proof audit storage; use synthetic data and select fields before logging real workloads.

## What the graders actually check

Run the notebook cells in order after every edit. The starters are intentionally incomplete. Check the printed score and the demonstration evidence; execution without an uncaught exception does not establish that the target control passes.

| Grader location | Current checks and raw credit | Expected starter → repaired state |
| --- | --- | --- |
| Lab 1: `lab1-auto-grader` | Required fields, accepted valid data, missing-field rejection, and selected wrong-type probes gate both scores. Inclusive range checks at 0.0/1.0 and rejection below/above the range earn 5; rejection of `secret_backdoor` earns 10. Both = 15; range only = 5; extras only = 10. | 0/15 → 15/15. |
| Lab 2: `84aaa3ad` | Manager has exactly the approval tool and permits delegation (5); Coder context contains the actual `architect_task` object (10). Neither repair = 0; Manager only = 5; context only = 10; both = 15. | 0/15 → 5/15 or 10/15 → 15/15. |
| Lab 3 cell 10 `03_guardrails_security_and_repair-06` | Rejects supplied hostile input (4); also accepts `"123"` (3); exactly three retries (3); four recorded calls with escalation (3); bounded simulated cost (2). | 0/15 → 15/15. Validator-only repair earns 7; retry-only repair earns 8. |
| Capstone cell 17 `capstone-15` | Separate Security approval/scanning tool lists (5); failed-QA rejection **and** validation-before-start log ordering (10); `final_audit` is a `SecurityAuditResult` (5). | 5/20 → 20/20. The starter already returns a typed result. |

The supplied Manager audit and oversight cells are additional formative evidence, not additional grader points. Complete their short decision notes. The Lab 2 gate controls only a local simulated QA inbox; the Lab 3 oversight record inspects the existing bounded loop.

These checks are deliberately small. Lab 1's grader checks required fields, selected types, both endpoints, and out-of-range probes; it does not establish the truth of findings or cover every possible payload. Lab 2's grader checks configuration; it does not inspect an executed TeamLog read, run CrewAI, check all Coder/QA tool lists, or score the separate typed-fixture cell. Lab 3's grader probes one malicious value and one safe value; it does not separately probe the 12-digit limit or extra-field rejection. The Capstone grader inspects the contract, log ordering, tool lists, and result type; its log check does not independently prove every runtime event, and it does not grade the historical fixture reference or scanner accuracy. Inspect the supplied demonstration cells and learner reasoning alongside scores.

## One Development Team, then a Security Team

```text
Human request
    |
    v
Development Team: Engineering Manager + Coder + QA Auditor
    |
    | DevDeliverable
    v
Python Coordinator: validate, record the gate, start Security
    |
    v
Security Team: Pen Tester + Security Manager
    |
    | SecurityAuditResult
    v
Inspect audit outcome and evidence; explain remaining risk in the ADR
```

The five roles are three Development agents and two Security agents. In the hierarchical Crew, the Development Manager is supplied through `manager_agent`; it is not listed in `dev_crew.agents`, which contains the two workers. `architect_task` in Lab 2 carries an approved brief; it is not an additional Architect Agent.

Lab 2 demonstrates the Development team's reusable tool lists. In the current Capstone configuration, the Development Manager has the routing tool, and the Coder/QA have no custom tools. The Security agents repeat the scanner/approval tool pattern. The deterministic adapters in Capstone cell 7 produce the patch and audit, while cell 13 constructs the two Crew configurations. Keep those two kinds of evidence distinct.

The pre-written Fast/Expert routing example is ungraded. `fast_agent` and `expert_agent` are `RoutingTarget` data records, not additional CrewAI Agents or live models. Its fixed costs illustrate a policy; they are not provider prices or a spend ceiling. The current notebook returns an audit approval flag, not a deployed release or an automated repair cycle between the teams.

## Course topics and research context

| Topic | Concept | Practical connection |
| ---: | --- | --- |
| 1 | Turn a vague request into a specification | [Assignment 01](ASSIGNMENTS.md#assignment-01-strategic-prompt-engineering) |
| 2 | Safe workspace and role-aware knowledge | [Assignment 02](ASSIGNMENTS.md#assignment-02-ai-workspace-and-role-context); Lab 2 context map |
| 3 | Represent the specification as a contract | Lab 1; [Assignment 03](ASSIGNMENTS.md#assignment-03-architectural-supervision) |
| 4 | Tool boundaries and bounded control flow | Preview Lab 3's input gate and repair loop |
| 5 | Coordinate Manager, Coder, and QA | Lab 2; [Assignment 04](ASSIGNMENTS.md#assignment-04-code-auditing) |
| 6 | Validate inputs and evaluate failure behavior | Lab 3; [Assignment 06](ASSIGNMENTS.md#assignment-06-code-validation) |
| 7 | Select which prior evidence a role needs | [Assignment 07](ASSIGNMENTS.md#assignment-07-context-engineering-access-lists) |
| 8 | Diagnose a failure using trace evidence | [Assignment 08](ASSIGNMENTS.md#assignment-08-debugging-sdlc) |
| 9 | Connect Development to Security and defend the design | Capstone notebook and ADR |

[Lecture 8](ASSIGNMENTS.md#assignment-08-debugging-sdlc-lecture-8-reference-discussion-choosing-an-orchestration-pattern) explains the course choice of CrewAI for visible roles and compares LangGraph state/recovery, AutoGen conversation patterns, and LlamaIndex retrieval. The [optional Capstone architecture extension](README.md#langgraph-architecture-reading) is reference/design only; no implementation or installation is assigned.

The [course syllabus](README.md#course-topics) maps each topic to the practical route. Procurement and HR/RAG are [formative simulations](ASSIGNMENTS.md#workshop-simulations), while the graded software pipeline remains Development to Security. RAG retrieves source material for a response; retrieval by itself does not constitute a multiagent system.

Slides 2–4 summarize bounded execution, contracts, and review. Research context remains in the [curated resource library](README.md#readings); framework literacy remains in the [comparison reference](README.md#framework-comparison). These written discussions are ungraded and add no course requirements.

Theory of Mind is a lens for asking what information each role needs; the course does not implement a psychological model. TeamLog is the local shared-rule example. Fugu-style discussion means explicit, inspectable routing/context choices; learners do not use a hosted Fugu endpoint. TRINITY, Conductor, ChatDev, and Reflexion provide research context for coordination, verification, and repair. Use the [curated resource library](README.md#readings) for citations and keep research claims separate from what the classroom fixtures demonstrate.

## Assessment: 100 course marks

| Component | Raw result | Course marks | Evidence to retain |
| --- | ---: | ---: | --- |
| Lab 1 · Context Engineering | /15 | 20 | Edited model and grader result |
| Lab 2 · Multi-Agent Management | /15 | 20 | Two configuration edits, typed fixture, grader result |
| Lab 3 · Manager Oversight | /15 | 20 | Input gate, retry state, grader result |
| Capstone implementation | /20 | 20 | Contract, Coordinator/tool repairs, audit result, grader result |
| Capstone ADR and defense | /20 | 20 | Risk/architecture (6), controls and evidence (7), credible next step (7) |
| **Total** | | **100** | |

Convert each lab using `raw_score × 20 ÷ 15`; retain the raw and converted scores. Assignments 01, 02, 07, and 08 are formative; they add no separate marks. The repository's current pytest result is supporting evidence, not a fixed “38-test” grading promise or proof of universal security.

A sound [Paper ADR](ASSIGNMENTS.md#ex5-capstone-virtual-software-company-architecture-decision-record-20-points) is an accepted Capstone pass route when your environment prevents execution. The same /20 ADR rubric applies. Sound reasoning meets the pass condition; it does not automatically receive full marks or supply missing implementation evidence.

## Factory and local CI/CD integration

Continue from the Capstone into [05 · Software Factory](notebooks/05_live_software_factory.ipynb) and [06 · Local CI/CD](notebooks/06_local_cicd.ipynb). These are integrated course labs. Replay verifies the local policy route. Paced simulation and fast replay use the same fixtures; no live provider mode exists.

The [factory guide](extensions/live_software_factory.md) maps the Engineering Manager/orchestrator, Coder, Security, UI/UX, and QA roles to illustrative model labels, simulated cost entries, and typed evidence. The [Capstone ERD](resources/diagrams/capstone_factory_erd.md) explains actual run, artifact, review, approval, QA, publication, and separate teaching-cost records. Retain the candidate revision, review results, gate decisions, simulation ledger and actual $0.00 evidence, and local publication receipt.

The [CrewAI learning bridge](crewai_learning/README.md) runs real CrewAI tasks with local fixture LLMs. The older [mock pipeline](extensions/11_mock_cicd_pipeline.ipynb) is a comparison simulation; notebook 06 and the factory CLI are the current release route.

[Course home](README.md) · [Learner paths](README.md#learner-paths) · [Slide index](README.md#main-deck-slide-index)
