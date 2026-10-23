# Assignment 06: Manager Oversight — Code Validation and Bounded Repair

[Course home](../README.md) · [Learner paths](../README.md#learner-paths) · [Slide index](../README.md#main-deck-slide-index)

**Maps to:** Lecture 6 — Safety Nets, Tool Validation, and Evals · **Core activity:** Lab 3, Security and Bounded Repair · **Type:** Auto-graded lab

## Objective

Act as delivery manager: set tool/retry policies, inspect QA and worker evidence, and escalate a failed task within its budget.

## Task

In [`03_lab_security.ipynb`](../notebooks/03_lab_security.ipynb):

1. Complete `SecureToolInput` so malicious SQL-like input (including the supplied `DROP TABLE` payload) raises a Pydantic `ValidationError` before the dry-run tool is called, while a numeric user ID such as `"123"` is accepted.
2. Set `MAX_RETRIES = 3`. Confirm the loop makes at most four calls total (one initial attempt plus three retries) and escalates when all attempts fail.

This notebook uses a local dry-run function; it does not connect to a database or implement a complete SQL-injection defense.

## Management Oversight Action

Run the supplied `lab3-management-oversight` cell. Review hostile-input rejection, safe-input acceptance, absence of the unsafe value from `tool_call_log`, four mock calls, $0.20 simulated spend, and the escalation flag. In the corrected always-failing scenario, record `ESCALATE_TO_HUMAN` with that evidence and a human reviewer as next owner. If a control fails, record `BLOCK_AND_REPAIR_CONTROLS` and repair it. The action makes no extra call, release, or human notification. It is formative with no new code TODO or marks.

## Pass/fail

- **Pass:** Unsafe input is rejected, the safe input passes, escalation follows three retries, simulated cost stops with the loop, the oversight and decision note record escalation, and the unchanged grader reports **15/15**.
- **Revise:** Any unsafe value reaches the tool, a safe ID is rejected, or the retry loop exceeds its bound.

No live model or external service is required.

[Course home](../README.md) · [Learner paths](../README.md#learner-paths) · [Slide index](../README.md#main-deck-slide-index)
