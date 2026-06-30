# Ex5 CAPSTONE: Virtual Software Company

## Prompt

Build an end-to-end multi-agent system that ingests a mock GitHub issue and outputs validated code plus a generated pull request description. The system must behave like a small software company with typed roles, governed tools, shared memory, dynamic routing, and self-repair.

Your `run_company(issue: str, max_repairs: int = 2)` function should make the agentic lifecycle explicit:

1. **Perception:** PM ingests the raw issue and extracts requirements.
2. **Reasoning:** Tech Lead decomposes work and plans execution.
3. **Execution:** Coder and QA write code, run tests, and gather feedback.
4. **Learning:** Repair loop evaluates failures and updates memory.
5. **Governance:** Security and Release enforce compliance before final output.

## Required Agents

- Product Manager: converts issue into `TaskSpec`
- Tech Lead: decomposes work into `SubTask` objects
- Coder: produces `CodePatch`
- QA Tester: runs tests and emits `TestResult`
- Security Reviewer: checks tool use, data handling, and unsafe code patterns
- Release Manager: emits `PullRequestSummary`
- API Gateway: accepts external requests, maps API keys to identities, and starts the workflow asynchronously

## Required Deliverables

1. Architecture diagram showing agent flow, memory routing, and repair loop.
2. Pydantic schemas for every inter-agent artifact.
3. MCP-style tool gateway with per-agent authorization.
4. Shared memory layer that stores requirements, decisions, failures, and review notes.
5. Dynamic router that selects worker model class by task complexity and risk.
6. Self-repair loop with maximum retry budget.
7. Test evidence showing at least one failed patch is repaired.
8. Final PR description generated from validated artifacts.
9. Governance note mapping the design to IoA or AGNTCY-style A2A interoperability.
10. Emergency escalation path when the repair loop exceeds `max_repairs`.
11. `PullRequestSummary.status` set to `SHIPPED` or `ESCALATED_TO_HUMAN`.
12. FastAPI gateway with `POST /tasks` and `GET /tasks/{task_id}`.
13. Background task or simulated asynchronous worker that runs `run_company()` without blocking the API response.
14. CrewAI comparison implementation: build one equivalent orchestration path using CrewAI or the self-contained CrewAI learning guide patterns in `crewai_learning/README.md`.
15. Trade-off analysis comparing custom implementation vs CrewAI vs hybrid governance.

## Technical Constraints

- No raw executable code may be accepted without schema validation.
- Tool calls must include caller identity, tool name, arguments, and data sensitivity.
- Repair loop must stop after a fixed retry budget and escalate if unresolved.
- At least one unauthorized tool call must be tested and blocked.
- At least one memory access attempt must be denied due to sensitivity.
- Escalation must be machine-checkable through `PullRequestSummary.status`, not only human-readable prose.
- `POST /tasks` must accept a raw external JSON payload simulating a GitHub webhook, Slack command, or Jira ticket.
- The API must map an incoming `X-API-Key` or `Authorization` header to an `AgentIdentity`.
- If the identity is `external_vendor`, the API must reject requests that attempt to set `risk="high"` or access restricted memory.
- The POST endpoint must return `202 Accepted` immediately with a `task_id`.
- `GET /tasks/{task_id}` must return status and final summary when available.
- The CrewAI comparison must demonstrate at least one of: task dependencies, parallel execution, file outputs, or `kickoff(inputs={...})` dynamic inputs.
- If real CrewAI is not installed, learners may write a design-level comparison using the self-contained CrewAI guide, but must explain where `Agent`, `Task`, `Crew`, and `Process` fit.
- The hybrid option must keep the custom governance layer around framework-managed orchestration.

## API Gateway Scenario

Naive failure: an external webhook sends arbitrary JSON directly to the coder and crashes the workflow.

Required intervention: the API gateway acts as the governance perimeter. It validates the external payload, maps the key to identity, applies zero-trust policy, and only then starts the multi-agent pipeline.

## CrewAI Comparison Scenario

Naive failure: a learner treats CrewAI as a replacement for governance and lets framework tools run without policy checks.

Required intervention: CrewAI may handle orchestration, task dependencies, parallelism, file outputs, and runtime inputs, but the course governance layer still owns schemas, tool authorization, audit logging, repair budgets, and approval gates.

## Grading Rubric

- End-to-end architecture and typed contracts: 25%
- Working implementation, API behavior, and test evidence: 25%
- Tool governance and zero-trust controls: 20%
- Self-repair, routing, and memory quality: 15%
- CrewAI comparison and custom-vs-framework trade-off analysis: 10%
- PR summary and instructor-facing clarity: 5%
