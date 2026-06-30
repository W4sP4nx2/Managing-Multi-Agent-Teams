# Assignments & Exercises Index

This index is the course manager for learner work. It keeps the assignment path aligned with the mission of **Managing Multi-Agent Teams**: learners are not building random agents; they are learning to manage an AI workforce through typed contracts, governed tools, shared memory, bounded autonomy, API/A2A boundaries, and human oversight.

Start with the repository front door, then use this file as the assignment map:

- Course overview: [../README.md](../README.md)
- Setup and verification: [../SETUP.md](../SETUP.md)
- Notebook order: [../notebooks/notebook_manifest.yml](../notebooks/notebook_manifest.yml)
- Resource library: [../resources/README.md](../resources/README.md)

## How To Use This Index

1. Run the setup guide and sandbox preflight first.
2. Complete Assignment 00A before NB1 if learners need the conceptual foundation for why multi-agent systems exist.
3. Complete notebook exercises in order from NB1 through NB6 before the capstone track.
4. Use NB8, NB9, NB10, and NB11 when the assignment requires API boundaries, orchestration, human steering, or A2A security.
5. Treat [../crewai_learning/README.md](../crewai_learning/README.md) as a separate self-contained framework study path after the governance shell is understood.
6. Use starter code only where the assignment asks for implementation; otherwise submit diagrams, schemas, policies, or written design artifacts.

## Building Blocks

| Building Block | What Learners Practice | Evidence To Produce |
| --- | --- | --- |
| Single Agent Limit | Know when one agent is structurally insufficient | Failure-pressure table and upgrade path |
| Interaction Pattern | Identify cooperative, competitive, mixed, hierarchical, heterogeneous, and mixture-of-experts systems | Scenario classification and governance control |
| Architecture Choice | Select vertical, horizontal, or hybrid architecture | Decision matrix with risk if wrong |
| Agent Roster | Assign clear worker roles, goals, responsibilities, and failure paths | Role table, SOPs, handoff map |
| Typed Handoff | Convert loose text into strict Pydantic contracts | Valid models and rejected invalid payloads |
| Shared Memory | Preserve commitments while enforcing need-to-know access | Memory search with visibility and sensitivity filters |
| Tool Gateway | Put tools behind identity, scope, and trust-tier checks | Denied tool call plus audit evidence |
| Repair Loop | Feed schema/test failures back into bounded retries | Retry trace, repair memory, escalation ticket |
| Routing | Allocate work by risk, complexity, cost, and budget | Route decision and route trace |
| API Boundary | Turn external requests into governed internal work | `202`, `403`, task ID, status response |
| A2A Perimeter | Treat cross-organization agents as untrusted network traffic | Incident ticket and dead-letter evidence |
| Human Steering | Translate human intent into durable TeamLog state | Project plan, commitment update, review decision |
| Framework Bridge | Express the same concepts in CrewAI/LangGraph patterns | Context chain, hierarchical delegation, governed tool wrapper |

## Core Assignment Sequence

| Number | Assignment | Main Artifact | Learner Builds | Required Evidence |
| --- | --- | --- | --- | --- |
| Preflight | Controlled Jupyter Sandbox | [../notebooks/00_sandbox_preflight.ipynb](../notebooks/00_sandbox_preflight.ipynb) | A verified offline notebook environment | Package checks, working directory check, `/tmp` write probe |
| Assignment 00 | Assignment Syllabus | [assignment_syllabus.md](assignment_syllabus.md) | A mental model for the whole assignment path | Learner can explain the building blocks and scope exclusions |
| Assignment 00A | Multi-Agent Systems Foundations | [multi_agent_systems_foundations.md](multi_agent_systems_foundations.md) | Evolution from single agent to managed multi-agent teams, interaction patterns, architecture decisions, and failure maps | Learner can justify why a task needs multiple agents and which governance controls prevent predictable failures |
| Assignment 01 | Agent Roster & SOPs | [foundational_architecture_design.md](foundational_architecture_design.md) | A managed team design before implementation | Non-overlapping roles, handoff artifacts, failure paths |
| Assignment 02 | Basic Agent Governance Labs | [basic_agent_governance_labs.md](basic_agent_governance_labs.md) | Logistics Weather, Writer, QA, and CEO builder labs | Each lab proves a schema, boundary, memory rule, denial, or escalation |
| Assignment 03 | Type-Safe Handoffs | [ex2_1_type_safe_handoffs.md](ex2_1_type_safe_handoffs.md) | Customer-service handoffs with strict schemas | `TranscriptAnalysis`, `QualityEvaluation`, `FinalReport`, and rejection demo |
| Assignment 04 | Theory-of-Mind Memory | [ex2_tom_memory.md](ex2_tom_memory.md) | Governed shared memory and hidden constraints | Coder finds PostgreSQL constraint and cannot read restricted secrets |
| Assignment 05 | MCP Tool Governance | [ex2_3_mcp_tool_governance.md](ex2_3_mcp_tool_governance.md) | Tool scopes, trust tiers, and audit events | Unauthorized tool call is denied and logged |
| Assignment 06 | RAG & MCP Architecture | [advanced_implementation_governance.md](advanced_implementation_governance.md) | Memory plus tool-boundary architecture | Diagram shows where identity, sensitivity, retrieval, and policy are enforced |
| Assignment 07 | API Boundary & Async Orchestration | [../notebooks/08_api_boundaries_async_orchestration.ipynb](../notebooks/08_api_boundaries_async_orchestration.ipynb) | FastAPI gateway, async task store, status endpoint | Internal admin receives `202`; external high-risk request receives `403` |
| Assignment 08 | Internal Brain: Advanced Orchestration | [../notebooks/09_advanced_fugu_orchestration.ipynb](../notebooks/09_advanced_fugu_orchestration.ipynb) | Dynamic scaffold, debate record, escalation path | High-risk work inserts SecurityReviewer; unresolved debate escalates |
| Assignment 09 | External Steering Wheel: CEO Interface | [../notebooks/10_vibe_coding_interface.ipynb](../notebooks/10_vibe_coding_interface.ipynb) | Natural-language steering converted into typed state | Mid-flight change updates TeamLog and downstream agents adapt |
| Assignment 10 | Enterprise A2A Perimeter | [../notebooks/11_enterprise_a2a_perimeter.ipynb](../notebooks/11_enterprise_a2a_perimeter.ipynb) | Cross-organization identity and payload defense | Malicious or restricted payload is blocked, ticketed, and quarantined |
| Assignment 11 | Trust & Governance Matrix | [ex4_trust_governance_matrix.md](ex4_trust_governance_matrix.md) | Enterprise role/tool/data authorization | Least-privilege matrix with explicit denial cases |
| Assignment 12 | From Whisper to Shipped Code | [assignment12_from_whisper_to_shipped_code.md](assignment12_from_whisper_to_shipped_code.md) | NB9 internal brain connected to NB10 human steering | Human request becomes typed plan, scaffold, debate, TeamLog pivot, and release decision |
| Assignment 13 | Virtual Software Company Capstone | [ex4_1_capstone_month_plan.md](ex4_1_capstone_month_plan.md) and [ex5_capstone_virtual_software_company.md](ex5_capstone_virtual_software_company.md) | End-to-end governed software team | Typed `PullRequestSummary` that ships or escalates through bounded governance |

## Notebook Exercise Map

These are practice exercises inside notebooks, not separate grading rubrics. They exist so learners can build the primitive before submitting the related assignment.

| Notebook | Exercise Theme | Assignment Connection |
| --- | --- | --- |
| [NB1](../notebooks/01_hello_multi_agent.ipynb) | Baseline collaboration and governed Logistics Weather builder lab | Assignment 01 and Assignment 02 |
| [NB2](../notebooks/02_shared_rag_memory.ipynb) | Shared memory, Theory of Mind, context compression | Assignment 04 |
| [NB3](../notebooks/03_mcp_tool_gateway.ipynb) | Zero-trust MCP-style tool gateway | Assignment 05 and Assignment 11 |
| [NB4](../notebooks/04_pydantic_delegation.ipynb) | Pydantic handoff contracts and hallucination rejection | Assignment 03 |
| [NB5](../notebooks/05_self_repair_loop.ipynb) | ChatDev-style bounded repair and Writer repair lab | Assignment 02 and Assignment 13 |
| [NB6](../notebooks/06_dynamic_routing.ipynb) | Fugu-style rule-based routing and budget awareness | Homework E |
| [NB7](../notebooks/07_debugging_agents.ipynb) | Broken-agent sandbox for schema drift, tool overreach, memory leakage, and loops | Assignment 02 support |
| [NB8](../notebooks/08_api_boundaries_async_orchestration.ipynb) | API gateway, async orchestration, and status polling | Assignment 07 and Assignment 13 |
| [NB9](../notebooks/09_advanced_fugu_orchestration.ipynb) | Dynamic scaffolds, debate, topology, typed delegation | Assignment 08 and Assignment 12 |
| [NB10](../notebooks/10_vibe_coding_interface.ipynb) | Vibe Coding CEO interface and TeamLog steering | Assignment 09 and Assignment 12 |
| [NB11](../notebooks/11_enterprise_a2a_perimeter.ipynb) | Enterprise A2A perimeter and adversarial QA lab | Assignment 10 and Assignment 11 |

## Starter Code Map

| Starter File | Supports | Learner Implements |
| --- | --- | --- |
| [starter_code/ex2_memory_system_starter.py](starter_code/ex2_memory_system_starter.py) | Assignment 04 | `SharedMemory.search()` and design creation from governed memory |
| [starter_code/ex4_governance_matrix_starter.py](starter_code/ex4_governance_matrix_starter.py) | Assignment 05 and Assignment 11 | `GovernancePolicy.authorize()` with scope and trust-tier checks |
| [starter_code/ex5_capstone_starter.py](starter_code/ex5_capstone_starter.py) | Assignment 13 | Orchestration loop, repair budget, release summary, and capstone extension points |
| [starter_code/module7_individual_agent_skills_starter.py](starter_code/module7_individual_agent_skills_starter.py) | Homework A | Specialist agent skill functions |
| [starter_code/module8_production_ready_features_starter.py](starter_code/module8_production_ready_features_starter.py) | Homework B | HITL, benchmarking, cost-aware caching, and memory controls |
| [starter_code/module9_deployment_operations_starter.py](starter_code/module9_deployment_operations_starter.py) | Homework C | Operations, sandbox, observability, and configuration versioning |
| [starter_code/module10_hr_governance_starter.py](starter_code/module10_hr_governance_starter.py) | Homework D | PII redaction and promotion approval governance |
| [starter_code/module11_marketing_orchestration_starter.py](starter_code/module11_marketing_orchestration_starter.py) | Homework E | Budget routing and brand-safety repair |
| [starter_code/module12_advanced_orchestration_starter.py](starter_code/module12_advanced_orchestration_starter.py) | Homework F | Discussion-support schemas for orchestration concepts |

## Extension Homework Sequence

The extension homework track is optional unless assigned by the instructor. It deepens the course without changing the six-module core.

| Homework | File | Purpose | Learner Experience |
| --- | --- | --- | --- |
| Homework A | [module7_individual_agent_skills.md](module7_individual_agent_skills.md) | Make specialists competent, not just governed | Code quality, test generation, security scanning, documentation agents |
| Homework B | [module8_production_ready_agent_features.md](module8_production_ready_agent_features.md) | Add human oversight and measurement | HITL approval, benchmarks, cost-aware caching, memory forgetting, A2A OpenAPI |
| Homework C | [module9_deployment_operations.md](module9_deployment_operations.md) | Move from notebook to operations | Containerization, observability, sandboxing, version control |
| Homework D | [module10_hr_governance.md](module10_hr_governance.md) | Practice high-stakes data governance | PII redaction, bias-safe handoffs, human approval |
| Homework E | [module11_marketing_orchestration.md](module11_marketing_orchestration.md) | Practice scale and budget governance | Campaign routing, budget halt, brand safety, hallucination repair |
| Homework F | [module12_advanced_orchestration.md](module12_advanced_orchestration.md) | Discuss advanced orchestration without turning into ML training | Learned orchestration, scaffolds, debate, adaptive topology as design concepts |
| Homework G | [module14_crewai_orchestration_patterns.md](module14_crewai_orchestration_patterns.md) and [../crewai_learning/README.md](../crewai_learning/README.md) | Study production framework expression separately from core notebooks | CrewAI agents, tasks, context chains, hierarchy, file outputs, and hybrid governance |

## Framework Bridge

The core assignments teach the governance primitives underneath any framework. The CrewAI/LangGraph study path shows how those primitives appear in production tools:

| Course Primitive | CrewAI Expression | LangGraph Expression |
| --- | --- | --- |
| Agent roster | `Agent(role=..., goal=..., backstory=...)` | Node responsibility |
| Typed handoff | `Task(output_pydantic=...)` | State schema |
| Context chain | `context=[upstream_task]` | State fields passed between nodes |
| Tool scope | Agent `tools=[...]` plus governed wrappers | Tool node with policy check |
| Repair loop | Retry settings and guarded tasks | Conditional edge back to worker |
| Routing | Hierarchical manager process | Router node and conditional edges |

The point is not to replace the course governance shell with a framework. The point is to wrap framework convenience with the same contracts, policies, memory controls, and audit trails learners already built.

## Scope Lock

Assignments stay inside the course mission. They do not ask learners to build trading bots, clinical decision systems, low-level ML training pipelines, or algorithm-optimization projects. The scenarios use software delivery, logistics weather-risk checks, writing/review, A2A security, marketing governance, HR governance, and human CEO steering because those keep the focus on orchestration, safety, memory, economics, and accountability.
