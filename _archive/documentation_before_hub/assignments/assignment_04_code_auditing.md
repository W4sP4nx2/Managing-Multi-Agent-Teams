# Assignment 04: Multi-Agent Management — Code Auditing and Team Oversight

[Course home](../README.md) · [Learner paths](../README.md#learner-paths) · [Lab 2 notebook](../notebooks/02_lab_crewai.ipynb) · [Slide index](../README.md#main-deck-slide-index) · [Factory simulation](../extensions/live_software_factory.md)

**Maps to:** Lecture 5 — Managing Teams, Team Memory, and Code Auditing · **Core activity:** Lab 2, CrewAI Contract Handoff · **Type:** Auto-graded lab

## Objective

Act as delivery manager for the Manager–Coder–QA team: audit role boundaries and context, then decide whether the typed proposal may enter QA review.

## Team map

![Lab 2 roles and local audit path, with separate configured relationships and simulated handoff.](../resources/diagrams/lab2-team-audit.svg)

You are the **human delivery manager**. The Engineering Manager coordinates; the Coder alone writes; QA owns independent read/verify work. The Architect task is a rule-carrying artifact, not another agent. Dashed arrows show the configured task/role relationships. The solid path is a local fixture → role/context and strict `CodePatch` gate → simulated QA inbox. A rejected proposal returns for repair and leaves that inbox empty. The configured QA task is not executed, and its supplied tool returns sample evidence rather than running tests.

**Navigate:** [Task](#task) → [Audit](#managers-audit-action) → [Pass/fail](#passfail) → [Submit](#submit) → [Live mapping](#factory-simulation-mapping).

## Skill Transparency & Least Privilege

Between the agent definitions and task configuration, run the supplied **Skill Transparency Matrix**. It reads each agent's actual custom tools, compares them with the role allowlist, and displays each tool's Action, Input, Output, and Warning metadata. The starter Manager's write permission must appear as excessive; the Coder and QA keep separate responsibilities.

After the first repair, rerun agents → matrix → tasks → fixture → audit → grader. Explain why visible tool documentation supports management judgment but does not grant OS isolation, prove model understanding, or execute a tool. The matrix observes configuration and adds no marks.

## Task

In [`02_lab_crewai.ipynb`](../notebooks/02_lab_crewai.ipynb), repair the two marked broken settings:

1. Remove `write_code_tool` from the Manager while retaining its approval and delegation responsibilities.
2. Set the Coder task context to `context=[architect_task]` to declare the Architect-rule dependency. The deterministic Coder fixture inspects this dependency and returns a string ID when it is present.

Keep the supplied Coder and QA contracts typed with `output_pydantic`, and retain `qa_task.context=[coder_task]`. These declare the task graph; the required path constructs the Crew without executing its tasks. The local tools are placeholders and do not write files or run commands. Context availability does not guarantee that a real model follows the rules.

Follow this order in the notebook:

1. **Run** the configuration, deterministic Coder fixture, and Manager's Audit Gate before editing.
2. **Inspect** every failed check and the empty `qa_inbox`; trace the missing rule on the team map.
3. **Edit** only the two marked agent and task configuration settings above.
4. **Rerun** agents → skill matrix → tasks → fixture → audit, record the decision, then run the unchanged auto-grader and Blind Agent debug.
5. **Submit** the notebook and evidence described below. No live model, real test, git operation, or deployment is required.

## Manager's Audit Action

Run the supplied `lab2-manager-audit-gate` cell after the fixture. Inspect all role tool lists, task owners/context, output models, and the current payload. A failed audit leaves `qa_inbox` empty; `PASS_TO_QA` admits one validated proposal. Record the decision, one observed check, and the next owner in the supplied Markdown sentence. This local inbox is not an executed QA task or release approval. The action is formative and adds no new code TODO or marks.

## Pass/fail

- **Pass:** The Manager has approval and delegation but lacks the code-writing tool, the Coder task lists the Architect task as context, the deterministic fixture validates as `CodePatch`, the Manager audit records `PASS_TO_QA`, the decision note cites evidence, and the unchanged grader reports **15/15**.
- **Revise:** The Manager can write code, the Coder lacks the Architect context, or the typed handoff fails.

The grader scores the Manager configuration and the Architect-task context dependency. It does not execute or score a TeamLog read, a QA task, or a live Crew run; inspect the typed-fixture cell separately. See [the course map](../COURSE_MAP.md#what-the-graders-actually-check) for exact cell IDs and grader coverage. Do not call a live model as part of this assignment.

<a id="submit"></a>
## Submit

Retain the completed Lab 2 notebook with its two repairs, the current fixture/audit output, the unchanged grader result, and the supplied decision sentence naming one observed check and the next owner. Follow your instructor's existing submission channel. `PASS_TO_QA` authorizes admission to this simulated inbox; it supplies no test result or production release approval.

## Factory simulation mapping

The [factory simulation guide](../extensions/live_software_factory.md) extends the same role boundaries: the Coder fixture writes a local candidate; separate Security, UI/UX, and QA checks inspect that artifact; local CI/CD records actual results. The Engineering Manager coordinates those results, and the human approves the simulated budget and local publication steps. Keep review decisions, test evidence, and approvals tied to the exact commit revision; a changed revision needs renewed evidence. A commit trailer or this local audit result alone does not establish independent review or publication authorization. This mapping is ungraded and adds no live execution to Assignment 04.

[Course home](../README.md) · [Learner paths](../README.md#learner-paths) · [Slide index](../README.md#main-deck-slide-index)
