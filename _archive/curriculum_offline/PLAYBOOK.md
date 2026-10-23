# Managing Multi-Agent Teams: Learner Playbook

[Course home](README.md) · [Learner paths](README.md#learner-paths) · [Slide index](README.md#main-deck-slide-index)

This two-day workshop begins with a task for one accountable agent, then asks when a helper is worth adding. A **multiagent system** contains agents interacting with one another and an environment. Compare interaction types and trace procurement and HR/RAG use cases, then build the controls behind a Development-to-Security workflow. The required Context Engineering, Multi-Agent Management (Code Auditing), and Manager Oversight (Code Validation) labs and deterministic Capstone run locally without model-provider credentials. Install dependencies before class; after setup, the practical path can run offline.

Start with the [course map](COURSE_MAP.md) for the five-notebook sequence, edit locations, and evidence checks. This Playbook explains the practical workflow, schedule, and assessment. Use the [main 21-slide deck](slides/managing_multi_agent_teams_workshop_v16.pptx) throughout and the [formative simulations](assignments/workshop_simulations.md) for slides 6–7.

The required path contains five notebooks: an ungraded preflight, three graded labs, and the Capstone. Each ends with a short, ungraded [design checkpoint](assignments/agent_building_design_guide.md) connecting the deck to the exercise. Desktop/video/cloud helpers, tool discovery, durable state, and user-interaction tools are discussion designs; the local notebooks do not execute them. [Optional extensions](extensions/README.md) are available for post-course study.

JupyterLab is where learners run the notebooks. CrewAI defines role and task configurations, and Pydantic validates declared data constraints. Lab 2 constructs a Crew and validates a deterministic response locally; the Capstone runs ordinary Python team adapters and separately constructs two Crews. Keep `USE_LIVE_LLM = False` in the five core notebooks. Hosted model providers are not required for the labs, repository checks, or Capstone path. Live execution is isolated in the optional [bonus notebook](extensions/bonus_live_demo.ipynb) at the end of Day 2.

A useful restaurant analogy: CrewAI defines the kitchen roles and task dependencies; Pydantic is the recipe card that sets the required fields and limits. In code, `output_pydantic=...` declares a CrewAI task's output model. The deterministic Capstone Coordinator validates `DevDeliverable` before calling the local Security adapter. The separate end-of-Day-2 bonus demonstrates one provider response constrained by a Pydantic model; it does not run the two Crews.

This teaching design adapts the [Stanford Teaching Commons AI Teaching Guide](instructor/stanford_teaching_guide_alignment.md): connect to a meaningful case, ask learners to predict before running a fixture, provide bounded practice and feedback, then ask them to explain evidence and transfer the decision. Stanford's four intersecting AI-literacy domains (functional, ethical, rhetorical, pedagogical) are mapped to the workshop in that reference. It is a local adaptation, not a Stanford endorsement.

## Core Course Focus: Managed Team Delivery

The practicals address four risks: malformed handoffs, forgotten rules, unsafe tool access, and unbounded repair attempts.

| Pillar | Control | Learner outcome |
| --- | --- | --- |
| **Context Engineering** | Strict Pydantic contracts (Lab 1) | Reject schema violations before downstream use. |
| **Code Auditing** | Role tool lists, TeamLog, and explicit task context (Lab 2) | Keep rules visible as work passes between roles. |
| **Code Validation** | Input validation and tool boundaries (Lab 3) | Reject unsafe inputs and limit tool permissions. |
| **Bounded Autonomy** | Three retries after the initial attempt, then an escalation flag (Lab 3) | Bound repeated attempts and escalate unresolved work. |

A passing grader records that the defined check held for its fixture. Inspect the accepted data, rejected data, and workflow state alongside the score.

### Deterministic mode

Keep `USE_LIVE_LLM = False` in every core notebook. The five required notebooks contain no provider-call branch. The local fixtures make failures repeatable so a repair can be checked against the same input, without an internet connection or API key after setup. First-time dependency installation needs internet or a prepared environment/package bundle.

## Your management decisions

You supervise the same Manager–Coder–QA team across the three labs. Lab 1 sets the acceptance contract. In Lab 2, run the supplied **Manager's Audit Gate** after the fixture: a failed check keeps the local QA inbox empty, while `PASS_TO_QA` admits one typed proposal. In Lab 3, inspect the tool-call log, attempts, simulated spend, and escalation; corrected controls yield `ESCALATE_TO_HUMAN` for the always-failing task, with no release approval.

Record one decision-and-evidence sentence in each supplied Markdown template. These are formative oversight actions with no additional coding TODO or marks. Neither action runs a QA Crew or contacts a human. The Capstone then makes you the Workflow Coordinator managing Development-to-Security & Compliance boundaries.

## The Four-Step Student Roadmap

| Step | The Goal | The Tool | The "Win" Condition (How they know they passed) |
| --- | --- | --- | --- |
| **Step 1: The Contract** | Catch malformed AI output before downstream use. | **Pydantic** (Lab 1: Context Engineering) | The Auto-Grader prints `✅ SUCCESS: 15/15` because the schema rejects the adversarial fixture. |
| **Step 2: The Team** | Declare role context and typed task handoffs. | **CrewAI** (Lab 2: Multi-Agent Management) | The supplied audit records `PASS_TO_QA` and one typed local inbox item; the unchanged grader reaches 15/15. |
| **Step 3: The Guardrails** | Limit repair attempts and reject unsafe tool inputs. | **Bounded Loops & MCP-style input gate** (Lab 3: Manager Oversight) | The Manager records `ESCALATE_TO_HUMAN`: unsafe calls are absent, four mock attempts stop at $0.20, and the unchanged grader reaches 15/15. |
| **Step 4: The Delivery** | Connect two specialist teams through a typed, auditable handoff. | **Capstone** | The validated Dev fixture starts the Security adapter and returns a typed audit result; code grader reaches 20/20 or the Paper ADR is sound. |

## Learner Path

### Get the course files

Clone the repository:

```bash
git clone https://github.com/W4sP4nx2/Managing-Multi-Agent-Teams.git
cd Managing-Multi-Agent-Teams
```

If Git is unreliable, use the [repository ZIP](https://github.com/W4sP4nx2/Managing-Multi-Agent-Teams/archive/refs/heads/main.zip), extract it, and open a terminal in the course folder. A first package installation needs internet unless the instructor provides a prepared environment or local package bundle.

### Set up JupyterLab

Follow [SETUP.md](SETUP.md). Use Python 3.12 for the required CrewAI lab. Install the core requirements, then open `notebooks/00_sandbox_preflight.ipynb`. Follow [the notebook manifest](notebook_manifest.yml) for the three practical labs and Capstone.

The required environment is a native Python virtual environment. Docker and deployment are optional study topics.

### How to work each exercise

1. Read the scenario and identify the failure.
2. Predict which contract, role boundary, or retry limit should stop it.
3. Fill in the marked code or fix the deliberate bug.
4. Run the cells and inspect the result or exception.
5. Point to the evidence that shows the handoff or guardrail worked.

## One Team in the Labs; Two Teams in the Capstone

Labs 1–3 use one Development Team with these role boundaries:

| Role | Responsibility | Tool boundary |
| --- | --- | --- |
| Engineering Manager | Delegates and reviews the assigned work. | Approval tool; no writing or testing tool. |
| Coder | Proposes the assigned implementation. | Writing tool; no approval or testing tool. |
| QA Auditor | Returns a separate test report. | Testing tool; no writing or approval tool. |

In Lab 2, `team_log` supplies Architect rules to `architect_task`, and the learner makes that task available through `coder_task.context`. Context makes information available; it does not force a real model to follow it. The task graph declares `output_pydantic=CodePatch` and a Coder-to-QA dependency. The required demonstration validates a local Coder fixture, and the grader checks the two configuration repairs. No CrewAI tasks are executed.

The Capstone adds a Security & Compliance Team. Local adapters emit `DevDeliverable`, validate it before Security consumes it, and return `SecurityAuditResult`. The notebook records an approval flag and evidence; it does not deploy or release code. Its separate CrewAI configuration has three Development agents and two Security agents. The Development Coder/QA currently have no custom tools; the Security scanner/approval tools repeat Lab 2's reusable-tool pattern. See [the cell map](COURSE_MAP.md#control-and-cell-map) for the implementation locations.

Tool lists limit which custom tools the framework exposes; they do not provide OS isolation. The Lab 2 tools are placeholders, the Lab 3 lookup is a dry run, and the Capstone scanner checks only fixed teaching markers. A typed result establishes representation and declared constraints, not semantic correctness or verified security.

### Pre-written Capstone helper: Cost-Aware Dynamic Routing

The Capstone shows a policy routing low- and medium-complexity work to a Fast target and high-complexity work to an Expert target. These are `RoutingTarget` records, not additional CrewAI Agents or live models. The deterministic example uses illustrative per-task costs to compare routes. Learners read the function and route trace; the helper has no implementation task or grade. The optional CrewAI Manager exposes the same policy through a tool wrapper.

The router demonstrates relative savings; routing alone is not a spend limit. Lab 3 makes the bound concrete: at most three retries after the initial attempt means at most four calls per task, then the workflow stops and escalates. With the mock's `$0.05` per-call fixture, that is at most `$0.20` per task. A provider-backed system should also enforce an explicit per-task or cumulative spend ceiling before issuing a call.

### NIST control alignment

These exercises illustrate selected controls; completing them does not certify a system as compliant. Lab 2's Manager tool allowlist and separate Coder/QA duties map conceptually to **AC-6 Least Privilege** and **AC-5 Separation of Duties**. Lab 3's input syntax and range checks map to **SI-10 Information Input Validation**. See [NIST SP 800-53 Rev. 5, current update](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) and the [NIST control assessment index](https://csrc.nist.gov/projects/risk-management/about-rmf/assess-step/assessment-cases-download-page).

### CISA secure-AI guidance alignment

The same labs give learners small, repeatable examples of CISA's secure-by-design direction: set role and tool boundaries before execution (Lab 2), validate inputs and cap repair attempts (Lab 3), and pass typed, reviewable evidence into the Security Team (Capstone). These are classroom examples, not a CISA assessment or a compliance claim. See CISA's [Guidelines for Secure AI System Development announcement](https://www.cisa.gov/news-events/alerts/2023/11/26/cisa-and-uk-ncsc-unveil-joint-guidelines-secure-ai-system-development) and the [joint lifecycle guidance](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development), which covers secure design, development, deployment, and operation.

```text
Human request
     |
     v
Development Team: Manager -> Coder -> QA
     |
     | DevDeliverable (Pydantic contract)
     v
Security Team: Pen Tester -> Security Manager
     |
     | SecurityAuditResult
     v
Typed audit outcome and evidence for the ADR
```

## Working with the scaffold

- Complete only the marked TODOs or deliberate bugs. The surrounding imports, fixtures, and graders are provided.
- After each edit, rerun the dependent cells in order. Move to the next lab once the grader reaches `15/15`, the evidence is understood, and the supplied management decision note is complete.
- If your environment prevents Capstone execution, submit a one-page Paper ADR covering the inter-team schema, role tools, and remaining risk/evidence/next step. The [Capstone brief](assignments/ex5_capstone_virtual_software_company.md) provides the questions and rubric. Sound reasoning meets the Capstone pass condition; marks still follow the stated rubric.

## Two-Day Schedule

The [workshop syllabus](assignments/assignment_syllabus.md) groups nine competency topics into the sessions below. One main 21-slide presentation supports the entire route. Procurement and HR/RAG are formative walkthroughs, not additional graded implementations. The practical sequence remains one preflight, three labs, and one software Capstone.

### Day 1 — MAS foundations, contracts, and team context

| Time | Session | Activity and completion evidence |
| --- | --- | --- |
| 09:00–10:30 | Starting small, MAS foundations, and use cases · slides 1–8 | Define a first task and when it needs a helper; classify MAS interaction types; trace [procurement and HR/RAG](assignments/workshop_simulations.md), identify coordination risks, then run the [preflight](notebooks/00_sandbox_preflight.ipynb). |
| 10:45–12:00 | Lab 1: Context Engineering — Working Brief and Typed Contracts · slides 9–10 | Prepare a short context packet; connect it to typed constraints; repair the weak Pydantic schema and reach `✅ SUCCESS: 15/15`. |
| 13:00–14:00 | Roles, context, and framework literacy · slides 11–12, 17 | Compare general, computer-use, video, and cloud coding helper designs with Manager–Coder–QA responsibilities; inspect context dependencies; compare CrewAI, LangGraph, AutoGen, and Microsoft Agent Framework using the [framework reference](resources/framework_comparison.md). |
| 14:15–16:30 | Lab 2: Multi-Agent Management — Code Auditing and Team Oversight · slides 11–12 | Repair tools/context, inspect the supplied Manager audit and local QA inbox, record the decision, and reach 15/15. |

### Day 2 — Security, bounded repair, and team-to-team delivery

| Time | Session | Activity and completion evidence |
| --- | --- | --- |
| 09:00–10:30 | Capability choice, tool design, and debugging · slides 13–17, 19 | Choose an adequate capability, identify a human pairing point, and discuss stable tools, state receipts, and useful errors; select role-specific evidence using the [academic resources](resources/curated_resource_library.md); diagnose a failure from the supplied workflow trace. |
| 10:45–12:00 | Lab 3: Manager Oversight — Code Validation and Bounded Repair · slides 14–16 | Repair the gate/retry limit, inspect the Manager oversight evidence, record escalation, and reach `✅ SUCCESS: 15/15`. |
| 13:00–14:30 | Capstone build · slides 13, 18 | Validate `DevDeliverable` before the Coordinator starts the local Security adapter; inspect the audit result. |
| 14:45–15:45 | Defense and Paper ADR option · slides 18–19 | Present the inter-team contract, observed check results, and ADR, or submit a sound Paper ADR fallback. |
| 15:45–16:00 | Framework ecosystem and takeaways · slides 20–21 | Review broader framework choices as ungraded literacy; connect the five [agent-building takeaways](assignments/agent_building_design_guide.md#takeaways-and-evidence) to observed evidence and a next decision. |
| 16:00–16:15 · optional | Live LLM bonus · end of Day 2 | Instructor opens only [bonus_live_demo.ipynb](extensions/bonus_live_demo.ipynb), after required work and defenses. A separately configured provider/key and connectivity are needed only for this ungraded demo. |

Keep provider calls out of the core labs and Capstone. Skip the bonus when connectivity, credentials, or time are unavailable; required submissions and marks are complete before it begins.

## Assessment and Gradebook

There are three auto-graded labs. Each notebook grader reports `/15`; the tracker scales each score proportionally to `/20`. The Capstone adds 20 code marks and 20 ADR marks. Total: 100.

| Component | Course marks | Evidence |
| --- | ---: | --- |
| Lab 1 · Context Engineering: Typed Contracts | 20 | Schema blocks invalid mock data and accepts valid data. |
| Lab 2 · Multi-Agent Management: Code Auditing and Team Oversight | 20 | Grader checks Manager tool separation/delegation and Architect task context; inspect the deterministic typed Coder fixture separately. |
| Lab 3 · Manager Oversight: Code Validation and Bounded Repair | 20 | SQL-like input is rejected; retry loop ends after 3 retries and records escalation. |
| Capstone code | 20 | Failed QA is rejected, Coordinator gate precedes the local Security adapter, Security tools are separated, and a typed audit result is recorded. |
| Capstone ADR and defense | 20 | Risk and architecture (6), governance and proof (7), production next step (7). |
| **Total** | **100** | |

The lab conversion is `raw_score × 20 ÷ 15`. Keep the raw `/15` result for the Stop-at-Green signal; use the converted `/20` value in the gradebook.

Framework literacy is reference-only in [Lecture 8](assignments/assignment_08_debugging_sdlc.md#lecture-8-reference-discussion-choosing-an-orchestration-pattern). CrewAI makes roles and task dependencies visible here. The [optional LangGraph architecture extension](resources/framework_comparison.md#optional-capstone-architecture-extension-langgraph) explores state/recovery needs; LlamaIndex provides a retrieval comparison. No new package, implementation task, or marks are required.

### Capstone three-question ADR

1. What Pydantic schema governs the Development-Team-to-Security-Team handoff? Write the essential pseudo-code.
2. Which tools can each role use, and how do the boundaries enforce separation of duties?
3. What is the largest remaining risk, what test or audit evidence would show the controls worked, and what would you add before production?

The 20-point rubric awards 6 marks for risk and architecture, 7 for mapping governance to evidence, and 7 for a credible production next step. A sound Paper ADR is an accepted Capstone pass route when execution is blocked by the learner's environment.

### Repository verification

This is an **optional maintainer check in the full repository**, not an extra learner assignment. The compact learner ZIP does not include the repository test suite. Learners use the graders in their notebooks.

Maintainers install the verification environment described in [DEVELOPMENT.md](DEVELOPMENT.md), then run:

```bash
python tools/check_readiness.py
```

Retain the command, environment, and actual result in the delivery record. A fixed historical test count is not the pass condition.

## Submission checklist

- Three completed lab notebooks with the raw `/15` grader results and the supplied Lab 2/3 management decision notes.
- Capstone notebook with the contract, Coordinator gate, scoped Security tools, audit result, and `/20` code result, or the agreed Paper ADR route.
- One-page ADR answering risk, controls/evidence, and next step.
- Any supporting pytest log with its actual result and environment.

## Academic Grounding

The research provides theory and discussion context. See [Theory of Mind for Multi-Agent Collaboration via Large Language Models](https://aclanthology.org/2023.emnlp-main.13/) and [TEAMLOG in Action: A Case Study in Teamwork](https://www.comsis.org/pdf.php?id=244-0912) for role knowledge and shared commitments. See [TRINITY](https://arxiv.org/abs/2512.04695), [Conductor](https://arxiv.org/abs/2512.04388), [ChatDev](https://aclanthology.org/2024.acl-long.810/), and [Reflexion](https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html) to frame coordination, verification, and feedback. Cost-aware dynamic routing is a local policy with illustrative costs, not a learned orchestration system.

## Completion

For each activity, identify the risk, the responsible role or team, the observed evidence, and the next decision. Keep provider-backed exploration separate from the required deterministic submission.

[Course home](README.md) · [Learner paths](README.md#learner-paths) · [Slide index](README.md#main-deck-slide-index)
