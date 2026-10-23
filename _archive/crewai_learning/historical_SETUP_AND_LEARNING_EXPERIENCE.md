# CrewAI Setup Approach and Learning Experience

## Purpose

This document explains how to learn from the unzipped CrewAI project in this folder without mutating the original extracted work.

The project is a self-contained CrewAI lab aligned with the main course, **Managing Multi-Agent Teams: Agentic AI & Vibe Coding**. The main course teaches the governance shell: schemas, MCP-style tool boundaries, shared memory, bounded repair, audit logs, and API perimeters. This folder teaches how CrewAI expresses the orchestration layer: agents, tasks, context chains, tools, quality gates, and clean delivery.

## Folder Contract

Treat these files as the reference artifact:

```text
crewai_learning/academic_research_crewai-project.zip
crewai_learning/academic_research_crewai_project/
```

Do not edit the extracted project while studying the baseline. First verify it, read it, and map it to the course concepts. When you want to experiment, copy the extracted project into a separate sandbox folder and modify the copy.

Recommended sandbox pattern:

```bash
cd crewai_learning
cp -R academic_research_crewai_project experiments/my_research_crew
cd experiments/my_research_crew
```

The reference project stays clean. Your learning experiments live under `crewai_learning/experiments/`.

## What CrewAI Adds To The Course

CrewAI is useful when work goes beyond a single prompt:

- Multiple specialized agents need clear roles, goals, and backstories.
- Work must be decomposed into tasks with explicit context dependencies.
- Agents need tools for search, scraping, file processing, or external APIs.
- Outputs must be structured, validated, reviewed, and delivered as artifacts.
- A workflow needs state, branching, event handling, or human review.

In course language:

| Main Course Concept | CrewAI Learning Equivalent |
| --- | --- |
| Agent roster and SOPs | `agents.yaml` role, goal, backstory, tools |
| Type-safe handoffs | `expected_output`, guardrails, structured task contracts |
| Agentic RAG and shared memory | Knowledge files, task context, retrieved source evidence |
| MCP tool governance | Tool assignment, least-privilege tool design, external API boundaries |
| Bounded self-repair | Retry budgets, fallback outputs, BEST_EFFORT delivery |
| API and A2A perimeters | Flows, external triggers, deployable crew services |
| Clean production delivery | Report compiler and document delivery agent |

## Current Extracted Project

The unzipped project is:

```text
crewai_learning/academic_research_crewai_project/
```

It contains:

| Asset | Purpose |
| --- | --- |
| `pyproject.toml` | Project metadata and pinned CrewAI dependencies. |
| `uv.lock` | Locked dependency graph. |
| `AGENTS.md` | CrewAI-generated guidance for coding assistants. |
| `src/academic_research_writer_evaluator/crew.py` | Crew construction, agent methods, task methods, and process mode. |
| `src/academic_research_writer_evaluator/config/agents.yaml` | The 7 agent role definitions. |
| `src/academic_research_writer_evaluator/config/tasks.yaml` | The 7 task definitions and context chain. |
| `src/academic_research_writer_evaluator/tools/semantic_scholar_search_tool.py` | Custom Semantic Scholar tool. |
| `knowledge/user_preference.txt` | Local knowledge seed. |

The current verified structure is:

- 7 agents.
- 7 tasks.
- `Process.sequential`.
- `openai/gpt-4o-mini` configured as the LLM.
- Research tools include Exa, scraping, Semantic Scholar, arXiv, Serply, and Brave-style search.

This is intentionally sequential. Hierarchical manager behavior is a discussion and comparison topic, but this fixed quality-gate pipeline should run in a predictable order first.

## Setup Mode 1: Offline Structural Audit

Use this mode first. It checks structure without making live LLM or search API calls.

```bash
cd crewai_learning/academic_research_crewai_project
uv sync --locked
uv run python -m compileall -q src
```

Then check that the CrewAI graph can be constructed without spending LLM credits:

```bash
OPENAI_API_KEY=dummy EXA_API_KEY=dummy BRAVE_API_KEY=dummy SERPLY_API_KEY=dummy \
uv run python -c "from academic_research_writer_evaluator.crew import AcademicResearchWriterEvaluatorCrew; crew=AcademicResearchWriterEvaluatorCrew().crew(); print(len(crew.agents), len(crew.tasks), crew.process)"
```

Expected output:

```text
7 7 Process.sequential
```

What this proves:

- The locked environment installs.
- Python files are syntactically valid.
- Agent and task YAML can be loaded.
- Tool constructors can initialize when required keys are present.
- The crew graph can be created.

What this does not prove:

- OpenAI calls work.
- Exa, Brave, Serply, arXiv, or Semantic Scholar calls work.
- The final research report is high quality.
- The workflow is safe for production.

That distinction matters. A production professor should separate **structural validity** from **live agent quality**.

## Setup Mode 2: Live Local Run

Use this only when you are ready to call live APIs.

Create a local `.env` file inside the extracted project. Do not commit it.

```text
OPENAI_API_KEY=...
EXA_API_KEY=...
BRAVE_API_KEY=...
SERPLY_API_KEY=...
```

Then run:

```bash
cd crewai_learning/academic_research_crewai_project
uv run crewai run
```

Live-run checklist:

- Start with a narrow `research_topic`.
- Watch for fake URLs, placeholder URLs, and missing citations.
- Check whether the Quality Gate routes instead of rewriting content.
- Check whether the Report Compiler copies rather than invents content.
- Check whether the Document Delivery Agent strips logs and metadata.

If live execution fails, classify the failure:

| Failure | Likely Cause | First Fix |
| --- | --- | --- |
| Missing API key | `.env` incomplete | Add required key locally. |
| Tool rate limit | Search provider throttled | Retry later or reduce tool calls. |
| Hallucinated source | Research result did not propagate cleanly | Tighten source guardrails and context chain. |
| Article not in context | Task context chain broken | Verify `context:` in `tasks.yaml`. |
| Concurrent executor error | Hierarchical/delegation behavior used incorrectly | Keep this pipeline sequential. |
| Dirty final report | Delivery agent not stripping metadata | Strengthen clean delivery task contract. |

## Setup Mode 3: Safe Experimentation

Do not mutate the original extracted project for learning experiments. Copy it first:

```bash
cd crewai_learning
mkdir -p experiments
cp -R academic_research_crewai_project experiments/my_research_crew
cd experiments/my_research_crew
uv sync --locked
```

Good first experiments:

1. Change `research_topic` in `main.py`.
2. Add one new task between `evaluate_content` and `quality_gate_check`.
3. Add one stricter `expected_output` field to a task.
4. Remove one unnecessary tool from an agent and compare output quality.
5. Add a clean output file target only in the experiment copy.

Do not start by adding new frameworks, new databases, or custom training. The teaching goal is orchestration clarity.

## Learning Experience

Use this sequence.

### Step 1: Read The Crew As An Org Chart

Open:

```text
src/academic_research_writer_evaluator/config/agents.yaml
```

For each agent, answer:

1. What is its role?
2. What is its measurable goal?
3. What tools does it have?
4. What should it never do?
5. What downstream agent depends on its output?

Management principle: an agent is not a prompt. It is a worker with a role, scope, tools, and accountability.

### Step 2: Read The Tasks As A Dependency Graph

Open:

```text
src/academic_research_writer_evaluator/config/tasks.yaml
```

Trace the context chain:

```text
research_mission
  -> write_article
  -> evaluate_content
  -> quality_gate_check
  -> manager_review_and_score
  -> compile_final_report
  -> deliver_clean_report
```

Management principle: context is not magic. If a task does not receive upstream output through `context`, it cannot safely use it.

### Step 3: Identify The Quality Gates

Find every place the pipeline should stop, retry, warn, or proceed.

Examples:

- Research confidence below threshold.
- Article missing citations.
- Score below `40/50`.
- Quality Gate emits `RETRY_NEEDED`.
- Manager emits `REJECT_AND_RETRY`.
- Report Compiler detects article mismatch.
- Delivery Agent finds duplicate article sections.

Management principle: a managed AI team needs gates between roles. Otherwise one agent's mistake becomes everyone else's context.

### Step 4: Separate CrewAI Convenience From Governance

CrewAI gives a strong orchestration shell, but the production responsibilities remain yours:

- Do not give every agent every tool.
- Do not trust generated citations without verification.
- Do not let delivery agents recalculate scores.
- Do not hide execution failures inside polished markdown.
- Do not run high-cost workflows without budget control.

Management principle: frameworks accelerate teams, but governance makes them safe.

### Step 5: Compare Crews And Flows

Use a **Crew** when:

- A team of specialized agents collaborates on a task.
- The order of work is mostly known.
- You want role-based task execution and tool use.

Use a **Flow** when:

- You need explicit state management.
- You need event triggers, branching, or conditional routing.
- You need human-in-the-loop checkpoints.
- You need to combine deterministic business logic with agent calls.

For this project:

- Keep the extracted pipeline as a sequential Crew.
- Discuss Flow as the next production wrapper for API triggers, retries, human approvals, and deployment.

## Professor Delivery Script

"This folder is separate from the main course notebooks. In the main course, we built the governance shell: schemas, gateways, repair loops, and audit logs. Here, we study CrewAI as the orchestration framework.

First, we do not edit the original extracted project. We read it like an architecture diagram. The agents are the org chart. The tasks are the dependency graph. The tools are controlled capabilities. The expected outputs are contracts.

Then we run offline checks. This proves the crew can be constructed, but it does not prove quality. Quality requires live runs, API keys, tool behavior, source verification, and human review.

Finally, we copy the project into an experiment folder and change one thing at a time. This is how you learn production agent engineering: preserve a known baseline, create a sandbox, test a hypothesis, and reflect on the failure mode."

## Mini Assignments

### Assignment C1: Crew Org Chart

Create a table with one row per agent:

- Role.
- Goal.
- Tools.
- Upstream inputs.
- Downstream consumer.
- One thing this agent must never do.

Pass condition: every role has a clear boundary.

### Assignment C2: Context Chain Audit

Draw the task dependency graph from `tasks.yaml`.

Deliverable:

- A Mermaid or ASCII graph.
- One risk caused by missing context.
- One fix to the context chain.

Pass condition: `compile_final_report` receives the article, evaluation, quality gate, and manager review.

### Assignment C3: Guardrail Upgrade

Pick one task and strengthen its `expected_output`.

Constraints:

- Do this in an experiment copy, not the reference project.
- Add at least one required field.
- Add one failure condition.
- Explain which downstream failure this prevents.

Pass condition: the new expected output would help another agent parse the result.

### Assignment C4: Crew Vs Flow Decision

For each scenario, choose Crew or Flow:

1. Fixed research -> write -> evaluate -> deliver pipeline.
2. Slack webhook starts a job and human approval is required before publishing.
3. Three research agents debate and a manager selects the best answer.
4. A compliance workflow branches based on risk score.

Pass condition: learner explains the management reason, not just the framework feature.

## Production Takeaway

CrewAI does not replace the Managing Multi-Agent Teams architecture. It gives learners a production framework for expressing it.

The right mental model is:

```text
Governance Layer:
  Pydantic contracts, MCP boundaries, shared memory, audit logs, repair budgets

CrewAI Orchestration Layer:
  agents.yaml, tasks.yaml, context chains, tools, crews, flows

Delivery Layer:
  clean artifacts, reports, APIs, human approval, deployment
```

The course goal stays the same: learners are not just making agents talk. They are learning to manage an AI workforce safely.

