# Verification Pyramid for Managing Multi-Agent Teams

Use the [development workflow](../DEVELOPMENT.md) to create a failing regression test before changing a behavior. Install `requirements/maintenance.txt` in Python 3.12. The required workshop remains three labs and one Capstone.

## 1. Unit tests: individual rules

Run these during editing:

```sh
python -m pytest tests -m unit -q
```

| Rules | Tests |
| --- | --- |
| Pydantic contracts and unsafe paths | `tests/test_schemas.py` |
| Sensitivity-aware memory | `tests/test_memory.py` |
| Tool scope and all clearance combinations | `tests/test_tools.py` |
| Manager role tools, task ownership/context, and typed proposal validation | `tests/test_management_controls.py` |
| Four-call repair bound, successful early stop, simulated cost, and escalation evidence | `tests/test_management_controls.py` |
| Verification environment, reports, and gate failure behavior | `tests/test_readiness.py`, `tests/test_offline_runtime.py` |

The management tests load the actual pure definitions from the notebooks. They do not maintain a second implementation of the audit or oversight logic.

## 2. Integration tests: handoffs and workflow

```sh
python -m pytest tests -m integration -q
```

| Workflow | Tests |
| --- | --- |
| Typed task/patch/QA handoffs | `tests/test_handoffs.py` |
| Gateway authorization and TeamLog restrictions | `tests/test_intra_team_handoffs.py` |
| Complete local team flow and bounded repair | `tests/test_system.py`, `tests/test_ex5_capstone.py` |
| Hallucinated fields, overbroad authority, and a permanently failing Coder | `tests/test_adversarial_scenarios.py` |
| Separate live bonus: disabled mode, key check, typed response, and error paths using a fake local SDK | `tests/test_capstone_bridge.py` |

The system tests are also marked `integration`, so the readiness gate includes them. The bonus tests use a fake SDK to check the actual notebook's typed-output and failure paths without calling a provider; the filename retains its earlier bridge-test name.

## 3. Curriculum integration: real Jupyter kernels

```sh
python -m pytest tests/test_notebooks.py tests/test_offline_runtime.py -m integration -v
```

`tests/test_notebooks.py` reads the root manifest and handouts. It exercises preflight, starter/partial/fixed states for the three labs (including both Lab 2 partial repairs), and starter/fixed Capstone states. A separate check inspects output cleanliness across core, extension, bonus, and archived notebooks.

The tests apply instructor-guide repairs only to in-memory copies. They verify raw grader scores, Manager decisions, removal of stale QA work, retry/cost bounds, failed-QA rejection before Security starts, and typed audit results. The scanner checks only the course's SQL/XSS teaching markers.

Each scenario uses a separate kernel with provider credentials omitted and runtime tripwires for live Crew execution and external DNS/connections. Dedicated negative tests deliberately trigger those guards and require a failure. Loopback connections remain available for Jupyter. The guards support verification of this path; they are not a production sandbox.

## 4. Readiness and CI

Run the full gate before distribution or review:

```sh
python tools/check_readiness.py
```

It checks the Python version and exact direct dependency pins, runs `pip check`, then runs unit and integration stages. Any failed/error/skipped test, missing/empty report, timeout, or changed verification input makes the command fail.

Reports in `.test-results/readiness/` contain JUnit XML, executed copies, logs, environment versions, and input hashes. The [GitHub Actions workflow](../.github/workflows/readiness.yml) runs the same command on Ubuntu and Windows. Local results and remote CI results are separate evidence.

Record the actual run in the [assessment compliance checklist](assessment_compliance_checklist.md). Passing tests establish the stated deterministic workshop behaviors. They do not prove live LLM reliability, full vulnerability detection, or production deployment security.

## Review that still needs an instructor

- Check learning objectives, instructions, and the marked TODOs against the solution guide.
- Review slide readability and the short learner decision/ADR explanations.
- Confirm classroom hardware, package availability, accessibility, and Paper ADR arrangements.
- Preserve the three `/15` lab graders, `/20` Capstone code rubric, and `/20` ADR rubric.

Optional extension notebooks receive cleanliness checks. Their full behavior, archived API/A2A lessons, and the nested CrewAI project are outside this gate. Add explicit tests and dependencies before claiming readiness for those materials.

## Instructor diagnosis order

Inspect the contract, caller/tool authority, supplied context, and retry evidence before investigating a live model. Use deterministic regressions to preserve each repaired behavior.
