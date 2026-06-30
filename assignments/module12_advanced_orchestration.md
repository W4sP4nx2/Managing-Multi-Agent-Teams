# Homework F: Advanced Fugu Discussion

## Status

Optional conceptual reading and design discussion. This module is **not a graded implementation lab**.

Starter scaffold, if an instructor wants an optional demo: `assignments/starter_code/module12_advanced_orchestration_starter.py`

Instructor discussion guide: `instructor/solutions/module12_solution_guide.md`

## Why This Module Is Conceptual

Sakana Fugu is a strong research concept, but it is a poor core hands-on assignment for this course. The paper is about learned orchestrator models trained through reinforcement learning and evolutionary-style search over a pool of model and agent configurations. Learners in a 2-hour notebook lab do not have the compute, time, benchmark suite, or frontier model pool required to reproduce that.

The course should not ask learners to write an if/else heuristic and pretend it is learned orchestration. That creates a fake exercise and weakens the otherwise objective verification style of the curriculum.

## Pedagogical Boundary

NB6 teaches the practical foundation: transparent heterogeneous routing by cost, risk, and task type.

NB9 teaches the conceptual bridge: dynamic scaffolds, debate moderation, adaptive topology, and a tiny history-based learner. These are teaching adapters, not a reproduction of Fugu's training method.

Homework F is therefore used for reading, discussion, and architecture critique. It should not be used as a required graded coding assignment.

## What Sakana Fugu Covers vs. What We Teach

| Fugu concept | NB6/NB9 teaching adapter | Course stance |
| :--- | :--- | :--- |
| Learned orchestrator models trained with RL/evolution | Simple history-driven rule updates | Conceptual only; do not grade as "learned" orchestration |
| Dynamic agentic scaffolds | `WorkflowScaffold` examples | Useful design pattern |
| Collective intelligence | Typed debate records | Useful management pattern |
| Intra-workflow isolation | Extension prompt only | Discuss in architecture review |
| Persistent shared memory | Basic memory and routing history | Covered elsewhere in NB2 and NB9 |
| Adaptive topology selection | Deterministic restructurer demo | Useful concept, not a required production implementation |

## Discussion FUGU-1: From Heuristics to Learned Orchestration

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

## Discussion FUGU-2: Dynamic Scaffold Generation

Prompt: Design how a manager agent could choose between a single-agent workflow, a sequential workflow, and a parallel review workflow.

Deliverables:

- `WorkflowScaffold` schema sketch.
- Diagram for simple, medium, and high-risk workflows.
- Explanation of where isolation boundaries should exist.

Assessment:

- Scaffold design clarity: 35%
- Appropriate use of parallelism and reviewer joins: 35%
- Isolation and governance discussion: 30%

## Discussion FUGU-3: Collective Intelligence via Debate

Prompt: Two agents disagree about SQL vs. NoSQL. Design a debate record that preserves both positions and gives the manager enough evidence to decide or escalate.

Deliverables:

- `DebateRecord` schema sketch.
- Example debate transcript.
- Final decision or escalation rule.

Assessment:

- Preserves disagreement without collapsing nuance: 35%
- Produces an auditable decision record: 35%
- Includes clear escalation criteria: 30%

## Instructor Delivery Pattern

Teach this after NB6 and NB9. Be explicit:

"NB6 is a practical routing exercise. NB9 is a teaching adapter for advanced orchestration concepts. Sakana Fugu itself is a research system, not something we reproduce in this workshop. The goal is to recognize the architecture and management implications, not to fake an RL orchestrator in a notebook."
