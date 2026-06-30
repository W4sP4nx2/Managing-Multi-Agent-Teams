# Scope Alignment Verification

Last verified: 2026-06-30

## Scope Lock

This course is scoped to **Managing Multi-Agent Teams**.

It does not teach:

- Math-model optimization.
- Data engineering or ETL pipelines.
- Neural-network training, fine-tuning, backpropagation, or RL implementation.

It does teach:

- Management: governing, securing, and orchestrating autonomous agents.
- Engineering: building the typed pipes that keep agents safe, including Pydantic contracts, MCP-shaped gateways, FastAPI boundaries, audit trails, and bounded repair loops.
- Economics: controlling cost, context, and tool access through routing, shared memory, and explicit budgets.

## Phase Verification

| Phase | Asset | Verification |
| :--- | :--- | :--- |
| Vibe Coding Interface | `notebooks/10_vibe_coding_interface.ipynb` | Present. Teaches the human CEO loop through `ManagerInstruction`, `ProjectPlan`, `TeamCommitment`, and `HumanReviewDecision`. |
| Context Window Economics | `notebooks/02_shared_rag_memory.ipynb` | Present. Teaches compression with `ContextCompressionReport` and durable memory records. |
| Intelligent Orchestrator | `notebooks/09_advanced_fugu_orchestration.ipynb` | Present. Teaches a schema-constrained LLM manager pattern through `DelegationDecision`; the framework executes approved actions. |
| Enterprise A2A Perimeter | `notebooks/11_enterprise_a2a_perimeter.ipynb` | Present. Teaches cross-organization identity checks, payload classification, schema drift rejection, and Dead Letter Queue auditing. |
| CrewAI Self-Contained Study Track | `crewai_learning/README.md` | Present. Separate from notebooks. Teaches role clarity, context chains, sequential vs hierarchical process choice, guardrails, failure recovery, and clean delivery. |
| Story-Driven Exercises | NB1, NB2, NB3, NB4, NB5, NB6, NB8, NB10 | Present. Target notebooks use the Story -> Mission -> Takeaway pattern so exercises teach production management judgment, not only code changes. |
| Basic Agent Governance Labs | NB1, NB5, NB10, NB11 + `assignments/basic_agent_governance_labs.md` | Present. Logistics Weather, Writer, QA, and CEO examples are elevated into schemas, gateways, memory, repair budgets, A2A defense, and TeamLog exercises. |

## Manager Test Results

Commands run:

```bash
python3 -m pytest tests/ -v --tb=short
python3 src/enterprise_agent_team.py
python3 -B -c '<targeted manager checks>'
python3 -B -c '<python syntax check>'
```

Observed results:

- Full test suite: `38 passed`.
- Notebook execution suite: `11 passed`.
- Story-driven exercise marker check: target notebooks contain `The Story:`, `Your Mission:`, and `The Takeaway:`.
- Builder lab marker check: NB1 includes Governed Logistics Weather Agent, NB5 includes Bounded Writer Agent, NB10 includes Natural Language Becomes TeamLog, and NB11 includes Adversarial QA Agent.
- Core implementation: ran end-to-end and shipped after one bounded repair.
- Unsafe path rejection: passed. `CodePatch` rejected `../escape.py`.
- Unauthorized tool block: passed. `ToolPolicy` blocked a coder from calling `EXECUTE_TESTS` without scope.
- Repair budget escalation: passed. Capstone `run_company(..., max_repairs=0)` returned `ESCALATED_TO_HUMAN`.
- Python syntax check: passed across 29 Python files.

## No-Drift Rule

| Check | Result |
| :--- | :--- |
| Homework F scope | `assignments/module12_advanced_orchestration.md` is explicitly conceptual and not a graded implementation lab. |
| NB6 dynamic routing | `notebooks/06_dynamic_routing.ipynb` remains rule-based, deterministic, testable, and labeled as a teaching router. |
| NB9 Fugu bridge | `notebooks/09_advanced_fugu_orchestration.ipynb` is a teaching adapter for scaffolds, debate, topology, and typed delegation. It does not claim to reproduce Sakana Fugu training. |
| Basic agent labs | Logistics Weather, Writer, QA, and CEO exercises are beginner examples only at the surface. Each is still assessed through course primitives: Pydantic contracts, MCP/A2A gates, shared memory, bounded repair, TeamLog, and audit evidence. |
| ML/ETL drift scan | No course-content matches for fine-tuning, neural-network training, backpropagation, raw data pipelines, or ETL pipelines when generated `.inspect.ndjson` visual-QA artifacts are excluded. |
| False-positive note | The phrase `data pipelines` appears only as a candidate resume skill in HR governance examples. It is not taught as a data engineering module. |

## Instructor Verdict

The course now reads as a masterclass on engineering a safe AI workforce, not a tutorial on calling a multi-agent framework. The deterministic shell is labeled correctly, the LLM bridge is taught through mock and optional live adapters, and the capstone keeps the learner focused on managed autonomy: typed contracts, governed tools, shared memory, bounded repair, API boundaries, and human review.
