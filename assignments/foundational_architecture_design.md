# Foundational Exercise: Design A Governed Agent Roster

## Prompt

You are building a multi-agent team that takes a raw GitHub issue and outputs a fully tested Python function. Design the architecture before writing code.

## Deliverables

1. Agent roster with at least four agents: Product Manager, Coder, QA Tester, and Security Reviewer.
2. A typed handoff contract for each transition: issue -> `TaskSpec`, `TaskSpec` -> `CodePatch`, `CodePatch` -> `TestResult`, `TestResult` -> `ReviewDecision`.
3. Tool governance matrix mapping each agent to allowed MCP tools and denied tools.
4. SOP flow showing normal path and repair path.
5. One TeamLog commitment and one Theory-of-Mind memory entry.

## Technical Constraints

- Every agent-to-agent handoff must use a named schema.
- No agent may receive all tools.
- The repair path must include a bounded retry policy.
- Sensitive memory must only be visible to authorized roles.

## Grading Rubric

- Schema and handoff clarity: 35%
- Tool governance and zero-trust reasoning: 35%
- Self-repair and alignment design: 30%
