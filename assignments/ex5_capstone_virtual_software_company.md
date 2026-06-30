# Ex5 CAPSTONE: Virtual Software Company

## Prompt

Build an end-to-end multi-agent system that ingests a mock GitHub issue and outputs validated code plus a generated pull request description. The system must behave like a small software company with typed roles, governed tools, shared memory, dynamic routing, and self-repair.

This capstone is the proving ground for the full course. You are not submitting a coding bot. You are submitting a managed AI workforce whose architecture, interaction patterns, and failure mitigations are explicit.

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

1. Architecture Decision Record: choose vertical, horizontal, or hybrid and justify it against the task risk profile.
2. Architecture diagram showing agent flow, memory routing, repair loop, and governance perimeter.
3. Interaction pattern map showing where cooperative, competitive/mixed, hierarchical, heterogeneous, and mixture-of-experts behavior appears.
4. Pydantic schemas for every inter-agent artifact.
5. MCP-style tool gateway with per-agent authorization.
6. Shared memory layer that stores requirements, decisions, failures, and review notes.
7. Dynamic router that selects worker model class by task complexity and risk.
8. Self-repair loop with maximum retry budget.
9. Test evidence showing at least one failed patch is repaired.
10. Final PR description generated from validated artifacts.
11. Governance note mapping the design to IoA or AGNTCY-style A2A interoperability.
12. Emergency escalation path when the repair loop exceeds `max_repairs`.
13. `PullRequestSummary.status` set to `SHIPPED` or `ESCALATED_TO_HUMAN`.
14. FastAPI gateway with `POST /tasks` and `GET /tasks/{task_id}`.
15. Background task or simulated asynchronous worker that runs `run_company()` without blocking the API response.
16. CrewAI comparison implementation: build one equivalent orchestration path using CrewAI or the self-contained CrewAI learning guide patterns in `crewai_learning/README.md`.
17. Trade-off analysis comparing custom implementation vs CrewAI vs hybrid governance.
18. Challenge-mitigation proof tests for malfunction, coordination complexity, and unpredictable behavior.

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

## Architecture Selection Requirement

Choose one:

| Architecture | Best Fit | Capstone Interpretation |
| --- | --- | --- |
| Vertical | High-compliance work where every action needs central approval | Release Manager or Manager controls all transitions |
| Horizontal | Low-risk prototyping where speed matters more than central approval | Coder and QA negotiate through SharedMemory with minimal manager bottleneck |
| Hybrid | Recommended default for this capstone | Manager sets `ProjectPlan`; specialists execute; Coder/QA repair locally; Security/Release retains veto power |

Your ADR must explain why your selected architecture fits the issue risk profile and why the alternatives are weaker.

## Interaction Pattern Requirements

| Pattern | Capstone Block | Proof |
| --- | --- | --- |
| Cooperative | PM/Tech Lead share project constraints through memory | Tech Lead or scaffold cites a PM constraint such as database choice |
| Competitive/Mixed | Coder submits patch; QA/Security challenges it | Audit trail shows rejected patch or repair feedback before release |
| Hierarchical | Security or Release can veto Coder output | Unauthorized deploy or unsafe patch is blocked |
| Heterogeneous | Agents or model classes specialize by role/risk | Route trace shows different targets for different subtasks |
| Mixture of Experts | Router selects a specialist/model for a subtask | Route decision explains specialist choice |

## Required Challenge Proofs

1. **Agent Malfunction:** force a failed test or unsafe patch. The system must repair within budget or return `ESCALATED_TO_HUMAN`.
2. **Coordination Complexity:** feed an invalid handoff with an extra field or invalid enum. Pydantic must reject it before the next agent uses it.
3. **Unpredictable Behavior:** simulate a prompt-injection or rogue-agent attempt to call an unauthorized tool. The gateway must deny it and leave audit evidence.

## API Gateway Scenario

Naive failure: an external webhook sends arbitrary JSON directly to the coder and crashes the workflow.

Required intervention: the API gateway acts as the governance perimeter. It validates the external payload, maps the key to identity, applies zero-trust policy, and only then starts the multi-agent pipeline.

## CrewAI Comparison Scenario

Naive failure: a learner treats CrewAI as a replacement for governance and lets framework tools run without policy checks.

Required intervention: CrewAI may handle orchestration, task dependencies, parallelism, file outputs, and runtime inputs, but the course governance layer still owns schemas, tool authorization, audit logging, repair budgets, and approval gates.

## Grading Rubric

- Architecture ADR and interaction-pattern mapping: 15%
- End-to-end architecture and typed contracts: 20%
- Working implementation, API behavior, and test evidence: 20%
- Tool governance and zero-trust controls: 15%
- Self-repair, routing, and memory quality: 15%
- Challenge-mitigation proof tests: 10%
- CrewAI comparison and custom-vs-framework trade-off analysis: 5%
