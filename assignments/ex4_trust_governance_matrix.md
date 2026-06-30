# Ex4: Trust & Governance Matrix

## Prompt

Design and implement the governance layer for a production multi-agent workflow. Your design should follow enterprise agentic automation practices emphasized by IBM and Anthropic: explicit agent identity, typed A2A messages, tool permissions, agent-to-agent monitoring, and zero-trust policy checks before every tool execution.

In Andrew Ng terms: a multi-agent team should not be trusted because the agents sound smart. It should be trusted because every handoff is typed, every tool call is authorized, and every denied action leaves evidence.

## Scenario

An internal HR team collaborates with a vendor reporting agent to screen candidates and generate a compliance report. The Resume Parser may read resume text. The Bias Checker may run fairness checks and export approved reports. The vendor may export only public or approved confidential reports. No agent may bypass the governance gateway.

## Deliverables

1. Agent identity table with organization, role, trust tier, and cryptographic identity placeholder.
2. Tool governance matrix with allowed and denied MCP tools per agent.
3. A2A message schemas for at least three handoffs.
4. Data classification policy for public, confidential, and restricted content.
5. Threat mitigation matrix covering at least five risks: prompt injection, tool overreach, context leakage, stale identity, and unbounded delegation.
6. Runnable denial evidence showing that at least three unauthorized requests are blocked by policy.

## Technical Constraints

- No agent may have unrestricted tool access.
- Vendor agents must not access restricted internal memory.
- Every cross-org message must use a typed schema.
- Include one explicit policy denial example.
- Every tool call must produce an audit event with caller identity, requested tool, decision, and reason.

## Grading Rubric

- Zero-trust architecture completeness: 40%
- Typed A2A and data governance quality: 35%
- Threat analysis and mitigation practicality: 25%
