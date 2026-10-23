# Assignment 03: Context Engineering — Typed Contracts

[Course home](../README.md) · [Learner paths](../README.md#learner-paths) · [Slide index](../README.md#main-deck-slide-index)

**Maps to:** Lecture 3 — Intent-Based vs. Spec-Driven Work · **Core activity:** Lab 1, Pydantic Contract · **Type:** Auto-graded lab

**Navigate:** [Objective](#objective) → [Architecture and flow](#architecture-and-flow) → [Task](#task) → [Pass/fail](#passfail) → [Transfer checkpoint](#transfer-checkpoint-ungraded) → [Lab 2](../notebooks/02_lab_crewai.ipynb).

## Objective

Turn a business requirement into a typed contract that rejects malformed agent output before another task consumes it.

## Architecture and flow

![Lab 1 contract boundary: observe the weak schema accepting a malformed local fixture, then repair a strict schema that accepts valid probes and rejects invalid ones.](../resources/diagrams/lab1-contract-flow.svg)

**Text version:** manager defines acceptance criteria → fixed, untrusted local fixture → weak schema accepts an invalid score and discards an extra field → learner repairs the strict contract → grader checks accepted and rejected probes → **15/15** evidence.

The manager, Coder, and QA describe the intended team handoff. This lab executes Pydantic validation in one local Python process. The contract checks payload structure and declared constraints; claim accuracy and deployment readiness require separate evidence.

## Task

In [`01_lab_pydantic.ipynb`](../notebooks/01_lab_pydantic.ipynb), replace the weak starter with `StrictResearchOutput`. Require `topic: str`, `confidence_score: float`, and `findings: list[str]`; constrain the score to `0.0 <= confidence_score <= 1.0`; and forbid undeclared fields such as `secret_backdoor`.

Use Pydantic v2 `Field` constraints and `ConfigDict(extra="forbid")`. Keep the deterministic fixture unchanged so the same bad payload is tested before and after the gate is repaired.

## Pass/fail

- **Pass:** Valid data is accepted; the fixture with `confidence_score=150.5` and the extra `secret_backdoor` field are rejected; the notebook grader reports **15/15**.
- **Revise:** The model accepts either defect, rejects valid data, or is not a Pydantic model.

The fixture is local and deterministic; a provider call is not part of this assignment.

## Transfer checkpoint (ungraded)

In your working brief, map this boundary to the deterministic factory: identify the artifact producer, validator, downstream consumer, and repair route for rejected output. Name a separate control for simulated budget approval or local publication. A passing schema establishes the tested contract; budget and local publication decisions need their own authorization.

This discussion adds no implementation, credentials, marks, or separate scheduled activity. After **15/15**, continue to [Lab 2: CrewAI hierarchy](../notebooks/02_lab_crewai.ipynb) and [Assignment 04](assignment_04_code_auditing.md).

For the integrated deterministic continuation, use the [integrated factory simulation guide](../extensions/live_software_factory.md).

[Course home](../README.md) · [Learner paths](../README.md#learner-paths) · [Slide index](../README.md#main-deck-slide-index)
