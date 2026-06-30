# Ex5 Capstone Solution Guide: Virtual Software Company

## Required End State

A passing capstone ingests an issue, emits `TaskSpec`, decomposes into subtasks, creates a patch, runs tests, performs security review, repairs at least one failed patch, and outputs a PR summary.

The final summary must include a machine-checkable status:

- `SHIPPED` when the patch passes QA and security.
- `ESCALATED_TO_HUMAN` when the repair budget is exhausted.

The capstone must also expose an API gateway:

- `POST /tasks` accepts raw external JSON and returns `202 Accepted` with `task_id`.
- `GET /tasks/{task_id}` returns `PENDING`, `RUNNING`, `SHIPPED`, or `ESCALATED`.
- Incoming API keys map to internal agent identities.
- External/vendor identities cannot set high risk or access restricted memory.

The capstone must include a CrewAI comparison:

- Either a real CrewAI crew or a design-level comparison using `crewai_learning/README.md`.
- At least one production framework pattern: task dependency context, parallel tasks, output files, or dynamic `kickoff(inputs={...})` values.
- A short trade-off analysis comparing custom implementation, CrewAI implementation, and a hybrid governed CrewAI approach.

## Minimum Viable Architecture

```text
Issue
  -> API Gateway(External JSON -> AgentIdentity -> task_id)
  -> PM(TaskSpec)
  -> TechLead(list[SubTask])
  -> Router(RouteDecision)
  -> Coder(CodePatch)
  -> QA(TestResult)
  -> Security(SecurityReview)
  -> Release(PullRequestSummary)
             ^ repair memory on failure

Optional comparison path:
Issue -> CrewAI-style Crew(Agent + Task + Context) -> Same governance wrappers
```

## Strong Answer Indicators

- Includes an ADR choosing vertical, horizontal, or hybrid architecture and defending it against the task risk profile.
- Maps interaction patterns to implementation evidence:
  - Cooperative: PM/Tech Lead memory or TeamLog handoff.
  - Competitive or mixed: Coder vs QA/Security rejection and repair.
  - Hierarchical: Security or Release veto.
  - Heterogeneous: specialist roles or routed model classes.
  - Mixture of Experts: router chooses a specialist/model class.
- Demonstrates the three required challenge proofs: malfunction handling, coordination-complexity validation, and unauthorized-tool denial.
- All inter-agent artifacts are Pydantic models or equivalent strict schemas.
- Tool calls include caller, tool, arguments, and sensitivity.
- Unauthorized tool call test is present and passes by failing safely.
- Repair loop has a max retry budget and escalation state.
- Escalation is represented as `PullRequestSummary.status`, not only prose.
- PR summary is generated from validated artifacts, not freeform memory.
- API gateway blocks unauthorized external work before orchestration starts.
- CrewAI comparison does not bypass governance; framework-managed tasks still feed typed artifacts and governed tools.

## Common Mistakes

1. **Capstone works only on the happy path**
   - Wrong: the first patch passes and there is no failure demonstration.
   - Right: at least one test fails, repair memory captures the error, and a later attempt ships or escalates.

2. **Repair loop retries without using QA evidence**
   - Wrong: `code(task, feedback=[])` is called repeatedly with no change.
   - Right: QA failure logs are added to repair memory and passed into the next coding attempt.

3. **Security review is prose only**
   - Wrong: `"Looks safe to me"` as a string.
   - Right: `SecurityReview(approved=True, findings=[])` as a typed release gate.

4. **Tools are called directly instead of through the gateway**
   - Wrong: `run_tests(patch)` from the orchestrator with no caller identity.
   - Right: `ToolGateway.call(ToolRequest(caller=qa_identity, tool=Tool.RUN_TESTS, ...))`.

5. **No route trace or audit log**
   - Wrong: final PR summary appears with no explanation of agent decisions.
   - Right: `audit_trail` records PM parsing, Tech Lead decomposition, router choice, QA attempts, repairs, and security approval.

6. **No escalation path**
   - Wrong: loop runs until it happens to pass.
   - Right: `max_repairs` stops the loop and returns `PullRequestSummary(status="ESCALATED_TO_HUMAN", ...)` when unresolved.

7. **API endpoint runs the whole workflow synchronously**
   - Wrong: `POST /tasks` waits until all agents finish and then returns 200.
   - Right: `POST /tasks` returns 202 plus `task_id`; status is retrieved through `GET /tasks/{task_id}`.

8. **External identity is trusted as a plain string**
   - Wrong: `requester_email.endswith("@vendor.com")` decides permissions.
   - Right: API key maps to a typed `AgentIdentity`, then policy checks risk and data access.

9. **CrewAI is treated as a governance replacement**
   - Wrong: "CrewAI handles orchestration, so no policy gateway is needed."
   - Right: CrewAI can manage task flow, but Pydantic schemas, tool authorization, audit logs, and approval gates remain explicit.

10. **Framework comparison is only vague prose**
   - Wrong: one paragraph says CrewAI would be useful.
   - Right: a minimal CrewAI flow or explicit design based on `crewai_learning/README.md` demonstrates dependencies, guardrails, recovery, clean delivery, or dynamic inputs.

## Suggested Capstone Grading Flow

1. Run tests.
2. Inspect schemas.
3. Trigger invalid patch.
4. Trigger unauthorized tool call.
5. Confirm repair loop stops or ships.
6. Test `POST /tasks` and `GET /tasks/{task_id}`.
7. Confirm external vendor high-risk request is rejected.
8. Read PR summary for traceability to `TaskSpec`.
9. Inspect ADR and interaction pattern map.
10. Confirm challenge-mitigation proof tests are present.
11. Inspect CrewAI/custom comparison and verify governance remains in the loop.
