# Course Manager Notebook and Assignment Path

This path is the instructor-facing control map for the Jupyter sequence. It keeps the learner experience focused on managing multi-agent teams: typed contracts, governed tools, shared memory, bounded repair, routing, API boundaries, A2A security, and human steering.

## Controlled Sandbox Policy

| Decision | Course Default |
| --- | --- |
| Execution mode | `offline_deterministic` |
| Live LLM execution | `USE_LIVE_LLM = False` |
| Network access | Disabled for the core notebook path |
| Required packages | `pydantic`, `pytest`, `fastapi` |
| Recommended packages | `httpx`, `jupyter`, `nbval` |
| Optional packages | `crewai`, `chromadb`, `instructor`, `openai` |
| Output policy | Clear notebook outputs before commit |
| Alias policy | Keep aliases for compatibility; expose canonical NB0-NB11 |
| CrewAI policy | Keep separate in `crewai_learning/README.md` |

## Notebook Path

| Step | Notebook | Management Building Block | Assignment Connection |
| --- | --- | --- | --- |
| 0 | `notebooks/00_sandbox_preflight.ipynb` | Controlled environment and offline readiness | Preflight |
| 1 | `notebooks/01_hello_multi_agent.ipynb` | Sequential collaboration and audit trail | Assignment 01, Assignment 02 |
| 2 | `notebooks/02_shared_rag_memory.ipynb` | TeamLog, Theory of Mind, context compression | Assignment 04 |
| 3 | `notebooks/03_mcp_tool_gateway.ipynb` | MCP-style zero-trust tool boundary | Assignment 05 |
| 4 | `notebooks/04_pydantic_delegation.ipynb` | Pydantic handoff contracts | Assignment 03 |
| 5 | `notebooks/05_self_repair_loop.ipynb` | ChatDev-style bounded repair | Assignment 02, Assignment 13 |
| 6 | `notebooks/06_dynamic_routing.ipynb` | Fugu-style cost, risk, and budget routing | Homework E |
| 7 | `notebooks/07_debugging_agents.ipynb` | Broken-agent failure diagnosis | Assignment 02 |
| 8 | `notebooks/08_api_boundaries_async_orchestration.ipynb` | FastAPI boundary and async orchestration | Assignment 07 |
| 9 | `notebooks/09_advanced_fugu_orchestration.ipynb` | Dynamic scaffold, debate, adaptive topology | Assignment 08, Assignment 12 |
| 10 | `notebooks/10_vibe_coding_interface.ipynb` | Human CEO steering and TeamLog updates | Assignment 09, Assignment 12 |
| 11 | `notebooks/11_enterprise_a2a_perimeter.ipynb` | Enterprise A2A, schema drift, DLQ audit | Assignment 10, Assignment 11 |

## Assignment Path

| Stage | Learner Work | Evidence of Mastery |
| --- | --- | --- |
| Preflight | Run NB0 | Required packages import, no API keys required, `/tmp` write succeeds |
| Assignment 01 | Agent Roster & SOPs | Roles do not overlap; handoff artifacts are explicit |
| Assignment 02 | Basic Agent Governance Labs | Weather, Writer, QA, and CEO examples include schemas, boundaries, and escalation |
| Assignment 03 | Type-Safe Handoffs | Invalid handoffs fail validation; valid outputs are structured JSON |
| Assignment 04 | Theory-of-Mind Memory | Coder sees PM constraints but cannot read restricted secrets |
| Assignment 05 | MCP Tool Governance | Unauthorized tool calls are denied and audited |
| Assignment 06 | RAG & MCP Architecture | Design shows memory routing, sensitivity checks, and tool boundaries |
| Assignment 07 | API Boundary | Internal request gets `202`; external high-risk request gets `403` |
| Assignment 08 | Internal Brain | High-risk work inserts SecurityReviewer; unresolved debate escalates |
| Assignment 09 | External Steering Wheel | Natural-language change updates TeamLog; downstream agents adapt |
| Assignment 10 | Enterprise A2A Perimeter | Malicious or restricted cross-org payloads are ticketed and quarantined |
| Assignment 11 | Trust & Governance Matrix | Least-privilege role/tool/data policy has explicit denial cases |
| Assignment 12 | From Whisper to Shipped Code | Human intent becomes scaffold, debate, TeamLog pivot, and release decision |
| Assignment 13 | Virtual Software Company Capstone | System ships or escalates through a typed `PullRequestSummary` |

## Instructor Rule

Every notebook and assignment should answer three questions:

1. What management failure does this prevent?
2. What typed contract or boundary enforces it?
3. What evidence proves the system behaved safely?
