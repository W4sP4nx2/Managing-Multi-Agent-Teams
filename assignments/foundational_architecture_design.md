# Foundational Exercise: Design A Governed Agent Roster

## Prompt

You are building a multi-agent team that takes a raw GitHub issue and outputs a fully tested Python function. Design the architecture before writing code.

Before designing the roster, complete the same management check from Assignment 00A: explain why this should not be one "super agent." A useful analogy is a release room: the Product Manager owns intent, the Coder owns implementation, QA owns evidence, Security owns risk, and Release owns the final gate.

## Deliverables

1. Single-agent limitation note: identify three pressures that require multiple agents.
2. Agent roster with at least four agents: Product Manager, Coder, QA Tester, and Security Reviewer.
3. Interaction-pattern label: cooperative, hierarchical, heterogeneous, or mixed, with one-sentence justification.
4. Architecture choice: vertical, horizontal, or hybrid, with one risk if the wrong architecture is chosen.
5. A typed handoff contract for each transition: issue -> `TaskSpec`, `TaskSpec` -> `CodePatch`, `CodePatch` -> `TestResult`, `TestResult` -> `ReviewDecision`.
6. Tool governance matrix mapping each agent to allowed MCP tools and denied tools.
7. SOP flow showing normal path and repair path.
8. One TeamLog commitment and one Theory-of-Mind memory entry.

## Technical Constraints

- Every agent-to-agent handoff must use a named schema.
- No agent may receive all tools.
- The repair path must include a bounded retry policy.
- Sensitive memory must only be visible to authorized roles.

## Grading Rubric

- Multi-agent justification and architecture choice: 20%
- Schema and handoff clarity: 30%
- Tool governance and zero-trust reasoning: 30%
- Self-repair and alignment design: 20%
