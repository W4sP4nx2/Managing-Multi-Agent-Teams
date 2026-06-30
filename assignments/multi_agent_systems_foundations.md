# Assignment 00A: Multi-Agent Systems Foundations

## Credits & Alignment

Source inspiration: IBM Multi-Agent Systems Educational Module, provided in the course source notes.

This assignment adapts the module's core ideas into this course's mission: learners are not memorizing categories for trivia. They are learning how a professor, architect, or technical lead decides **when one agent is not enough**, what type of multi-agent system is needed, and what governance layer keeps that system safe.

## Professor's Vision

Before learners write a `ToolPolicy` or a `CodePatch`, they need the big picture.

A single agent is like one brilliant employee with one overloaded inbox. It can answer, summarize, and call a tool, but it becomes fragile when the job requires multiple specialties, conflicting goals, long-running state, security boundaries, or parallel work.

A managed multi-agent team is like an airport control tower, newsroom, or software release room:

- Each specialist has a role.
- The shared plan is visible.
- Sensitive information is need-to-know.
- Tool access is governed.
- Disagreements are escalated.
- Failures leave evidence.

This assignment gives learners the vocabulary and judgment to choose the right team shape before they touch implementation.

## Learning Objectives

By the end, learners can:

1. Explain why single-agent systems fail under scale, specialization, and accountability pressure.
2. Classify common multi-agent systems as cooperative, competitive, mixed, hierarchical, heterogeneous, or mixture-of-experts.
3. Choose vertical, horizontal, or hybrid architecture for a business scenario.
4. Map interaction patterns to governance controls: schemas, memory visibility, tool authorization, repair loops, and audit trails.
5. Identify the management failure prevented by each technical pattern.

## Building Blocks

| Building Block | Analogy | Course Connection |
| --- | --- | --- |
| Single Agent Limit | One employee handling product, security, QA, and release alone | Why NB1 starts simple but cannot stay simple |
| Cooperative Agents | A relay team passing a baton | Typed handoffs and context chains |
| Competitive Agents | Two vendors bidding for a route | Debate records, arbitration, and human review |
| Mixed System | Ride dispatch balancing driver, rider, and platform incentives | Tool policy plus TeamLog commitments |
| Hierarchical System | Incident commander coordinating specialists | NB9 scaffolds and NB10 CEO steering |
| Heterogeneous Team | Specialists with different jobs and tools | Coder, QA, Security, Release, PM specialization |
| Mixture of Experts | Routing a question to the right expert desk | NB6 routing and framework bridge |
| Vertical Architecture | Control tower | API gateway, centralized policy, release approval |
| Horizontal Architecture | Peer review room | Agent-to-agent protocols and shared state |
| Hybrid Architecture | Manager sets goal; specialists choose methods | Capstone orchestration and CrewAI/LangGraph bridge |

## Exercise 00A.1: The Single-Agent Stress Test

### Story

You hired one "super agent" to handle a software issue: read the GitHub ticket, design the feature, write code, test it, scan for security issues, and release it.

It works in a demo. Then the ticket includes a hidden constraint, an unsafe file path, a failing test, and a request from an external vendor.

### Mission

Write a short analysis showing where the single agent breaks.

Use this table:

| Failure Pressure | What Breaks In A Single Agent | Multi-Agent Control Needed |
| --- | --- | --- |
| Specialization |  |  |
| Tool security |  |  |
| Hidden constraints |  |  |
| Test failure |  |  |
| External requester |  |  |

### Required Evidence

- At least five failure pressures.
- Each pressure maps to one course control: Pydantic schema, MCP gateway, SharedMemory, repair loop, route decision, or human review.
- One sentence explaining why "just improve the prompt" is not enough.

### Production Takeaway

Single-agent prompting fails when the job requires management. Multi-agent systems are not about adding chatter; they are about adding roles, boundaries, and accountability.

## Exercise 00A.2: Classify The Interaction Pattern

### Story

You are the course architect reviewing proposed student projects. Some need agents to cooperate. Some need debate. Some need routing. Some need a manager.

### Mission

Classify each scenario using one primary pattern:

- Cooperative
- Competitive
- Mixed
- Hierarchical
- Heterogeneous
- Mixture of Experts

| Scenario | Pattern | Why | Governance Control |
| --- | --- | --- | --- |
| PM -> Coder -> QA -> Security -> Release |  |  |  |
| Two reviewers disagree about whether a patch is safe |  |  |  |
| Marketing wants 500 copy variants under a fixed budget |  |  |  |
| External security agent sends a scan result over HTTP |  |  |  |
| CEO changes the database choice mid-workflow |  |  |  |
| Researcher, Writer, Editor, and Fact Checker build a report |  |  |  |
| A router sends simple tasks to cheap models and high-risk tasks to reasoning models |  |  |  |
| A vendor agent tries to export restricted logs |  |  |  |
| A QA agent red-teams an internal A2A gateway |  |  |  |
| A manager creates a different workflow for low-risk and high-risk issues |  |  |  |

### Required Evidence

- One pattern per scenario.
- A one-sentence justification.
- A matching governance control for each scenario.

### Production Takeaway

The interaction pattern tells you what can go wrong. Cooperative systems need clean handoffs. Competitive systems need arbitration. Hierarchical systems need manager accountability. A2A systems need perimeter security.

## Exercise 00A.3: Architecture Decision Matrix

### Story

A manager asks, "Should this be centralized, decentralized, or hybrid?"

That is not a style preference. It is a risk decision.

### Mission

Choose an architecture for each scenario:

- Vertical: centralized manager or policy gateway controls the flow.
- Horizontal: agents coordinate peer-to-peer.
- Hybrid: centralized governance with decentralized specialist execution.

| Scenario | Architecture | Why | Risk If Wrong |
| --- | --- | --- | --- |
| Internal software release with security approval |  |  |  |
| Peer agents collaboratively summarize public documents |  |  |  |
| Cross-organization payroll/security scan request |  |  |  |
| Logistics weather-risk workflow for shipments |  |  |  |
| CEO-driven Vibe Coding session with mid-flight changes |  |  |  |
| Research writing pipeline with strict final delivery format |  |  |  |

### Required Evidence

- Architecture choice for each scenario.
- One risk of choosing the wrong architecture.
- One course artifact that supports the choice, such as `ToolPolicy`, `TaskSpec`, `TeamCommitment`, `WorkflowScaffold`, or `SecurityIncidentTicket`.

### Production Takeaway

Architecture is management encoded in software. Vertical systems protect sensitive decisions. Horizontal systems increase flexibility. Hybrid systems are often the enterprise default: central policy, specialist execution.

## Exercise 00A.4: Build A Minimal Pattern Catalog

### Story

Your future team will ask, "What kind of multi-agent system are we building?"

You need a reusable catalog they can consult before coding.

### Mission

Create a one-page pattern catalog with six rows:

| Pattern | Best Used When | Avoid When | Required Governance |
| --- | --- | --- | --- |
| Cooperative |  |  |  |
| Competitive |  |  |  |
| Mixed |  |  |  |
| Hierarchical |  |  |  |
| Heterogeneous |  |  |  |
| Mixture of Experts |  |  |  |

### Required Evidence

- Each row includes one concrete course scenario.
- Each row names at least one failure mode.
- Each row names a guardrail from the course.

### Production Takeaway

Pattern catalogs prevent architecture drift. They help teams choose a design because it fits the management problem, not because it sounds trendy.

## Exercise 00A.5: Failure Mode Map

### Story

Multi-agent systems fail differently from single-agent systems. One bad agent output can ripple through memory, tools, routing, and release.

### Mission

Build a failure mode map for a managed software team.

Use these failure classes:

- Agent malfunction.
- Coordination breakdown.
- Unpredictable behavior.
- Tool overreach.
- Memory leakage.
- Infinite repair loop.

| Failure Class | Example | Detection Signal | Mitigation |
| --- | --- | --- | --- |
| Agent malfunction |  |  |  |
| Coordination breakdown |  |  |  |
| Unpredictable behavior |  |  |  |
| Tool overreach |  |  |  |
| Memory leakage |  |  |  |
| Infinite repair loop |  |  |  |

### Required Evidence

- One detection signal per failure class.
- One mitigation per failure class.
- At least three mitigations must be typed artifacts, not prose policies.

### Production Takeaway

Failure is not an exception in multi-agent systems. It is part of the workflow. A managed team must detect, contain, repair, or escalate every predictable failure mode.

## Grading Rubric

| Criterion | Weight |
| --- | --- |
| Correct classification of interaction patterns and architectures | 30% |
| Clear mapping from management problem to technical guardrail | 30% |
| Production-quality failure analysis | 25% |
| Clear analogies and concise explanations | 15% |

## Submission Checklist

- [ ] Single-agent stress test is complete.
- [ ] Ten scenarios are classified by interaction pattern.
- [ ] Six scenarios are mapped to vertical, horizontal, or hybrid architecture.
- [ ] Pattern catalog includes guardrails and failure modes.
- [ ] Failure mode map includes detection and mitigation.
- [ ] No healthcare diagnosis, trading execution, or ML-training task is introduced.
