# Course Delivery Readiness Checklist

Use this checklist before a workshop, recording session, repository push, or capstone review. The goal is simple: learners should be able to set up, run, learn, extend, and submit without hidden instructor magic.

## Learner Journey

```text
┌─────────────────────────────────────────────────────────────────┐
│                    PRE-COURSE PREPARATION                        │
│  • Python 3.10+ installed                                        │
│  • Git installed                                                 │
│  • Repository cloned                                             │
│  • Virtual environment activated                                 │
│  • Dependencies installed                                        │
│  • Test run passes                                               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              WEEK 1-2: CORE FOUNDATIONS                          │
├─────────────────────────────────────────────────────────────────┤
│  Module 1: Foundations & Vibe Coding                             │
│  ├─ NB1: Baseline Multi-Agent Collaboration                      │
│  ├─ Builder Lab: Governed Logistics Weather Agent                │
│  └─ Ex1: Agent Roster & SOPs                                     │
│                                                                  │
│  Module 2: TeamLog & Theory of Mind                              │
│  ├─ NB2: Shared RAG Memory + Context Window Economics            │
│  ├─ Ex2.1: Type-Safe Handoffs                                    │
│  └─ Ex2.2: Theory-of-Mind Memory                                 │
│                                                                  │
│  Module 3: Agentic RAG & MCP                                     │
│  ├─ NB3: MCP Tool Gateway                                        │
│  └─ Ex2.3: MCP Tool Governance                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              WEEK 3-4: ADVANCED PATTERNS                         │
├─────────────────────────────────────────────────────────────────┤
│  Module 4: Pydantic AI & Type-Safety                             │
│  └─ NB4: Pydantic Type-Safe Delegation                           │
│                                                                  │
│  Module 5: Fugu Routing & ChatDev Self-Repair                    │
│  ├─ NB5: ChatDev-Style Self-Repair Loop                          │
│  ├─ Builder Lab: Bounded Writer Agent                             │
│  └─ NB6: Fugu-Style Dynamic Routing                              │
│                                                                  │
│  Module 6: Internet of Agents & Zero-Trust                       │
│  ├─ NB11: Enterprise A2A & Zero-Trust Perimeter                  │
│  ├─ Builder Lab: Adversarial QA Agent                             │
│  └─ Ex4: Trust & Governance Matrix                               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              WEEK 5-6: PRODUCTION & CAPSTONE                     │
├─────────────────────────────────────────────────────────────────┤
│  API Boundary Lab                                                │
│  └─ NB8: API Boundaries & Async Orchestration                    │
│                                                                  │
│  Advanced Orchestration                                          │
│  ├─ NB9: Advanced Fugu Orchestration                             │
│  └─ NB10: Vibe Coding CEO Interface                              │
│     └─ Builder Lab: Natural Language Becomes TeamLog              │
│                                                                  │
│  Assignment 12: From Whisper to Shipped Code                     │
│  └─ NB9 Internal Brain + NB10 External Steering Wheel             │
│                                                                  │
│  Extension Homework Track (Optional)                             │
│  ├─ Homework A: Specialist Agent Skills                          │
│  ├─ Homework B: Production Controls                              │
│  ├─ Homework C: Deployment & Operations                          │
│  ├─ Homework D: HR Governance                                    │
│  ├─ Homework E: Marketing Orchestration                          │
│  ├─ Homework F: Advanced Fugu Discussion                         │
│  └─ Homework G: CrewAI Applied Pipeline Engineering              │
│                                                                  │
│  Separate CrewAI Study Track                                     │
│  └─ crewai_learning/README.md                                    │
│     └─ Homework G readiness score + personal coding-agent team   │
│                                                                  │
│  CAPSTONE: Virtual Software Company                              │
│  └─ Ex5: End-to-End Multi-Agent System                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    POST-COURSE DELIVERABLES                      │
│  • Working capstone system                                       │
│  • GitHub repository with all notebooks                          │
│  • Understanding of:                                             │
│    - Pydantic schemas for type-safety                            │
│    - MCP tool governance                                         │
│    - Shared memory & Theory of Mind                              │
│    - Context window economics                                    │
│    - Bounded self-repair loops                                   │
│    - Heterogeneous routing and learned orchestration             │
│    - Zero-trust A2A interoperability                             │
│    - Enterprise A2A perimeter and Dead Letter Queue auditing      │
│    - FastAPI boundaries                                          │
│    - Human CEO review and approval loops                         │
│    - CrewAI role design, context chains, guardrails, recovery     │
│    - CrewAI Coder/QA/Review agent team readiness                  │
│    - Beginner-friendly governed Logistics Weather, Writer, QA,    │
│      and CEO labs                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Pre-Push Verification Sequence

Run this sequence locally before any push:

```bash
python3 -m pytest tests/ -v --tb=short
python3 src/enterprise_agent_team.py
python3 -m pytest tests/test_notebooks.py -v
```

Optional notebook execution check if `nbval` is installed:

```bash
cd notebooks
python3 -m pytest --nbval . --nbval-current-env
```

## Current Phase: Story-Driven Notebook Exercises

The primary learner notebooks now use a consistent exercise pattern:

1. **The Story:** a relatable production failure or management scenario.
2. **Your Mission:** concrete learner tasks that modify or extend the notebook.
3. **The Takeaway:** the production management principle the exercise teaches.

This pattern is required for NB1, NB2, NB3, NB4, NB5, NB6, NB8, and NB10. NB7 and NB9 keep their current exercise sections unless a dedicated rewrite is provided. NB11 is the current Enterprise A2A perimeter lab and should be delivered as a zero-trust network-boundary exercise. The current builder labs are Governed Logistics Weather Agent, Bounded Writer Agent, Natural Language Becomes TeamLog, and Adversarial QA Agent. CrewAI study material is separate from the notebook sequence and lives in `crewai_learning/README.md`.

Verification command:

```bash
python3 -c "import json, pathlib; targets={'01_hello_multi_agent.ipynb','02_shared_rag_memory.ipynb','03_mcp_tool_gateway.ipynb','04_pydantic_delegation.ipynb','05_self_repair_loop.ipynb','06_dynamic_routing.ipynb','08_api_boundaries_async_orchestration.ipynb','10_vibe_coding_interface.ipynb'}; [print(p.name, all(m in '\\n'.join(''.join(c.get('source', [])) for c in json.loads(p.read_text()).get('cells', []) if c.get('cell_type')=='markdown') for m in ['The Story:', 'Your Mission:', 'The Takeaway:'])) for p in sorted(pathlib.Path('notebooks').glob('*.ipynb')) if p.name in targets]"
```

## Release Checklist

- [ ] All notebooks run without errors.
- [ ] All tests pass.
- [ ] Core implementation runs successfully.
- [ ] Target notebook exercises use the Story -> Mission -> Takeaway pattern.
- [ ] Basic Agent Governance Labs are visible in NB1, NB5, NB10, NB11 and in `assignments/basic_agent_governance_labs.md`.
- [ ] No API keys are committed.
- [ ] `README.md` is clear and complete.
- [ ] All assignments have starter code where implementation is expected.
- [ ] All core assignments have instructor solution guides.
- [ ] Resource library is curated and GitHub-friendly.
- [ ] Course overview is aligned with modules.
- [ ] Setup guide is tested and working.
- [ ] `instructor/curriculum_maintenance_checklist.md` has been reviewed.
- [ ] `instructor/a2a_identity_tool_matrix.md` matches current enums and tool handlers.
- [ ] Homework G readiness checklist confirms CrewAI basics, setup plan, Coder/QA/Review agents, guardrails, state, retry loop, and reusable template.
- [ ] No `__pycache__`, `.pytest_cache`, `.env`, or `.DS_Store` files are present.
- [ ] Markdown files have valid local links or intentionally external links.
- [ ] Python files pass syntax checks or are covered by tests.

## Instructor Notes

- Use `tests/test_notebooks.py` as the canonical offline notebook execution check. It executes notebook code cells without requiring API keys.
- Use `nbval` only when the environment has the plugin installed and you want output-level notebook validation.
- Live LLM cells should remain disabled by default with `USE_LIVE_LLM = False`.
- The capstone is ready when `PullRequestSummary.status` is machine-checkable as `SHIPPED` or `ESCALATED_TO_HUMAN`.
- Teach every rewritten notebook exercise by reading the story first, then naming the management failure, then letting learners implement the mission. Do not skip the takeaway; it is the bridge from code to production judgment.
- For the CrewAI study track, emphasize that it is self-contained companion material. It can be studied without changing the core notebook sequence, and real CrewAI implementation requires learners to install `crewai` and configure an LLM.
