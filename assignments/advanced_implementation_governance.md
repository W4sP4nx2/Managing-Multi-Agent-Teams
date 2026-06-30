# Advanced Exercise: Implement Type-Safe Self-Repair With Tool Governance

## Prompt

Extend `src/enterprise_agent_team.py` so the virtual software company can process two task types: math utility functions and string utility functions. The system must dynamically route tasks, enforce schemas, govern tools, and self-correct failed tests.

## Deliverables

1. New Pydantic schemas or discriminated unions for math and string task outputs.
2. A LangGraph or equivalent state graph with explicit nodes for PM, router, coder, QA, reviewer, and repair memory.
3. An MCP-compatible tool boundary with at least two tools and per-agent authorization.
4. Unit tests or notebook cells proving that invalid patches and unauthorized tool calls are rejected.
5. A short governance note explaining how the design maps to IoA or AGNTCY-style zero-trust A2A interoperability.

## Technical Constraints

- Use `extra="forbid"` or equivalent strict schema enforcement.
- Do not pass raw LLM strings between agents as executable instructions.
- Tool calls must include agent identity, requested tool, arguments, and data sensitivity.
- The repair loop must stop after a fixed retry budget and escalate.

## Grading Rubric

- Correct implementation of typed orchestration and routing: 40%
- Security controls and MCP-style governance: 35%
- Evidence of self-correction and test coverage: 25%
