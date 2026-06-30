# Managing Multi-Agent Teams: Agentic AI & Vibe Coding

This GitHub page is the learner-facing course overview. It explains what the course is, what learners will build, and how the modules fit together.

Start here:

- Setup: [00_welcome/setup_guide.md](00_welcome/setup_guide.md)
- Notebook order: [notebooks/notebook_manifest.yml](notebooks/notebook_manifest.yml)
- Assignment path: [assignments/index.md](assignments/index.md)
- Resource library: [resources/README.md](resources/README.md)
- Workspace map and asset inventory: [00_welcome/README.md](00_welcome/README.md)

## Course Promise

By the end of this course, learners can design, build, test, and govern a production-grade multi-agent system that turns a raw software request into validated code through typed delegation, tool governance, shared memory, and self-repair.

## Course Philosophy

Most Agentic AI courses teach you how to make agents talk. This course teaches you how to manage them when they lie, fail, and hallucinate. We do not rely on the LLM to be perfect. We rely on Pydantic schemas to enforce contracts, MCP gateways to enforce security, and bounded repair loops to enforce resilience. You will learn to build systems that are safe to deploy on Monday morning.

The offline notebooks intentionally use deterministic mocks first. That is not because the LLM is unimportant; it is because the governance layer must be understood before API keys, rate limits, and model variability enter the room. Then the course shows the bridge: a mock LLM adapter that returns messy JSON, Pydantic rejection, repair feedback, and optional live LLM cells learners can enable with their own keys.

## Three-Layer Delivery Model

Layer 1: The Deterministic Shell. Learners first run Pydantic schemas, tool policies, shared memory, and bounded repair loops with predictable mocked agents. In this layer, we assume the agents are perfect so we can test the pipes, security gates, and contracts.

Layer 2: The Mock LLM Adapter. Next, learners introduce simulated LLM failure: messy JSON, hallucinated fields, unsafe paths, invalid enums, and missing fields. The governance shell catches the failure and sends validation feedback into the repair loop.

Layer 3: The Live LLM Integration. Finally, learners can enable optional `USE_LIVE_LLM = True` cells with their own API keys. The same schemas from Layer 1 now constrain a real model, and the same repair loop handles real nondeterminism.

Instructor script: "Look at the deterministic agent function. It is hard-coded on purpose. If we plugged in a real LLM before understanding the governance shell, we would not know whether a failure came from the schema, the gateway, the prompt, or the model. First we isolate the rules. Then we use the mock LLM adapter to simulate failure. Finally we flip on the live LLM and use the same contracts to govern the dynamic brain."

## Audience

This course is for engineers, technical leads, AI builders, and curriculum facilitators who already understand basic LLM prompting and want to move into managed agent teams.

## Prerequisites

- Intermediate Python
- Basic JSON and API literacy
- Basic understanding of LLM prompting
- Comfort reading stack traces and test output
- Optional: prior exposure to CrewAI, AutoGen, LangGraph, MCP, or Pydantic

## Learning Objectives

After completing the course, learners will be able to:

1. Explain why single-agent prompting breaks down for complex software workflows.
2. Design agent rosters, SOPs, and typed handoff contracts.
3. Implement shared memory patterns inspired by TeamLog and Theory of Mind.
4. Use MCP-style tool boundaries and zero-trust authorization policies.
5. Build Pydantic-enforced inter-agent contracts.
6. Implement bounded self-repair loops based on ChatDev architecture.
7. Route tasks across heterogeneous model classes using Fugu-style routing, then explain how learned orchestration extends beyond static rules.
8. Design enterprise-grade agent ecosystems with identity, permissions, and A2A schemas.
9. Manage an AI workforce through a human CEO interface that turns natural-language directives into typed plans, commitments, dispatches, and approvals.
10. Secure cross-organization agent messages with an A2A perimeter, payload classification, schema checks, and dead-letter auditing.
11. Compare custom orchestration with CrewAI-style production patterns for task dependencies, parallelism, artifact outputs, dynamic inputs, coding-agent teams, and hybrid governance.
12. Elevate beginner agents such as Logistics Weather, Writer, QA, and CEO assistants into governed production exercises with schemas, gateways, memory, repair budgets, A2A defense, and TeamLog.

## Module Map

| Module | Theme | Primary Artifact | Learner Outcome |
| --- | --- | --- | --- |
| Pre-Course | Controlled Jupyter Sandbox | NB0 | Verify packages, offline mode, working directory, and `/tmp` write access |
| 1 | Foundations & Vibe Coding | NB1 + Ex1 | Build a simple sequential agent team |
| 2 | TeamLog & Theory of Mind | NB2 + Ex2 | Use memory to preserve commitments, hidden constraints, and compressed long-term context |
| 3 | Agentic RAG & MCP | NB3 + Ex3 | Govern tool access through a standardized boundary |
| 4 | Pydantic AI & Type-Safety | NB4 | Enforce schemas between agents |
| 5 | Fugu Routing & ChatDev Self-Repair | NB5 + NB6 | Build bounded repair loops and rule-based heterogeneous routing |
| 6 | Internet of Agents & Zero-Trust | NB11 + Ex4 | Design and test secure interoperable A2A systems across organizational boundaries |
| API Boundary | Gateway & Async Orchestration | NB8 | Expose the system through governed HTTP endpoints |
| Advanced Orchestration | Fugu Concepts | NB9 + Assignment 08 + Homework F | Progress from rule-based routing to conceptual learned orchestration, dynamic scaffolds, debate, and adaptive topology |
| Vibe Coding CEO Interface | Human Manager Loop | NB10 + Assignment 09 | Manage an AI workforce through natural-language directives, plan edits, and final approval |
| Enterprise A2A Perimeter | Cross-Org Zero-Trust | NB11 | Block unsafe cross-organization messages and audit denied payloads |
| CrewAI Self-Contained Study Track | Production Framework Bridge | `crewai_learning/README.md` | Map course governance patterns to CrewAI-style crews, context chains, coding-agent teams, guardrails, failure recovery, and clean delivery |
| Capstone | Virtual Software Company | NB8 + Assignment 13 | Integrate all patterns end to end |

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
| Vibe Coding CEO Interface | NB10 | Teaches the human-manager interface: natural language becomes typed plans, commitments, dispatches, and approval decisions |
| Context Window Economics | NB2 upgrade | Teaches cognitive-load management through context compression and durable memory |
| Intelligent Orchestrator | NB9 upgrade | Bridges deterministic routing to typed LLM-manager delegation and escalation as a teaching adapter |
| From Whisper to Shipped Code | Assignment 12 | Connects NB9's Internal Brain with NB10's External Steering Wheel in one governed release journey |
| CrewAI Framework Bridge | `crewai_learning/README.md` | Shows when to use production orchestration frameworks, how to design a personal coding-agent team, and how to wrap framework convenience with course governance |
| Basic Agent Governance Labs | `assignments/basic_agent_governance_labs.md` | Gives instructors simple Logistics Weather, Writer, QA, and CEO exercises that still assess schemas, gateways, memory, repair, and escalation |
| Assignment Syllabus | `assignments/assignment_syllabus.md` | Gives the professor-level building-block map and learning experience for the whole assignment sequence |

## Scope Exclusions

To keep the course focused on **Managing Multi-Agent Teams**, we explicitly exclude:

- Trading bots, portfolio strategy, or market execution examples.
- Healthcare diagnosis, clinical triage, or medical calculation examples.
- Low-level ML training, fine-tuning, backpropagation, or algorithm optimization.

The course uses software delivery, logistics weather-risk checks, writing/review, A2A security, and human CEO steering because these scenarios keep attention on orchestration, security, memory, and bounded autonomy.

## Success Criteria

A learner is successful when they can:

- Set up the environment using the setup guide, run NB0 successfully, and complete the verification commands.
- Complete the core notebooks before attempting Assignment 12 and the capstone. Use NB9 and NB11 for advanced orchestration and enterprise perimeter practice, and use `crewai_learning/README.md` as a separate self-contained CrewAI study path.
- Explain the purpose of each schema, tool policy, and routing decision.
- Submit a capstone with typed contracts, governed tools, shared memory, and bounded repair.

An instructor is successful when they can:

- Teach all six modules in a two-day workshop.
- Grade each non-capstone assignment with the objective rubrics and solution guides.
- Use the solution guides to diagnose common learner mistakes.
- Connect each lab back to production reliability, security, and maintainability.

## Teaching Arc

The course follows an Andrew Ng-style progression:

1. Start with the intuitive problem.
2. Use a simple analogy.
3. Show the architecture.
4. Implement the smallest practical version.
5. Name the production failure mode.
6. Add the guardrail.
