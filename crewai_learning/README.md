# Multi-Agent AI Systems: A Practical CrewAI Learning Guide

## Self-Contained Study Material

This folder is a **self-contained CrewAI learning track**. It is intentionally separate from the core notebook sequence in `notebooks/`.

Use this guide when you want to study CrewAI-style orchestration, CrewAI Studio/UI workflow design, task context chains, guardrails, quality gates, manager review, and clean document delivery without changing the main "Managing Multi-Agent Teams" notebook path.

The runnable CrewAI project lives here:

```text
crewai_learning/academic_research_crewai_project/
```

The original archive is preserved here:

```text
crewai_learning/academic_research_crewai-project.zip
```

Start with the setup and learning-experience guide:

[SETUP_AND_LEARNING_EXPERIENCE.md](/Users/lwinnaingkyaw/Documents/Training%20Managing%20Multi-Agent%20Teams/crewai_learning/SETUP_AND_LEARNING_EXPERIENCE.md)

That guide explains how to run, audit, and learn from the unzipped CrewAI project without mutating the original extracted work.

## Mission Alignment

This guide supports the original course mission:

> Managing Multi-Agent Teams means learning how to design, govern, debug, and deliver reliable agent workflows that survive contact with production reality.

The main course teaches the governance layer: Pydantic contracts, MCP gateways, shared memory, bounded repair, A2A perimeters, and auditability.

This self-contained CrewAI guide teaches the orchestration layer: role design, task dependencies, sequential vs hierarchical process choice, guardrails, failure analysis, and clean delivery.

The two tracks fit together:

- Main course: **why safe AI workforces need governance**.
- CrewAI guide: **how to shape production crews and task pipelines**.

## Course Philosophy

> "Don't wait until you feel ready. Start building, break things, fix them.
> That's how you actually learn AI systems."
> — Inspired by Andrew Ng

This guide follows the journey of building a production-grade multi-agent research pipeline from a blank crew to a 7-agent CrewAI research writer and evaluator with guardrails, structured outputs, quality gates, recovery patterns, and clean document delivery.

Every concept is taught in the order it appears during a real build, not in the order a textbook would present it.

## Alignment Reflection

This track is aligned with the current extracted CrewAI project, not an abstract idealized crew.

| Check | Current State | Teaching Decision |
| --- | --- | --- |
| Project type | CrewAI crew generated project | Keep this as a self-contained framework study track. |
| Process mode | `Process.sequential` in `crew.py` | Teach hierarchy as a comparison concept, but run this fixed quality-gate pipeline sequentially. |
| Agent count | 7 agents in `agents.yaml` and `crew.py` | Use the 7-role pipeline as the concrete teaching artifact. |
| Task count | 7 tasks in `tasks.yaml` and `crew.py` | Treat clean delivery as a first-class task, not post-processing. |
| Governance fit | Guardrails, quality gates, context chains, retry budgets | Map each CrewAI concept back to Managing Multi-Agent Teams. |
| Runtime boundary | Live run requires API keys and network tools | Separate offline structural tests from live LLM/tool execution. |

The key reflection: this folder is not another notebook module. It is a separate CrewAI learning lab. The main course teaches the governance shell; this folder teaches how a production framework expresses roles, tasks, context, tools, and delivery.

## Official CrewAI Positioning

CrewAI fits this course when learners need more than a single prompt or chatbot: multi-step work, specialized agents, tool use, structured outputs, human review, and workflows that combine autonomous reasoning with explicit business logic.

This folder uses CrewAI as the practical framework layer for those patterns while preserving the main course's governance lessons:

- **Crews** express role-based collaboration among specialized agents.
- **Flows** are the production control layer when learners need state, branching, and event-driven orchestration.
- **This extracted project** is intentionally kept as a sequential crew so learners can see task context chains and quality gates before introducing dynamic Flow control.

References:

- [CrewAI: When to Use CrewAI](https://github.com/crewAIInc/crewAI#when-to-use-crewai)
- [CrewAI Installation](https://docs.crewai.com/en/installation)
- [CrewAI Quickstart](https://docs.crewai.com/v1.15.1/en/quickstart)
- [CrewAI current Quickstart](https://docs.crewai.com/en/quickstart)
- [CrewAI LLM Configuration](https://docs.crewai.com/en/concepts/llms#setting-up-your-llm)

## Personal Coding Agent Team Track

This section answers the course question: **Are learners ready to create their own AI coding team?**

Yes, but with one important boundary. The course does **not** require every learner to configure a live LLM backend inside the core exercise. Individual API keys, provider choice, and CLI authentication are environment-specific. The required class deliverable is an offline, governed coding-agent skeleton. Learners with keys can then run the CrewAI CLI path as an optional extension.

### Learning Outcomes

By the end of this track, each learner can:

1. Explain CrewAI basics: agents, tasks, crews, process modes, context, guardrails, and outputs.
2. Document a safe setup path for Python, the CrewAI CLI, and LLM environment variables.
3. Design a personal coding team with Coder, QA, and Review agents.
4. Implement a bounded retry loop: if review fails, route back to the Coder with typed feedback.
5. Package the coding team as a reusable class template with setup instructions and a showcase script.

### Setup Boundary

Required for design and offline grading:

- Python environment.
- Course schemas and offline mocks.
- CrewAI concepts from the official installation and quickstart docs.
- Written `.env` safety plan.

Optional for live execution:

- CrewAI CLI installed locally.
- LLM configured with provider API keys.
- Real CrewAI scaffold created from the CLI.
- Live `crewai run` or Flow execution.

Useful commands to document:

```bash
# Official CLI-oriented path used by current CrewAI docs
uv tool install crewai

# Package-level experimentation when appropriate
pip install crewai

# Common crew scaffold
crewai create crew my_coding_team

# Flow scaffold, if supported by the installed CLI version
crewai create flow my_coding_flow
```

If `crewai create flow` is not available in a learner's CLI version, the learner should scaffold a crew first and add a Flow wrapper manually. The concept matters more than the exact CLI subcommand.

### Coding Agent Building Blocks

| Building Block | Course Primitive | CrewAI Expression |
| --- | --- | --- |
| Coder agent | `CodePatch` contract | Agent role, coding task, patch output |
| QA agent | `TestResult` contract | Test task, tool call, evidence output |
| Review agent | `ReviewDecision` contract | Review task, approval gate |
| Retry loop | Bounded self-repair | Flow/router logic or explicit orchestration wrapper |
| State | `TeamState` / TeamLog | Flow state, task context, audit trail |
| Guardrails | Pydantic + policy checks | Task guardrails and structured outputs |
| Reusable template | Capstone pattern | CrewAI project scaffold and README |

### Readiness Checklist and Score

Score out of 100.

| Area | Evidence | Points |
| --- | --- | ---: |
| CrewAI basics | Learner can explain agents, tasks, crews, process modes, and task context. | 15 |
| Environment plan | Learner documents Python, CrewAI CLI, LLM key requirements, and `.env` safety. | 15 |
| Coding agents | Learner designs Coder, QA, and Review agents with non-overlapping roles. | 20 |
| Guardrails and state | Learner defines typed state, review decisions, retry budget, and approval logic. | 20 |
| Orchestration loop | Learner shows `review fails -> back to coder` with a bounded retry path. | 15 |
| Reusable template | Learner packages setup instructions, project structure, and peer demo checklist. | 15 |

Readiness interpretation:

- 90-100: Ready to run a personal CrewAI coding team with live keys.
- 75-89: Ready for offline skeleton and guided live setup.
- 60-74: Understands pieces but needs help connecting state, guardrails, and retry.
- Below 60: Revisit the core governance notebooks before running CrewAI live.

### Student Showcase

Each learner should be able to demo:

1. A typed coding task enters the system.
2. The Coder returns a patch.
3. QA returns test evidence.
4. Review approves, rejects, or requests changes.
5. A failed review routes back to the Coder within a retry budget.
6. The final result is either shipped or escalated with a typed ticket.

Peer review questions:

- Are the Coder, QA, and Review responsibilities separated?
- Is every handoff typed?
- Where are LLM/API keys kept out of the repo?
- What happens when QA fails twice?
- Can another student run the offline skeleton without your private setup?

## Required Inputs

Before running or adapting this CrewAI pipeline, collect these inputs:

| Input | Required | Default / Example | Why It Matters |
| --- | --- | --- | --- |
| `research_topic` | Yes | `"AI agent orchestration trends"` | Primary variable that drives the whole research pipeline. |
| CrewAI project path | Yes | `crewai_learning/academic_research_crewai_project/` | All run commands should execute from this folder. |
| Process mode | Yes | `Process.sequential` | The extracted project is a fixed quality-gate pipeline, so sequential execution is safer and easier to debug. |
| LLM | Yes for live build | `openai/gpt-4o-mini` | Used by each agent and by `chat_llm` in `crew.py`. |
| `OPENAI_API_KEY` | Yes for live build | Stored in local `.env`, never committed | Required for live LLM calls. |
| `EXA_API_KEY` | Yes for live build | Stored in local `.env`, never committed | Required by `ExaSearchTool`. |
| `BRAVE_API_KEY` | Yes if using writer search | Stored in local `.env`, never committed | Required by `BraveSearchTool`. |
| `SERPLY_API_KEY` | Yes if using Serply tools | Stored in local `.env`, never committed | Required by `SerplyScholarSearchTool`. |
| Research tools | Yes for live build | Exa, ScrapeWebsite, Semantic Scholar, arXiv, Serply, Brave | Determines source quality and retrieval coverage. |
| Academic source allowlist | Yes | `arxiv.org`, `semanticscholar.org`, `.edu` | Prevents fake or low-quality citations. |
| Confidence threshold | Yes | `0.8` | Decides when research is strong enough to stop. |
| Evaluation pass threshold | Yes | `40/50` | Prevents one minor citation issue from overriding a strong article. |
| Retry budget | Yes | Research `2`, Writing `2`, Evaluation `1`, Manager `0` | Keeps autonomy bounded. |
| Output format | Yes | Clean `.md` report | Ensures reader-facing delivery, not pipeline metadata. |
| Guardrail schema style | Yes | XML, JSON Schema, or Pydantic | Makes every handoff machine-checkable. |
| Human override policy | Recommended | Manager can approve `BEST_EFFORT` with notes | Prevents dead-end pipelines when partial delivery is acceptable. |

## Local Verification Status

The extracted project has been checked locally.

| Verification | Result |
| --- | --- |
| Zip safety check | Passed: no unsafe paths. |
| Dependency sync | Passed with `uv sync --locked`. |
| CrewAI version in project venv | `1.15.0`. |
| Python syntax check | Passed with `uv run python -m compileall -q src`. |
| YAML config parse | Passed: 7 agents and 7 tasks. |
| Crew graph construction | Passed with dummy API keys: 7 agents, 7 tasks, `Process.sequential`. |
| Full live kickoff | Not run without real API keys and network access. |
| Project tests | No tests are currently present in the extracted `tests/` folder. |

Recommended structural checks:

```bash
cd crewai_learning/academic_research_crewai_project
uv sync --locked
uv run python -m compileall -q src
```

Recommended graph-build check without spending LLM credits:

```bash
cd crewai_learning/academic_research_crewai_project
OPENAI_API_KEY=dummy EXA_API_KEY=dummy BRAVE_API_KEY=dummy SERPLY_API_KEY=dummy \
uv run python -c "from academic_research_writer_evaluator.crew import AcademicResearchWriterEvaluatorCrew; crew=AcademicResearchWriterEvaluatorCrew().crew(); print(len(crew.agents), len(crew.tasks), crew.process)"
```

For a real run, add a local, uncommitted `.env` file with the required keys, then run:

```bash
cd crewai_learning/academic_research_crewai_project
uv run crewai run
```

## Learning Map

```text
research_topic
      |
      v
Research Mission
      |
      v
Write Article
      |
      v
Evaluate Content
      |
      v
Quality Gate
      |
      v
Manager Review and Score
      |
      v
Compile Final Report
      |
      v
Deliver Clean Report
```

# Academic Research Writer & Evaluator

## Sequential CrewAI Workflow With Manager Review

### Overview

- **Process:** Sequential, using `Process.sequential` in `crew.py`.
- **Manager role:** `workflow_manager` task performs review, scoring, diagnostics, and routing after upstream tasks complete.
- **LLM:** `openai/gpt-4o-mini`.
- **Input Variable:** `{research_topic}`.
- **Agents:** 7.
- **Tasks:** 7.
- **Flow:** Sequential pipeline with gate-based routing.
- **Output:** Clean reader-facing `.md` document.

## Pipeline Architecture

```text
┌─────────────────────────────────────────────────────┐
│ INPUT: {research_topic}                             │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│ 1. Research Mission                                 │
│ Academic Research Specialist                        │
│ ReAct loop, max 5 iterations, confidence >= 0.8     │
│ Tools: Exa, scrape, Semantic Scholar, arXiv, Serply │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│ 2. Write Article                                    │
│ Senior Content Writer                               │
│ 1000+ words, 8+ sources, inline APA citations       │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│ 3. Evaluate Content                                 │
│ Content Quality Evaluator                           │
│ 5 dimensions x 10, threshold 40/50                  │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│ 4. Quality Gate                                     │
│ Routes only: PROCEED, RETRY, PIPELINE_ERROR         │
│ Never modifies content                              │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│ 5. Manager Review and Score                         │
│ Workflow Manager                                    │
│ Metrics, multi-dim score, state, diagnostics, route │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│ 6. Compile Final Report                             │
│ Report Compiler                                     │
│ Verbatim copy engine, no rewriting                  │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│ 7. Deliver Clean Report                             │
│ Document Delivery Agent                             │
│ Strip metadata, deliver clean markdown              │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│ OUTPUT: Clean .md document                          │
└─────────────────────────────────────────────────────┘
```

## Agents

| # | Role | Model | Tools | Design Decision |
| --- | --- | --- | --- | --- |
| 1 | Academic Research Specialist | `gpt-4o-mini` | ExaSearchTool, ScrapeWebsiteTool, SemanticScholarSearchTool, ArxivPaperTool, SerplyScholarSearchTool | ReAct loop, mandatory multi-tool coverage. |
| 2 | Senior Content Writer | `gpt-4o-mini` | BraveSearchTool, SerplyScholarSearchTool | Zero-tolerance inline citation rule with supplemental search support. |
| 3 | Content Quality Evaluator | `gpt-4o-mini` | SerplyScholarSearchTool | Total score decides approval. |
| 4 | Quality Gate | `gpt-4o-mini` | None | Routes only, never modifies. |
| 5 | Workflow Manager | `gpt-4o-mini` | None | 5-skill sequential framework. |
| 6 | Report Compiler | `gpt-4o-mini` | None | Photocopier, not editor. |
| 7 | Document Delivery Agent | `gpt-4o-mini` | None | Strip pipeline noise, deliver clean `.md`. |

## Task Blueprint

### Task 1: Research Mission

**Agent:** Academic Research Specialist  
**Context:** none  
**Logic:** ReAct loop: `THOUGHT -> ACTION -> OBSERVATION`, max 5 iterations.

Rules:

- Break early if confidence >= `0.8`.
- Query the three primary research tools each iteration: Semantic Scholar, arXiv, and Exa.
- Use scrape, Serply, and Brave-style search as supporting tools where the CrewAI tool configuration allows it.
- Require credibility >= `0.85` per source where available.
- Return `PARTIAL_RESULTS = true` if iteration 5 still has confidence below `0.8`.

Confidence formula:

```text
confidence =
  (num_sources / 9) * 0.25
+ (sources_with_url / num_sources) * 0.25
+ avg_credibility * 0.25
+ coverage_score * 0.25
```

Coverage score:

- `1.0`: 3+ subtopics.
- `0.5`: partial coverage.
- `0.0`: single subtopic.

Output:

- `confidence_score`
- `sources[]`
- APA citations
- `iterations`
- `PARTIAL_RESULTS`
- `error_log`

### Task 2: Write Article

**Agent:** Senior Content Writer  
**Context:** Research Mission

Requirements:

- Minimum 1000 words.
- Minimum 8 unique sources.
- Target distribution: 3 arXiv, 3 Semantic Scholar, and at least 1 ExaSearch source where available.
- If a tool returns too few sources, use all available sources and record the gap in `quality_notes`.
- Every claim needs an inline APA citation.
- References must use academic URLs only: arXiv, Semantic Scholar, or `.edu`.
- Real-world examples must be labeled `Illustrative Example`.
- No invented URLs.

Graceful degradation:

| Missing Field | Replacement |
| --- | --- |
| Author | `Unknown Author` |
| Year | `n.d.` |
| URL | `[URL_NOT_AVAILABLE]` |
| Title | `Untitled Paper` |

Structure:

```text
Abstract -> 4-6 sections -> Key Takeaways -> References
```

### Task 3: Evaluate Content

**Agent:** Content Quality Evaluator  
**Context:** Research Mission, Write Article

Scoring rubric:

| Dimension | Score | Deductions |
| --- | ---: | --- |
| Accuracy | 0-10 | Non-academic URL: -3 each |
| Citation Completeness | 0-10 | Missing citation: -1 each |
| Source Quality | 0-10 | Non-academic source: -2 each |
| URL Validity | 0-10 | Broken/non-academic URL: -2 each |
| Structure | 0-10 | Missing abstract, sections, key takeaways, or references |

Retry logic:

```text
score < 40 and retry_count < 2  -> RETRY_RESEARCH
score < 40 and retry_count >= 2 -> BEST_EFFORT
score >= 40                    -> approved
```

### Task 4: Quality Gate Check

**Agent:** Quality Gate  
**Context:** Research Mission, Write Article, Evaluate Content

Routing:

```text
approved or BEST_EFFORT         -> PROCEED_TO_DELIVERY
RETRY_RESEARCH                  -> RETRY_NEEDED
ERROR or missing approval_status -> PROCEED_TO_DELIVERY with BEST_EFFORT warning
confirmed infrastructure failure -> PIPELINE_ERROR
```

Hard rule: exactly one decision. No content modification.

### Task 5: Manager Review and Score

**Agent:** Workflow Manager  
**Context:** Research Mission, Write Article, Evaluate Content, Quality Gate Check

5-skill framework:

1. **Metrics Recorder:** Extract and timestamp scores from upstream agents.
2. **Multi-Dimension Scorer:** Calculate final quality score.
3. **Workflow State Tracker:** Track retry budgets and hard-stop flags.
4. **Diagnostic Reporter:** Explain gaps, root causes, recommended actions, and suggested queries.
5. **Decision Router:** Approve, approve with notes, reject/retry, or error.

Quality formula:

```text
overall_quality =
  research.confidence * 0.30
+ (min(citations, 8) / 8) * 0.25
+ (accuracy / 10) * 0.25
+ (structure / 10) * 0.20
```

Decision:

```text
>= 0.8 -> APPROVE
>= 0.6 -> APPROVE_WITH_NOTES
<  0.6 -> REJECT_AND_RETRY
```

### Task 6: Compile Final Report

**Agent:** Report Compiler  
**Context:** Quality Gate Check, Manager Review and Score, Write Article, Evaluate Content

Only proceeds if manager decision is `APPROVE` or `APPROVE_WITH_NOTES`.

Output structure:

```text
⚠️ Disclaimer
🎯 Executive Summary
📚 Key Findings
📰 Full Article (verbatim)
🔗 Sources
📊 Evaluation Scorecard
🧠 Manager Review and Log
💡 Recommendations
```

### Task 7: Deliver Clean Report

**Agent:** Document Delivery Agent  
**Context:** Compile Final Report

Responsibilities:

- Remove JSON execution logs.
- Remove routing decisions.
- Remove duplicate article copies.
- Preserve the full article verbatim.
- Deliver only reader-facing markdown.

## Guardrails

| Task | Guard Condition |
| --- | --- |
| Research Mission | `confidence_score` present, 0-1; sources list >= 3 with live URL and APA |
| Write Article | `word_count >= 1000`; >= 6 inline citations; academic references; abstract present |
| Evaluate Content | `overall_score` 0-50; all 5 dimensions present; valid `approval_status` |
| Quality Gate | Exactly one routing decision from valid set |
| Manager Review | `overall_quality` 0-1; valid decision; execution log >= 4 timestamped entries |
| Compile Final Report | All required sections present; full article not summarized |
| Deliver Clean Report | No execution metadata; no duplicate article; clean `.md` only |

## Known Risks And Teaching Failures From The Build

| Issue | Detail | Fix |
| --- | --- | --- |
| Hallucinated sources | `example.com` URLs appeared | Propagate real tool results and enforce URL allowlist |
| Guardrails not yet set in UI | Studio task guardrails were missing | Add task-level guardrails manually |
| Manager goal/backstory incomplete in early UI drafts | The extracted YAML now defines `workflow_manager` clearly | Keep role and backstory explicit in Crew settings |
| Quality Gate bypassed error | Manager overrode `PIPELINE_ERROR` | Tighten decision router |
| Context starvation | Report Compiler could not see article | Fix task context chain |
| Concurrent execution crash | Hierarchical manager invoked same executor twice | Use sequential process for fixed pipelines |

## Retry and Error Boundaries

| Stage | Max Retries | On Exceed |
| --- | ---: | --- |
| Research | 2 | `PARTIAL_RESULTS = true` |
| Writing | 2 | `BEST_EFFORT` delivery |
| Evaluation | 1 | `BEST_EFFORT` delivery |
| Manager | 0 | `HARD_STOP` flag |

## Six-Week Applied Pipeline Engineering Path

### Week 1: Agent Design and Role Clarity

Core concept: An agent is not just a prompt. It is role + goal + backstory + tools.

Andrew Ng-style insight:

> Think of backstory as the system prompt on steroids. It encodes not just instructions but how to think.

Assignments:

- **1.1 Role Audit:** For each agent, verify role clarity, measurable goal, decision-framework backstory, and minimal tools.
- **1.2 Anti-Pattern Identification:** Identify at least three issues in an overly broad "Research and Writing Assistant" agent.

Study keywords:

`agent role definition`, `ReAct framework`, `tool selection principle`, `single responsibility`, `backstory engineering`

### Week 2: Task Design and Context Chains

Core concept: Tasks define data flow. A broken context chain creates hallucination or downstream failure.

Andrew Ng-style insight:

> Think of context as function arguments. If you do not pass the data in, the function cannot use it.

Assignments:

- **2.1 Context Chain Design:** Design a 5-agent website summarization and fact-checking pipeline.
- **2.2 Expected Output Contract:** Write the contract for an academic article evaluator, including fields, data types, and fail conditions.

Study keywords:

`DAG`, `context propagation`, `task dependency management`, `contract-first task design`, `context starvation`

### Week 3: Hierarchical vs Sequential Process

Core concept: Hierarchy sounds powerful, but fixed pipelines are usually more reliable as sequential workflows.

Comparison:

| Dimension | Sequential | Hierarchical |
| --- | --- | --- |
| Execution order | Fixed | Manager decides |
| Manager agent | None | Auto-created or custom LLM manager |
| Debugging | Easier | Harder |
| Best for | Defined pipelines | Dynamic routing |
| Risk | Low | Concurrent calls, opaque delegation |

Assignments:

- **3.1 Process Selection:** Choose sequential or hierarchical for four scenarios and justify.
- **3.2 Debug the Crash:** Diagnose `Executor is already running. Cannot invoke the same executor instance concurrently.`

Study keywords:

`sequential process`, `hierarchical process`, `manager LLM`, `concurrent execution`, `delegation loop`

### Week 4: Guardrails and Output Validation

Core concept: Guardrails are contracts between tasks. They reject malformed responses before they cascade.

Andrew Ng-style insight:

> Guardrails are not optional polish. They are error boundaries.

Assignments:

- **4.1 Design a SQL Guardrail:** Validate safe query shape and reject destructive SQL.
- **4.2 Cascade Failure Trace:** Compare what downstream agents receive with and without guardrails.

Study keywords:

`schema validation`, `XML schema`, `JSON schema`, `error boundary`, `fail-fast`, `graceful degradation`

### Week 5: Failure Analysis and Recovery Patterns

Core concept: Failures are expected events. Production pipelines define recovery behavior.

Failure taxonomy:

| Failure Type | Example | Recovery Pattern |
| --- | --- | --- |
| Cascade | Evaluator wrong status causes gate failure | Fix root decision rule |
| Context starvation | Agent cannot see upstream output | Fix context chain |
| Concurrent execution | Same agent called twice | Switch to sequential |
| Hallucinated sources | `example.com` references | URL verification |
| Token overload | Truncated response | Simplify task |
| Score fabrication | Compiler recalculates score | Copy-verbatim rule |
| Wrong routing | Strong score becomes retry | Total score is only decider |
| Tool rate limiting | HTTP 429 | Retry once, fallback |

Assignments:

- **5.1 Failure Mode Matrix:** Create a 12-failure matrix for Research -> Write -> Review -> Publish.
- **5.2 Root Cause Analysis:** Trace `[ERROR: Article not in context]` backward to at least five possible causes.

Study keywords:

`FMEA`, `circuit breaker`, `retry with backoff`, `BEST_EFFORT`, `PARTIAL_RESULTS`, `dead letter queue`

### Week 6: Pipeline Architecture and Clean Delivery

Core concept: A pipeline is finished only when it produces clean reader-facing output.

Separation of concerns:

```text
Agent Role      -> what it does
Task Description -> how it does it
Expected Output -> what it returns
Guardrail       -> what makes output valid
Context         -> what it can see
```

Assignments:

- **6.1 Pipeline Design:** Design a 5-agent competitor blog monitoring pipeline.
- **6.2 Clean Delivery Layer:** Design a Document Delivery Agent that strips metadata and duplicates from a 2000-word report.

Study keywords:

`separation of concerns`, `pipeline architecture`, `clean output design`, `metadata stripping`, `formatting engine`

## Capstone Project: Build a Multi-Agent Research Pipeline

Requirements:

- Minimum 5 agents.
- Sequential process unless the task order is genuinely unknown.
- At least one guardrail per task.
- Correct context chain.
- Recovery pattern for at least 3 failure modes.
- Final clean `.md` delivery.
- Documented required inputs.
- One quality gate that routes without modifying content.

Grading rubric:

| Criterion | Points |
| --- | ---: |
| Agent role clarity | 20 |
| Context chain correctness | 20 |
| Guardrail coverage | 20 |
| Failure recovery defined | 20 |
| Clean output delivery | 20 |
| Total | 100 |

## Master Keyword Index

Agent design:

`role definition`, `goal specification`, `backstory engineering`, `tool selection`, `single responsibility`, `allow_delegation`

Task and context:

`context chain`, `DAG`, `task dependency`, `expected output contract`, `async execution`, `context starvation`

Process and orchestration:

`sequential process`, `hierarchical process`, `manager LLM`, `concurrent execution`, `workflow routing`

Validation and guardrails:

`XML schema validation`, `JSON schema output contract`, `error boundary`, `cascade failure`, `fail-fast`, `verbatim copy rule`

Failure patterns:

`root cause analysis`, `FMEA`, `BEST_EFFORT`, `PARTIAL_RESULTS`, `retry with backoff`, `dead letter queue`

Architecture:

`pipeline architecture`, `separation of concerns`, `clean document delivery`, `metadata vs content`, `reader-facing output`

## Recommended Study Path

Foundational:

- Andrew Ng: AI For Everyone.
- Andrew Ng: AI Agentic Design Patterns.
- CrewAI official documentation.

Intermediate:

- ReAct: Synergizing Reasoning and Acting in Language Models.
- Toolformer: Language Models Can Teach Themselves to Use Tools.
- AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation.

Advanced:

- ChatDev: Communicative Agents for Software Development.
- AgentBench: Evaluating LLMs as Agents.
- LLM-based Multi-Agent Systems for Software Engineering.

Pipeline engineering:

- Designing Machine Learning Systems, Chip Huyen.
- Building LLM Applications for Production, Chip Huyen.
- Patterns for Building LLM-based Systems, Eugene Yan.

## Lessons From This Build

| Principle | How It Appeared |
| --- | --- |
| Iterate fast, do not over-plan | Pipeline evolved from 3 to 7 agents through failures |
| Understand failure modes | Each run revealed one new failure to fix |
| Simple beats clever | Sequential beat hierarchical for a fixed pipeline |
| Data quality matters most | Real arXiv URLs beat `example.com` every time |
| Measure what matters | 5-dimension rubric with 40/50 pass threshold |
| Build error recovery first | `BEST_EFFORT`, fallbacks, and override rules |
| Separate concerns cleanly | 7 agents, each doing exactly one thing |

Build it. Break it. Fix it. That is how you learn.
