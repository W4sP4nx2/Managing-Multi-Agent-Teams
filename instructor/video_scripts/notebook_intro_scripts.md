# Notebook "Why This Matters" Intro Scripts

## Instructor Delivery Pattern

For each module, use the same arc:

1. Naive approach: show what breaks without governance or skill.
2. Intervention: introduce the pattern, such as MCP, shared memory, TeamLog, bounded repair, or routing.
3. Production reality: show the typed, governed version catching the failure and recording evidence.

## NB1: Hello Multi-Agent

This notebook solves the first problem in multi-agent learning: seeing the handoff. One agent creates context, another agent uses it. In production, this becomes PM to coder, coder to QA, QA to reviewer. If you skip this, every advanced pattern feels abstract.

Instructor add-on: after the baseline handoff, introduce the Governed Logistics Weather Agent builder exercise. The analogy is an operations desk: the logistics coordinator asks for a weather-risk check, but the gateway checks identity, hides the API key, validates the request, and returns a typed shipping-risk receipt. This keeps a friendly first lab aligned with the course mission.

## NB2: Shared RAG Memory

This notebook solves the problem of agents forgetting what the team already decided. Shared memory lets constraints, acceptance criteria, and prior failures persist across roles. If you skip this, agents will keep rediscovering or contradicting decisions.

## NB3: MCP Tool Standardization

This notebook solves the problem of unsafe tool access. MCP gives tools a standard shape, and a policy gateway decides whether a specific agent may call a specific tool. If you skip this, your agents can become powerful but ungoverned.

## NB4: Pydantic Type-Safe Delegation

This notebook solves the problem of raw text pretending to be software. Pydantic schemas make every handoff executable and reject malformed outputs. If you skip this, downstream agents and tools consume hallucinated fields.

## NB5: Self-Repair Loop

This notebook solves the problem of first-draft failure. The system tests, records evidence, repairs, and stops after a budget. If you skip this, failures either ship silently or loop forever.

Instructor add-on: use the Bounded Writer Agent exercise to show the same repair principle outside code. The editor's typed feedback is the repair context. The retry budget is the management boundary.

## NB6: Dynamic Routing

This notebook solves the problem of using one model for every job. Fugu-style routing chooses a worker based on complexity, risk, and cost. If you skip this, systems become slow, expensive, and hard to govern.

## NB7: Debugging Agents

This notebook teaches the failure modes directly: schema drift, tool overreach, unbounded repair, and memory leakage. If you skip debugging, learners can build demos but struggle to diagnose production behavior.

## NB8: API Boundaries & Asynchronous Orchestration

This notebook solves the problem of agents living in a local Python vacuum. Real multi-agent systems are triggered by webhooks, tickets, and A2A HTTP calls. The API gateway becomes the governance perimeter: external JSON is authenticated, mapped to identity, validated into internal contracts, and launched asynchronously with status polling. If you skip this, your agents cannot safely connect to the outside world.

## NB9: Advanced Fugu Orchestration

This notebook is a discussion-to-code bridge. NB6 teaches transparent rule-based routing; NB9 shows dynamic scaffolds, debate, adaptive topology, and simple history-based routing updates. Keep the scope clear: this course is teaching orchestration management, not training learned orchestrator models.

## NB10: Vibe Coding CEO Interface

This notebook solves the human-manager interface. Natural language becomes a typed `ProjectPlan`, durable `TeamCommitment`, and final `HumanReviewDecision`. The key teaching move is to show that the Coder should not act on raw CEO text; it should act on governed TeamLog state.

## NB11: Enterprise A2A & Zero-Trust Perimeter

This notebook solves the cross-organization boundary problem. Internal and external agents exchange typed A2A messages, but the gateway checks organization, classification, schema, and payload safety before delivery. Use the Adversarial QA Agent exercise to show prompt injection and data exfiltration being blocked, ticketed, and quarantined.
