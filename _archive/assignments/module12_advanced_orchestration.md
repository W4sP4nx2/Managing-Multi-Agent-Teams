# Homework F: Advanced Orchestration Discussion

> **Optional post-course material.** This is outside the required three labs and Capstone and adds no workshop marks. Follow the [current exercise index](../../assignments/index.md) for the assessed path. Historical NB/module labels belong to this supplementary material.

## Status

Optional conceptual reading and design discussion. This module is **not a graded implementation lab**.

Optional starter scaffold: [module12_advanced_orchestration_starter.py](starter_code/module12_advanced_orchestration_starter.py)

## Why This Module Is Conceptual

Learned orchestration is useful as an advanced research topic, but it is outside this course's hands-on scope. Reproducing a trained orchestrator would require a training setup, benchmark suite, and model pool that do not fit a two-day workshop.

NB6 asks learners to write a simple rule-based Python router as an optional extension. The target is an inspectable cost-and-risk policy, not a trained orchestrator.

## Pedagogical Boundary

NB6 teaches an optional practical foundation: learners implement a transparent local Python routing policy by cost, risk, and task type. It does not call a hosted routing service or claim to learn a policy.

NB9 teaches advanced workflow concepts: dynamic scaffolds, debate moderation, adaptive topology, and a small history-based example. These are teaching adapters, not a trained orchestration system.

Homework F is therefore used for reading, discussion, and architecture critique. It should not be used as a required graded coding assignment.

## Orchestration Concepts and Course Examples

| Orchestration concept | NB6/NB9 teaching adapter | Course stance |
| :--- | :--- | :--- |
| Learned orchestrator models trained with RL/evolution | Simple history-driven rule updates | Conceptual only; do not grade as "learned" orchestration |
| Dynamic agentic scaffolds | `WorkflowScaffold` examples | Useful design pattern |
| Collective intelligence | Typed debate records | Useful management pattern |
| Intra-workflow isolation | Extension prompt only | Discuss in architecture review |
| Persistent shared memory | Basic memory and routing history | Covered elsewhere in NB2 and NB9 |
| Adaptive topology selection | Deterministic restructurer demo | Useful concept, not a required production implementation |

## Discussion F-1: From Rules to Learned Orchestration

Prompt: Compare a static keyword router with a learned orchestrator. Explain what evidence would be required before a production system should update routing behavior.

Deliverables:

- One-page design note.
- `RoutingHistory` schema sketch.
- Explanation of why 10 mocked failures are not the same as RL training.
- Risk analysis for allowing an orchestrator to update routing policy automatically.

Assessment:

- Distinguishes heuristics from learned orchestration: 40%
- Identifies required telemetry and evaluation data: 30%
- Names safety risks and rollback strategy: 30%

## Discussion F-2: Dynamic Scaffold Generation

Prompt: Design how a manager agent could choose between a single-agent workflow, a sequential workflow, and a parallel review workflow.

Deliverables:

- `WorkflowScaffold` schema sketch.
- Diagram for simple, medium, and high-risk workflows.
- Explanation of where isolation boundaries should exist.

Assessment:

- Scaffold design clarity: 35%
- Appropriate use of parallelism and reviewer joins: 35%
- Isolation and governance discussion: 30%

## Discussion F-3: Collective Intelligence via Debate

Prompt: Two agents disagree about SQL vs. NoSQL. Design a debate record that preserves both positions and gives the manager enough evidence to decide or escalate.

Deliverables:

- `DebateRecord` schema sketch.
- Example debate transcript.
- Final decision or escalation rule.

Assessment:

- Preserves disagreement without collapsing nuance: 35%
- Produces an auditable decision record: 35%
- Includes clear escalation criteria: 30%
