# Curriculum Maintenance Checklist

Use the [automated development workflow](../DEVELOPMENT.md) throughout editing. Run its full readiness gate before releases and teaching, then use this checklist for curriculum and distribution review.

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

## 2. Optional Advanced Identity and Tool Matrix

Checklist:

- [ ] If maintaining the archived cross-organization A2A extension, open `_archive/advanced_scaling/instructor/a2a_identity_tool_matrix.md`.
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

- [ ] Edit current handouts in place. If using `tools/build_core_notebooks.py`, run it on a private copy first and review its output against the current handouts before replacing them. Preserve supplied management actions and cell IDs.
- [ ] Clear outputs before commit.
- [ ] Search for absolute paths such as `/Users/` or `C:\\Users\\`.
- [ ] Confirm every core notebook sets `USE_LIVE_LLM = False` and contains no provider-call branch. Keep optional live execution only in `extensions/bonus_live_demo.ipynb`, defaulted off and scheduled at the end of Day 2.
- [ ] In Python 3.12 with `requirements/maintenance.txt`, run `python -m pytest tests/test_notebooks.py -v`.

Commands:

```bash
rg "/Users/|C:\\\\Users\\\\" notebooks
python -m pytest tests/test_notebooks.py -v
```

## 4. Assignment and Rubric Alignment

Checklist:

- [ ] Every assignment has clear deliverables, constraints, and rubric weights.
- [ ] Every implementation-heavy assignment has starter code.
- [ ] Every core assignment has an instructor solution guide.
- [ ] `assignments/basic_agent_governance_labs.md` stays aligned with its local examples and the Capstone Security Team; the external A2A QA exercise stays archived.
- [ ] Required tests named in assignment text are represented in tests or instructor guidance.
- [ ] The [grading files](GRADING.md) match the three `/15` lab graders scaled to `/20` each, Capstone code `/20`, and ADR `/20`. Formative exercises and optional extensions add no marks.

Notes:

- Keep the required course to three graded labs and one Capstone.
- The Capstone's cost-aware routing helper stays pre-written and ungraded. Do not turn it into a fourth lab or a router grading task.
- Optional homework tracks remain outside the required two-day path.

## 5. Secret and Key Scrubbing

Checklist:

- [ ] No API keys in notebooks, docs, or starter files.
- [ ] `.env` is ignored and absent from the repo.
- [ ] The separate bonus notebook gates live calls behind `USE_LIVE_LLM = False`; core notebooks contain no live calls.
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
python tools/check_readiness.py
```

## 7. Release Hygiene

Checklist:

- [ ] No `__pycache__`, `.pytest_cache`, `.DS_Store`, or `.env` files.
- [ ] Markdown local links resolve.
- [ ] Resource library uses links/transcripts instead of heavy videos.
- [ ] README and setup guide point to the current notebook and assignment map.
- [ ] `notebooks/` contains exactly the five canonical handouts; `notebook_manifest.yml` stays at the repository root.
- [ ] README explicitly links all nine lectures to the five core notebooks or eight lightweight assignment briefs, and links `resources/curated_resource_library.md`.

Commands:

```bash
find . -name "__pycache__" -o -name ".pytest_cache" -o -name ".DS_Store" -o -name ".env"
python tools/check_readiness.py
```
