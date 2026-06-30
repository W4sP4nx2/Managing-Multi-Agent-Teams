# Curriculum Maintenance Checklist

This is the boring manual grind that keeps the course coherent. Run it before major releases, after schema changes, and before teaching a workshop.

## 1. Schema Synchronization

The same concepts appear in several teaching contexts: `TaskSpec`, `CodePatch`, `ToolRequest`, `AgentIdentity`, `ReviewDecision`, `PullRequestSummary`, `WeatherRequest`, `WeatherResponse`, `EditorFeedback`, `SecurityIncidentTicket`, `ProjectPlan`, and `TeamCommitment`.

Checklist:

- [ ] Run `rg "class (TaskSpec|CodePatch|ToolRequest|AgentIdentity|ReviewDecision|PullRequestSummary|WeatherRequest|WeatherResponse|EditorFeedback|SecurityIncidentTicket|ProjectPlan|TeamCommitment)"`.
- [ ] Confirm duplicate schemas are intentional teaching copies, not stale versions.
- [ ] If a field is added to `src/enterprise_agent_team.py`, update starter code, notebooks, tests, and solution guides.
- [ ] Prefer importing from `src/` in production-style examples when it does not make the notebook harder to understand.
- [ ] Keep `extra="forbid"` on schema boundaries that represent inter-agent contracts.

Command:

```bash
rg "class (TaskSpec|CodePatch|ToolRequest|AgentIdentity|ReviewDecision|PullRequestSummary|WeatherRequest|WeatherResponse|EditorFeedback|SecurityIncidentTicket|ProjectPlan|TeamCommitment)" .
```

## 2. A2A Identity and Tool Matrix

Checklist:

- [ ] Open `instructor/a2a_identity_tool_matrix.md`.
- [ ] Confirm each role has an explicit trust tier.
- [ ] Confirm every tool in an enum has a handler or a deliberate denial path.
- [ ] Confirm string literals match exactly across notebook, starter, and solution files.
- [ ] Confirm external/vendor identities cannot access restricted data.

Common drift:

- `risk="high"` in one file vs. `Risk.HIGH` in another.
- `execute_tests` vs. `run_tests`.
- `security_reviewer` vs. `security`.

## 3. Notebook Hygiene

Checklist:

- [ ] Regenerate notebooks from `tools/build_core_notebooks.py`.
- [ ] Clear outputs before commit.
- [ ] Search for absolute paths such as `/Users/` or `C:\\Users\\`.
- [ ] Confirm all live LLM cells default to `USE_LIVE_LLM = False`.
- [ ] Run `python3 -m pytest tests/test_notebooks.py -v`.

Commands:

```bash
python3 -B tools/build_core_notebooks.py
rg "/Users/|C:\\\\Users\\\\" notebooks
python3 -m pytest tests/test_notebooks.py -v
```

## 4. Assignment and Rubric Alignment

Checklist:

- [ ] Every assignment has clear deliverables, constraints, and rubric weights.
- [ ] Every implementation-heavy assignment has starter code.
- [ ] Every core assignment has an instructor solution guide.
- [ ] `assignments/basic_agent_governance_labs.md` stays aligned with NB1, NB5, NB10, NB11 builder exercises and `instructor/solutions/basic_agent_governance_labs_solution_guide.md`.
- [ ] Required tests named in assignment text are represented in tests or instructor guidance.
- [ ] `instructor/grading_rubrics.xlsx` matches the assignment list.

Notes:

- Homework F is intentionally not a graded implementation lab. It is reading and design discussion.
- Fugu-style RL/evolutionary orchestrator training should not be graded in this course.

## 5. Secret and Key Scrubbing

Checklist:

- [ ] No API keys in notebooks, docs, or starter files.
- [ ] `.env` is ignored and absent from the repo.
- [ ] Live LLM cells are gated behind `USE_LIVE_LLM = False`.
- [ ] Placeholder keys are clearly fake, such as `sk-internal-admin` for local API identity tests.

Command:

```bash
rg -n "(sk-[A-Za-z0-9_-]{20,}|OPENAI_API_KEY=.*[A-Za-z0-9]{10,}|ANTHROPIC_API_KEY=.*[A-Za-z0-9]{10,}|api_key\\s*=\\s*['\\\"][A-Za-z0-9_-]{20,})" .
```

## 6. Starter Code vs. Solution Drift

Checklist:

- [ ] Starter files parse without syntax errors.
- [ ] Starter TODOs match the solution's conceptual shape.
- [ ] Solutions run without modifying tests.
- [ ] New tools added to solutions also appear in starter enums or TODOs.
- [ ] New schemas added to assignments also appear in starter files.

Commands:

```bash
python3 -B -c "import ast, pathlib; files=[p for p in pathlib.Path('assignments/starter_code').glob('*.py')]; [ast.parse(p.read_text(), filename=str(p)) for p in files]; print('starter syntax ok')"
python3 -m pytest tests/ -v --tb=short
```

## 7. Release Hygiene

Checklist:

- [ ] No `__pycache__`, `.pytest_cache`, `.DS_Store`, or `.env` files.
- [ ] Markdown local links resolve.
- [ ] Resource library uses links/transcripts instead of heavy videos.
- [ ] README and setup guide point to the current notebook and assignment map.

Commands:

```bash
find . -name "__pycache__" -o -name ".pytest_cache" -o -name ".DS_Store" -o -name ".env"
python3 -m pytest tests/ -v --tb=short
```
