# Assignment Syllabus: Managing Multi-Agent Teams

This syllabus explains how the assignments fit together. The course is not asking learners to build random agents. It is training them to manage an AI workforce through typed contracts, governed tools, shared memory, bounded autonomy, A2A security, and human oversight.

## Scope Lock

The assignment track excludes:

- Trading bots, portfolio strategy, or market execution.
- Healthcare diagnosis, clinical triage, or medical calculation.
- Low-level ML training, fine-tuning, backpropagation, or algorithm optimization.

Assignments use software delivery, logistics weather-risk checks, writing/review, A2A security, and human CEO steering because those scenarios keep attention on orchestration, security, memory, and bounded autonomy.

## Learning Experience

Each assignment should feel like a small management simulation:

1. A team receives work.
2. A boundary converts messy intent into typed state.
3. Agents act only through allowed tools and visible memory.
4. Failures produce structured evidence.
5. The system repairs within a budget or escalates.
6. The final artifact can be audited by a human.

The instructor should keep asking one question: **What management failure does this technical pattern prevent?**

## Building Blocks

| Block | Skill | Evidence |
| --- | --- | --- |
| Handoff | Agents pass work through explicit artifacts | `TaskSpec`, `CodePatch`, `TestResult`, `ReviewDecision` |
| Type Safety | Raw LLM output becomes validated state | Pydantic rejects extra fields, invalid enums, unsafe paths |
| Tool Governance | Agents request tools through policy gates | `ToolRequest`, `ToolResult`, denied audit events |
| Shared Memory | Agents recover commitments without leaking secrets | role-filtered memory search and sensitivity checks |
| TeamLog | Global commitments override local agent goals | no-network, database choice, or release constraints are enforced |
| Repair | Failure evidence feeds the next attempt | typed feedback, repair memory, retry budget |
| Routing | Work is allocated by cost, complexity, and risk | route trace and budget preflight |
| API/A2A | External systems become governed internal requests | `202 Accepted`, identity mapping, incident tickets, DLQ |
| Human Steering | Natural language becomes durable team state | `ProjectPlan`, `TeamCommitment`, `HumanReviewDecision` |

## Assignment Path

| Number | Assignment | Professor's Vision | Learner Builds | Success Evidence |
| --- | --- | --- | --- | --- |
| 1 | Assignment 01: Agent Roster & SOPs | Learners first learn to design a team before coding one. | Agent roles, handoff artifacts, SOPs, and failure paths. | Roster has clear ownership and no overlapping responsibilities. |
| 2 | Assignment 02: Basic Agent Governance Labs | Simple agents become governed systems. | Logistics Weather gateway, bounded Writer loop, adversarial QA perimeter, CEO TeamLog steering. | Each lab proves a schema, a boundary, and an escalation or denial path. |
| 3 | Assignment 03: Type-Safe Handoffs | Learners stop passing raw text between agents. | `TranscriptAnalysis`, `QualityEvaluation`, `FinalReport`. | Invalid handoffs fail validation and valid outputs become structured JSON. |
| 4 | Assignment 04: Theory-of-Mind Memory | Learners learn that shared memory is not open memory. | Memory records, visibility rules, role-filtered retrieval. | Coder finds PM constraint but cannot read restricted secrets. |
| 5 | Assignment 05: MCP Tool Governance | Learners learn that tool access is the riskiest moment. | Governance policy, tool scopes, trust tiers, audit log. | Unauthorized tool call is denied and logged. |
| 6 | Assignment 06: RAG & MCP Architecture | Learners connect memory, retrieval, and tools into one nervous system. | Architecture diagram, contracts, and governance plan. | Design shows where identity, sensitivity, and policy are enforced. |
| 7 | Assignment 07: API Boundary | Learners expose the agent team safely to external systems. | FastAPI gateway, async task store, status endpoint. | Internal admin receives `202`; external vendor high-risk request receives `403`. |
| 8 | Assignment 08: Internal Brain | Learners build dynamic scaffolds and debate protocols. | `WorkflowScaffold`, `DebateRecord`, `EscalationTicket`. | High-risk work inserts SecurityReviewer and unresolved contention escalates. |
| 9 | Assignment 09: External Steering Wheel | Learners make the human manager explicit. | Natural-language directives parsed into typed project state. | Mid-flight change updates TeamLog and downstream agents adapt. |
| 10 | Assignment 10: Enterprise A2A Perimeter | Learners secure cross-organization agent messages. | A2A message validation, schema drift rejection, DLQ. | Malicious or restricted payload is blocked, ticketed, and quarantined. |
| 11 | Assignment 11: Trust & Governance Matrix | Learners design enterprise-scale access rules. | Identity matrix, tool matrix, data classification, A2A rules. | Every role has least-privilege access and explicit denial cases. |
| 12 | Assignment 12: From Whisper to Shipped Code | Learners connect NB9's internal brain to NB10's external steering wheel. | Translation, scaffold, debate, TeamLog pivot, human approval, release summary. | A human whisper becomes a typed, governed, shipped artifact. |
| 13 | Assignment 13: Virtual Software Company Capstone | Learners integrate the whole course. | PM, Tech Lead, Coder, QA, Security, Release, memory, tools, repair, API. | System ships or escalates through a typed `PullRequestSummary`. |

## Extension Homework

| Homework | Purpose | Learner Experience |
| --- | --- | --- |
| Homework A: Specialist Agent Skills | Make specialists competent, not just governed. | Build code-quality, test-generation, security-scan, and documentation agents. |
| Homework B: Production Controls | Add human oversight and measurement. | Implement HITL approval, benchmarks, cost-aware caching, and memory forgetting. |
| Homework C: Deployment & Operations | Move from notebook to operations. | Containerize, observe, sandbox, and version agent configurations. |
| Homework D: HR Governance | Practice high-stakes data governance. | Redact PII, prevent bias-safe handoff leakage, and require human approval. |
| Homework E: Marketing Orchestration | Practice scale and budget governance. | Route campaign tasks by cost, enforce brand safety, and repair hallucinated drafts. |
| Homework F: Advanced Fugu Discussion | Discuss advanced orchestration without turning into ML training. | Analyze learned orchestration, scaffolds, debate, and topology as design concepts. |
| Homework G: CrewAI Applied Pipeline Engineering | Study a production framework separately from the core governance notebooks. | Compare sequential/hierarchical processes, context chains, guardrails, and clean delivery. |
