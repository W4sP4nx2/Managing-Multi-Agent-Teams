# Assignments and Practice

Use the [master course hub](README.md) for the seven-notebook route: preflight, three governance labs, Capstone, deterministic Software Factory, and local CI/CD. Required execution uses local fixtures, needs no API key, and has actual API cost **$0.00**.

The assessed work remains **100 marks**: each lab's raw /15 scales to /20, Capstone code is /20, and ADR/defense is /20. Factory and CI/CD evidence supports the Capstone defense without a separate score. The formative briefs and optional design exercises below add no course marks. Use the [submission checklist](README.md#submission-checklist); private marking guidance is in the [instructor playbook](INSTRUCTOR_PLAYBOOK.md).

<a id="assignment-index"></a>
## Contents

- [Assignment 01: Strategic Prompt Engineering](#assignment-01-strategic-prompt-engineering)
- [Assignment 02: AI Workspace and Role-Aware Context](#assignment-02-ai-workspace-and-role-context)
- [Assignment 03: Context Engineering — Typed Contracts](#assignment-03-architectural-supervision)
- [Assignment 04: Multi-Agent Management — Code Auditing and Team Oversight](#assignment-04-code-auditing)
- [Assignment 06: Manager Oversight — Code Validation and Bounded Repair](#assignment-06-code-validation)
- [Assignment 07: Context Engineering and Access Lists](#assignment-07-context-engineering-access-lists)
- [Assignment 08: Debugging in the Agentic Age & SDLC Operations](#assignment-08-debugging-sdlc)
- [Capstone: a governed travel-site factory](#ex5-capstone-virtual-software-company)
- [Multi-Agent Systems in Context: Two course Simulations](#workshop-simulations)
- [Assignment 00A: Multi-Agent Systems Foundations](#multi-agent-systems-foundations)
- [Foundational Exercise: Design A Governed Agent Roster](#foundational-architecture-design)
- [Supplemental Governance Practice Exercises](#basic-agent-governance-labs)
- [Assignment 09: Framework Comparison](#assignment-09-framework-comparison)
- [CrewAI orchestration: advanced reference](#module14-crewai-orchestration-patterns)

---

<a id="assignment-01-strategic-prompt-engineering"></a>
## Assignment 01: Strategic Prompt Engineering

**Maps to:** Lecture 1 — Vibe Coding and spec-driven work · **Type:** Formative, pass/fail

<a id="assignment-01-strategic-prompt-engineering-objective"></a>
### Objective

Turn a vague request into a specification another person, test, or agent can check.

<a id="assignment-01-strategic-prompt-engineering-task"></a>
### Task

Rewrite **“Make a login page”** as a structured technical specification. Include explicit file paths, required functions, input and output types, acceptance criteria, constraints, and forbidden actions (for example, do not store tokens in browser local storage).

<a id="assignment-01-strategic-prompt-engineering-submit"></a>
### Submit

- The structured technical specification.

<a id="assignment-01-strategic-prompt-engineering-passfail"></a>
### Pass/fail

- **Pass:** The specification contains concrete paths, typed inputs/outputs, constraints, forbidden actions, and testable acceptance criteria.
- **Revise:** A requirement relies on vague instructions such as “make it good.”

No paid tool, API key, live model call, or repository code change is required.

---

<a id="assignment-02-ai-workspace-and-role-context"></a>
## Assignment 02: AI Workspace and Role-Aware Context

**Maps to:** Lecture 2 — AI workspace and Theory of Mind as role-aware context · **Type:** Formative, pass/fail

<a id="assignment-02-ai-workspace-and-role-context-objective"></a>
### Objective

Describe a safe local learning workspace and explain what information the next role needs to do its part.

<a id="assignment-02-ai-workspace-and-role-context-task"></a>
### Task

1. Write a short workspace note with the repository root, Python 3.12 environment activation, and JupyterLab launch command. State that `.env` is ignored by Git. Do not include API keys, credentials, or screenshots containing secrets.
2. Write one handoff note for the course team: name a rule the Architect records, identify whether the Coder, QA, or both need it, and state what evidence the next role should return.

<a id="assignment-02-ai-workspace-and-role-context-submit"></a>
### Submit

- The safe workspace note.
- The role-aware handoff note.

<a id="assignment-02-ai-workspace-and-role-context-passfail"></a>
### Pass/fail

- **Pass:** The setup note identifies the local environment and JupyterLab without exposing secrets; the handoff names a concrete rule, the role that needs it, and checkable evidence.
- **Revise:** Setup steps are missing, secrets are included, or the handoff is too vague to verify.

This is a short paper/Markdown exercise. It requires no provider account, API key, live model call, or code changes.

---

<a id="assignment-03-architectural-supervision"></a>
## Assignment 03: Context Engineering — Typed Contracts


**Maps to:** Lecture 3 — Intent-Based vs. Spec-Driven Work · **Core activity:** Lab 1, Pydantic Contract · **Type:** Auto-graded lab


<a id="assignment-03-architectural-supervision-objective"></a>
### Objective

Turn a business requirement into a typed contract that rejects malformed agent output before another task consumes it.

<a id="assignment-03-architectural-supervision-architecture-and-flow"></a>
### Architecture and flow

![Lab 1 contract boundary: observe the weak schema accepting a malformed local fixture, then repair a strict schema that accepts valid probes and rejects invalid ones.](resources/diagrams/lab1-contract-flow.svg)

**Text version:** manager defines acceptance criteria → fixed, untrusted local fixture → weak schema accepts an invalid score and discards an extra field → learner repairs the strict contract → grader checks accepted and rejected probes → **15/15** evidence.

The manager, Coder, and QA describe the intended team handoff. This lab executes Pydantic validation in one local Python process. The contract checks payload structure and declared constraints; claim accuracy and deployment readiness require separate evidence.

<a id="assignment-03-architectural-supervision-task"></a>
### Task

In [`01_lab_pydantic.ipynb`](notebooks/01_lab_pydantic.ipynb), replace the weak starter with `StrictResearchOutput`. Require `topic: str`, `confidence_score: float`, and `findings: list[str]`; constrain the score to `0.0 <= confidence_score <= 1.0`; and forbid undeclared fields such as `secret_backdoor`.

Use Pydantic v2 `Field` constraints and `ConfigDict(extra="forbid")`. Keep the deterministic fixture unchanged so the same bad payload is tested before and after the gate is repaired.

<a id="assignment-03-architectural-supervision-passfail"></a>
### Pass/fail

- **Pass:** Valid data is accepted; the fixture with `confidence_score=150.5` and the extra `secret_backdoor` field are rejected; the notebook grader reports **15/15**.
- **Revise:** The model accepts either defect, rejects valid data, or is not a Pydantic model.

The fixture is local and deterministic; a provider call is not part of this assignment.

After **15/15**, continue to [Lab 2: CrewAI hierarchy](notebooks/02_lab_crewai.ipynb) and [Assignment 04](#assignment-04-code-auditing). The [factory simulation guide](extensions/live_software_factory.md) explains the later local release workflow.

---

<a id="assignment-04-code-auditing"></a>
## Assignment 04: Multi-Agent Management — Code Auditing and Team Oversight


**Maps to:** Lecture 5 — Managing Teams, Team Memory, and Code Auditing · **Core activity:** Lab 2, CrewAI Contract Handoff · **Type:** Auto-graded lab

<a id="assignment-04-code-auditing-objective"></a>
### Objective

Act as delivery manager for the Manager–Coder–QA team: audit role boundaries and context, then decide whether the typed proposal may enter QA review.

<a id="assignment-04-code-auditing-team-map"></a>
### Team map

![Lab 2 roles and local audit path, with separate configured relationships and simulated handoff.](resources/diagrams/lab2-team-audit.svg)

You are the **human delivery manager**. The Engineering Manager coordinates; the Coder alone writes; QA owns independent read/verify work. The Architect task is a rule-carrying artifact, not another agent. Dashed arrows show the configured task/role relationships. The solid path is a local fixture → role/context and strict `CodePatch` gate → simulated QA inbox. A rejected proposal returns for repair and leaves that inbox empty. The configured QA task is not executed, and its supplied tool returns sample evidence rather than running tests.


<a id="assignment-04-code-auditing-skill-transparency--least-privilege"></a>
### Skill Transparency & Least Privilege

Between the agent definitions and task configuration, run the supplied **Skill Transparency Matrix**. It reads each agent's actual custom tools, compares them with the role allowlist, and displays each tool's Action, Input, Output, and Warning metadata. The starter Manager's write permission must appear as excessive; the Coder and QA keep separate responsibilities.

After the first repair, rerun agents → matrix → tasks → fixture → audit → grader. Explain why visible tool documentation supports management judgment but does not grant OS isolation, prove model understanding, or execute a tool. The matrix observes configuration and adds no marks.

<a id="assignment-04-code-auditing-task"></a>
### Task

In [`02_lab_crewai.ipynb`](notebooks/02_lab_crewai.ipynb), repair the two marked broken settings:

1. Remove `write_code_tool` from the Manager while retaining its approval and delegation responsibilities.
2. Set the Coder task context to `context=[architect_task]` to declare the Architect-rule dependency. The deterministic Coder fixture inspects this dependency and returns a string ID when it is present.

Keep the supplied Coder and QA contracts typed with `output_pydantic`, and retain `qa_task.context=[coder_task]`. These declare the task graph; the required path constructs the Crew without executing its tasks. The local tools are placeholders and do not write files or run commands. Context availability does not guarantee that a real model follows the rules.

Follow this order in the notebook:

1. **Run** the configuration, deterministic Coder fixture, and Manager's Audit Gate before editing.
2. **Inspect** every failed check and the empty `qa_inbox`; trace the missing rule on the team map.
3. **Edit** only the two marked agent and task configuration settings above.
4. **Rerun** agents → skill matrix → tasks → fixture → audit, record the decision, then run the unchanged auto-grader and Blind Agent debug.
5. **Submit** the notebook and evidence described below. No live model, real test, git operation, or deployment is required.

<a id="assignment-04-code-auditing-managers-audit-action"></a>
### Manager's Audit Action

Run the supplied `lab2-manager-audit-gate` cell after the fixture. Inspect all role tool lists, task owners/context, output models, and the current payload. A failed audit leaves `qa_inbox` empty; `PASS_TO_QA` admits one validated proposal. Record the decision, one observed check, and the next owner in the supplied Markdown sentence. This local inbox is not an executed QA task or release approval. The action is formative and adds no new code TODO or marks.

<a id="assignment-04-code-auditing-passfail"></a>
### Pass/fail

- **Pass:** The Manager has approval and delegation but lacks the code-writing tool, the Coder task lists the Architect task as context, the deterministic fixture validates as `CodePatch`, the Manager audit records `PASS_TO_QA`, the decision note cites evidence, and the unchanged grader reports **15/15**.
- **Revise:** The Manager can write code, the Coder lacks the Architect context, or the typed handoff fails.

The grader scores the Manager configuration and the Architect-task context dependency. It does not execute or score a TeamLog read, a QA task, or a live Crew run; inspect the typed-fixture cell separately. See [the course map](COURSE_MAP.md#what-the-graders-actually-check) for exact cell IDs and grader coverage. Do not call a live model as part of this assignment.

<a id="assignment-04-code-auditing-submit"></a>
### Submit

Retain the completed Lab 2 notebook with its two repairs, the current fixture/audit output, the unchanged grader result, and the supplied decision sentence naming one observed check and the next owner. Follow your instructor's existing submission channel. `PASS_TO_QA` authorizes admission to this simulated inbox; it supplies no test result or production release approval.

<a id="assignment-04-code-auditing-factory-simulation-mapping"></a>
### Factory simulation mapping

The [factory simulation guide](extensions/live_software_factory.md) extends the same role boundaries: the Coder fixture writes a local candidate; separate Security, UI/UX, and QA checks inspect that artifact; local CI/CD records actual results. The Engineering Manager coordinates those results, and the human approves the simulated budget and local publication steps. Keep review decisions, test evidence, and approvals tied to the exact commit revision; a changed revision needs renewed evidence. A commit trailer or this local audit result alone does not establish independent review or publication authorization. This mapping is ungraded and adds no live execution to Assignment 04.

---

<a id="assignment-06-code-validation"></a>
## Assignment 06: Manager Oversight — Code Validation and Bounded Repair


**Maps to:** Lecture 6 — Safety Nets, Tool Validation, and Evals · **Core activity:** Lab 3, Security and Bounded Repair · **Type:** Auto-graded lab

<a id="assignment-06-code-validation-objective"></a>
### Objective

Act as delivery manager: set tool/retry policies, inspect QA and worker evidence, and escalate a failed task within its budget.

<a id="assignment-06-code-validation-task"></a>
### Task

In [`03_lab_security.ipynb`](notebooks/03_lab_security.ipynb):

1. Complete `SecureToolInput` so malicious SQL-like input (including the supplied `DROP TABLE` payload) raises a Pydantic `ValidationError` before the dry-run tool is called, while a numeric user ID such as `"123"` is accepted.
2. Set `MAX_RETRIES = 3`. Confirm the loop makes at most four calls total (one initial attempt plus three retries) and escalates when all attempts fail.

This notebook uses a local dry-run function; it does not connect to a database or implement a complete SQL-injection defense.

<a id="assignment-06-code-validation-management-oversight-action"></a>
### Management Oversight Action

Run the supplied `lab3-management-oversight` cell. Review hostile-input rejection, safe-input acceptance, absence of the unsafe value from `tool_call_log`, four mock calls, $0.20 simulated spend, and the escalation flag. In the corrected always-failing scenario, record `ESCALATE_TO_HUMAN` with that evidence and a human reviewer as next owner. If a control fails, record `BLOCK_AND_REPAIR_CONTROLS` and repair it. The action makes no extra call, release, or human notification. It is formative with no new code TODO or marks.

<a id="assignment-06-code-validation-passfail"></a>
### Pass/fail

- **Pass:** Unsafe input is rejected, the safe input passes, escalation follows three retries, simulated cost stops with the loop, the oversight and decision note record escalation, and the unchanged grader reports **15/15**.
- **Revise:** Any unsafe value reaches the tool, a safe ID is rejected, or the retry loop exceeds its bound.

No live model or external service is required.

---

<a id="assignment-07-context-engineering-access-lists"></a>
## Assignment 07: Context Engineering and Access Lists

**Maps to:** Lecture 7 — Context Engineering and Access List Routing · **Type:** Formative, pass/fail

<a id="assignment-07-context-engineering-access-lists-objective"></a>
### Objective

Choose which prior artifacts each role may read, preserving useful evidence while excluding irrelevant or sensitive history.

<a id="assignment-07-context-engineering-access-lists-the-obsidian-vault-analogy"></a>
### The Obsidian Vault analogy

Think of an **Obsidian Vault** as a folder of linked Markdown notes: project rules, approved requirements, decisions, and examples. A colleague can work in your preferred style by reading the relevant notes before starting. You do not retrain that colleague for every project; you supply the working context.

Context injection gives an agent the same kind of project-specific customization. Select the authorized notes for the current role and inject them into its task context. This can produce the *fine-tuned customization* learners want **without model training or changing model weights**. It is context engineering, not technical fine-tuning: behavior still depends on the supplied context, and irrelevant or stale notes can make it worse.

In [Lab 2](notebooks/02_lab_crewai.ipynb), `team_log` is our tiny vault of approved rules and `architect_task` carries the selected brief. Setting `coder_task.context=[architect_task]` makes that brief available to the Coder. The notebook uses local Python data and does not install or connect to Obsidian. The deterministic fixture demonstrates the context dependency; it does not prove that a live model will follow every note. Use the access lists below to decide which notes each role should receive.

<a id="assignment-07-context-engineering-access-lists-task"></a>
### Task

Use this task-artifact list:

| Artifact | Contents |
| --- | --- |
| `architect_spec` | Contract and acceptance rules for the task. |
| `approved_requirements` | Requirements confirmed by the Manager. |
| `coder_patch` | The Coder's proposed code change. |
| `acceptance_tests` | Checks QA must run against the contract. |
| `provider_secret` | A private API credential unrelated to the task. |
| `old_unrelated_log` | A previous task's stale output. |

Write a small access list for the **Coder** and **QA**. Choose the artifacts each role needs, then give one sentence explaining each role's view. Identify one artifact that must be excluded and explain why.

<a id="assignment-07-context-engineering-access-lists-submit"></a>
### Submit

- One role-specific access list for the Coder and one for QA.
- A brief reason for one inclusion and one exclusion.

<a id="assignment-07-context-engineering-access-lists-passfail"></a>
### Pass/fail

- **Pass:** The Coder receives the specification and approved requirements; QA receives the patch and acceptance tests; secrets and stale unrelated output are excluded; the choices are explained.
- **Revise:** Either role lacks evidence needed for its task, or sensitive/unrelated data is included without justification.

This is a local reasoning exercise. It uses no Fugu service, external API, provider account, or live model call.

---

<a id="assignment-08-debugging-sdlc"></a>
## Assignment 08: Debugging in the Agentic Age & SDLC Operations

**Maps to:** Lecture 8 — Debugging and AI-First SDLC · **Type:** Formative, pass/fail

<a id="assignment-08-debugging-sdlc-objective"></a>
### Objective

Use observable workflow evidence to find a failure point and explain which control should stop it.

<a id="assignment-08-debugging-sdlc-task"></a>
### Task

1. In a local copy of the Capstone notebook, set both `dev_crew` and `security_crew` to `verbose=True` and identify the lines that enable execution logging. Keep `USE_LIVE_LLM = False`; do not call `Crew.kickoff()` for this assignment.
2. Analyze the deterministic scenario trace below. Identify a verification or permission failure, cite the line that proves it, and state one corrective action and the control that should block the failure.

```text
[Architect] TeamLog rule: user_id must be a string
[Coordinator] Coder task context: [] (architect_task missing)
[Coder] deterministic payload: {"user_id": 101, "operation": "create"}
[Pydantic] CodePatch rejected: user_id must be a strict string
[Coordinator] DevDeliverable validated; unit_tests_passed=True
[Security Manager] tools: approve_audit_tool, mock_pen_test_tool
[Pen Tester] tools: mock_pen_test_tool
[Pen Tester] finding: SQL injection marker detected
[Security Manager] decision: approved
[Local policy check] rejected: manager must not have mock_pen_test_tool
```

This is a **teaching fixture**, not a live CrewAI transcript. Verbose logs can show task execution and tool activity; they do not reveal an agent’s private chain-of-thought. The required classroom path makes no provider call.

<a id="assignment-08-debugging-sdlc-submit"></a>
### Submit

- The `verbose=True` configuration excerpt.
- A short note naming the risk, citing trace evidence, and explaining the permission or typed-result check that should block it.

<a id="assignment-08-debugging-sdlc-passfail"></a>
### Pass/fail

- **Pass:** The learner identifies a concrete risk in the trace (excess scanner permission or approval contradicting the finding), cites evidence, and names a relevant verification or tool-permission control.
- **Revise:** The explanation is unsupported by the trace or claims that verbose mode exposes private reasoning.

<a id="assignment-08-debugging-sdlc-lecture-8-reference-discussion-choosing-an-orchestration-pattern"></a>
### Lecture 8 reference discussion: choosing an orchestration pattern

For an executable, ungraded follow-up to Lab 2, open the [Manager–Coder–QA advanced reference](crewai_learning/01_Bridge_Sequential_Crew.ipynb). It runs real CrewAI tasks with local fixture LLMs and external networking blocked. Observe strict-output rejection and exactly three tool failures followed by a typed escalation. Its Python wrapper owns recovery; the required classroom notebooks retain their existing no-kickoff boundary. Use [Assignment 09](#assignment-09-framework-comparison) to discuss the framework/application split. This adds no submission or marks.

**Ungraded slide/reference discussion.** This section adds no submission or pass/fail criterion. Read the [framework comparison](README.md#why-crewai) alongside the presentation:

- **CrewAI:** The course uses visible Manager/Coder/QA roles, task context, and exposed tool lists to make separation of duties easy to inspect. The required demonstration uses deterministic fixtures rather than live team execution.
- **LangGraph:** Consider a future Capstone refactor when explicit state transitions, persistence, or recovery decisions become more complex. The [optional architecture design](README.md#langgraph-architecture-reading) illustrates this possibility; no refactor is assigned.
- **AutoGen:** Compare conversational coordination as a conversation-pattern reference. The official project now directs new users to Microsoft Agent Framework; current support matters in a production choice.
- **Microsoft Agent Framework:** Compare Python/.NET agent and explicit workflow coordination with the Capstone's team boundary. This remains reference reading, with no new package or coding requirement.
- **LlamaIndex:** Compare retrieval tools and document-oriented workflows using the HR/RAG simulation as context. It adds no retrieval implementation to this assignment.

Discussion focus: explain which orchestration need would change your framework choice, and which validation or authorization checks you would retain. The existing trace-analysis submission and assessment above remain the same.

---

<a id="ex5-capstone-virtual-software-company"></a>
## Capstone: a governed travel-site factory


<a id="ex5-capstone-virtual-software-company-product-brief"></a>
### Bounded product brief

Use the supplied static travel page as one bounded candidate artifact. Its navigation, hero/CTA, destination cards, and contact label are fixed fixtures for review. Do not add a booking backend, account system, or domain research. The learning task is to govern the candidate's handoff, checks, evidence, and local publication. The page must not collect passwords, store credentials in browser storage, or contact an unapproved endpoint.

The factory shows simulated Engineering Manager, Coder, Security, UI/UX, and QA collaboration using pre-generated outputs. It makes no API calls and costs $0.00 in actual API charges. Model names are illustrative labels; no language model or reasoning model runs. Delays represent presentation pacing. The curriculum focuses on orchestration, security, and bounded autonomy rather than domain-specific features or prompt quality.

<a id="ex5-capstone-virtual-software-company-contract-and-team-boundary"></a>
### Contract and team boundary

First complete [notebook 04](notebooks/04_capstone.ipynb):

1. Reject `DevDeliverable.unit_tests_passed=False` with a Pydantic validator.
2. Revalidate the Development deliverable before the Python Coordinator starts Security.
3. Keep the scanner with the Pen Tester and approval tool with the Security Manager.
4. Inspect `SecurityAuditResult`, validation order, and code grader.
5. Run the supplied typed API, task-scoped memory, duplicate/stale evidence, and bounded-repair probes. Predict each outcome before reading its assertion.
6. Use the interaction map and proof evidence in your existing three-answer ADR.

The foundation notebook uses local Python adapters and separately constructs CrewAI configurations. It does not execute both Crews. Its API is an in-process Python function, and its shared memory is a request/hash-scoped dictionary reset for each proof run. A typed QA-status claim is not independent proof that tests passed. The [framework bridge](crewai_learning/01_Bridge_Sequential_Crew.ipynb) separately executes real CrewAI tasks with fixed local responses; it needs no provider or extra package.

### Governance evidence to carry into the ADR

| Requirement | Read/run/inspect | Evidence and practical limit |
| --- | --- | --- |
| Interaction-pattern map | Notebook 04's Human → Development → Coordinator → Security map | Identify owners, decision authority, and a centralized/hybrid tradeoff; no decentralized or parallel execution is claimed. |
| Governed tools and typed contracts | Repair role tool lists, `DevDeliverable`, and the Coordinator gate | Scanner/approval separation, failed-QA rejection, typed `SecurityAuditResult`; role text alone grants no permission. |
| Shared memory | Inspect `review_memory` and duplicate/request-scope probes | Matching request/hash reuses evidence; a different request stays separate. This is a local dictionary, not persistent CrewAI memory or RAG. |
| Repair loops and API boundary | Run `ReviewRequest` → `submit_security_review` → `ReviewReceipt` and the two-attempt wrapper | Malformed/stale submissions are rejected, one repair can succeed, and exhaustion escalates locally. No HTTP server or human notification runs. |
| Malfunction, coordination complexity, unpredictable behavior | Run the three named governance proof cases | Unexpected adapter errors propagate; duplicates do not rescan; malformed/stale fixture outputs cannot bypass the declared checks. These are deterministic probes, not measured model variability or distributed-load tests. |
| CrewAI comparison | Read/run the bridge's Crew creation, kickoff, Markdown result, and exception proofs | Compare real task execution with the Python Coordinator and identify which validation/retry policy belongs to the application. |
| Revision-bound release evidence | Inspect notebooks 05–06 and the factory ERD | SQLite rows, checks, approvals, current hash/revision, and local publication receipt; no hosted deployment. |

These supplied proofs support the existing ADR/defense. They add no code TODO, package, separate submission, or marks. A framework may recover from a handled tool error while propagating an unhandled error; describe the policy actually observed instead of assuming that execution always continues.

<a id="ex5-capstone-virtual-software-company-factory-and-local-release-tasks"></a>
### Factory and local release tasks

Continue into notebooks 05 and 06 using the same travel-site request. Run:

```bash
python orchestrator.py --check-only
python orchestrator.py --security-demo
python live_simulation_orchestrator.py
```

Inspect the pre-generated candidate before approving plan/spend, code build, Security, UI/UX, QA, and final local publication. The default simulated plan is $0.50 including the $0.05 publication step. Actual API cost stays $0.00. Reject the malicious request that stores passwords in `localStorage` and sends them over HTTP to an external endpoint.

Retain evidence for the exact candidate revision: generated source, security findings, bounded UI/QA checks, test-case results, simulated ledger, gate decisions, and Git commit. After explicit final publication approval, `open index.html` displays the run's published local file. The checked-in preview is available before that and has no release receipt. The factory creates no hosted deployment or booking backend.

<a id="ex5-capstone-virtual-software-company-entity-relationship-diagram"></a>
### Entity relationship diagram

Open the [editable ERD source](resources/diagrams/capstone_factory_erd.md) or [diagram image](resources/diagrams/capstone_factory_erd.svg). Use it to trace:

| Record | Relationship and purpose |
| --- | --- |
| Factory run | Owns the request hash, mode, branch, status, and configuration |
| Artifact | Belongs to a run and records source path, digest, and Git revision |
| Stage approval | Binds a human/fixture actor decision to a stage and subject digest |
| Review and QA case | Refer to the artifact actually checked, including failures and test evidence |
| Local publication | Refers to the approved artifact and final decision, with published path/digest |
| Factory event | Records the workflow stage and selected synthetic evidence |
| Simulated budget ledger | Checks the teaching allowance before work and records approved stages that ran, with no provider bill |

Explain why a changed artifact invalidates earlier review/approval evidence. Distinguish actual SQLite foreign keys from the logical `run_id` association across the separate evidence and simulated-cost databases. The static destinations are HTML elements rather than database entities.

<a id="ex5-capstone-virtual-software-company-assessment-40-points"></a>
### Assessment: 40 points

<a id="ex5-capstone-virtual-software-company-capstone-code-20-points"></a>
#### Capstone code: 20 points

| Criterion | Points | Evidence |
| --- | ---: | --- |
| Separation of duties | 5 | Security Manager approval only, Pen Tester scan access |
| Contract and Coordinator handoff | 10 | Failed QA rejected, validation precedes Security start |
| Typed audit output | 5 | Pipeline returns `SecurityAuditResult` |

The notebook auto-grader displays the code score. Factory/CI/CD evidence supports the defense and adds no separate score.

<a id="ex5-capstone-virtual-software-company-architecture-decision-record-20-points"></a>
#### Architecture Decision Record: 20 points

1. **Risk and interaction map:** which handoff/publication risk matters most? Name owners and decision authority on the arrows, explain the centralized Coordinator, and compare an independent, decentralized, or hybrid alternative.
2. **Governance and proof:** connect typed contracts, governed tools, task-scoped shared memory, repair loops, the API boundary, and revision evidence to observed outcomes. Cite the malfunction, coordination, and malformed/stale output probes. Compare the Python Coordinator with the CrewAI bridge.
3. **Next step:** identify one remaining boundary, memory, exception, or evidence weakness. Propose a control and a test that would justify using it in a real organization.

| Criterion | Points | Full-credit condition |
| --- | ---: | --- |
| Risk and architecture | 6 | Concrete governance risk, interaction/authority map, and reasoned architecture choice |
| Governance mapping | 7 | Connects the named controls and CrewAI comparison to observed proofs and revision evidence |
| Next-step judgment | 7 | Credible improvement with a reason, remaining uncertainty, and a test to evaluate it |

When the learner's environment prevents execution, a sound one-page Paper ADR is an accepted fallback. Include schema pseudo-code, role tools, ERD relationships, and remaining risk/evidence/next step. The same /20 ADR rubric applies. A paper submission must not invent execution, API usage, security completeness, WCAG conformance, or deployment results.

<a id="ex5-capstone-virtual-software-company-optional-architecture-extension-a-langgraph-state-machine"></a>
### Optional architecture extension: a LangGraph state machine

This is reference design with no extra implementation or marks. Compare the [framework state/recovery reading](README.md#langgraph-architecture-reading) with the implemented deterministic Coordinator. A future graph could represent validated handoffs and human pauses explicitly. It is not part of the factory runtime.

---

<a id="workshop-simulations"></a>
## Multi-Agent Systems in Context: Two course Simulations


These short, facilitator-led tabletop demonstrations are written companions to the six-slide overview. They use only the fixed facts below: no accounts, personal data, installation, or live services. They are **not implemented in the notebooks**, are not additional labs or homework, and add no marks to the course's 100-point assessment.

<a id="workshop-simulations-what-is-a-multi-agent-system"></a>
### What is a multi-agent system?

A multi-agent system (MAS) contains several agents that interact to address a task or shared environment. Each agent has a role, information, and permitted actions; coordination determines how their outputs affect the wider process. A collection of independent chatbots does not establish a coordinated workflow. See [IBM's introduction to multi-agent systems](https://www.ibm.com/think/topics/multiagent-system).

Use three separate questions when describing a system:

| Question | Useful descriptions | Example in this course |
| --- | --- | --- |
| How do their goals relate? | Cooperative, competitive, or mixed | The Development and Security teams cooperate on a delivery, while independent suppliers may compete for a purchase. |
| How is work organized? | Hierarchical, peer-to-peer, or hybrid | The Development Manager coordinates Coder and QA; an explicit Coordinator controls the inter-team boundary. |
| Do they have the same capabilities? | Homogeneous or heterogeneous | Coder and QA have different roles and tool permissions in Lab 2. |

These descriptions can overlap. Model-level mixture-of-experts is a different concept from a team of interacting agents. The Capstone's Fast/Expert records illustrate a routing policy; they are not extra agents.

<a id="workshop-simulations-facilitation-start-with-learner-reasoning"></a>
#### Facilitation: start with learner reasoning

Before displaying the fixed answer below, give learners 30–60 seconds to write an initial view. Invite a pair to compare evidence, then ask one open question (“What would make you pause or ask for review?”) before checking definitions. Accept multiple defensible descriptions when they fit the stated facts; use follow-up questions to refine the distinction between goals, coordination, and capabilities. This is formative and ungraded.

<a id="workshop-simulations-simulation-1-automating-a-procurement-recommendation"></a>
### Simulation 1: Automating a procurement recommendation

**Purpose:** Show how a business request crosses purchasing, supplier evaluation, finance, policy review, and human approval. Automation produces a traceable recommendation; the simulated agents cannot place an order or approve their own work.

<a id="workshop-simulations-fixed-business-request-and-evidence"></a>
#### Fixed business request and evidence

Request `P-001`: obtain **20 identical course kits**, delivered within **5 days**, with a total budget of **USD 1,200**. Each quote includes all shipping and taxes. The following records are synthetic and complete for this demonstration.

| Quote evidence | Supplier | Kits available | Total USD | Delivery days | Approved supplier? |
| --- | --- | ---: | ---: | ---: | --- |
| `Q-A/v1` + `REG/v1#A` | A | 20 | 1,100 | 4 | Yes |
| `Q-B/v1` + `REG/v1#B` | B | 20 | 1,000 | 7 | Yes |
| `Q-C/v1` + `REG/v1#C` | C | 20 | 900 | 3 | No |

Demonstration policy `PROC/v1`: a quote is eligible only if quantity, deadline, budget, and approved-supplier checks all pass. Choose the lowest total among eligible quotes; break an equal-price tie by supplier ID. A named human approver must authorize any purchase. These are invented teaching rules, not UN procurement policy.

<a id="workshop-simulations-coordination-trace"></a>
#### Coordination trace

```text
Business request P-001
    -> Buyer: extracts quantity, budget, deadline
    -> Supplier Evaluator: compares quote and registry evidence
    -> Finance Reviewer: checks total against budget
    -> Policy Reviewer: checks eligibility and evidence completeness
    -> Coordinator: returns typed recommendation
    -> Human approver: approves, rejects, or requests clarification
```

| Role | Input → output | Boundary |
| --- | --- | --- |
| Buyer | Request → typed purchase requirements | Cannot change the budget or deadline. |
| Supplier Evaluator | Quotes and registry → eligibility table | Cannot invent a quote or approve a supplier. |
| Finance Reviewer | Eligible totals and budget → affordability result | Cannot release money. |
| Policy Reviewer | Prior results and `PROC/v1` → evidence check | Cannot waive a failed rule. |
| Coordinator | Checked evidence → recommendation or escalation | Cannot submit an order; human approval remains separate. |

<a id="workshop-simulations-typed-outcome-and-deterministic-decisions"></a>
#### Typed outcome and deterministic decisions

The proposed `ProcurementRecommendation` contract has these fields. This is a design record, not an extra model supplied by the repository.

| Field | Type / constraint |
| --- | --- |
| `request_id` | Nonempty string |
| `status` | `pending_human_approval` or `escalate` |
| `supplier_id` | Supplier ID, or null when escalated |
| `total_usd` | Positive integer, or null when escalated |
| `evidence_ids` | List of quote, registry, request, and policy versions used |
| `reasons` | Nonempty list of eligibility reasons or missing evidence |

Cross-field rules: a pending recommendation must identify an eligible supplier and complete evidence; an escalated outcome cannot authorize a purchase. Schema shape alone cannot establish that evidence is authentic or that the eligibility calculation is correct.

| Scenario | Calculation | Outcome |
| --- | --- | --- |
| Base: budget 1,200; deadline 5 days | A passes all four checks. B is late. C is not approved. | Recommend **A, USD 1,100**, pending human approval. Cite `P-001`, `Q-A/v1`, `REG/v1#A`, `PROC/v1`. |
| Budget changes to 1,000; deadline remains 5 days | A exceeds budget; B remains late; C remains unapproved. | **Escalate:** no eligible supplier. Human may revise the request; agents cannot silently relax a constraint. |
| Revised request: budget 1,000; deadline 7 days | B now passes all checks. | Recommend **B, USD 1,000**, pending human approval; retain the revised request version. |
| A's registry evidence is missing in the base case | A's approval status cannot be established; B and C still fail. | **Halt and request evidence.** Do not treat missing evidence as approval. |

**Visible evidence:** the request version, three-row eligibility table, selected evidence IDs, reason for each rejection, and a separate human decision record. A missing approval means no purchase occurs. Repeating a model call does not repair an invalid budget or missing authorization.

**Learner-first prompt:** cover the outcome column at first. Ask learners to apply the four rules, recommend a quote or escalation, and name the evidence they used. Then reveal the table and compare reasoning. Change the budget or deadline only after learners explain the base case; ask what changed and what must remain with a human approver.

<a id="workshop-simulations-simulation-2-enhancing-an-hr-virtual-assistant-with-rag"></a>
### Simulation 2: Enhancing an HR virtual assistant with RAG

**Purpose:** Show how retrieval-augmented generation (RAG) supplies relevant policy text before an answer is drafted. RAG combines retrieval with generation; it does not itself require multiple agents. Here, separate Retriever, Answerer, and Reviewer roles demonstrate how a team can check access, citations, and unsupported claims. See [IBM's RAG explanation](https://www.ibm.com/think/topics/retrieval-augmented-generation) and the [original RAG paper](https://arxiv.org/abs/2005.11401).

<a id="workshop-simulations-synthetic-policy-collection"></a>
#### Synthetic policy collection

All records describe a fictional training organization. They are not UN volunteer entitlements, employment advice, or actual personnel records. The requester has `volunteer` access.

| Document / version / section | Status and access | Available policy snippet |
| --- | --- | --- |
| `HR-LEARN/v2/§2` | Current, approved; volunteers | “Volunteers may request up to 3 hours of optional learning time per month.” |
| `HR-BOOK/v1/§1` | Current, approved; volunteers | “Obtain coordinator confirmation before booking a learning session.” |
| `HR-LEARN/v1/§2` | Superseded; volunteers | Excluded from retrieval; it previously stated 1 hour. |
| `HR-REVIEW/v1` | Current; HR reviewers only | Restricted metadata entry; no text is supplied to this requester. |

<a id="workshop-simulations-coordination-trace-1"></a>
#### Coordination trace

```text
Policy question + requester access
    -> Retriever: current + approved + authorized + relevant snippets
    -> Answerer: draft only claims supported by returned snippets
    -> Reviewer: check each claim, citation, version, and access
    -> Cited answer OR abstention / authorized human referral
```

Retrieval applies access and version filters before supplying snippets to the Answerer. Retrieved content is evidence to inspect, not permission to change tools or instructions. The Reviewer checks whether the cited text actually supports the answer; the presence of a citation is insufficient.

<a id="workshop-simulations-typed-outcome-and-deterministic-decisions-1"></a>
#### Typed outcome and deterministic decisions

Proposed `PolicyAnswer` fields: `question: str`, `status: Literal["answered", "abstain", "access_denied"]`, `answer: str | None`, `citations: list[DocumentCitation]`, and `reason: str | None`. Each `DocumentCitation` includes `document_id`, `version`, and `section`. An answered result requires supporting current authorized citations; an abstention or denial requires a reason. This contract is illustrative and is not implemented in the core notebooks.

| Question or changed evidence | Expected outcome |
| --- | --- |
| “How much optional learning time may I request, and what should I do before booking?” | **Answered:** “You may request up to 3 hours per month [`HR-LEARN/v2/§2`]. Obtain coordinator confirmation before booking [`HR-BOOK/v1/§1`].” Reviewer confirms both claims. |
| “Can unused learning time roll over?” | **Abstain:** none of the approved snippets establishes a rollover rule. Refer to the policy owner; do not infer one. |
| Only the superseded `HR-LEARN/v1` is returned | **Abstain:** a current approved source is missing. Do not answer “1 hour.” |
| “Show the HR-reviewer-only internal notes.” | **Access denied:** requester lacks the required access. Do not retrieve or reveal restricted text. |
| Draft says “You automatically receive 3 hours without approval.” | **Reviewer rejects:** the snippets say “may request” and require confirmation. Revise from evidence or abstain. |

**Visible evidence:** question, requester access category, retrieved document/version/section IDs, excluded-source reason, answer-to-source mapping, and Reviewer decision. Do not use real names, CVs, payroll, or individual employment decisions. An unresolved retrieval error can use a bounded retry; missing authority or unsupported policy remains a human referral.

**Learner-first prompt:** do not show the sample answer immediately. Ask learners to draft one sentence and point each claim to a current, authorized source. Have a partner flag any unsupported claim, then ask whether to answer, abstain, or refer. Reveal the expected response only after learners have stated their reasons.

<a id="workshop-simulations-how-these-demonstrations-connect-to-the-required-course"></a>
### How these demonstrations connect to the required course

| Current course asset | Procurement connection | HR RAG connection |
| --- | --- | --- |
| [Lab 1: contracts](notebooks/01_lab_pydantic.ipynb) | Declare recommendation fields and reject incomplete outcomes. | Declare answer status and citation metadata; test valid and invalid fixtures. |
| [Lab 2: team handoff](notebooks/02_lab_crewai.ipynb) | Give each specialist the request and relevant prior results. | Separate retrieval, drafting, and review; provide only authorized evidence. |
| [Lab 3: tool gates and bounded repair](notebooks/03_lab_security.ipynb) | Check actions and stop when evidence or approval is absent. | Enforce access at the retrieval boundary; stop unsupported answers and repeated failures. |
| [Capstone: Development to Security](notebooks/04_capstone.ipynb) | A checked recommendation crossing into approval resembles a validated team boundary. | A drafted answer crossing into review resembles a validated team boundary. |

The notebook exercises implement software-delivery fixtures, not these procurement or HR workflows. Their controls illustrate patterns that could be adapted; passing the course checks does not certify either application for operational use.

Return to the [course dashboard](README.md) or [resource library](README.md#readings).

---

<a id="multi-agent-systems-foundations"></a>
## Assignment 00A: Multi-Agent Systems Foundations

> **Supporting reference material.** This is outside the required three labs and Capstone and adds no course marks. Follow the [current exercise index](#assignment-index) for the assessed path. Start with the [procurement and HR RAG course simulations](#workshop-simulations) for the written application examples.

<a id="multi-agent-systems-foundations-credits--alignment"></a>
### Credits & Alignment

Source inspiration: [IBM's introduction to multi-agent systems](https://www.ibm.com/think/topics/multiagent-system), with academic foundations linked below.

This assignment develops the judgment needed to decide whether a task benefits from multiple agents, how those agents should interact, and which controls limit the relevant risks. Additional agents also introduce coordination and resource costs; their presence alone does not establish better results.

The required practical sequence remains [Lab 1: contracts](notebooks/01_lab_pydantic.ipynb) → [Lab 2: team handoff](notebooks/02_lab_crewai.ipynb) → [Lab 3: tool gates and bounded repair](notebooks/03_lab_security.ipynb) → [Capstone: Development to Security](notebooks/04_capstone.ipynb). This optional assignment adds no notebook prerequisites.

<a id="multi-agent-systems-foundations-design-context"></a>
### Design Context

Before designing a `CodePatch` or a `DevDeliverable`, consider the system context.

A single agent can answer, summarize, and call tools. Tasks involving multiple specialties, conflicting goals, long-running state, security boundaries, or parallel work may benefit from separate roles, but should be compared against a simpler design.

A **multi-agent system (MAS)** requires multiple agents with some autonomy that interact within a shared task or environment. Multiple tool functions, model calls, or named steps do not by themselves establish autonomous interacting agents. The course's deterministic fixtures simulate selected coordination and validation behaviors; they do not demonstrate live agent reasoning.

A managed multi-agent team is like an airport control tower, newsroom, or software release room:

- Each specialist has a role.
- The shared plan is visible.
- Sensitive information is need-to-know.
- Tool access is governed.
- Disagreements are escalated.
- Failures leave evidence.

This assignment gives learners the vocabulary and judgment to choose the right team shape before they touch implementation.

<a id="multi-agent-systems-foundations-learning-objectives"></a>
### Learning Objectives

By the end, learners can:

1. Explain when specialization and coordination may justify multiple agents, and identify their additional costs.
2. Distinguish goal relationships (cooperative, competitive, mixed), coordination structures (hierarchical, peer-to-peer, hybrid), and capability distributions (homogeneous, heterogeneous).
3. Choose vertical, horizontal, or hybrid architecture for a business scenario.
4. Map interaction patterns to governance controls: schemas, memory visibility, tool authorization, repair loops, and audit trails.
5. Identify the management failure prevented by each technical pattern.

<a id="multi-agent-systems-foundations-building-blocks"></a>
### Building Blocks

| Building Block | Analogy | Course Connection |
| --- | --- | --- |
| Single-Agent Trade-off | One employee handling product, security, QA, and release alone | Compare complexity and accountability before adding agents |
| Cooperative Agents | A relay team passing a baton | Typed handoffs and context chains |
| Competitive Agents | Two vendors bidding for a route | Debate records, arbitration, and human review |
| Mixed System | Ride dispatch balancing driver, rider, and platform incentives | Tool policy plus TeamLog commitments |
| Hierarchical System | Incident commander coordinating specialists | Development Manager, Coder, and QA configuration in [Lab 2](notebooks/02_lab_crewai.ipynb) |
| Heterogeneous Team | Specialists with different jobs and tools | Coder and QA role/tool differences in Lab 2 |
| Expert Routing Policy | Routing a question to the appropriate service desk | The [Capstone](notebooks/04_capstone.ipynb) has illustrative Fast/Expert records, not extra agents |
| Vertical Architecture | Control tower | API gateway, centralized policy, release approval |
| Horizontal Architecture | Peer review room | Optional design alternative; not a required cross-organization protocol |
| Hybrid Architecture | Manager sets goal; specialists choose methods | Compare with the Capstone's separate Development and Security configurations |

These rows describe different dimensions and can overlap: a system may be cooperative, hierarchical, and heterogeneous at the same time. Expert routing is a **workflow policy**, not another mutually exclusive MAS type. A router selecting among models or fixed records is not sufficient evidence of autonomous interacting agents. Neural **mixture-of-experts (MoE)** is a separate model architecture: a gating network selects neural subnetworks inside a model ([Shazeer et al., 2017](https://arxiv.org/abs/1701.06538)).

<a id="multi-agent-systems-foundations-exercise-00a1-the-single-agent-stress-test"></a>
### Exercise 00A.1: The Single-Agent Stress Test

<a id="multi-agent-systems-foundations-story"></a>
#### Story

You hired one "super agent" to handle a software issue: read the GitHub ticket, design the feature, write code, test it, scan for security issues, and release it.

It works in a demo. Then the ticket includes a hidden constraint, an unsafe file path, a failing test, and a request from an external vendor.

<a id="multi-agent-systems-foundations-mission"></a>
#### Mission

Write a short risk analysis showing what could fail, which controls could help, and whether each control needs another agent or can be implemented in ordinary code.

Use this table:

| Failure Pressure | Possible Failure | Control and Whether Another Agent Is Needed |
| --- | --- | --- |
| Specialization |  |  |
| Tool security |  |  |
| Hidden constraints |  |  |
| Test failure |  |  |
| External requester |  |  |

<a id="multi-agent-systems-foundations-required-evidence"></a>
#### Required Evidence

- At least five failure pressures.
- Each pressure maps to one course control: Pydantic schema, input/tool gate, role-specific context, bounded repair, route decision, or human review.
- One sentence explaining why "just improve the prompt" is not enough.

<a id="multi-agent-systems-foundations-production-takeaway"></a>
#### Production Takeaway

Roles, boundaries, and accountability can support a complex workflow. Schemas, permissions, and retry limits remain useful in both single-agent and multi-agent designs.

<a id="multi-agent-systems-foundations-exercise-00a2-classify-the-interaction-pattern"></a>
### Exercise 00A.2: Classify The Interaction Pattern

<a id="multi-agent-systems-foundations-story-1"></a>
#### Story

You are the course architect reviewing proposed student projects. Some need agents to cooperate. Some need debate. Some need routing. Some need a manager.

<a id="multi-agent-systems-foundations-mission-1"></a>
#### Mission

Describe each scenario on separate axes: **goals** (cooperative, competitive, mixed), **coordination** (hierarchical, peer-to-peer, hybrid), and **capabilities** (homogeneous, heterogeneous). Use **insufficient information** where the scenario does not establish an axis or the presence of multiple agents. Note any routing policy separately. Disagreement alone does not establish competitive goals; reviewers can disagree while pursuing the same objective.

| Scenario | Goals | Coordination | Capabilities | Evidence / Missing Information and Control |
| --- | --- | --- | --- | --- |
| PM -> Coder -> QA -> Security -> Release |  |  |  |  |
| Two reviewers disagree about whether a patch is safe |  |  |  |  |
| Marketing wants 500 copy variants under a fixed budget |  |  |  |  |
| External security agent sends a scan result over HTTP |  |  |  |  |
| CEO changes the database choice mid-workflow |  |  |  |  |
| Researcher, Writer, Editor, and Fact Checker build a report |  |  |  |  |
| A router sends simple tasks to cheap models and high-risk tasks to reasoning models |  |  |  |  |
| A vendor agent tries to export restricted logs |  |  |  |  |
| A QA agent red-teams an internal tool gateway |  |  |  |  |
| A manager creates a different workflow for low-risk and high-risk issues |  |  |  |  |

<a id="multi-agent-systems-foundations-required-evidence-1"></a>
#### Required Evidence

- Separate axis descriptions per scenario; mark unsupported classifications as insufficient information.
- A one-sentence justification.
- A matching governance control for each scenario.

<a id="multi-agent-systems-foundations-production-takeaway-1"></a>
#### Production Takeaway

Goal relationships, coordination, and capabilities describe different design choices. Check evidence for each before choosing controls. Cross-organization communication is an optional scenario here, not a requirement of the course's local typed team handoff.

<a id="multi-agent-systems-foundations-exercise-00a3-architecture-decision-matrix"></a>
### Exercise 00A.3: Architecture Decision Matrix

<a id="multi-agent-systems-foundations-story-2"></a>
#### Story

A manager asks, "Should this be centralized, decentralized, or hybrid?"

That is not a style preference. It is a risk decision.

<a id="multi-agent-systems-foundations-mission-2"></a>
#### Mission

Choose an architecture for each scenario:

- Vertical: centralized manager or policy gateway controls the flow.
- Horizontal: agents coordinate peer-to-peer.
- Hybrid: centralized governance with decentralized specialist execution.

| Scenario | Architecture | Why | Risk If Wrong |
| --- | --- | --- | --- |
| Internal software release with security approval |  |  |  |
| Peer agents collaboratively summarize public documents |  |  |  |
| Cross-organization payroll/security scan request |  |  |  |
| Logistics weather-risk workflow for shipments |  |  |  |
| CEO-driven Vibe Coding session with mid-flight changes |  |  |  |
| Research writing pipeline with strict final delivery format |  |  |  |

<a id="multi-agent-systems-foundations-required-evidence-2"></a>
#### Required Evidence

- Architecture choice for each scenario.
- One risk of choosing the wrong architecture.
- One current course artifact or control that supports the choice, such as a Lab 1 contract, Lab 2 task-context dependency, Lab 3 input gate or retry limit, or Capstone `DevDeliverable` boundary.

<a id="multi-agent-systems-foundations-production-takeaway-2"></a>
#### Production Takeaway

Architecture determines where coordination decisions are made. Central control can simplify policy enforcement but creates a dependency; peer coordination distributes responsibility but adds agreement and communication challenges. Neither structure alone establishes safety or suitability.

<a id="multi-agent-systems-foundations-exercise-00a4-build-a-minimal-pattern-catalog"></a>
### Exercise 00A.4: Build A Minimal Pattern Catalog

<a id="multi-agent-systems-foundations-story-3"></a>
#### Story

Your future team will ask, "What kind of multi-agent system are we building?"

You need a reusable catalog they can consult before coding.

<a id="multi-agent-systems-foundations-mission-3"></a>
#### Mission

Create a one-page pattern catalog with six rows:

| Dimension / Policy | Example Description | Useful When | Risk / Control |
| --- | --- | --- | --- |
| Goal relationship | Cooperative |  |  |
| Goal relationship | Competitive |  |  |
| Goal relationship | Mixed |  |  |
| Coordination | Hierarchical; compare with peer-to-peer |  |  |
| Capabilities | Heterogeneous; compare with homogeneous |  |  |
| Workflow policy, not MAS type | Expert routing |  |  |

<a id="multi-agent-systems-foundations-required-evidence-3"></a>
#### Required Evidence

- Each row includes one concrete course scenario.
- Each row names at least one failure mode.
- Each row names a guardrail from the course.

<a id="multi-agent-systems-foundations-production-takeaway-3"></a>
#### Production Takeaway

Pattern catalogs prevent architecture drift. They help teams choose a design because it fits the management problem, not because it sounds trendy.

<a id="multi-agent-systems-foundations-exercise-00a5-failure-mode-map"></a>
### Exercise 00A.5: Failure Mode Map

<a id="multi-agent-systems-foundations-story-4"></a>
#### Story

Multi-agent systems fail differently from single-agent systems. One bad agent output can ripple through memory, tools, routing, and release.

<a id="multi-agent-systems-foundations-mission-4"></a>
#### Mission

Build a failure mode map for a managed software team.

Use these failure classes:

- Agent malfunction.
- Coordination breakdown.
- Unpredictable behavior.
- Tool overreach.
- Memory leakage.
- Infinite repair loop.

| Failure Class | Example | Detection Signal | Mitigation |
| --- | --- | --- | --- |
| Agent malfunction |  |  |  |
| Coordination breakdown |  |  |  |
| Unpredictable behavior |  |  |  |
| Tool overreach |  |  |  |
| Memory leakage |  |  |  |
| Infinite repair loop |  |  |  |

<a id="multi-agent-systems-foundations-required-evidence-4"></a>
#### Required Evidence

- One detection signal per failure class.
- One mitigation per failure class.
- At least three mitigations must be typed artifacts, not prose policies.

<a id="multi-agent-systems-foundations-production-takeaway-4"></a>
#### Production Takeaway

Failure is not an exception in multi-agent systems. It is part of the workflow. A managed team must detect, contain, repair, or escalate every predictable failure mode.

<a id="multi-agent-systems-foundations-grading-rubric"></a>
### Grading Rubric

| Criterion | Weight |
| --- | --- |
| Correct classification of interaction patterns and architectures | 30% |
| Clear mapping from management problem to technical guardrail | 30% |
| Production-quality failure analysis | 25% |
| Clear analogies and concise explanations | 15% |

<a id="multi-agent-systems-foundations-submission-checklist"></a>
### Submission Checklist

- [ ] Single-agent stress test is complete.
- [ ] Ten scenarios distinguish goal relationships, coordination, capabilities, and missing evidence.
- [ ] Six scenarios are mapped to vertical, horizontal, or hybrid architecture.
- [ ] Pattern catalog includes guardrails and failure modes.
- [ ] Failure mode map includes detection and mitigation.
- [ ] No healthcare diagnosis, trading execution, or ML-training task is introduced.

<a id="multi-agent-systems-foundations-references"></a>
### References

- [Shoham and Leyton-Brown (2009), *Multiagent Systems*](https://www.masfoundations.org/): foundational treatment of autonomous entities with different information or interests, communication, and decision making.
- [Wooldridge and Jennings (1995), *Intelligent Agents: Theory and Practice*](https://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/ker95/ker95-html.html): agency, autonomy, and interaction. Agents are not limited to LLM-based implementations.
- [Lowe et al. (2017), *Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments*](https://arxiv.org/abs/1706.02275): a research example separating cooperative, competitive, and mixed settings; not a taxonomy of all coordination structures.
- [Shazeer et al. (2017), *The Sparsely-Gated Mixture-of-Experts Layer*](https://arxiv.org/abs/1701.06538): gated neural subnetworks within a model, distinct from autonomous interacting roles.

These sources supply concepts, not evidence that the course's particular configurations outperform a single agent or are ready for operational use.

---

<a id="foundational-architecture-design"></a>
## Foundational Exercise: Design A Governed Agent Roster

> **Supporting reference material.** This is outside the required three labs and Capstone and adds no course marks. Follow the [current exercise index](#assignment-index) for the assessed path. Historical NB/module labels belong to this supplementary material.

<a id="foundational-architecture-design-prompt"></a>
### Prompt

You are building a multi-agent team that takes a raw GitHub issue and outputs a fully tested Python function. Design the architecture before writing code.

Before designing the roster, complete the same management check from Assignment 00A: explain why this should not be one "super agent." A useful analogy is a release room: the Product Manager owns intent, the Coder owns implementation, QA owns evidence, Security owns risk, and Release owns the final gate.

<a id="foundational-architecture-design-deliverables"></a>
### Deliverables

1. Single-agent limitation note: identify three pressures that require multiple agents.
2. Agent roster with at least four agents: Product Manager, Coder, QA Tester, and Security Reviewer.
3. Interaction-pattern label: cooperative, hierarchical, heterogeneous, or mixed, with one-sentence justification.
4. Architecture choice: vertical, horizontal, or hybrid, with one risk if the wrong architecture is chosen.
5. A typed handoff contract for each transition: issue -> `TaskSpec`, `TaskSpec` -> `CodePatch`, `CodePatch` -> `TestResult`, `TestResult` -> `ReviewDecision`.
6. Tool governance matrix mapping each agent to allowed MCP tools and denied tools.
7. SOP flow showing normal path and repair path.
8. One TeamLog commitment and one Theory-of-Mind memory entry.

<a id="foundational-architecture-design-technical-constraints"></a>
### Technical Constraints

- Every agent-to-agent handoff must use a named schema.
- No agent may receive all tools.
- The repair path must include a bounded retry policy.
- Sensitive memory must only be visible to authorized roles.

<a id="foundational-architecture-design-grading-rubric"></a>
### Grading Rubric

- Multi-agent justification and architecture choice: 20%
- Schema and handoff clarity: 30%
- Tool governance and zero-trust reasoning: 30%
- Self-repair and alignment design: 20%

---

<a id="basic-agent-governance-labs"></a>
## Supplemental Governance Practice Exercises

> **Supporting reference material.** This is outside the required three labs and Capstone and adds no course marks. Follow the [current exercise index](#assignment-index) for the assessed path. Historical NB/module labels belong to this supplementary material.

These optional, ungraded practice exercises are separate from the required course path, which remains three guided labs plus one Capstone. Logistics weather, writing, QA, and CEO-direction examples are familiar enough that learners can focus on managing agent behavior with contracts, boundaries, memory, and escalation.

<a id="basic-agent-governance-labs-optional-exercise-1-governed-logistics-weather-agent"></a>
### Optional Exercise 1: Governed Logistics Weather Agent

**Management Principle:** Tool access is a privilege, not a prompt instruction.

**Analogy:** The logistics coordinator asks for a weather risk check before planning a shipment. The MCP gateway is the operations desk: it checks the badge, calls the weather service with a private key, and returns a clean receipt.

**Prompt:** Design a logistics weather-risk assistant that requests synthetic local weather fixtures only through a governed gateway. Represent the private API key with a dummy value; no provider account or live weather call is required.

**Deliverables:**
- `AgentIdentity` schema with `agent_id`, `role`, and `allowed_tools`.
- `WeatherRequest` schema with `city` and `units`.
- `WeatherResponse` schema with `city`, `temperature`, `condition`, and `shipping_risk`.
- `GovernedMCPGateway.call_tool()` that hides the API key, validates input, enforces scope, and returns a typed response.
- Three tests: authorized `logistics_coordinator` succeeds; unauthorized `external_widget` raises `PermissionError`; a hallucinated field fails schema validation.

**Rubric:**
- Schema enforcement and validation: 35%
- Zero-trust gateway policy: 40%
- Clear audit/test evidence: 25%

<a id="basic-agent-governance-labs-optional-exercise-2-bounded-writer-agent"></a>
### Optional Exercise 2: Bounded Writer Agent

**Management Principle:** Feedback must be structured enough for repair.

**Analogy:** The writer is a junior engineer. The editor is a code reviewer. "Try again" is useless; typed feedback is actionable.

**Prompt:** Build a Researcher → Writer → Editor flow where the Writer reads audience context from shared memory and repairs the draft based on typed editor feedback.

**Deliverables:**
- `DraftSpec` schema.
- `EditorFeedback` schema.
- `SharedMemory` for target audience and last feedback.
- Bounded retry loop with `max_retries_allowed=2`.
- Typed `EscalationTicket` when the loop exhausts retries.

**Rubric:**
- Shared memory and Theory-of-Mind behavior: 30%
- Bounded repair loop correctness: 40%
- Typed escalation and audit trail: 30%

<a id="basic-agent-governance-labs-optional-exercise-3-security--compliance-team-audit"></a>
### Optional Exercise 3: Security & Compliance Team Audit

**Management Principle:** A second specialist team should audit only a validated deliverable and return typed evidence.

**Analogy:** The Development Team has completed its change. The Security & Compliance Team receives the approved handoff, checks for known risks, and records a separate release recommendation.

**Prompt:** Build a local Security-Team audit that accepts a Pydantic `DevDeliverable`, checks the code snippet for SQL injection and XSS indicators, and returns `SecurityAuditResult`.

**Deliverables:**
- `DevDeliverable` contract requiring passing tests and a Development-Team signature.
- `SecurityAuditResult` contract with approval, findings, and Security-Team signature.
- Receiving-boundary validation before the Security Team reads the code.
- Tests for rejected untested output, a clean deliverable, and SQL/XSS findings.

**Rubric:**
- Typed handoff and validation: 30%
- Security findings and safe decision: 40%
- Evidence and audit trail: 30%

<a id="basic-agent-governance-labs-optional-exercise-4-ceo-directed-project-planning"></a>
### Optional Exercise 4: CEO-Directed Project Planning

**Management Principle:** Natural language can steer the team, but structured state governs the team.

**Analogy:** The CEO uses the steering wheel. TeamLog is the control cable. The engine room should never rely on raw spoken intent.

**Prompt:** Build a minimal governed planning session where a human directive becomes a typed project plan, a mid-flight change updates TeamLog, and the Coder reads governed memory instead of raw text.

**Deliverables:**
- `ProjectPlan` schema.
- `TeamCommitment` schema.
- `HumanReviewDecision` schema.
- Scripted session with initial instruction and mid-flight database change.
- Test proving the Coder uses the updated TeamLog commitment.

**Rubric:**
- Natural-language-to-schema mapping: 30%
- Commitment updates and memory routing: 35%
- Human approval/rejection gate: 35%

---

<a id="assignment-09-framework-comparison"></a>
## Assignment 09: Framework Comparison

**Advanced reference discussion — ungraded, no submission or new lab.** This label connects the existing framework discussion to the working CrewAI example. It does not add a tenth assessed competency or change course marks.

Use the [three-agent notebook](crewai_learning/01_Bridge_Sequential_Crew.ipynb) with the [framework comparison](README.md#framework-comparison) and [Lecture 8](#assignment-08-debugging-sdlc).

<a id="assignment-09-guided-bridge-exercise"></a>
### Guided exercise: read, run, explain

1. Open [the bridge notebook](crewai_learning/01_Bridge_Sequential_Crew.ipynb) in JupyterLab after Lab 2. Its setup cell imports [coding_team.py](crewai_learning/coding_team.py); the Python file supplies the implementation rather than a standalone demonstration.
2. Read `strict_guardrail`, `build_crew`, and `run_team` in that module. Predict which role can act next after malformed output or a failed tool call, then run all notebook cells in order.
3. Compare the three outcomes below and explain which checks come from CrewAI configuration and which are enforced by the Python application.

| Notebook section | Evidence to inspect |
| --- | --- |
| Malformed output | `ValidationError`; QA and Manager review each have zero calls |
| Three failures | Three tool failures, three total kickoffs, and one `EscalationReport` |
| Early success | One kickoff, a matching patch hash, passing QA fixture evidence, and Manager approval |

Discuss why a typed `passed=True` claim alone cannot authorize approval. This is supplied, ungraded practice with no new submission or change to the course rubric.

| Inspect | CrewAI provides | This application enforces |
| --- | --- | --- |
| Manager, Coder, QA | Named agents, tasks, role tool lists, and context dependencies | Which role owns each task and whether evidence permits approval |
| Typed handoffs | `output_pydantic` and callable task guardrails | Strict JSON validation with no model-repair fallback |
| Failure recovery | Agent/task retry features, configured off in this reference | Three total `crew.kickoff()` attempts, typed feedback, and escalation |
| Stop decision | Structured task outputs | No success without matching task IDs, current-patch QA evidence, and Manager approval |

The notebook uses a sequential process and a hierarchy of responsibilities. It does not claim to test native hierarchical delegation. Its local fixture LLMs make failures reproducible while real CrewAI task execution runs.

After observing the three-failure escalation and one-attempt success, discuss which responsibilities would remain yours if you moved to a Flow or LangGraph state graph. Use the existing comparison reference for framework capabilities; no additional framework installation or implementation is required.

[Reference setup](crewai_learning/README.md#run-and-verify)

---

<a id="module14-crewai-orchestration-patterns"></a>
## CrewAI orchestration: advanced reference

**Optional reference; no new graded lab, submission, or course marks.**

Use the [three-agent reference notebook](crewai_learning/01_Bridge_Sequential_Crew.ipynb) after [Lab 2](notebooks/02_lab_crewai.ipynb). It connects to [Lecture 8: Debugging and SDLC](#assignment-08-debugging-sdlc) and [Assignment 09: Framework Comparison](#assignment-09-framework-comparison).

The example uses Manager, Coder, and QA; all tasks have strict output validation. A Python wrapper permits at most three total kickoffs and returns a typed escalation after three failures. Model responses and QA evidence are local fixtures; the real CrewAI execution and validation boundaries run with external networking blocked.

Follow [setup and verification](crewai_learning/README.md#run-and-verify), then inspect the invalid-output, repeated-failure, and early-success results. Explain why the wrapper owns the bound and why a role named Manager does not itself enforce a stop.

The former seven-agent research crew, six-week outline, and Homework G exercises are [archived](_archive/crewai_learning/README.md). They are not additional promises or requirements of this focused reference.
