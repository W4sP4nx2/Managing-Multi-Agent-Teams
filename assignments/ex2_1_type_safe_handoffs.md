# Exercise 2.1: Type-Safe Handoffs

## Mission

Build a customer-service multi-agent crew where every agent returns a strict Pydantic schema instead of raw text.

## Business Problem

A support team receives high-volume customer transcripts. A single agent can summarize the issue, but production support requires division of labor:

- Transcript Analyzer extracts structured facts.
- Quality Evaluator checks completeness and policy risk.
- Final Report Agent produces a CRM-ready artifact.

## Required Schemas

- `TranscriptAnalysis`
- `QualityEvaluation`
- `FinalReport`

## Deliverables

1. Implement the three schemas in `assignments/starter_code/ex2_memory_system_starter.py`.
2. Modify the agents so each one returns a schema object, not a raw dictionary.
3. Print valid JSON for each handoff.
4. Generate invalid output and show Pydantic rejecting it.
5. Explain which downstream failure the schema prevented.

## Technical Constraints

- Use `ConfigDict(extra="forbid")`.
- Use `Literal` or enums for bounded categories.
- Add at least one field constraint with `Field(...)`.
- The final report must be generated from typed inputs only.

## Grading Rubric

- Strict schema design and validation: 40%
- Working multi-agent handoff flow: 35%
- Invalid-output rejection demonstration: 15%
- Explanation of production value: 10%
