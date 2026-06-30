# Assignment 12: From Whisper to Shipped Code

## Vision

You have built the governance shell in NB1-NB8. Now connect the **Internal Brain** from NB9 with the **External Steering Wheel** from NB10.

This is one long production journey:

> A human whisper becomes a typed plan, a governed workflow scaffold, a debated patch, a TeamLog update, and finally a human-approved release artifact.

This assignment is also the bridge from Assignment 00A theory into the capstone. You are not building a coding bot. You are proving that human intent can become a **hybrid, heterogeneous, partially hierarchical multi-agent system** with typed context chains, zero-trust tools, bounded repair, and human veto power.

## Architecture Decision Record

Before implementation, submit a one-page ADR with:

1. Selected architecture: vertical, horizontal, or hybrid.
2. Risk profile of the task.
3. Why the selected architecture fits better than the alternatives.
4. Where the manager has authority.
5. Where specialist agents have autonomy.
6. Which failure modes the architecture is designed to contain.

Recommended capstone-aligned answer: **hybrid**. The manager creates the `ProjectPlan` and `WorkflowScaffold` through centralized oversight, while Coder and QA use a bounded repair loop with local autonomy.

## Building Blocks

| Layer | Notebook | Building Block | What It Proves |
| --- | --- | --- | --- |
| Steering Wheel | NB10 | `ManagerInstruction` -> `ProjectPlan` | Natural language becomes typed state |
| TeamLog | NB10 | `TeamCommitment(key="db", value="MongoDB")` | Human changes become durable memory |
| Internal Brain | NB9 | `WorkflowScaffold` | Complexity creates the right team shape |
| Collective Intelligence | NB9 | `DebateRecord` | Conflicting agent evidence becomes structured |
| Escalation | NB9/NB10 | `EscalationTicket` and `HumanReviewDecision` | Humans intervene when agents cannot resolve contention |
| Release | NB10/Capstone | `PullRequestSummary` | Final artifact is auditable and typed |

## Interaction Pattern Map

Map each interaction pattern to one concrete implementation point:

| Pattern | Required Implementation | Required Proof |
| --- | --- | --- |
| Cooperative | PM/Manager and Tech Lead share project constraints through TeamLog or shared memory | Tech Lead output cites a stored commitment or memory record |
| Competitive or Mixed | Coder wants to ship, QA or Security challenges the patch | Audit trail shows at least one rejected transition before approval or escalation |
| Hierarchical | Human/Manager/Security has veto power over release | `HumanReviewDecision` or security decision blocks release when needed |
| Heterogeneous | Different agent roles or model classes handle different work | Route trace or scaffold shows specialist assignment |
| Mixture of Experts | Router chooses the right worker/model for a subtask | Route decision explains why a subtask was sent to that target |

You do not need to implement all patterns as separate frameworks. You do need to show that the patterns are visible in the architecture and enforced by artifacts.

## Exercise 9.1: Dynamic Scaffold

**Problem:** A linear chain fails when the task is high-risk.

**Task:** Implement `WorkflowScaffold` generation from a `TaskComplexity` or `ProjectPlan`.

**Constraint:** If `risk_level == "high"`, the scaffold must include `SecurityReviewer` before final review.

**Deliverable:** A test showing:

- Low-risk task creates a small scaffold.
- High-risk secure login task creates a scaffold with `SecurityReviewer`.
- The scaffold includes explicit `execution_order`.

## Exercise 9.2: Debate Protocol

**Problem:** The Coder says "ship"; the Security Reviewer says "block."

**Task:** Implement `DebateRecord` and a `DebateModerator`.

**Constraint:** If contention cannot be resolved, the moderator must emit an `EscalationTicket`.

**Deliverable:** A test showing:

- A resolvable database debate produces a final decision.
- An unresolved release-readiness debate produces an escalation ticket for the human.

## Exercise 10.1: Translation Layer

**Problem:** The CEO says, "Build a REST API for auth." The system needs a typed `ProjectPlan`.

**Task:** Implement `parse_manager_instruction()` and `manager_create_plan()`.

**Constraint:** Use a mock LLM adapter or live structured-output call, but always validate through Pydantic.

**Deliverable:** A test showing:

- Valid CEO instruction becomes a `ProjectPlan`.
- Invalid database choice fails schema validation before reaching agents.

## Exercise 10.2: Mid-Flight Pivot

**Problem:** The CEO changes their mind: "Actually, use MongoDB."

**Task:** Implement `manager_apply_human_change()`.

**Constraint:** The Coder must never read the raw CEO sentence. It must read `TeamCommitment(key="db", value="MongoDB")`.

**Deliverable:** A test showing:

- Initial commitment stores the original database.
- Mid-flight change updates TeamLog.
- Coder reads the updated commitment.

## Exercise 10.3: Human Veto

**Problem:** Agents can produce a technically valid patch that the human should stop.

**Task:** Implement `HumanReviewDecision(status: Literal["approved", "rejected", "needs_changes"])`.

**Constraint:** 

- `rejected` halts release and logs the decision.
- `needs_changes` routes back to the NB9 debate or repair path.
- `approved` allows release.

**Deliverable:** A test for all three statuses.

## Final Build: Single Long Journey

Implement:

```python
def run_enterprise_pipeline(
    ceo_initial_prompt: str,
    ceo_mid_flight_change: str,
) -> PullRequestSummary:
    ...
```

Scenario:

1. CEO types: `Build a secure login system.`
2. Manager translates it into `ProjectPlan(risk_level="high")`.
3. NB9 generates a scaffold that includes `SecurityReviewer`.
4. Coder writes the patch.
5. Security Reviewer debates the patch and finds a flaw.
6. System pauses for human input.
7. CEO types: `Fix the flaw and use MongoDB.`
8. Manager updates `TeamCommitment(key="db", value="MongoDB")`.
9. Coder reads TeamLog, revises the patch, and submits again.
10. Human returns `HumanReviewDecision(status="approved")`.
11. Release manager returns a typed `PullRequestSummary`.

## Required Evidence

- One-page ADR.
- Interaction pattern map.
- Printed or logged `ProjectPlan`.
- Printed or logged `WorkflowScaffold`.
- Printed or logged `DebateRecord`.
- Printed or logged `TeamCommitment` before and after the pivot.
- Final `PullRequestSummary`.
- Audit trail showing parse, scaffold, debate, pivot, re-execution, and approval.

## Challenge Mitigation Proof

Include three proof tests or notebook cells:

1. **Agent Malfunction:** force a QA/security failure and show bounded repair or typed escalation.
2. **Coordination Complexity:** pass an invalid or hallucinated handoff and show Pydantic rejection before downstream use.
3. **Unpredictable Behavior:** attempt an unauthorized tool call and show gateway denial.

## Rubric

| Criterion | Weight |
| --- | ---: |
| ADR and architecture justification | 15 |
| Interaction pattern mapping | 15 |
| Translation layer and schema validation | 15 |
| Dynamic scaffold, debate, and escalation behavior | 20 |
| TeamLog mid-flight pivot | 15 |
| Challenge mitigation proof tests | 10 |
| Final release gate and audit trail | 10 |

## Core Lesson

Vibe Coding is not magic. It is the rigorous translation of human intent into typed, governed state, then execution by a deterministic, observable orchestration machine.
