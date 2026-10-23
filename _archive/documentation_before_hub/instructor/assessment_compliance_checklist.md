# Curriculum Assessment Compliance Checklist

Use this checklist for workshop readiness. The canonical [course map](../COURSE_MAP.md) maps controls, learner edits, and actual grader coverage to notebook cell IDs. Learner marks go in the [assessment score tracker](assessment_score_tracker.xlsx). Course sequence and fallback rules are in [PLAYBOOK.md](../PLAYBOOK.md). Instructor repairs for the intentional broken starts are in the [core notebook solution guide](solutions/core_notebook_solution_guide.md).

## Acceptance audit - 19 October 2026

This section supersedes the historical verification record below. Results describe the current local distribution. On 19 October 2026, the user declined physical printing; the digital rubric satisfies the delivery requirement.

| Requested condition | Current evidence | Status |
| --- | --- | --- |
| Clean four-command setup under five minutes | A new isolated `.venv` installed the unchanged workshop requirements in **57.927 seconds**; JupyterLab served `/lab` after **63.976 seconds**. `pip check` found no broken requirements. | Pass on this Mac |
| Offline Labs 1-3 with `USE_LIVE_LLM = False` | Full readiness gate passed: **78 unit + 44 integration = 122 tests**, no failures/errors/skips. Repaired Labs 1-3 each earned **15/15** in real kernels with provider credentials removed, external DNS/connections blocked, and Crew execution tripwires enabled. | Pass |
| All notebook outputs cleared | Literal `jupyter nbconvert --clear-output --inplace` ran on **all 20 distributed notebooks**, including archived lessons. Every code output is empty and execution count null; notebooks total **319,711 bytes**. Test-executed copies and environments remain ignored. | Pass |
| Lab 1/2 sabotage and partial credit | Both labs verified in real kernels at **0/15** unchanged, **5/15** or **10/15** for separate partial repairs, and **15/15** fully repaired. Lab 1 reject-everything/missing-field sabotage and Lab 2 extra-Manager-tool checks also pass. | Pass |
| Five-file Golden Path | [Root manifest](../notebook_manifest.yml) lists preflight, `01_lab_pydantic`, `02_lab_crewai`, `03_lab_security`, and `04_capstone`; no manifest remains inside `notebooks/`. | Pass |
| Legacy material archived | Fugu/advanced orchestration, API boundaries, and legacy A2A notebooks are under `_archive/` or `extensions/`; old FastAPI Capstone and A2A governance starters/solutions are under `_archive/advanced_scaling/assignments/starter_code/`. | Pass |
| Nine lectures and eight briefs mapped | [README interactive syllabus](../README.md#interactive-syllabus-nine-un-mandated-lectures) links all nine lectures to the core notebooks or eight lightweight briefs. | Pass |
| Curated resource library linked | [Library](../resources/curated_resource_library.md) exists and is linked from README. | Pass |
| Obsidian Vault analogy | [Lecture 7](../assignments/assignment_07_context_engineering_access_lists.md#the-obsidian-vault-analogy) and [Lab 2](../notebooks/02_lab_crewai.ipynb) explain customization through injected context without training or changing model weights. | Pass |
| Four-framework comparison | Displayed slide 17 of the main v16 deck contains CrewAI, LangGraph, AutoGen, and Microsoft Agent Framework, with no legacy label. Stale external notebook links have been corrected. | Pass |
| ADR 6/7/7 rubric | One-page [PDF](../output/pdf/capstone_paper_adr_quick_sheet.pdf) and [scoring anchors](capstone_paper_adr_quick_sheet.md) are ready for digital use. The user declined physical printing on 19 October 2026. | Pass; digital delivery |
| Lab scaling and 100-point gradebook | Formula evaluation checks raw `/15 x 20 / 15`, maximum **100/A**, partial **42.66666666666667/F**, zero **0/F**, grade thresholds, and blank-score behavior at first/middle/last learner rows. | Pass |
| Live demo isolated at Day 2 end | [Bonus notebook](../extensions/bonus_live_demo.ipynb) is separate, disabled by default, ungraded, and scheduled after required work and defenses. Core notebooks contain no provider execution branch. | Pass |

Setup evidence is stored locally in `.test-results/clean-install-20261019/result.json`, with requirement-file hashes, install log, and Jupyter startup log. The test environment started without a `.venv` at that path; the existing working environment was preserved. This verifies a fresh install on this Mac, not a timing guarantee for every learner computer. The final readiness and distribution audit are recorded below.

## Current readiness evidence

Final gate: `python tools/check_readiness.py` using the fresh environment plus the exact `requirements-test.txt` pins. Python **3.12.3**, macOS **26.3 arm64**, `pip check` clean, **78 unit + 44 integration = 122 passed**, no failures, errors, or skips. Run ID: `20261019T041127Z-eeef0c2d`. Verification-input SHA256: `ce5656e131c67a00d62e5c13dde02f0ce3918eb8f198307dd60acffd00f82ed6`.

Local receipts: `.test-results/readiness/summary.json`, `.test-results/acceptance/audit.json`, and `.test-results/assessment/tracker-audit.json`. The acceptance audit matches current requirement hashes, the exact five-file layout, all notebook outputs, nine lecture rows/eight brief links, archived starters, displayed framework slide 17, and the final workbook hash against its 21 calculation cases. All **71 active Markdown files** have valid local links and heading anchors. The bonus is checked with a local fake SDK and in a disabled real kernel; no paid provider call was needed.

Current artifact SHA256 values:

- Main v16 deck: `59c49d06c3802cb3b245a832c7fbd537d098d2eed0bf675c896af18edc2f6db4`.
- Learner score tracker: `442807f4ce8687117d6342567201786ebb95422ccae51bb3ed087f3895cae093`.
- Print-ready ADR PDF: `50d0246fb72ce6f4d42cf8caa0ed8b61ba50816bc0becd65f2e600754d8a871f`.

The PDF was rendered and visually inspected. Physical printing is not required following the user's instruction on 19 October 2026; no physical print is claimed. All requested checklist items, with that change, are complete. Remote Windows/Linux CI and live-model reliability are outside this local verification result.

## Assessment plan: 100 marks

| Component | Course marks | Required evidence | Where to check |
| --- | ---: | --- | --- |
| Lab 1 · Context Engineering: Typed Contracts | 20 | Bad mock output rejected; valid output accepted; raw grader `/15` converted to `/20`. | [Lab 1](../notebooks/01_lab_pydantic.ipynb), grader cell |
| Lab 2 · Multi-Agent Management: Manager audit | 20 | Grader checks Manager approval/delegation without writing and the Architect task in Coder context. Inspect the deterministic typed `CodePatch` fixture and supplied Coder/QA tool lists separately. | [Lab 2](../notebooks/02_lab_crewai.ipynb), cells 4, 6, 8 (audit), 9 (decision), and 11 (grader); no Crew execution |
| Lab 3 · Manager Oversight: Code Validation | 20 | Unsafe SQL-like input is rejected; loop stops after 3 retries and escalates; raw grader `/15` converted to `/20`. | [Lab 3](../notebooks/03_lab_security.ipynb), grader cell |
| Capstone code | 20 | Pydantic rejects failed QA; Coordinator validates before Security starts; Manager/Pen Tester tool scopes are separate; typed `SecurityAuditResult` is returned. | [Capstone notebook](../notebooks/04_capstone.ipynb), auto-grader and `tests/` |
| Capstone ADR and defense | 20 | Three questions: risk, governance/evidence, next step; rubric 6/7/7. | [Capstone brief](../assignments/ex5_capstone_virtual_software_company.md) |
| **Total** | **100** | | |

The gradebook conversion is `raw_lab_score × 20 ÷ 15`. Keep the raw `/15` signal visible for the Stop-at-Green rule. A sound one-page Paper ADR is an accepted Capstone pass route when code cannot run because of hardware, package, power, or connectivity constraints.

## Historical verification record (through 18 October 2026)

| Check | Evidence / completion rule | Status | Date / notes |
| --- | --- | :---: | --- |
| Repository tests | `python tools/check_readiness.py` after installing `requirements-test.txt`. | Pass (Python 3.12.3, 2026-10-17) | 112 passed: 73 unit and 39 integration; no failures, errors, or skips. Exact direct pins and `pip check` passed. |
| Required notebook execution | Preflight, three labs, and Capstone execute using deterministic local data. | Pass (real Jupyter kernels, 2026-10-17) | All five required notebooks executed across 14 starter/partial/fixed scenarios. Provider credentials were omitted and live-call/network tripwires remained untriggered in these scenarios. |
| Lab 1 broken/partial/fixed | Grader reports 0, partial, then 15/15 after separate interventions. | Pass (automated kernel tests) | 0/15, 5/15, 15/15. |
| Lab 2 broken/partial/fixed | Broken Manager configuration fails; Manager-only repair earns partial marks; repaired Manager and Architect-task context earn 15/15. | Pass (automated kernel tests) | Starter 0/15; permissions only 5/15; context only 0/15; both 15/15. These remain structural configuration/fixture checks; no live Crew or QA task runs. |
| Lab 3 broken/partial/fixed | Weak validator/unbounded loop fails; partial fixes earn partial marks; full controls earn 15/15. | Pass (automated kernel tests) | 0/15; validator only 7/15; bounded retries only 8/15; both controls 15/15. |
| Manager's Audit Gate | Run the supplied Lab 2 audit with broken, partial, and corrected configurations; inspect the local QA inbox. | Pass (automated unit + kernel tests) | Broken and partial configurations block; corrected configuration admits one typed item. Overbroad tools, wrong owners, invalid/constructed payloads, and missing context/output models block. Replaying the action after a bad proposal clears a previously accepted inbox item. No release or provider call runs. |
| Management Oversight | Inspect the Lab 3 decision against actual fixture calls, tool log, cost, and escalation. | Pass (automated unit + kernel tests) | Partial states block; full repair records escalation at four calls/$0.20 with no release approval. Invalid evidence and an unsafe history entry block. A successful worker stops early. |
| Capstone grader broken/fixed | The initial tool boundary and coordinator gate fail; complete repairs pass all 20 code points. | Pass (automated kernel tests) | Starter 5/20; instructor-guide repairs 20/20. A forged failed-QA model is rejected before Security starts; unsafe teaching markers produce a typed rejection. |
| Two-team Capstone handoff | The local Dev adapter's output is validated before calling the local Security adapter; the optional live bridge passes validated output to the second Crew. | Pass (automated integration tests) | Actual notebook pipeline and `tests/test_ex5_capstone.py` pass. `tests/test_capstone_bridge.py` verifies valid, missing, and failed-QA outputs using the actual optional branch with local fake endpoints. This is not a live provider result. |
| Notebook handout is clean | Active distributed `.ipynb` files have empty code outputs and null execution counts. | Pass (automated) | All nine active notebooks checked. Core execution hashes confirm handouts remain unchanged. Archived notebook execution/cleanliness is outside this gate. |
| Deterministic toggle | With `USE_LIVE_LLM = False`, core labs and Capstone run without provider credentials or runtime network calls. | Pass (local deterministic path) | Teach this as a deliberate mock/stub mode, not a Wi-Fi test. The preflight asserts the toggle; optional live calls remain off. No network-disconnection test is required. |
| Learner setup | Platform-specific setup instructions work in a fresh Python 3.12 virtual environment; ZIP route is documented. | Pass on this Mac (2026-10-08) | Fresh install of the final `requirements-workshop.txt` took 73.1 seconds; `pip check` found no broken requirements; JupyterLab 4.6.4 started on localhost; the full core suite passed. Setup plus verification took 86.4 seconds. Learner network and hardware can change timing. |
| Paper ADR fallback | Instructor accepts the one-page ADR and grades with the Capstone rubric. | Documented | Playbook and Capstone assignment define the fallback and 20-point rubric; instructor briefing remains to be done. |
| Historical v14 slide review | Prior 14-slide deck review covering MAS foundations, three management labs, framework literacy, and the two-team Capstone. | Superseded by v15 | The v14 review recorded its own package/layout/font/import/arithmetic checks and hash. Its assertions describe that historical file, not the active deck. |
| Historical v15 teaching-design review | The 14-slide deck keeps the course content while adding prediction, learner decisions, evidence checks, reflection, transfer, and explicit assessment scaling. | Superseded by v16 | Review recorded 2026-10-17 for the pre-navigation v15 snapshot. Slide 1 opens with the Vibe Coding vs. Governed Engineering contrast; slide 5 assigns Knowledge, Drafting, and Compliance roles and adds a no-source instructor reveal; slide 6 shows Code `/20` + ADR `/20`. Independent visual QA reviewed slides 1, 4–6, 8, 9, 12, and 14 with no fit issues or collisions. Slides 2, 10, and 13 carry forward unchanged from v14. The score conversion is raw `/15 × 20 ÷ 15` to `/20`; the 3×20 + 20 + 20 total equals 100. SHA256: `d475a7d307da7b7dbb47ac3e1638952acd63e1e06615f1d65def71f9b9cef110`. |
| Active v16 deck and learner navigation | Current 21-slide deck, README index, curriculum maps, and five formative notebook checkpoints agree. | Pass (2026-10-18) | Package, layout, font-policy, native-table arithmetic, and re-import checks passed. Independent visual QA inspected all 21 LibreOffice-rendered slides. All 51 internal slide links resolve; 360 local documentation/notebook links and anchors passed. Existing notebook code cells, positions, outputs, and metadata were preserved. See the [alignment record](agent_building_slide_alignment.md) for scope and verification limits. |
| Grade arithmetic | Three labs scale from `/15` to `/20`; Capstone code and ADR contribute `/20` each. | Pass | Verified after score-tracker formula update. |
| NIST / CISA teaching alignment | Map the relevant governance examples to official control and secure-AI guidance without claiming certification. | Pass (conceptual mapping) | Playbook maps Lab 2 to NIST AC-5/AC-6 and Lab 3 to SI-10, and links the joint CISA/NCSC secure-AI lifecycle guidance. |
| Cost-aware routing scope | The Capstone router is pre-written and ungraded; it is not a fourth lab. | Pass | The Manager example routes low/medium tasks to Fast and high tasks to Expert. A separate duplicate routing exercise was moved to `_archive/`. |

## Historical automated readiness run (17 October 2026)

On **17 October 2026**, a fresh Python **3.12.3** virtual environment on **macOS 26.3 arm64** installed `requirements-test.txt`. The full readiness command exited **0** with **73 unit + 39 integration = 112 passed**, no failed/error/skipped tests, and no incompatible dependencies. All eight direct package pins matched. Run ID: `20261017T090613Z-8d5290ed`.

Verification-input SHA256: `970852888845818efb502b030f21f9ecebb4fafc9dd50a3090ea9e86fe2c3ca7`. The generated `.test-results/readiness/summary.json` records per-file hashes, versions, JUnit results, and executed copies. Rerun after changing an input; historical success is not a current result.

The clearance matrix initially exposed a public-to-confidential authorization defect in `src/enterprise_agent_team.py`. The policy now checks the full public/confidential/restricted order, and all nine combinations pass. Learner TODOs and assessment marks remain unchanged.

The [CI workflow](../.github/workflows/readiness.yml) uses the same gate on Ubuntu and Windows for pull requests, pushes, and manual dispatch. It is prepared locally; remote CI has not run in this session. The [development guide](../DEVELOPMENT.md) defines the early unit-test cycle and the evidence limits. This is a deterministic workshop distribution result, not a production AI deployment certification.

## Test crosswalk

| Outcome | Test evidence |
| --- | --- |
| Pydantic rejects unsafe or extra handoff data | `tests/test_schemas.py`, `tests/test_handoffs.py`, and Lab 1 grader |
| Bounded repair terminates and escalates | `tests/test_adversarial_scenarios.py::test_infinite_coder_loop_stops_after_three_calls_and_escalates`; `tests/test_ex5_capstone.py` |
| Tool policy rejects malicious or unauthorized requests | `tests/test_adversarial_scenarios.py`, `tests/test_tools.py`, and Lab 3 grader |
| Manager permissions, context, ownership, and current proposal | `tests/test_management_controls.py` plus real Lab 2 kernel scenarios in `tests/test_notebooks.py` |
| Dev-to-Security handoff is automatic, typed, and rejects failed QA before starting Security | `tests/test_ex5_capstone.py` and repaired Capstone kernel assertions |
| Separate live bonus stays disabled without credentials and validates structured results/errors with a fake SDK | `tests/test_capstone_bridge.py` and the disabled bonus kernel scenario in `tests/test_offline_runtime.py` |
| Core notebook sources stay runnable and clear | `tests/test_notebooks.py`; tripwire behavior in `tests/test_offline_runtime.py` |
| Readiness gate fails on invalid environments and failed/missing/empty/skipped reports | `tests/test_readiness.py` |

## Score record

| Learner / cohort | Lab 1 raw /15 | Lab 1 /20 | Lab 2 raw /15 | Lab 2 /20 | Lab 3 raw /15 | Lab 3 /20 | Capstone code /20 | ADR /20 | Total /100 | Grade | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| | | | | | | | | | | | |

Grade bands: A 80–100; B 65–79; C 50–64; F below 50. The spreadsheet is the individual learner tracker; this table is a compact paper backup.
