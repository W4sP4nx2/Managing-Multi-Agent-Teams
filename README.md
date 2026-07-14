# SRE for AI: Managing Multi-Agent Teams in Production

**Stop Vibe Coding. Start Managing Vibe Coders.**

This GitHub page is the learner-facing course overview. It explains what the course is, what learners will build, and how the modules fit together.

Start here:

- Setup guide: [SETUP.md](SETUP.md)
- Notebook order: [notebooks/notebook_manifest.yml](notebooks/notebook_manifest.yml)
- Assignment path: [assignments/index.md](assignments/index.md)
- Resource library: [resources/README.md](resources/README.md)

This README is the course overview. It is the front page learners should read first on GitHub: the promise, mission, module map, scope boundary, and success criteria all live here.

## Course Promise

By the end of this course, you will be the **Senior Staff Engineer** who can tame reckless AI agents. You'll build guardrails, circuit breakers, and zero-trust boundaries that prevent brilliant-but-unstable AI "junior developers" from taking down production. You'll ship a multi-agent system that survives real-world chaos: infinite loops, hallucinated credentials, sycophantic agreement loops, and budget overruns.

## Course Philosophy

**Most Agentic AI courses show you the magic. This course shows you the disaster—and then teaches you to prevent it.**

Week 1, you'll build an unconstrained CrewAI team. It will loop infinitely. It will hallucinate API keys. It will agree with its own bad code. You'll watch it burn tokens and crash.

Then we give you the superhero tools:
- **Pydantic schemas** as the sheriff that rejects malformed output
- **MCP gateways** as the zero-trust bouncer blocking dangerous commands
- **Theory of Mind** as the shared memory that prevents coordination failures
- **Bounded repair loops** as the automatic retry mechanism with escape hatches
- **Circuit breakers** as the budget enforcer that throws hard exceptions at $1.00

This isn't "vibe coding." This is **SRE for AI**—the enterprise-grade discipline of deploying agents safely on Monday morning.

## The Flip: Learn Pain Before Cure

| Phase | What You Build | What Breaks | What You Learn |
|-------|---------------|-------------|----------------|
| **NB1: The Wild West** | Raw Writer + Reviewer agents | Infinite sycophantic loop, hallucinated code | Why unconstrained agents fail |
| **NB2: The Pydantic Sheriff** | Rigid `ReviewTicket` schema | Free-text rejection becomes structured validation | Typed handoffs beat natural language |
| **NB3: The Sandbox** | MCP gateway with auth policies | Agent tries `rm -rf /`, gets blocked | Zero-trust tool boundaries |
| **NB4: The Bounded Repair** | ChatDev-style self-repair loop | Schema violations trigger auto-retry (max 3 attempts) | Resilience through capped recursion |
| **NB5+: Production Patterns** | DLQ, routing, budget breakers, A2A perimeter | Complex failures need complex guardrails | Enterprise AgentOps |

Live LLMs are available from Day 1 via Ollama (pre-installed in Codespaces). No API key anxiety. No rate limit surprises. Just pure, unfiltered chaos—and the tools to contain it.

## Audience

This course is for **Senior Backend Engineers, Technical Leads, and AI Builders** who need to deploy multi-agent systems to production. You already understand basic LLM prompting, but you've seen agents fail in embarrassing ways: infinite loops, hallucinated credentials, sycophantic agreement, budget overruns. You want enterprise-grade patterns—Zero-Trust AI, Bounded Autonomy, Typed Handoffs, and Agentic Circuit Breakers—that separate production-ready systems from weekend hobbyist demos.

## Prerequisites

- Intermediate Python
- Basic JSON and API literacy
- Basic understanding of LLM prompting
- Comfort reading stack traces and test output
- Optional: prior exposure to CrewAI, AutoGen, LangGraph, MCP, or Pydantic

## Learning Objectives

After completing the course, learners will be able to:

1. Explain why single-agent prompting breaks down for complex software workflows.
2. Classify multi-agent interaction patterns and choose vertical, horizontal, or hybrid architectures.
3. Design agent rosters, SOPs, and typed handoff contracts.
4. Implement shared memory patterns inspired by TeamLog and Theory of Mind.
5. Use MCP-style tool boundaries and zero-trust authorization policies.
6. Build Pydantic-enforced inter-agent contracts.
7. Implement bounded self-repair loops based on ChatDev architecture.
8. Route tasks across heterogeneous model classes using Fugu-style routing, then explain how learned orchestration extends beyond static rules.
9. Design enterprise-grade agent ecosystems with identity, permissions, and A2A schemas.
10. Manage an AI workforce through a human CEO interface that turns natural-language directives into typed plans, commitments, dispatches, and approvals.
11. Secure cross-organization agent messages with an A2A perimeter, payload classification, schema checks, and dead-letter auditing.
12. Compare custom orchestration with CrewAI-style production patterns for task dependencies, parallelism, artifact outputs, dynamic inputs, coding-agent teams, and hybrid governance.
13. Elevate beginner agents such as Logistics Weather, Writer, QA, and CEO assistants into governed production exercises with schemas, gateways, memory, repair budgets, A2A defense, and TeamLog.

## Module Map: From Chaos to Control

| Module | Theme | Primary Artifact | The "Aha!" Moment |
| --- | --- | --- | --- |
| **NB1** | The Wild West: Unconstrained Agents | Two agents in infinite loop | Watch your agents burn tokens agreeing with bad code |
| **NB2** | The Pydantic Sheriff | `ReviewTicket` schema | First time schema rejection stops hallucinated output |
| **NB3** | The Sandbox: MCP Gateway | Zero-trust auth policy | Agent tries `rm -rf /` and gets blocked |
| **NB4** | Bounded Repair Loop | ChatDev-style retry (max 3) | Auto-repair fixes schema violations without human intervention |
| **NB5-6** | Dynamic Routing & Circuit Breakers | Budget breaker at $1.00 | Hard exception prevents budget overrun |
| **NB7** | Dead-Letter Queue | DLQ serializer | Failed agents drop to human-review queue instead of crashing |
| **NB8** | API Boundary & Async Orchestration | Governed HTTP endpoints | External requests hit rate-limited, authenticated gateway |
| **NB9** | Advanced Orchestration Patterns | Learned routing vs static rules | LLM-as-router makes smarter decisions than hardcoded if-statements |
| **NB10** | Vibe Coding CEO Interface | Natural language → typed plans | Human directive becomes structured `ProjectPlan` + `TeamCommitment` |
| **NB11** | Enterprise A2A Perimeter | Cross-org payload auditor | Unsafe inter-agent message blocked and logged to DLQ |
| **Capstone** | Virtual Software Company | Dockerized CRUD API + tests | Multi-agent team ships production-ready microservice end-to-end |

## Basic Agent Governance Labs

These labs are the low-floor, high-ceiling bridge for learners who need simple scenarios before the capstone.

| Lab | Primary Notebook | What It Teaches |
| --- | --- | --- |
| Governed Logistics Weather Agent | NB1 | A friendly tool-use example becomes MCP-style identity, schema, and gateway governance |
| Bounded Writer Agent | NB5 | A familiar writer/editor loop becomes typed feedback, shared memory, retry budget, and escalation |
| Natural Language Becomes TeamLog | NB10 | Human directives become `ProjectPlan` and `TeamCommitment`, not loose downstream prompt text |
| Adversarial QA Agent | NB11 | QA becomes a red-team A2A perimeter test with typed incident tickets and Dead Letter Queue evidence |

## Extension Homework Track

The six-module core teaches learners how to manage multi-agent teams. The extension homework track teaches learners how to make individual agents skilled, production-ready, and operable without confusing those extensions with the required core sequence.

| Homework | Theme | Primary Artifact | Learner Outcome |
| --- | --- | --- | --- |
| Homework A | Specialist Agent Skills | `assignments/module7_individual_agent_skills.md` | Build code quality, test generation, security scanning, and documentation agents |
| Homework B | Production Controls | `assignments/module8_production_ready_agent_features.md` | Add human approval, benchmarks, cost control, long-term memory, and A2A OpenAPI contracts |
| Homework C | Deployment & Operations | `assignments/module9_deployment_operations.md` | Containerize, observe, sandbox, and version managed agents |
| Homework D | HR Governance Track | `assignments/module10_hr_governance.md` | Apply governance to PII redaction, bias-safe handoffs, and human approval |
| Homework E | Marketing Orchestration Track | `assignments/module11_marketing_orchestration.md` | Apply routing, budget, brand safety, and hallucination repair to campaign workflows |
| Homework F | Advanced Fugu Discussion | `assignments/module12_advanced_orchestration.md` | Optional reading and design discussion; not a graded implementation lab |
| Homework G | CrewAI Applied Pipeline Engineering | `crewai_learning/README.md` | Self-contained CrewAI study material for coding-agent teams, hierarchical research pipelines, guardrails, quality gates, and clean delivery |

## Critical Integrative Assignments

| Assignment | Artifact | Why It Matters |
| --- | --- | --- |
| Multi-Agent Systems Foundations | `assignments/multi_agent_systems_foundations.md` | Teaches when one agent is not enough, how to classify interaction patterns, and how to choose vertical, horizontal, or hybrid architecture |
| Vibe Coding CEO Interface | NB10 | Teaches the human-manager interface: natural language becomes typed plans, commitments, dispatches, and approval decisions |
| Context Window Economics | NB2 upgrade | Teaches cognitive-load management through context compression and durable memory |
| Intelligent Orchestrator | NB9 upgrade | Bridges deterministic routing to typed LLM-manager delegation and escalation as a teaching adapter |
| From Whisper to Shipped Code | Assignment 12 | Connects NB9's Internal Brain with NB10's External Steering Wheel in one governed release journey |
| CrewAI Framework Bridge | `crewai_learning/README.md` | Shows when to use production orchestration frameworks, how to design a personal coding-agent team, and how to wrap framework convenience with course governance |
| Basic Agent Governance Labs | `assignments/basic_agent_governance_labs.md` | Gives instructors simple Logistics Weather, Writer, QA, and CEO exercises that still assess schemas, gateways, memory, repair, and escalation |
| Assignment Syllabus | `assignments/assignment_syllabus.md` | Gives the professor-level building-block map and learning experience for the whole assignment sequence |
| Virtual Software Company Capstone | `assignments/ex5_capstone_virtual_software_company.md` | Requires an ADR, interaction-pattern map, and proof tests for malfunction, coordination complexity, and unpredictable behavior |

## Scope Exclusions

To keep the course focused on **Managing Multi-Agent Teams**, we explicitly exclude:

- Trading bots, portfolio strategy, or market execution examples.
- Healthcare diagnosis, clinical triage, or medical calculation examples.
- Low-level ML training, fine-tuning, backpropagation, or algorithm optimization.

The course uses software delivery, logistics weather-risk checks, writing/review, A2A security, and human CEO steering because these scenarios keep attention on orchestration, security, memory, and bounded autonomy.

## Success Criteria

A learner is successful when they can:

- **Set up the environment** using the setup guide, run NB0 successfully, and complete the verification commands.
- **Demonstrate the failure** by running NB1's unconstrained agents and watching them loop infinitely or hallucinate.
- **Deploy the first guardrail** in NB2 and show Pydantic rejecting malformed agent output.
- **Block a dangerous command** in NB3 by implementing zero-trust MCP gateway policies.
- **Auto-repair failures** in NB4 with bounded retry loops that fix schema violations without human intervention.
- **Complete the capstone** with a Dockerized CRUD API that includes typed contracts, governed tools, shared memory, circuit breakers, DLQ integration, and proof tests for malfunction scenarios.

## The Competitive Moat: SRE for AI

Most courses teach capabilities: "Make agents write a blog post." This course teaches **reliability**: "Make agents survive production."

| Other Courses | This Course |
|--------------|-------------|
| How to make agents talk | How to stop them from lying |
| Demo-ware that breaks in prod | Guardrails that deploy Monday morning |
| Unlimited token budgets | Circuit breakers at $1.00 |
| Free-text handoffs | Typed Pydantic contracts |
| Trust all tools | Zero-trust MCP gateways |
| Infinite retry loops | Bounded repair with DLQ escape |
| Single-org playground | Cross-org A2A perimeter defense |

**Key Terms You'll Master:** Zero-Trust AI, Bounded Autonomy, Typed Handoffs, Agentic Circuit Breakers, Dead-Letter Queues, Semantic Routing Gateways, A2A Perimeter Checks, Theory of Mind Memory, ChatDev Self-Repair, Fugu Dynamic Routing.

Instructor delivery materials live in [instructor/](instructor/). Use that folder for rubrics, solution guides, delivery checklists, verification commands, and teaching support.
