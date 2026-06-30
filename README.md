# Managing Multi-Agent Teams: Agentic AI & Vibe Coding

This workspace contains a complete training material set that moves learners from single-agent prompting to governed, type-safe, multi-agent systems.

## Philosophy

Most agent tutorials teach agents to talk. This course teaches learners to manage agents when they hallucinate, call the wrong tool, forget context, or fail tests. The offline path uses deterministic mocks so the contracts, governance, memory, and repair patterns are easy to inspect. The LLM bridge is then introduced through a mock adapter and optional live-key cells.

The course is delivered in three layers: deterministic shell first, mock LLM adapter second, live LLM integration third. That separation is intentional: learners debug the governance layer before model nondeterminism enters the room.

## Course Architecture

1. **The Brain**: TeamLog-style collective commitments and Theory of Mind memory.
2. **The Nervous System**: Agentic RAG and MCP-standardized tools.
3. **The Body**: Pydantic data contracts with CrewAI/AutoGen-style orchestration.
4. **The Reflexes**: Fugu-style heterogeneous routing and ChatDev self-repair loops.
5. **The Ecosystem**: Internet of Agents, AGNTCY-style interoperability, and Zero-Trust governance.

## Assets

- `00_welcome/course_overview.md`: syllabus, objectives, success criteria, and module map.
- `00_welcome/setup_guide.md`: environment setup, optional integrations, API keys, and verification.
- `resource_library.md`: curated research, frameworks, videos, and teaching materials.
- `resources/README.md`: GitHub-optimized resource library with papers, video transcripts, and cited schemas.
- `crewai_learning/README.md`: self-contained CrewAI learning guide for applied pipeline engineering, separate from the notebook sequence.
- `src/enterprise_agent_team.py`: runnable Python implementation.
- `guides/technical_implementation_guide.md`: production implementation notes and architecture diagram.
- `instructor/technical_implementation_playbook.md`: instructor scenarios for MCP, Agentic RAG, TeamLog, and ChatDev self-repair.
- `instructor/management_principle_matrix.md`: management principles, business impact, code evidence, and assessment prompts.
- `instructor/verification_pyramid.md`: automated test pyramid, delivery checklists, and CI-style commands.
- `instructor/course_manager_notebook_assignment_path.md`: canonical notebook path, sandbox policy, and assignment path for course managers.
- `instructor/course_delivery_readiness_checklist.md`: pre-course, weekly learning path, post-course deliverables, and pre-push checks.
- `instructor/curriculum_maintenance_checklist.md`: manual maintenance checklist for schema sync, notebook hygiene, secrets, and starter/solution drift.
- `instructor/a2a_identity_tool_matrix.md`: canonical role, trust tier, and tool matrix for A2A governance consistency.
- `tests/`: pytest suite covering schemas, tools, memory, handoffs, A2A/API boundaries, notebooks, and capstone flow.
- `slides/module_decks/`: six module-specific PowerPoint decks, 13 slides each.
- `slides/teaching_slides_content.md`: six-slide executive overview sequence.
- `slides/managing_multi_agent_teams_6_slide_sequence.pptx`: editable PowerPoint deck.
- `notebooks/notebook_manifest.yml`: canonical notebook order, runtime policy, package tiers, aliases, and assignment links.
- `notebooks/00_sandbox_preflight.ipynb`: controlled Jupyter sandbox check for package imports, offline mode, working directory, and `/tmp` write access.
- `notebooks/01_hello_multi_agent.ipynb`: baseline software-delivery multi-agent collaboration.
- `notebooks/02_shared_rag_memory.ipynb`: Shared RAG memory and Theory-of-Mind retrieval.
- `notebooks/03_mcp_tool_gateway.ipynb`: MCP-style tool gateway and zero-trust policy.
- `notebooks/04_pydantic_delegation.ipynb`: strict typed handoff contracts.
- `notebooks/05_self_repair_loop.ipynb`: ChatDev-style bounded repair loop.
- `notebooks/06_dynamic_routing.ipynb`: Fugu-style heterogeneous routing.
- `notebooks/07_debugging_agents.ipynb`: bonus broken-agent sandbox.
- `notebooks/08_api_boundaries_async_orchestration.ipynb`: FastAPI gateway, async orchestration, and status polling.
- `notebooks/09_advanced_fugu_orchestration.ipynb`: advanced Fugu concepts including dynamic scaffolds, debate, adaptive topology, and simple learned routing.
- `notebooks/10_vibe_coding_interface.ipynb`: human CEO interface for natural-language directives, plan review, mid-workflow commitment changes, and final approval.
- `notebooks/11_enterprise_a2a_perimeter.ipynb`: enterprise A2A perimeter for cross-organization identity, payload classification, schema drift rejection, and Dead Letter Queue auditing.
- `assignments/`: numbered assignment sequence, extension homework, and capstone prompts.
- `assignments/module7_individual_agent_skills.md`: Homework A, specialist-agent skill track.
- `assignments/module8_production_ready_agent_features.md`: Homework B, HITL, benchmark, cost, and memory track.
- `assignments/module9_deployment_operations.md`: Homework C, deployment and operations track.
- `assignments/module10_hr_governance.md`: Homework D, PII redaction, bias-safe HR handoffs, and promotion approval.
- `assignments/module11_marketing_orchestration.md`: Homework E, campaign budget routing, brand safety, and hallucination repair.
- `assignments/module12_advanced_orchestration.md`: Homework F, optional Fugu reading/design discussion; clarifies learned orchestration without pretending a notebook can reproduce RL training.
- `crewai_learning/README.md`: optional self-contained CrewAI study path; not part of the core notebook sequence.
- `assignments/starter_code/`: starter scaffolds for Ex2, Ex4, and Ex5.
- `assignments/starter_code/*_solution.py`: runnable instructor solutions for Ex2, Ex4, and Ex5.
- `instructor/solutions/`: instructor solution guides.
- `instructor/grading_rubrics.xlsx`: grading workbook with detailed criteria and quick grading sheet.
- `assignments/basic_agent_governance_labs.md`: beginner-friendly Logistics Weather, Writer, QA, and CEO labs upgraded into schema, gateway, memory, repair, A2A, and TeamLog governance exercises.
- `assignments/assignment_syllabus.md`: professor-level assignment path, building blocks, learning experience, and scope exclusions.

## Quick Start

```bash
python3 src/enterprise_agent_team.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/ -v --tb=short
```

The implementation runs offline using Pydantic and a clearly labeled local teaching adapter for MCP-style tool calls. In production, replace that adapter with the official MCP Python SDK client/server boundary.

## Recommended Teaching Order

1. Course overview, setup guide, and `notebooks/00_sandbox_preflight.ipynb`.
2. Module 1 deck + NB1 + Ex1.
3. NB1 builder lab: Governed Logistics Weather Agent.
4. Module 2 deck + NB2 + Ex2.
5. Module 3 deck + NB3 + Ex3.
6. Module 4 deck + NB4.
7. Module 5 deck + NB5/NB6, including the Bounded Writer Agent lab.
8. Module 6 deck + NB11 + Ex4, including the Adversarial QA Agent lab.
9. NB8 API boundary lab.
10. NB9 advanced orchestration and NB10 CEO interface, including Natural Language Becomes TeamLog.
11. Assignment 12: From Whisper to Shipped Code.
12. Capstone Assignment 13.
13. Optional separate CrewAI study path: `crewai_learning/README.md`.

Mandatory production-readiness path:

1. `assignments/ex2_1_type_safe_handoffs.md`: customer-service handoffs with `TranscriptAnalysis`, `QualityEvaluation`, and `FinalReport`.
2. `assignments/ex2_3_mcp_tool_governance.md`: five-tool zero-trust gateway.
3. `assignments/ex4_1_capstone_month_plan.md`: four-week capstone build plan.

Compatibility aliases are kept for earlier filenames:

- `03_mcp_tool_standardization.ipynb` mirrors `03_mcp_tool_gateway.ipynb`.
- `04_pydantic_type_safe_delegation.ipynb` mirrors `04_pydantic_delegation.ipynb`.
- `06_dynamic_routing_fugu.ipynb` mirrors `06_dynamic_routing.ipynb`.

Reference-only notebook:

- `01_type_safe_multi_agent_team.ipynb` is retained for earlier course drafts. Do not expose it as part of the canonical learner path; use `notebooks/notebook_manifest.yml` as the source of truth.
