# Homework G: CrewAI Applied Pipeline Engineering

## Purpose

This module is now delivered as a **self-contained CrewAI study track**, separate from the core notebook sequence.

Primary study material: [`../crewai_learning/README.md`](../crewai_learning/README.md)

It bridges the course's custom governance shell with an industry-standard orchestration framework. Learners should understand that CrewAI can manage agents, tasks, dependencies, hierarchical review, guardrails, failure recovery, and clean delivery, while the course's Pydantic, MCP, audit, and zero-trust patterns still govern production safety.

Use the exercises below as focused checkpoints after reading the full guide.

## Scope Note: Everyone Gets a Coding Agent Team

The goal of this homework is that every learner can design their own AI coding team: a Coder agent, QA agent, Review agent, retry loop, state model, and reusable project template.

We do **not** require every learner to configure a personal LLM backend during the core exercise. Individual API keys, CLI authentication, and provider-specific settings are optional because they vary by learner environment. The required deliverable is the governed architecture and offline runnable skeleton. Learners who have keys may run the CrewAI CLI path as an extension.

## Readiness Checklist and Score

Score the learner's CrewAI readiness out of 100.

| Area | Evidence | Points |
| --- | --- | ---: |
| CrewAI basics | Learner can explain agents, tasks, crews, process modes, and task context. | 15 |
| Environment plan | Learner documents Python, CrewAI CLI, LLM key requirements, and `.env` safety. | 15 |
| Coding agents | Learner designs Coder, QA, and Review agents with non-overlapping roles. | 20 |
| Guardrails and state | Learner defines typed state, review decisions, retry budget, and approval logic. | 20 |
| Orchestration loop | Learner shows `review fails -> back to coder` with a bounded retry path. | 15 |
| Reusable template | Learner packages setup instructions, project structure, and peer demo checklist. | 15 |

Readiness interpretation:

- 90-100: Ready to run a personal CrewAI coding team with live keys.
- 75-89: Ready for offline skeleton and guided live setup.
- 60-74: Understands pieces but needs help connecting state, guardrails, and retry.
- Below 60: Revisit core course patterns before running CrewAI live.

## Exercise 14.1: Task Dependency Graphs

**Scenario:** A job-application crew needs three tasks: analyze a job posting, analyze a candidate profile, and tailor a resume. The resume task must not run until both upstream tasks finish.

**Prompt:** Build a CrewAI-style job application workflow with:

- `research_task`: extracts job requirements.
- `profile_task`: builds candidate profile from GitHub/personal writeup.
- `resume_task`: depends on both upstream outputs through `context=[research_task, profile_task]`.

**Deliverables:**

- A runnable notebook cell or Python script.
- A diagram showing the dependency graph.
- Evidence that `resume_task` uses both upstream outputs.

**Constraints:**

- Use typed task/result objects when using the offline adapter.
- If using real CrewAI, keep all LLM/API cells optional and documented.
- Do not pass raw unstructured text between tasks without naming the source task.

**Rubric:**

| Criterion | Weight |
| --- | ---: |
| Correct dependency graph and execution order | 40% |
| Clear evidence that context is consumed by downstream task | 35% |
| Explanation of why dependencies prevent context loss | 25% |

## Exercise 14.2: Parallel Execution

**Scenario:** Job research and candidate profiling are independent. Running them one after another wastes time.

**Prompt:** Mark the independent tasks as parallel/async work and compare runtime against a sequential baseline.

**Deliverables:**

- Sequential runtime measurement.
- Parallel runtime measurement.
- Short analysis of when parallelism is safe vs dangerous.

**Constraints:**

- Only parallelize tasks that do not depend on each other.
- Preserve final task dependency: resume tailoring still waits for both upstream results.
- Do not claim a speedup unless the timing evidence supports it.

**Rubric:**

| Criterion | Weight |
| --- | ---: |
| Correct use of independent parallel tasks | 40% |
| Runtime evidence and interpretation | 30% |
| Clear explanation of dependency safety | 30% |

## Exercise 14.3: File Outputs

**Scenario:** Production agents do not only return in-memory objects. They create deliverables: resumes, reports, PR summaries, audit logs, and release notes.

**Prompt:** Add file persistence to the resume task using a CrewAI-style `output_file="tailored_resume.md"` field.

**Deliverables:**

- Generated `tailored_resume.md` artifact or temporary-file proof.
- Test that the file exists and contains the expected resume content.
- Reflection on when file outputs need security scanning before release.

**Constraints:**

- Use a temporary directory in tests or notebooks unless the assignment explicitly asks for a committed artifact.
- Do not write secrets, API keys, PII, or unrestricted prompt logs to disk.
- Include the output path in the task result or audit trail.

**Rubric:**

| Criterion | Weight |
| --- | ---: |
| Correct file output behavior | 40% |
| Verification that artifact exists and contains expected content | 35% |
| Security and audit reflection | 25% |

## Exercise 14.4: Hybrid Pattern: CrewAI + Course Governance

**Scenario:** CrewAI can orchestrate work quickly, but enterprise systems still need zero-trust policy checks before any tool touches real data.

**Prompt:** Build a governed CrewAI-style tool wrapper that:

- Receives a tool call from an agent.
- Converts it into the course's `ToolRequest` shape.
- Runs the authorization policy.
- Calls the underlying tool only if authorized.
- Logs allowed and denied events.

**Deliverables:**

- `GovernedCrewAITool` or equivalent wrapper.
- One allowed test.
- One denied test.
- Short comparison: custom implementation vs CrewAI vs hybrid.

**Constraints:**

- Authorization must happen before the underlying tool runs.
- Denied calls must be auditable.
- The wrapper must preserve typed inputs/outputs at the boundary.

**Rubric:**

| Criterion | Weight |
| --- | ---: |
| Correct governance wrapper design | 40% |
| Allowed and denied tests both pass | 35% |
| Trade-off analysis: control vs convenience | 25% |

## Exercise 14.5: Learn CrewAI Basics

**Scenario:** A learner wants to use industry tools, but "install and run" is not the real learning goal. The learning goal is to understand how CrewAI expresses a managed team.

**Prompt:** Create a short CrewAI basics note that explains:

- How to install the CrewAI CLI or package.
- How the official quickstart scaffolds a CrewAI project.
- What agents, tasks, crews, process modes, and task context mean.
- Where LLM configuration and API keys live.

**Deliverables:**

- `crewai_basics.md`.
- A setup checklist with Python version, CrewAI install command, optional `crewai create crew <project_name>` scaffold, and `.env` key safety.
- A diagram showing `Agent -> Task -> Crew -> Result`.

**Constraints:**

- Do not commit API keys.
- Do not require live model execution for grading.
- Mention that the current official installation path recommends `uv tool install crewai`; `pip install crewai` can be used for package-level experimentation when appropriate.
- If your local CLI supports flow scaffolding, document `crewai create flow`; otherwise document how to add a Flow around a crew manually.

**Rubric:**

| Criterion | Weight |
| --- | ---: |
| Correct explanation of CrewAI primitives | 40% |
| Safe setup and key-handling plan | 35% |
| Clear bridge back to course governance patterns | 25% |

## Exercise 14.6: Build Your Coding Agent Roster

**Scenario:** Every learner should leave with the design for a personal coding team. The team should not be a chatbot. It should be a small managed workforce.

**Prompt:** Design a CrewAI-style coding team with:

- `CoderAgent`: writes a patch from a typed task.
- `QAAgent`: runs or simulates tests and returns typed test evidence.
- `ReviewAgent`: approves, rejects, or requests changes.

**Deliverables:**

- Agent definitions with role, goal, backstory, tools, and `allow_delegation` stance.
- Task definitions for coding, testing, and reviewing.
- Typed artifacts: `CodingTask`, `CodePatch`, `TestResult`, and `ReviewDecision`.
- A short explanation of what each agent is **not** allowed to do.

**Constraints:**

- The Coder must not execute tests directly.
- QA must not approve release.
- Reviewer must not rewrite code silently.
- Unknown fields in typed artifacts must be rejected.

**Rubric:**

| Criterion | Weight |
| --- | ---: |
| Role clarity and separation of duties | 35% |
| Typed contracts and guardrails | 35% |
| Least-privilege tool design | 30% |

## Exercise 14.7: Implement the Bounded Retry Loop

**Scenario:** The Coder writes a patch, QA fails it, and Review rejects it. A production system cannot retry forever.

**Prompt:** Implement an offline orchestration skeleton that follows:

```text
Task -> Coder -> QA -> Review
                 ^       |
                 |       v
              repair <- needs_changes
```

If `ReviewDecision.status == "needs_changes"`, route back to the Coder with typed feedback. If the retry budget is exhausted, return an `EscalationTicket`.

**Deliverables:**

- Offline Python skeleton or CrewAI Flow pseudocode.
- `TeamState` schema with task, patch, test result, review decision, retry count, and audit log.
- One passing run.
- One failing run that escalates.

**Constraints:**

- Retry budget must be explicit.
- Review feedback must be structured, not raw prose.
- Audit log must show each transition.
- The exercise may run without live CrewAI or LLM calls.

**Rubric:**

| Criterion | Weight |
| --- | ---: |
| Correct conditional orchestration | 40% |
| Bounded retry and escalation behavior | 35% |
| Typed state and audit trail | 25% |

## Exercise 14.8: Package as a Reusable Template and Showcase

**Scenario:** A class cohort should be able to compare coding-agent teams without copying hidden instructor setup.

**Prompt:** Package your coding-agent team as a reusable class template.

**Deliverables:**

- `README.md` setup instructions.
- Project tree showing where `agents.yaml`, `tasks.yaml`, `crew.py`, tools, tests, and outputs live.
- Optional CrewAI scaffold command:
  - `crewai create crew my_coding_team` for crew scaffolding.
  - `crewai create flow my_coding_flow` only if supported by your installed CLI.
- A showcase script or transcript demonstrating task -> patch -> QA -> review -> retry/ship.
- Peer review checklist with at least five review questions.

**Constraints:**

- Live model keys are optional and must stay outside the repo.
- Template must include offline mocks so classmates can inspect the workflow.
- The showcase must include at least one failure path, not only a happy path.

**Rubric:**

| Criterion | Weight |
| --- | ---: |
| Reusable project structure and setup instructions | 35% |
| End-to-end demo including failure path | 35% |
| Peer review and iteration checklist | 30% |

## Production Takeaway

CrewAI is a deployment accelerator, not a governance replacement. Use it to manage task structure, dependencies, parallelism, files, runtime inputs, and optional Flow-style state. Keep the course's governance layer around it: strict schemas, least-privilege tools, audit trails, repair budgets, and human approval.
