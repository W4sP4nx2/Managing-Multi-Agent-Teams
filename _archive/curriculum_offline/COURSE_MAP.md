# Course Map: Managing Multi-Agent Teams

[Course home](README.md) · [Learner paths](README.md#learner-paths) · [Slide index](README.md#main-deck-slide-index)

This map connects course concepts, learner actions, notebook tasks, and evidence. The teaching sequence is **connect → predict → practice → respond → explain → transfer**: a meaningful case and open question first, a bounded repair second, then feedback and evidence before the Capstone transfer. The design adapts the Stanford Teaching Commons' AI-literacy and assignment guidance; see the [teaching-design alignment](instructor/stanford_teaching_guide_alignment.md). Start with a **multiagent system (MAS)**: agents interacting with one another and an environment. Explore interaction types, procurement, and an HR/RAG use case before the practical route. Then use **spec-driven development**: define the expected artifact, make relevant context available, limit tools, validate the handoff, and inspect evidence before accepting a result. The two-day workshop groups nine competency topics into Context Engineering (Lab 1), Multi-Agent Management/Code Auditing (Lab 2), Manager Oversight/Code Validation (Lab 3), and a two-team software Capstone.

The required runtime is deterministic. Learners construct CrewAI roles and task dependencies, then exercise local Python fixtures. The required path does **not** execute live CrewAI teams, generate a working login service, run real penetration tests, or deploy a product. Its deliverable is a repaired, inspectable workflow and an Architecture Decision Record (ADR) explaining its controls and remaining risks.

## Choose your route

| You need… | Open… |
| --- | --- |
| The environment and four setup commands | [SETUP.md](SETUP.md) |
| The next notebook and the precise learner edits | [Five-notebook order](#five-notebook-order), then [control and cell map](#control-and-cell-map) |
| Concepts, simulations, and slides | [README slide dashboard](README.md#click-through-course-journey) · [Workshop syllabus](assignments/assignment_syllabus.md) · [Simulation walkthroughs](assignments/workshop_simulations.md) |
| Exercise instructions | [Assignment index](assignments/index.md) · [Capstone brief](assignments/ex5_capstone_virtual_software_company.md) |
| The classroom schedule and assessment | [Learner Playbook](PLAYBOOK.md) |
| Assessment and the Paper ADR route | [Assessment](#assessment-100-course-marks) · [Capstone brief](assignments/ex5_capstone_virtual_software_company.md) |
| Research context | [Curated academic and technical resources](resources/curated_resource_library.md) |
| Agent-building design prompts | [Design guide](assignments/agent_building_design_guide.md); formative checkpoints at the end of each notebook |
| Framework literacy on slides 17 and 20 | [Framework comparison](resources/framework_comparison.md); ungraded slide/reference reading |

## Five-notebook order

Install [the required workshop environment](SETUP.md), start JupyterLab from the repository root, and open these notebooks in order. The [manifest](notebook_manifest.yml) records this runtime sequence. The [21-slide main deck](slides/managing_multi_agent_teams_workshop_v16.pptx) opens with the agenda and starting with one agent (slides 1–2), then introduces action risks, MAS types, applications, and two formative simulations (slides 3–7). These walkthroughs add no runnable notebook, package, or grade. Slide 8 leads into the practical sequence below. The nine competency topics in the syllabus share this same route.

| Order | Notebook | What the learner does | Completion evidence |
| ---: | --- | --- | --- |
| 0 | [Sandbox preflight](notebooks/00_sandbox_preflight.ipynb) | Run package, mode, workspace, and temporary-write checks. | Required packages are present; deterministic mode and workspace assertions pass. Ungraded. |
| 1 | [Lab 1: Context Engineering — Typed Contracts](notebooks/01_lab_pydantic.ipynb) | Replace the TODO model with declared fields, a confidence range, and forbidden extra fields. | The valid fixture passes; the invalid score and extra field are rejected; grader reports 15/15. |
| 2 | [Lab 2: Multi-Agent Management — Code Auditing and Team Oversight](notebooks/02_lab_crewai.ipynb) | Remove the Manager's writing tool and add the Architect task to the Coder's context. | Audit records `PASS_TO_QA` with one typed local inbox item; management note completed; unchanged grader reports 15/15. |
| 3 | [Lab 3: Manager Oversight — Code Validation and Bounded Repair](notebooks/03_lab_security.ipynb) | Validate a short numeric ID and set three retries after the initial attempt. | Unsafe fixture blocked; four mock calls cost $0.20; oversight records `ESCALATE_TO_HUMAN`; note completed; unchanged grader reports 15/15. |
| 4 | [Capstone: Development to Security](notebooks/04_capstone.ipynb) | Reject failed QA, validate before Security starts, separate approval/scanning tools, and complete the ADR. | Code grader reports 20/20; typed audit result and adversarial fixture are inspected; ADR receives a separate /20 score. |

Each core notebook sets `USE_LIVE_LLM = False`; these are separate notebook settings. The five core notebooks contain no provider-call branch and run offline after setup without an API key. Initial dependency installation needs internet or a prepared environment/package bundle. The optional provider-backed example is isolated in [extensions/bonus_live_demo.ipynb](extensions/bonus_live_demo.ipynb), reserved for the end of Day 2. The readiness tests exercise core notebooks with provider credentials removed and external network connections blocked.

## Formative agent-building checkpoints

The [design guide](assignments/agent_building_design_guide.md) connects new deck topics to short Markdown checkpoints at the end of the five notebooks. Discuss them or write a brief answer. They add no runnable cells, dependencies, graded TODOs, or marks; the existing code cells and grader locations stay the same.

| Notebook | Slides | Design checkpoint |
| --- | --- | --- |
| Preflight | 1–3, 8 | [Start with one agent](assignments/agent_building_design_guide.md#start-with-one-agent): define the task and the first reason to add a helper. |
| Lab 1 | 9–10 | [Context packet](assignments/agent_building_design_guide.md#context-engineering): task, approved rule, output contract, and excluded context. |
| Lab 2 | 11–12 | [Helper roles](assignments/agent_building_design_guide.md#one-main-agent-and-specialist-helpers): scoped input, return artifact, and a withheld tool. |
| Lab 3 | 14–16 | [Stable tools](assignments/agent_building_design_guide.md#stable-tools-and-loading-on-demand), an [actionable error, and a state receipt](assignments/agent_building_design_guide.md#state-changes-and-actionable-errors). |
| Capstone | 13, 18, 21 | [Least-cost adequate route and human pairing](assignments/agent_building_design_guide.md#choosing-a-capability-and-pairing-with-the-human), then [takeaways tied to evidence](assignments/agent_building_design_guide.md#takeaways-and-evidence). |

The local notebooks do not execute desktop, video, or cloud coding helpers, tool discovery, durable state storage, or user-interaction tools. These are proposed designs. TeamLog and oversight records are in-memory fixtures; the Fast/Expert route uses illustrative costs and does not benchmark the capability ladder. Distinguish a useful design proposal from an observed notebook result.

## Control and cell map

Use the stable cell IDs below to find the learner edit, audit, and grader; introductory diagrams can move numeric cell positions. Legacy Lab 3 and Capstone numbers count all cells, including Markdown, from 1. The [Lab 1 and Lab 2 diagram guide](resources/diagrams/README.md) provides a visual route with text descriptions and standards references.

Implementation references: CrewAI documents [task context and structured output](https://docs.crewai.com/en/concepts/tasks), [agent tool configuration](https://docs.crewai.com/en/concepts/agents), and [reusable custom tools](https://docs.crewai.com/en/learn/create-custom-tools). Pydantic documents the [field validators](https://docs.pydantic.dev/latest/concepts/validators/) used at the Capstone boundary. The table below maps those APIs to the current teaching fixtures.

| Mechanism | Exact notebook location | Learner edit or observation | What the mechanism establishes |
| --- | --- | --- | --- |
| Contract before downstream use | Lab 1: `lab1-broken-state`; `lab1-learner-workspace` | Observe the weak model, then declare `topic`, `confidence_score`, and `findings`; add `Field(ge=0.0, le=1.0)` and `ConfigDict(extra="forbid")`. | Representation, field constraints, and rejection of undeclared fields. This does not establish whether findings are true. |
| Role-aware context / TeamLog | Lab 2: `88df3214` — configuration; `38b0ca66` — deterministic response | Keep the supplied `team_log`; set `coder_task.context=[architect_task]`. | Makes a prior task's output available in the task graph. The mock chooses a string ID when that dependency exists. Context availability does not prove an LLM read, understood, or followed a rule. |
| Typed intra-team handoff | Lab 2: `88df3214`; `38b0ca66` | Inspect `coder_task.output_pydantic=CodePatch`, `qa_task.context=[coder_task]`, and `qa_task.output_pydantic=QAReport`; validate the local response. | Declares the Coder-to-QA dependency and output models. The required demonstration validates the Coder fixture locally; it does not execute a QA task. |
| Reusable skills as tools | Lab 2: `88df3214` — `@tool` functions | Inspect `write_code_tool`, `approve_code_tool`, and `run_tests_tool`. | One named function can be exposed to selected roles. These tools return placeholder strings: they write no files, approve no real code, and run no test commands. |
| Specialized role limits | Lab 2: `88df3214` — Agent tool lists | Change the Manager to `tools=[approve_code_tool]`; retain delegation. Keep Coder `[write_code_tool]` and QA `[run_tests_tool]`. | Restricts which custom tools CrewAI exposes to each role. This is framework-level availability, not OS/process isolation or proof that arbitrary code cannot access resources. |
| Input gate before a tool | Lab 3, cell 3 `03_guardrails_security_and_repair-02`; safe case cell 5 `03_guardrails_security_and_repair-04` | Add forbidden extra fields and a `user_id` validator accepting 1–12 digits. | Rejects the supplied SQL-like payload before the dry-run function is called. This is an MCP-style boundary exercise, not a running MCP service or comprehensive SQL/prompt-injection defense. |
| Bounded repair and escalation | Lab 3, cell 3 `03_guardrails_security_and_repair-02` — `MAX_RETRIES` and `run_repair_loop` | Set `MAX_RETRIES=3` and rerun the state calculation. | The always-failing mock performs one initial attempt plus three retries, then returns `escalated=True`. The mock cost stops at $0.20; there is no real charge or human notification. |
| Manager's Audit Gate | Lab 2: `lab2-manager-audit-gate`; `lab2-manager-audit-decision` | Run the supplied helper after the fixture; inspect every check and record decision, evidence, and next owner. | Audits all three tool lists, Manager delegation, task owners, context/model declarations, and the current payload. `BLOCK` leaves the local QA inbox empty; `PASS_TO_QA` admits one validated `CodePatch`. It executes no QA task or release. Formative, no extra marks. |
| Management Oversight | Lab 3, cell 7 `lab3-management-oversight`; decision cell 8 `lab3-manager-decision` | Inspect the unsafe-call log, valid/invalid input checks, four-call budget, cost, and escalation; record the next owner. | For the always-failing fixture, corrected controls produce `ESCALATE_TO_HUMAN` and no release approval. Failed checks produce `BLOCK_AND_REPAIR_CONTROLS`. The record adds no calls and sends no notification. Formative, no extra marks. |
| Failed-QA contract gate | Capstone, cell 5 `capstone-04` — `DevDeliverable` | Add a field validator rejecting `unit_tests_passed=False`. | Enforces the supplied QA-status claim. It does not independently run tests or prove that `True` is truthful. |
| Inter-team boundary | Capstone, cell 7 `capstone-06` — `coordinate_handoff`; explanation cell 10 `capstone-09` | Revalidate `candidate.model_dump()` as `DevDeliverable`; record validation before the Security-start event. | Validates the artifact before calling the local Security adapter. A plain Python Coordinator connects the teams; it is not a sixth agent. |
| Reusable Security tool and separate approval | Capstone, cell 13 `capstone-11` — `mock_pen_test_tool`, `approve_audit_tool`, and Security Agents | Remove `mock_pen_test_tool` from the Security Manager; retain it for the Pen Tester. | Repeats Lab 2's named-tool pattern. The scanner detects a short fixed list of SQL/XSS markers; it is not a production security scanner. |
| Optional live structured output | Separate [bonus notebook](extensions/bonus_live_demo.ipynb); Capstone cells 14–15 `capstone-12` / `capstone-13` contain navigation only | Optional instructor demonstration at the end of Day 2. | The bonus requests one provider response using the `ResearchOutput` Pydantic model and inspects the parsed result. It does not execute either Crew or the Development-to-Security handoff. No provider calls appear in the core Capstone. |
| Adversarial inspection and design judgment | Capstone, cell 19 `capstone-17`; cell 20 `capstone-18` | Inspect failed-QA rejection and marker findings; answer risk, controls/evidence, and next-step questions. | Separates structural validation from code review and records the learner's reasoning about what remains unproven. |

## Enterprise DX and AX

Labs 2–3 and the Capstone define two small helpers in their first code cell. `inspect_state(step, data)` displays selected, synthetic workflow evidence as indented JSON. `safe_validate(schema, data)` returns the validated model or prints a concise governance block and returns `None` after an expected Pydantic validation error. Callers must check for `None` before using a result. The helper does not repair an invalid artifact or authorize a handoff. Internal audit, grader, and receiving-boundary checks retain their strict validation behavior.

The **Blind Agent Debug** exercise at the end of Lab 2 asks learners to inspect missing Architect context, identify the numeric `generated_output.user_id`, repair `coder_task.context=[architect_task]`, and rerun the actual demonstration and Manager gate. The historical failing trace stays unchanged. This five-minute task adds no marks.

Agent experience (AX) comes from the tool contract: **Action, Input, Output, Warning**. The docstrings describe when to use a tool, accepted arguments, returned evidence, and boundaries. Lab 3's ID validation still runs before its dry-run lookup; the Capstone still separates scanning from approval. Clear documentation supports tool choice, while code enforces the relevant checks.

The [Markmap outline](slides/managing_multi_agent_teams_mindmap.md) and closing slide connect these controls to four curriculum branches. The Strategy, Policy, and Culture lenses organize the discussion, with human review and escalation across them. Codex / ChatGPT is the workshop workspace reference; the core runtime remains CrewAI configurations and local Python fixtures. Lab 1's privacy connection is context minimization and rejection of undeclared fields, not an implemented PII detector. Inspector output is a local teaching log, not durable or tamper-proof audit storage; use synthetic data and select fields before logging real workloads.

## What the graders actually check

Run the notebook cells in order after every edit. The starters are intentionally incomplete. Check the printed score and the demonstration evidence; execution without an uncaught exception does not establish that the target control passes.

| Grader location | Current checks and raw credit | Expected starter → repaired state |
| --- | --- | --- |
| Lab 1: `lab1-auto-grader` | Required fields, accepted valid data, missing-field rejection, and selected wrong-type probes gate both scores. Inclusive range checks at 0.0/1.0 and rejection below/above the range earn 5; rejection of `secret_backdoor` earns 10. Both = 15; range only = 5; extras only = 10. | 0/15 → 15/15. |
| Lab 2: `84aaa3ad` | Manager has exactly the approval tool and permits delegation (5); Coder context contains the actual `architect_task` object (10). Neither repair = 0; Manager only = 5; context only = 10; both = 15. | 0/15 → 5/15 or 10/15 → 15/15. |
| Lab 3 cell 10 `03_guardrails_security_and_repair-06` | Rejects supplied hostile input (4); also accepts `"123"` (3); exactly three retries (3); four recorded calls with escalation (3); bounded simulated cost (2). | 0/15 → 15/15. Validator-only repair earns 7; retry-only repair earns 8. |
| Capstone cell 17 `capstone-15` | Separate Security approval/scanning tool lists (5); failed-QA rejection **and** validation-before-start log ordering (10); `final_audit` is a `SecurityAuditResult` (5). | 5/20 → 20/20. The starter already returns a typed result. |

The supplied Manager audit and oversight cells are additional formative evidence, not additional grader points. Complete their short decision notes. The Lab 2 gate controls only a local simulated QA inbox; the Lab 3 oversight record inspects the existing bounded loop.

These checks are deliberately small. Lab 1's grader checks required fields, selected types, both endpoints, and out-of-range probes; it does not establish the truth of findings or cover every possible payload. Lab 2's grader checks configuration; it does not inspect an executed TeamLog read, run CrewAI, check all Coder/QA tool lists, or score the separate typed-fixture cell. Lab 3's grader probes one malicious value and one safe value; it does not separately probe the 12-digit limit or extra-field rejection. The Capstone grader inspects the contract, log ordering, tool lists, and result type; its log check does not independently prove every runtime event, and it does not grade the separate live bonus or scanner accuracy. Inspect the supplied demonstration cells and learner reasoning alongside scores.

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

## Workshop topics and research context

| Topic | Concept | Practical connection |
| ---: | --- | --- |
| 1 | Turn a vague request into a specification | [Assignment 01](assignments/assignment_01_strategic_prompt_engineering.md) |
| 2 | Safe workspace and role-aware knowledge | [Assignment 02](assignments/assignment_02_ai_workspace_and_role_context.md); Lab 2 context map |
| 3 | Represent the specification as a contract | Lab 1; [Assignment 03](assignments/assignment_03_architectural_supervision.md) |
| 4 | Tool boundaries and bounded control flow | Preview Lab 3's input gate and repair loop |
| 5 | Coordinate Manager, Coder, and QA | Lab 2; [Assignment 04](assignments/assignment_04_code_auditing.md) |
| 6 | Validate inputs and evaluate failure behavior | Lab 3; [Assignment 06](assignments/assignment_06_code_validation.md) |
| 7 | Select which prior evidence a role needs | [Assignment 07](assignments/assignment_07_context_engineering_access_lists.md) |
| 8 | Diagnose a failure using trace evidence | [Assignment 08](assignments/assignment_08_debugging_sdlc.md) |
| 9 | Connect Development to Security and defend the design | Capstone notebook and ADR |

[Lecture 8](assignments/assignment_08_debugging_sdlc.md#lecture-8-reference-discussion-choosing-an-orchestration-pattern) explains the course choice of CrewAI for visible roles and compares LangGraph state/recovery, AutoGen conversation patterns, and LlamaIndex retrieval. The [optional Capstone architecture extension](resources/framework_comparison.md#optional-capstone-architecture-extension-langgraph) is reference/design only; no implementation or installation is assigned.

The [workshop syllabus](assignments/assignment_syllabus.md#course-topic-map) maps each topic to the current main deck. Procurement and HR/RAG are [formative simulations](assignments/workshop_simulations.md), while the graded software pipeline remains Development to Security. RAG retrieves source material for a response; retrieval by itself does not constitute a multiagent system.

Slides 10, 12, and 16 retain research context in small reference bullets and speaker notes; the [curated resource library](resources/curated_resource_library.md) supplies the readings. Slides 17 and 20 cover framework literacy using the [comparison reference](resources/framework_comparison.md). This is an ungraded slide/reference objective within the existing course.

Theory of Mind is a lens for asking what information each role needs; the workshop does not implement a psychological model. TeamLog is the local shared-rule example. Fugu-style discussion means explicit, inspectable routing/context choices; learners do not use a hosted Fugu endpoint. TRINITY, Conductor, ChatDev, and Reflexion provide research context for coordination, verification, and repair. Use the [curated resource library](resources/curated_resource_library.md) for citations and keep research claims separate from what the classroom fixtures demonstrate.

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

A sound [Paper ADR](assignments/ex5_capstone_virtual_software_company.md#architecture-decision-record-20-points) is an accepted Capstone pass route when your environment prevents execution. The same /20 ADR rubric applies. Sound reasoning meets the pass condition; it does not automatically receive full marks or supply missing implementation evidence.

## After the workshop

The optional [CrewAI advanced reference](crewai_learning/README.md) follows Lab 2 and supports Lecture 8 and [Assignment 09](assignments/assignment_09_framework_comparison.md). It runs real CrewAI tasks with local fixture LLMs and external networking blocked, proving strict output rejection and three-attempt escalation. It is separate from the five required notebooks and adds no marks.

After the Capstone, the optional [Mock CI/CD Pipeline](extensions/11_mock_cicd_pipeline.ipynb) extends the handoff lesson to a three-feature lifecycle. Learners inspect `FEAT-002` at `BLOCKED`, resubmit a corrected description with old evidence cleared, rerun QA and Security gates, and record an explicit Manager decision for the new revision. Missing approval holds at `SECURITY_APPROVED`; approval permits the local `DEPLOYED` state. It is an offline sequential simulation using existing Pydantic, adds no marks, and performs no real deployment. See the [README walkthrough](README.md#optional-mock-cicd-pipeline).

[Optional extensions](extensions/README.md) provide further study. They add no required notebooks or course marks.

[Course home](README.md) · [Learner paths](README.md#learner-paths) · [Slide index](README.md#main-deck-slide-index)
