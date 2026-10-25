# Instructor Playbook

Private instructor reference for **Managing Multi-Agent Teams**. Keep this file and solution guides out of the learner pack. Learners start at the [master hub](README.md).

The current route has **seven notebooks and six slides**. Three lab scores `/15` each convert to `/20`; Capstone code `/20` and ADR `/20` complete the `/100` portfolio. The required runtime uses deterministic local fixtures, no provider APIs or API keys, and actual API cost **$0.00**. Factory work includes real local Git/files and explicit stage approvals; publication is local. Fixture scans and scores do not establish comprehensive security, privacy compliance, or live-model reliability.

## Contents

- [Course route, skill transparency and code-cell map](#course-manager-notebook-assignment-path)
- [Setup and go/no-go readiness](#course-delivery-readiness-checklist)
- [Teaching playbook and discussion prompts](#teaching-notes)
- [Five-minute deterministic factory demonstration](#demo-script)
- [Assessment files, marks and calculation rules](#grading)
- [Paper ADR worksheet and partial credit](#capstone-paper-adr-quick-sheet)
- [Private delivery schedule](#delivery-schedule)
- [Notebook and control crosswalk](#notebook-control-crosswalk)
- [Teaching-design rationale and AI-use policy](#stanford-teaching-guide-alignment)
- [Management principles and evidence](#management-principle-matrix)
- [Technical scenarios and instructor Q&A](#technical-implementation-playbook)
- [Tests, notebooks and verification limits](#verification-pyramid)
- [Maintenance and release hygiene](#curriculum-maintenance-checklist)
- [Scope and research boundaries](#scope-alignment-verification)
- [Assessment evidence and historical verification](#assessment-compliance-checklist)
- [Supplemental Governance Practice Exercises: Solution Guide](#basic-agent-governance-labs-solution-guide)
- [Ex1 Solution Guide: Agent Roster & SOPs](#ex1-solution-guide)
- [Ex2 Solution Guide: Theory-of-Mind Memory System](#ex2-solution-guide)
- [Ex3 Solution Guide: RAG & MCP Architecture](#ex3-solution-guide)
- [Ex4 Solution Guide: Trust & Governance Matrix](#ex4-solution-guide)
- [Capstone Solution Guide](#ex5-capstone-solution-guide)

The older standalone notes are consolidated here. Stable explicit anchors preserve links to their original sections. The current [core notebook solution guide](instructor/solutions/core_notebook_solution_guide.md) remains separate because automated rehearsal reads its documented repairs. Historical and optional examples are marked as references; they add no required work or marks.

---

<a id="course-manager-notebook-assignment-path"></a>

## Instructor Notebook and Assignment Path

Start with the canonical [COURSE_MAP.md](COURSE_MAP.md) for the purpose, exact notebook cell IDs, learner edits and grader coverage. The [teaching notes](#teaching-notes) contain scripts, preparation, and handover guidance. This page maps the seven-notebook course route: preflight, three labs, the Capstone, the deterministic Software Factory, and local CI/CD.

| Order | Notebook or brief | Instructor focus | Required evidence |
| --- | --- | --- | --- |
| 0 | [Preflight](notebooks/00_sandbox_preflight.ipynb) | Confirm dependencies, deterministic mode, notebook kernel, and repository-root workspace. | Preflight completes without provider credentials. |
| 1 | [Lab 1](notebooks/01_lab_pydantic.ipynb) · [Assignment 03](ASSIGNMENTS.md#assignment-03-architectural-supervision) | Repair the weak Pydantic data contract. | Supplied invalid output is rejected and valid data passes; grader 15/15. |
| 2 | [Lab 2](notebooks/02_lab_crewai.ipynb) · [Assignment 04](ASSIGNMENTS.md#assignment-04-code-auditing) | Inspect the Skill Transpa`rency Matrix before task setup, then repair the Manager's tools and Coder's Architect-task dependency. | Structural grader 15/15; inspect the local typed `CodePatch` fixture separately. |
| 3 | [Lab 3](notebooks/03_lab_security.ipynb) · [Assignment 06](ASSIGNMENTS.md#assignment-06-code-validation) | Combine unsafe-input validation and bounded retries. | SQL-like fixture blocked; one initial call plus three retries, then escalation; grader 15/15. |
| 4 | [Capstone notebook](notebooks/04_capstone.ipynb) · [brief and ADR](ASSIGNMENTS.md#ex5-capstone-virtual-software-company) | Connect deterministic Development and Security adapters through `DevDeliverable`; inspect the separate Crew configurations. | Failed QA rejected, validation precedes Security start, separate Security tools, typed audit result; grader 20/20 and ADR /20, or sound Paper ADR fallback. |
| 5 | [Software Factory Simulation](notebooks/05_live_software_factory.ipynb) | Review fixture roles, simulated budget, bounded checks, and human gates. | Candidate revision, review reports, ledger and decisions; actual API cost $0.00. |
| 6 | [Local CI/CD](notebooks/06_local_cicd.ipynb) | Reject missing/stale evidence and require final local publication approval. | Exact-candidate checks, failure evidence, and matching local file/receipt when approved. |

<a id="course-manager-notebook-assignment-path--stable-code-cell-map"></a>

### Stable code-cell map

Use stable IDs when diagrams change numeric cell positions. Run cells in order after each repair.

| Notebook | Edit or observation IDs | Verification IDs and limits |
| --- | --- | --- |
| Lab 1 | `lab1-broken-state`, `lab1-learner-workspace` | `lab1-auto-grader`: range 5, extra-field rejection 10; typed-valid shape gates both. |
| Lab 2 | `88df3214` agents → `lab2-skill-transparency` → `lab2-task-configuration` → `38b0ca66` fixture | `lab2-manager-audit-gate`, `lab2-manager-audit-decision`, `84aaa3ad` grader. Manager tools/delegation 5; Architect context 10. No Crew or QA task executes. |
| Lab 3 | `03_guardrails_security_and_repair-02` input model, `MAX_RETRIES=3`, loop | `lab3-management-oversight`, `lab3-manager-decision`, `03_guardrails_security_and_repair-06` grader; raw credit 4/3/3/3/2. |
| Capstone | `capstone-04` contract; `capstone-06` Coordinator; `capstone-11` Security tools | `capstone-15` grader: tools 5, failed-QA + validation ordering 10, typed audit 5. `capstone-17` adversarial fixture; `capstone-18` ADR. |
| Factory | Role/config and typed fixture inspection; temporary isolated Git rehearsal | Compare exact candidate hash/revision, six labeled fixture decisions, simulated ledger and publication receipt. CLI supplies actual human gates. |
| Local CI/CD | Preflight/security commands; denied publication and mutated candidate rehearsals | Missing approval and stale evidence must block. Keep old publication unchanged on denial; actual API cost remains zero. |

The full [control and cell map](COURSE_MAP.md#control-and-cell-map) includes the boundaries of each fixture. The preserved [core solution guide](instructor/solutions/core_notebook_solution_guide.md) contains repair instructions and is private.

<a id="course-manager-notebook-assignment-path--skill-transparency-matrix-in-lab-2"></a>

### Skill Transparency Matrix in Lab 2

Slide 4 and the notebook expose configured authority before the learner creates tasks. Markdown cell `lab2-skill-transparency-guide` explains the management decision. Code cell `lab2-skill-transparency` follows the actual Engineering Manager, Coder, and QA Agent definitions and precedes `lab2-task-configuration`.

`build_skill_transparency` reads each Agent's current tools and their actual name/description metadata. The displayed columns are **Role**, **Actual tools**, **Allowed tools**, and **Least privilege**. Each detail exposes **Action, Input, Output, Warning** from the configured tool description. The cell does not call tools, change permissions, train a model, or run a Crew.

The starter Manager exposes writing and approval, so its least-privilege result is false. After the learner removes its writing tool, rerunning the matrix should show the exact approval-only allowlist and a true result. Coder retains the writing tool; QA retains `run_tests_tool`. The check requires exact names with no duplicates. A row that merely omits an excess tool from a printed list would hide the defect; inspect the actual Agent object instead.

Ask the learner which excess permission they found, which role still owns writing, and what evidence supports the repair. Tool descriptions help an agent choose an action. The framework's configured tool list controls exposure inside that framework, while OS permissions, credentials, process isolation, and independent production policy require separate controls.

<a id="course-manager-notebook-assignment-path--executive-brief-evidence-audit"></a>

### Executive-brief evidence audit

| Module | What the course establishes | Boundary to explain |
| --- | --- | --- |
| 1 · Contracts | Declared Pydantic fields, range/extra-field constraints, and supplied rejection probes | A schema does not establish truth, eliminate hallucinations, or detect arbitrary PII without explicit rules. |
| 2 · Team | Actual tool metadata, role allowlists, task-context declarations, and local audit/inbox behavior | Available context does not prove a real model follows a rule; the foundation lab executes fixtures. |
| 3 · Guardrails | Supplied unsafe-input rejection, bounded mock call count, cost fixture, and escalation record | Selected fixtures do not prove complete injection defense or unrestricted production cost control. |
| 4 · Capstone and factory | Validated Development-to-Security adapter handoff, role separation, actual local files/Git/review evidence, and explicit publication gates | The Capstone uses local Python adapters rather than running both Crews. Publication is local, not a hosted production deployment. |

The deterministic factory supports repeatable local demonstrations after dependency setup. Its actual API cost is $0.00. Fixture checks provide evidence about those cases, with no general guarantee of reliability, security, privacy compliance, or enterprise readiness. Retain the /100 portfolio rubric without treating a score as certification.

<a id="course-manager-notebook-assignment-path--team-boundary"></a>

### Team boundary

Labs teach the Engineering Manager, Coder, and QA pattern. The Capstone adds a Security Manager and Pen Tester. The required workflow runs ordinary Python adapters, while separate CrewAI objects model the teams. All foundation notebooks keep `USE_LIVE_LLM = False`. The factory and CI/CD use deterministic fixtures with actual API cost $0.00 and no API keys. Dependencies need installation before offline execution; the historical bonus is a fixture-only reference. The archive at [`_archive/advanced_scaling/`](_archive/advanced_scaling/README.md) retains network A2A material outside the learner path.

Lab 2 context makes Architect rules available; it does not prove a model followed them. Its tool lists are framework permissions, not OS isolation. Its QA tool and the Capstone scanner are fixtures, not real test/scanning services. Use [the course map's evidence limits](COURSE_MAP.md#what-the-graders-actually-check) when briefing another instructor.

<a id="course-manager-notebook-assignment-path--grading"></a>

### Grading

Each lab auto-grader reports `/15`; the assessment tracker converts raw lab scores to `/20`. Capstone code is `/20`; ADR and defense are `/20`. See [the compliance checklist](#assessment-compliance-checklist) for readiness and test evidence.

<a id="course-manager-notebook-assignment-path--preparation-and-maintenance-resources"></a>

### Preparation and maintenance resources

- [Teaching notes and course maintenance](#teaching-notes)
- [Core notebook solution guide](instructor/solutions/core_notebook_solution_guide.md)
- [Delivery readiness checklist](#course-delivery-readiness-checklist)
- [Grading files and usage](#grading)
- [Assessment compliance checklist](#assessment-compliance-checklist) · [Score tracker](instructor/assessment_score_tracker.xlsx)
- [Archived materials](_archive/README.md)

---

<a id="course-delivery-readiness-checklist"></a>

## Course delivery readiness

Use this private reference with the [course map](COURSE_MAP.md), [learner playbook](README.md#golden-path), and [manifest](notebook_manifest.yml). The current route contains seven notebooks: preflight, three graded labs, Capstone, deterministic factory, and local CI/CD. The current deck has six slides. Required execution uses local fixtures and no provider APIs; actual API cost is $0.00.

<a id="course-delivery-readiness-checklist--day-1-opening-script"></a>

### Opening script

> Welcome. Before we write code, find the deterministic-mode cell in preflight. The foundation notebooks set `USE_LIVE_LLM = False`. We test roles, handoffs, schemas and gates with supplied local fixtures. The factory then adds actual local files, Git operations, persisted evidence and six explicit approval decisions. We do not need a provider account or API key. Initial package installation needs internet or a prepared package bundle.

The historical bonus notebook redirects to the no-cost simulation. Do not configure paid services for this course.

<a id="course-delivery-readiness-checklist--gono-go-checklist"></a>

### Go/no-go checklist

1. **Setup rehearsal:** create a disposable rehearsal environment; follow [SETUP.md](SETUP.md) with Python 3.12. Record elapsed time and errors on a representative learner machine. A prior fast install is not a guarantee for a new device. Keep the working environment intact.
2. **Automated gate:** install `requirements/maintenance.txt` in the maintainer environment and run `python tools/check_readiness.py`. Inspect summary, environment, input hashes and JUnit reports. Required checks must pass without skips.
3. **All seven notebooks:** inspect preflight, broken/partial/repaired lab states, the Capstone handoff, factory and CI/CD. Confirm handouts retain TODOs, empty outputs and null execution counts.
4. **Partial credit:** verify Lab 1 `0/5/10/15`, Lab 2 `0/5/10/15`, and Lab 3 `0/7/8/15` depending on the repaired control. Do not replace learner notebooks with repaired copies.
5. **Factory rehearsal:** run `python orchestrator.py --check-only`, then `python orchestrator.py --security-demo`. Rehearse the [five-minute demonstration](#demo-script) in a disposable workspace. Inspect the candidate hash/revision before each decision; `--no-input` must deny.
6. **Access and fallback:** prepare a repository ZIP or package bundle, digital ADR sheet, tracker and accessible alternative explanations. Printing is optional; no physical print is claimed.
7. **Release evidence:** record the current command result and limits in the assessment evidence section. Separate local checks from remote CI, browser checks, or a hosted deployment.

<a id="course-delivery-readiness-checklist--two-day-delivery"></a>

### Private delivery planning

Use the [private delivery schedule](#delivery-schedule) for historical session allocations. It includes the integrated factory and local CI/CD. Learner navigation follows competency order and carries no classroom timetable.

<a id="course-delivery-readiness-checklist--instructor-guardrails"></a>

### Instructor guardrails

Use the [three classroom guardrails](#teaching-notes--three-classroom-guardrails): preserve the scaffold, stop at the repaired score, and accept the Paper ADR route when execution is inaccessible.

<a id="course-delivery-readiness-checklist--grade-and-submissions"></a>

### Grade and submissions

Use the [assessment files and marks](#grading--marks). Collect three raw lab scores, separate Capstone code and ADR scores, and a concrete evidence-based strength and next step. The factory/CI evidence supports the Capstone discussion without new marks.

<a id="course-delivery-readiness-checklist--readiness-record"></a>

### Readiness record

Record current repository-test counts and actual setup/deterministic-mode rehearsal results in [assessment_compliance_checklist.md](#assessment-compliance-checklist). Distinguish checks that were run from steps that are only documented.

---

<a id="teaching-notes"></a>

## Instructor Teaching Notes

Instructor preparation and delivery material is kept here. The learner route starts at the [README dashboard](README.md), [course map](COURSE_MAP.md), and [learner playbook](README.md#golden-path).

Use the [notebook and assignment path](#course-manager-notebook-assignment-path), [readiness checklist](#course-delivery-readiness-checklist), [assessment compliance checklist](#assessment-compliance-checklist), and [core solution guide](instructor/solutions/core_notebook_solution_guide.md) together. Preserve the TODOs in distributed learner notebooks.

The learner-facing approach adapts the [Stanford Teaching Commons AI Teaching Guide](#stanford-teaching-guide-alignment). Review the [outcomes, four AI-literacy lenses, and policy draft](#stanford-teaching-guide-alignment) before class; do not describe this local adaptation as Stanford endorsed.

<a id="teaching-notes--facilitate-the-practice-and-feedback-cycle"></a>

### Facilitate the practice-and-feedback cycle

Use the same sequence in the written simulations and notebook labs:

1. **Connect:** open with a short workplace or learner-relevant scenario. Invite several possible perspectives before narrowing to the course's fixed facts.
2. **Predict:** before revealing the simulation outcome or running a fixture, ask learners to write or discuss what might fail and what evidence they would expect.
3. **Practice:** give quiet think time first. Offer pair discussion as an option. The scaffold should include imports, fixture, code context, and grader; keep the learner's target control small and visible.
4. **Respond:** ask learners to read the rejection, trace, audit, or grader message as feedback. Give a hint before supplying an answer, then allow a revision.
5. **Explain:** ask “What did the check establish? What did it leave untested?” Accept a brief spoken explanation, a written sentence, or an annotated diagram for formative reflection.
6. **Transfer:** ask how the same decision changes when the input, authority, or stakeholder changes; collect the Capstone ADR as the summative reasoning artifact.

Frame a broken starter as a planned, low-stakes diagnostic case. Do not turn a visible failure into a public performance or use speed as a proxy for understanding. Give learners choice of working alone or with a partner, and use the Paper ADR route when the environment is a barrier. The graded code outcomes and rubric remain the same when the alternative route applies.

<a id="teaching-notes--discussion-prompts-for-the-application-slides"></a>

#### Discussion prompts for the written application walkthroughs

- **Procurement:** Before showing the recommendation in the walkthrough, ask which quote qualifies under all four rules, what evidence could change that choice, and which decision remains with a person.
- **HR/RAG:** Ask pairs to match each answer claim to a current, authorized snippet. Then ask what the assistant should do when the policy collection does not answer the question.
- **After a notebook grader:** Ask the learner to name one passed check, one boundary of the check, and one next test or review action.

<a id="teaching-notes--facilitate-the-notebook-exercises"></a>

### Facilitate the notebook exercises

Start with each notebook's Run / Edit / Inspect / Finish guide and embedded exercise diagram. Ask learners to identify the local object they are inspecting, the marked control they will edit, and the output that would show the repair worked:

- **Preflight:** inspect package, working-directory, and temporary-file checks. No learner code edits are needed.
- **Lab 1:** follow the supplied dictionary through the weak model, edit the strict contract, and explain the acceptance and rejection results.
- **Lab 2:** repair the two configuration settings, inspect the tool matrix and fixture audit, then compare role responsibilities, acceptance rules, and four routing patterns. Admission to `qa_inbox` does not execute QA.
- **Lab 3:** validate before the mock lookup, bound the failing worker to an initial attempt plus three retries, and explain the escalation record.
- **Capstone and delivery labs:** trace the typed API handoff, scoped review memory, bounded repair, and local candidate through the supplied adversarial checks; connect them to the ADR interaction map.
- **Optional CrewAI bridge:** create a real sequential Crew, call `kickoff`, display final-task Markdown, and compare exception stop, bounded recovery, and escalation. All responses are scripted locally; no LLM or reasoning model runs.

Keep reflection tied to observed notebook behavior. Preserve the existing TODOs, graders, and ADR criteria. A learner can explain a result aloud, in a short note, or by annotating the exercise diagram.

<a id="teaching-notes--day-1-opening-deterministic-mode"></a>

### Opening: deterministic mode

Use the [opening script](#course-delivery-readiness-checklist--day-1-opening-script). All seven required notebooks use deterministic local execution. The factory's simulated model labels and delays are teaching devices; no provider service is called. Installation needs internet or a prepared bundle, while required execution needs no provider keys. The historical bonus is a fixture-only reference.

<a id="teaching-notes--why-a-native-virtual-environment"></a>

### Why a native virtual environment?

> Docker is useful for packaging and deployment. This workshop uses a native Python virtual environment so class time focuses on contracts, role boundaries, verification, and bounded repair. Container deployment belongs to optional study. First-time package installation still needs internet or a prepared package bundle.

<a id="teaching-notes--why-separate-coder-and-qa-roles"></a>

### Why separate Coder and QA roles?

> A separate QA role provides a distinct review step. The Coder proposes a typed patch; QA returns separate evidence. The course fixtures demonstrate the interface and permission pattern. They do not prove that a model is an independent or complete reviewer.

<a id="teaching-notes--slide-17-script-universal-patterns-across-frameworks"></a>

### Written reference script: universal patterns across frameworks

> The decision tree gives us a shortlist based on the dominant need. Clear task ownership points us toward CrewAI. Stateful branching and recovery point us toward LangGraph. Existing AutoGen applications give us conversation patterns to inspect. Document retrieval points us toward LlamaIndex. Python and .NET workflow integration gives us a reason to evaluate Microsoft Agent Framework. These are starting points, and capabilities overlap.
>
> The patterns we teach transfer across all of them. Pass explicit context and typed artifacts between roles. Give each tool only the authority it needs. Verify the result with evidence, bound retries and spending, and define when a human must approve or take over. A framework supplies abstractions. We still design and test those controls. CrewAI remains the only required framework in this workshop.

**Source note, checked 17 October 2026:** AutoGen's [GitHub metadata](https://api.github.com/repos/microsoft/autogen) reports `archived: false`, while its [README](https://github.com/microsoft/autogen#autogen) says Microsoft no longer maintains it and directs new users to [Microsoft Agent Framework](https://github.com/microsoft/agent-framework). Avoid claiming either active Microsoft development or a formal GitHub archive state from one signal alone. The [framework reference](README.md#framework-sources) records the official repositories for the frameworks in the written comparison.

<a id="teaching-notes--three-classroom-guardrails"></a>

### Three classroom guardrails

1. **Provide the scaffold.** Keep imports, mocks, surrounding workflow, and grader intact. Learners repair only the marked control: field constraints, task context, role tools, input validation, or retry limits.
2. **Stop at green.** Once a lab reports `15/15`, move to the next activity. Retain the evidence and ask for the learner's explanation of its limits.
3. **Accept the Paper ADR route.** When execution is blocked by laptop, package, power, or connectivity problems, use the [print-ready ADR sheet](#capstone-paper-adr-quick-sheet) and the stated /20 ADR rubric. Sound reasoning meets the Capstone pass condition; it does not automatically award full marks or create missing implementation evidence.

<a id="teaching-notes--preparation-and-distribution"></a>

### Preparation and distribution

Follow the [go/no-go checklist](#course-delivery-readiness-checklist--gono-go-checklist). Rehearse private repaired copies, preserve TODOs and cleared outputs in learner handouts, and retain the rubric, score tracker, Paper ADR and current test evidence. The factory CLI provides the interactive human-approval route; notebook/test fixture actors do not constitute human authorization.

<a id="teaching-notes--grading-and-feedback"></a>

### Grading and feedback

Follow the [marks and score rules](#grading--marks). Retain raw lab results and converted marks, grade code and ADR separately, then give one concrete strength and one practical next step tied to observed evidence.

<a id="teaching-notes--course-maintenance-and-handover"></a>

### Course maintenance and handover

1. Read the [course map](COURSE_MAP.md), [private delivery schedule](#delivery-schedule), syllabus and README slide index.
2. Confirm seven required notebooks and six slides against the manifest and presentation package.
3. Rehearse broken, partial and repaired copies with the [core solution guide](instructor/solutions/core_notebook_solution_guide.md). Historical success does not verify edited files.
4. Distinguish configuration from execution: Lab 2 constructs roles/tasks and exercises fixtures; Capstone runs local Python adapters and constructs separate Crew objects. The optional [CrewAI bridge](crewai_learning/README.md) executes real CrewAI tasks with local fixture LLMs, with no provider calls.
5. After notebook changes, update stable cell IDs, manifest, solution guide, assessment descriptions and slide navigation together.
6. Keep private solutions and this playbook out of the learner ZIP. Keep optional and archived material outside the required path.

<a id="teaching-notes--optional-track-delivery-notes"></a>

### Optional-track delivery notes

These notes support post-course study; they add no required labs or marks.

<a id="teaching-notes--module10_hr_governancemd"></a>

#### module10_hr_governance.md

Start with the naive path: raw resume output goes to evaluation, and `promote` goes straight to payroll. Then introduce the governance interventions: PII quarantine, bias-safe handoff, and human approval. End by showing the production reality: HR agents can assist, but policy and humans retain authority over sensitive data and irreversible actions.

<a id="teaching-notes--module11_marketing_orchestrationmd"></a>

#### module11_marketing_orchestration.md

Start with the naive path: every task goes to the expensive model, and social posts publish immediately. Then introduce the interventions: cost-aware routing, budget preflight, brand-safety scanning, governed publish tools, and bounded repair. End with the production reality: marketing agents can scale creativity only when routing, spend, and brand policy are first-class system components.

<a id="teaching-notes--module12_advanced_orchestrationmd"></a>

#### module12_advanced_orchestration.md

Teach this after NB6 and NB9. Be explicit:

"The Capstone shows a pre-written rule-based cost-aware router. NB6 and NB9 are optional extensions for learners who want to study more routing and workflow concepts. The required workshop does not train an orchestration model."

---

<a id="demo-script"></a>

## Instructor demo: deterministic Software Factory

This private facilitation script targets a five-minute demonstration. Learner pages use competency order without classroom timings. Run locally before presenting and retain actual evidence. The command makes no API calls, needs no API keys, and incurs $0.00 in API charges.

<a id="demo-script--preparation"></a>

### Preparation

Activate the course environment. Run `python orchestrator.py --check-only` and `python orchestrator.py --security-demo`. Keep a terminal and browser visible. Choose a disposable factory workspace so the candidate and decisions belong to this demonstration.

<a id="demo-script--five-minute-walkthrough"></a>

### Five-minute walkthrough

| Time | Instructor action | Evidence to discuss |
| --- | --- | --- |
| 0:00–0:40 | Show the travel-site request, role labels, and profile. State that outputs are fixtures and delays are presentation pacing. | Actual API cost $0.00. Simulated plan $0.50. |
| 0:40–1:10 | Run `python live_simulation_orchestrator.py --delay-seconds 1.5`. Review and approve plan/spend. | Human decision binds the configured teaching budget. |
| 1:10–2:00 | Inspect the typed plan, approve preparing the Coder fixture, then inspect its generated page source. | Actual local files in an isolated Git worktree. |
| 2:00–3:05 | Explain and approve each bounded Security, UI/UX, and QA action, then inspect its result before continuing. | A failed result blocks the next stage; avoid claiming no vulnerabilities or full WCAG conformance. |
| 3:05–3:40 | Review the final artifact/revision and approve local publication. Run `open index.html`. | Real local page, receipt/digest, no hosted deployment. |
| 3:40–4:25 | Run `python orchestrator.py --security-demo`. Show password storage, insecure HTTP, and exfiltration findings. | Malicious request blocks with no publication. |
| 4:25–5:00 | Connect contracts to Lab 1, role separation to Lab 2, attempt/budget gates to Lab 3, and evidence to the ERD/CI/CD lab. | Learners name the failed gate and next accountable owner. |

If discussion takes longer, shorten pacing with `--delay-seconds 0`; do not bypass gates. `--no-input` must stop at approval. A fixture actor injected by automated tests is test evidence, not a human approval.

---

<a id="grading"></a>

## Assessment files

| File | Use |
| --- | --- |
| [Grading rubric](instructor/grading_rubrics.xlsx) | Current five assessment components, notebook score branches, and a single-submission calculation sheet. |
| [Learner score tracker](instructor/assessment_score_tracker.xlsx) | Cohort record with raw lab scores, converted course marks, total, and grade. |
| [Assessment compliance checklist](#assessment-compliance-checklist) | Release evidence and the scope of the automated checks. |
| [Capstone brief](ASSIGNMENTS.md#ex5-capstone-virtual-software-company) | Code criteria and the three-question ADR rubric. |
| [Paper ADR sheet](#capstone-paper-adr-quick-sheet) and [print-ready PDF](pdf/capstone_paper_adr_quick_sheet.pdf) | Accepted fallback with the same ADR rubric and 6/7/7 partial-credit anchors. |
| [Notebook solution guide](instructor/solutions/core_notebook_solution_guide.md) | Instructor repairs for the intentional broken starts. |

<a id="grading--marks"></a>

### Marks

| Component | Raw result | Course marks |
| --- | ---: | ---: |
| [Lab 1: Pydantic contract](notebooks/01_lab_pydantic.ipynb) | /15 | /20 |
| [Lab 2: CrewAI team handoff](notebooks/02_lab_crewai.ipynb) | /15 | /20 |
| [Lab 3: Tool gates and bounded repair](notebooks/03_lab_security.ipynb) | /15 | /20 |
| [Capstone code](notebooks/04_capstone.ipynb) | /20 | /20 |
| Capstone ADR and defense | /20 | /20 |
| **Total** | | **/100** |

Convert each lab with `raw score × 20 ÷ 15`. Keep the full precision in the tracker; formatting displays two decimals. Lecture exercises are formative and have no additional marks.

The Lab 1 and Lab 2 graders each award two independent controls worth 5 and 10 raw points, so the possible totals are 0, 5, 10, or 15. Lab 1 awards 5 for the inclusive confidence range and 10 for rejecting undeclared fields; both require the valid typed field shape. Lab 2 awards 5 for Manager permissions/delegation and 10 for the `architect_task` context dependency. The detailed rubric mirrors these allocations. Lab 2 does not measure a live Crew run or an executed TeamLog read. Lab 3 awards 4/3/3/3/2 raw points. Capstone code awards 5/10/5 and the ADR awards 6/7/7.

Enter raw results in the yellow tracker cells. Converted marks and totals calculate automatically. A missing component leaves the total and grade blank; an earned zero remains zero. Grade bands use the unrounded total: A at least 80, B at least 65 and below 80, C at least 50 and below 65, and F below 50.

Use the Paper ADR fallback according to the [playbook](README.md#golden-path). Sound reasoning satisfies the fallback pass condition; it does not automatically earn full marks or fabricated code evidence. Enter the paper score in **ADR & defense /20**. If code could not be assessed, leave **Capstone code /20** blank, record the reason, and document any explicitly agreed accommodation separately. The tracker intentionally leaves the total blank until all five component marks are present.

The paper sheet divides the ADR rubric into 6 marks for risk and architecture, 7 for governance and evidence, and 7 for the next step. Each question has point allocations so instructors can award partial credit consistently.

<a id="grading--rubric-maintenance"></a>

### Rubric maintenance

The workbooks remain under `instructor/`.

The [rubric builder](instructor/build_grading_rubrics.mjs) regenerates `grading_rubrics.xlsx` and its previews with `@oai/artifact-tool`. It does not overwrite the cohort score tracker. Run it in a prepared artifact runtime, using `--output-dir` for a temporary review location before replacing the published rubric.

The [paper worksheet builder](tools/build_paper_adr.py) regenerates the one-page A4 PDF using ReportLab. This is an instructor asset build step, separate from learner setup.

---

<a id="capstone-paper-adr-quick-sheet"></a>

## Capstone Paper ADR - Offline Fallback

Use this one-page worksheet when a learner cannot run the Capstone because of a device, package, power, or connectivity failure. No code execution is required. The learner may write by hand or type short answers. [Open the print-ready A4 PDF](pdf/capstone_paper_adr_quick_sheet.pdf).

**Learner:** ______________________________  **Date:** ______________  **Case:** ______________________________

<a id="capstone-paper-adr-quick-sheet--three-questions"></a>

### Three questions

1. **Contract and architecture - 6 marks**  
   What risk does the Development-to-Security boundary address? Name the `DevDeliverable` fields and sketch how the Coordinator validates the handoff before Security starts.

   ____________________________________________________________________________________

   ____________________________________________________________________________________

   ____________________________________________________________________________________

2. **Governance and evidence - 7 marks**  
   Which tools may the Manager, Coder, QA, Pen Tester, and Security Manager roles use? What test or audit evidence would show that the handoff and role boundaries held? Label evidence as observed or proposed.

   ____________________________________________________________________________________

   ____________________________________________________________________________________

   ____________________________________________________________________________________

3. **Production next step - 7 marks**  
   What is the largest remaining risk, what concrete control would you add before production, and how would you check that the control works?

   ____________________________________________________________________________________

   ____________________________________________________________________________________

   ____________________________________________________________________________________

<a id="capstone-paper-adr-quick-sheet--score"></a>

### Score

| Criterion | Marks |
| --- | ---: |
| Risk and architecture | ____ / 6 |
| Governance mapping and proof | ____ / 7 |
| Production next step | ____ / 7 |
| **Total** | **____ / 20** |

A sound, evidence-based ADR satisfies the Capstone fallback pass condition. Score the same 20-point rubric; the paper option is not an automatic full-mark award.

<a id="capstone-paper-adr-quick-sheet--instructor-scoring-anchors"></a>

### Instructor scoring anchors

Award points for the quality of each explanation, including partial credit within each allocation.

| Question | Point allocations |
| --- | --- |
| 1 - Contract and architecture | Concrete handoff risk (2); correct `DevDeliverable` fields and validation rule (2); explains Development, Coordinator, and Security boundaries (2). |
| 2 - Governance and evidence | Development role/tool separation (2); Pen Tester scan access and Security Manager approval separation (2); suitable contract rejection and ordered audit evidence (2); distinguishes observed from proposed evidence (1). |
| 3 - Production next step | Specific remaining risk (2); control that addresses that risk with a credible rationale (3); practical verification or acceptance check (2). |

Expected contract fields are `code_snippet`, `unit_tests_passed`, and `dev_team_signature`. A failed QA result must stop the handoff before Security starts. A diagram or pseudo-code can express the boundary.

Record this sheet's score in **ADR & defense /20**. It awards ADR marks only. The fallback may satisfy the accepted Capstone pass route, but it does not create code execution evidence or code marks. If code could not be assessed, leave its score blank and record the reason or an explicitly agreed accommodation separately. The tracker leaves the course total blank while a required mark is missing.

---

<a id="delivery-schedule"></a>

## Instructor delivery schedule

Private facilitation reference. Learner navigation uses competency order without delivery dates or durations. The schedule below uses the practical notebook sequence and written walkthroughs. Integrate the factory and local CI/CD rehearsals into the delivery allocation rather than presenting them as an end-of-course bonus.



The [course syllabus](README.md#course-topics) groups nine competency topics into the sessions below. Procurement and HR/RAG are formative walkthroughs, not additional graded implementations. The practical sequence contains one preflight, three labs, one software Capstone, and the integrated factory and local CI/CD labs.

<a id="delivery-schedule--day-1--mas-foundations-contracts-and-team-context"></a>

#### Day 1 — MAS foundations, contracts, and team context

| Time | Session | Activity and completion evidence |
| --- | --- | --- |
| 09:00–10:30 | MAS foundations and written simulations | Identify role responsibilities and acceptance rules; classify MAS interaction types; trace [procurement and HR/RAG](ASSIGNMENTS.md#workshop-simulations), identify coordination risks, then run the [preflight](notebooks/00_sandbox_preflight.ipynb). |
| 10:45–12:00 | Lab 1: Context Engineering — Working Brief and Typed Contracts | Prepare a short context packet; connect it to typed constraints; repair the weak Pydantic schema and reach `✅ SUCCESS: 15/15`. |
| 13:00–14:00 | Roles, context, and framework literacy | Compare Manager–Coder–QA responsibilities with independent, decentralized, centralized and hybrid routing; inspect context dependencies; compare CrewAI, LangGraph, AutoGen, and Microsoft Agent Framework using the [framework reference](README.md#framework-comparison). |
| 14:15–16:30 | Lab 2: Multi-Agent Management — Code Auditing and Team Oversight | Repair tools/context, inspect the supplied Manager audit and local QA inbox, record the decision, and reach 15/15. |

<a id="delivery-schedule--day-2--security-bounded-repair-and-team-to-team-delivery"></a>

#### Day 2 — Security, bounded repair, and team-to-team delivery

| Time | Session | Activity and completion evidence |
| --- | --- | --- |
| 09:00–10:30 | Governed tools and debugging | Inspect the Lab 2 tool allowlists, input schemas and audit record; select role-specific evidence using the [academic resources](README.md#readings); diagnose a failure from the supplied workflow trace. |
| 10:45–12:00 | Lab 3: Manager Oversight — Code Validation and Bounded Repair | Repair the gate/retry limit, inspect the Manager oversight evidence, record escalation, and reach `✅ SUCCESS: 15/15`. |
| 13:00–14:30 | Capstone and factory build | Validate `DevDeliverable` before the Coordinator starts the local Security adapter; inspect the audit result. Use [notebook 05](notebooks/05_live_software_factory.ipynb) to connect the travel-site brief to fixture outputs, simulated costs, candidate Git revision, and approval evidence. |
| 14:45–15:45 | Local CI/CD, defense, and Paper ADR option | Use [notebook 06](notebooks/06_local_cicd.ipynb) to demonstrate denied publication and stale-evidence blocks. Present the inter-team contract, observed checks, and ADR, or submit a sound Paper ADR fallback. |
| 15:45–16:00 | Framework ecosystem and observed controls | Review broader framework choices as ungraded literacy; connect a typed contract, tool boundary, bounded retry and approval decision to the evidence observed in the notebooks. |

<a id="delivery-schedule--integrated-factory-facilitation"></a>

### Integrated factory facilitation

Use the [five-minute demonstration script](#demo-script) during the factory block. The paced terminal run uses deterministic outputs, actual local files and Git operations, six explicit human approvals, and simulated costs; actual API cost is $0.00. No API keys or provider setup are required. Inspect the evidence before each decision and identify local publication accurately. The notebook rehearsals use clearly labeled fixture decisions rather than human approval.

---

<a id="notebook-control-crosswalk"></a>

## Notebook and control crosswalk

Use the [course map](COURSE_MAP.md), [assignment briefs](ASSIGNMENTS.md), and each notebook's Run / Edit / Inspect / Finish guide to connect practical work to the control being taught.

| Exercise | Control | Observable learner evidence |
| --- | --- | --- |
| Preflight | Check the local environment before execution. | Package, working-directory and temporary-file checks pass. |
| Lab 1 | Validate typed context at a boundary. | The repaired contract accepts valid data and rejects malformed data; the grader reaches 15/15. |
| Lab 2 | Limit tools, supply dependencies, and audit a handoff. | The repaired tools/context settings, skill matrix, typed patch and Manager decision support admission to the local QA inbox; the grader reaches 15/15. |
| Lab 3 | Validate input and bound repair attempts. | The local lookup rejects invalid input; the failing worker stops after the initial attempt plus three retries and records escalation; the grader reaches 15/15. |
| Capstone | Govern a Development-to-Security handoff. | The typed API boundary, scoped review memory, repair loop and adversarial checks support the interaction map and ADR. |
| Factory and local CI/CD | Bind decisions to revision-specific evidence before local publication. | Candidate revision, gate decisions, stale-evidence and denied-publication checks, and local publication receipt. |
| Optional CrewAI bridge | Compare configured roles with actual framework execution. | A real sequential Crew runs with scripted local responses; final-task Markdown and exception handling remain inspectable. |

The required sequence and assessment remain preflight, three labs, Development-to-Security Capstone, factory and local CI/CD. Course marks remain three labs × 20, Capstone implementation /20, and ADR/defense /20. Notebook reflections and the optional bridge add no marks. The supplied notebooks use local deterministic fixtures and do not call a model provider.

[Teaching notes](#teaching-notes) · [Assessment checklist](#assessment-compliance-checklist) · [Learner paths](README.md#learner-paths)

---

<a id="stanford-teaching-guide-alignment"></a>

## Teaching-design alignment: Stanford Teaching Commons

**Purpose:** document how this workshop adapts the Stanford Teaching Commons' AI teaching and course-design guidance to a short, technical course on multi-agent systems. This is an independent local adaptation, not a Stanford-reviewed or Stanford-endorsed curriculum. Source pages checked 17 October 2026.

<a id="stanford-teaching-guide-alignment--design-commitments"></a>

### Design commitments

The guide recommends intentional, course-specific choices about AI, attention to student success and workload, meaningful assignments with clear learning objectives, and human-centered AI literacy. This workshop uses those ideas to shape when learners see an answer, what they must decide, and what counts as evidence.

| Stanford AI-literacy lens | Workshop connection | Learner evidence |
| --- | --- | --- |
| **Functional** — how AI works and where it is limited | Define a multiagent system; distinguish a model response from orchestration, validation, and tool execution. | Trace roles and handoffs; explain what the deterministic fixture does and does not simulate. |
| **Ethical** — reliability, privacy, access, bias, and responsibility | Examine unsupported claims, source access, least privilege, simulated cost, and human approval. | Reject an unsafe or unsupported path; name a remaining risk and responsible decision-maker. |
| **Rhetorical** — use and critique human- and AI-generated language | Turn a natural-language request into testable requirements; evaluate whether a claim is supported by the requested evidence. | Revise a specification and justify which evidence supports or fails to support an output. |
| **Pedagogical** — use AI in ways that support learning | Keep required work deterministic and scaffolded; use prediction, practice, feedback, revision, and reflection before transfer. | Explain which control they changed, what feedback showed, and what they can transfer to a new case. |

The literacy domains overlap. They supplement the workshop's four engineering controls; they do not replace the technical pillar map.

<a id="stanford-teaching-guide-alignment--learning-cycle-used-in-the-workshop"></a>

### Learning cycle used in the workshop

Use the [practice-and-feedback cycle](#teaching-notes--facilitate-the-practice-and-feedback-cycle): connect, predict, practice, respond, explain and transfer. Treat starter failures as low-stakes diagnosis, allow reflection and revision, and offer solo/paired reasoning, hints and the Paper ADR route. Do not grade speed or publicly rank errors.

<a id="stanford-teaching-guide-alignment--observable-course-outcomes"></a>

### Observable course outcomes

| Given… | Learners will be able to… | Evidence |
| --- | --- | --- |
| A short synthetic workflow | Identify its agents, environment, interactions, and one coordination risk. | Opening discussion or annotated role map. |
| A weak schema and valid/invalid fixtures | Repair a Pydantic contract that accepts the valid record and rejects both supplied defects. | Lab 1 grader and a brief explanation of one untested property. |
| A starter team configuration and audit trace | Repair Manager permissions and Coder context, then decide whether a typed proposal may enter the local QA inbox. | Lab 2 grader, `PASS_TO_QA`/`BLOCK` evidence, and a management note. |
| An unsafe tool request and an always-failing mock | Configure the input boundary and a three-retry ceiling; explain the four-call maximum and escalation result. | Lab 3 grader and observed call/cost/escalation record. |
| A Development-to-Security handoff | Gate the artifact, separate scan from approval, and defend one unresolved risk with a next-step recommendation. | Capstone evidence and the 20-point ADR. |

The outcomes use observable actions and named conditions. The rubric distinguishes structural validity from truth, configured context from proven model behavior, and local tool lists from operating-system isolation.

<a id="stanford-teaching-guide-alignment--practice-feedback-and-assessment"></a>

### Practice, feedback, and assessment

| Stage | Role in learning | Marks |
| --- | --- | ---: |
| Procurement and HR/RAG simulations | Low-stakes, open-ended discussion; learners inspect evidence and propose a decision before the facilitator reveals the worked example. | Formative only |
| Labs 1–3 | Scaffolded repair, deterministic re-run, grader feedback, and a short decision/evidence note. | 15 raw points per lab, scaled to 20 each |
| Capstone | Integrate the controls at a team boundary; inspect adversarial fixtures and explain residual risk. | Code /20 and ADR /20 |
| Paper ADR option | Preserve the reasoning outcome when a learner cannot run the environment; assess using the same stated ADR rubric. | ADR /20, with no implied code evidence |

Keep the criteria visible before learners begin. Give at least one chance to interpret feedback and revise before moving on. Accept a short written explanation, spoken explanation, or annotated workflow sketch for formative reflection, while retaining the same required code and rubric evidence for graded implementation.

<a id="stanford-teaching-guide-alignment--suggested-learner-facing-ai-use-policy"></a>

### Suggested learner-facing AI-use policy

Adapt and publish a course policy that matches local institutional rules before delivery. A starting draft is:

> The required notebooks use local deterministic fixtures and do not need a model-provider account. You may use an AI assistant as a tutor to clarify concepts or interpret an error if your instructor permits it. Do not ask it to complete a graded TODO for you or submit generated code you cannot explain. Disclose substantial assistance, verify every suggestion against the notebook evidence, and never submit personal, confidential, or restricted data to an external service. Ask the instructor when a use is unclear.

The policy is meant to protect learner agency and make expectations predictable, not to imply that the local Stanford or another institution's policies apply here. Provide documentation, local examples, instructor help, and the Paper ADR path so access to a paid tool is never required.

<a id="stanford-teaching-guide-alignment--where-the-design-is-implemented"></a>

### Where the design is implemented

- [README](README.md): learner-facing AI-literacy frame, outcomes, and direct paths.
- [Workshop syllabus](README.md#course-topics): observable outcomes, session sequence, and assessment alignment.
- [Teaching notes](#teaching-notes): openers, facilitation moves, feedback, and distribution guidance.
- [Simulation walkthroughs](ASSIGNMENTS.md#workshop-simulations): predict/compare/discuss before revealing a deterministic decision.
- [Notebook manifest](notebook_manifest.yml) and [Course Map](COURSE_MAP.md): skill order, learner actions, and evidence.
- [six-slide main deck](slides/managing_multi_agent_teams_6_slides.pptx): open questions, visible learner actions, governance concepts, and end-of-course takeaways.
- [Notebook 1](notebooks/01_lab_pydantic.ipynb), [Notebook 2](notebooks/02_lab_crewai.ipynb), [Notebook 3](notebooks/03_lab_security.ipynb), and [Capstone](notebooks/04_capstone.ipynb): prediction, scaffolded repair, feedback, and reflection in Markdown instructions; code cells and graders remain the course fixtures.

<a id="stanford-teaching-guide-alignment--references"></a>

### References

- [Artificial Intelligence Teaching Guide](https://teachingcommons.stanford.edu/teaching-guides/artificial-intelligence-teaching-guide), Stanford Teaching Commons.
- [Understanding AI Literacy](https://teachingcommons.stanford.edu/teaching-guides/artificial-intelligence-teaching-guide/understanding-ai-literacy), Stanford Teaching Commons.
- [Exploring the Pedagogical Uses of AI Chatbots](https://teachingcommons.stanford.edu/teaching-guides/artificial-intelligence-teaching-guide/exploring-pedagogical-uses-ai-chatbots), Stanford Teaching Commons.
- [Analyzing the Implications of AI for Your Course](https://teachingcommons.stanford.edu/teaching-guides/artificial-intelligence-teaching-guide/analyzing-implications-ai-your-course), Stanford Teaching Commons.
- [Integrating AI into Assignments](https://teachingcommons.stanford.edu/teaching-guides/artificial-intelligence-teaching-guide/integrating-ai-assignments), Stanford Teaching Commons.
- [Creating Learning Outcomes](https://teachingcommons.stanford.edu/teaching-guides/foundations-course-design/course-planning/creating-learning-outcomes), Stanford Teaching Commons.
- [Formative Assessment and Feedback](https://teachingcommons.stanford.edu/teaching-guides/foundations-course-design/feedback-and-assessment/formative-assessment-and-feedback) and [Increasing Student Engagement](https://teachingcommons.stanford.edu/teaching-guides/foundations-course-design/learning-activities/increasing-student-engagement), Stanford Teaching Commons.

---

<a id="management-principle-matrix"></a>

## Management Principle Matrix

Use this matrix to keep the course anchored on managing multi-agent teams, not merely implementing agent code.

| Scenario | Management Principle | Business Impact If Missing | Code Evidence | Assessment Question |
| --- | --- | --- | --- | --- |
| MCP Zero-Trust Tool Boundary | Resource allocation and least-privilege access | Unauthorized tools can trigger refunds, offers, exports, or restricted data leaks | `ToolGateway.call()` denies the rogue vendor and appends `AuditEvent(allowed=False)` | Can the learner design a tool policy where QA can read test results but cannot issue refunds or offers? |
| Agentic RAG and Theory of Mind | Context delegation with need-to-know memory | Agents forget constraints or retrieve sensitive secrets they should not see | Coder retrieves PostgreSQL constraint but receives 0 password records | Can the learner explain how an agent discovers teammate knowledge without seeing all memory? |
| TeamLog Collective Commitment | Mission alignment and global constraint enforcement | Agents pass local tasks while violating enterprise rules such as offline-only execution | `check_teamlog_commitments()` blocks `CALL_EXTERNAL_API` under a no-network commitment | Can the learner decide where global rules belong and prove they override local agent goals? |
| ChatDev Bounded Self-Repair | Quality control with bounded autonomy | Broken code ships, or agents loop forever and burn budget | `run_company()` returns `PullRequestSummary(status="SHIPPED" or "ESCALATED_TO_HUMAN")` | Can the learner define when to retry, when to switch strategy, and when to escalate? |
| Cost-Aware Dynamic Routing | Allocate work by task complexity and cost | Every task goes to the expensive worker, wasting budget on routine work | The Capstone's pre-written `cost_aware_router()` logs the selected Fast or Expert tier and compares illustrative costs | Can the learner explain why routine work uses Fast and high-complexity work uses Expert? |
| API Boundary and Async Orchestration | External intake governance and non-blocking work management | Messy webhooks hit internal agents directly, or slow workflows block HTTP clients | NB8 maps API keys to identity, returns `202 Accepted`, and exposes `GET /tasks/{task_id}` polling | Can the learner explain why the API gateway is the governance perimeter? |
| Advanced cross-organization A2A (archived) | Network trust negotiation and message quarantine | Internal agents can leak PII or accept untrusted external messages | Optional archived notebook validates identity, classification, schemas, and denials | This is advanced reference material, not part of the two-day learner path. |
| Governed Logistics Weather Agent | Tool access through a least-privilege gateway | API keys leak into prompts or unauthorized widgets call privileged tools such as shipment cancellation | NB1 builder exercise validates `WeatherRequest`, returns `WeatherResponse`, and blocks `external_widget` | Can the learner explain why even a simple weather-risk call belongs behind a gateway? |
| Bounded Writer Agent | Structured feedback and retry budgets | Writer/editor loops become blind retries with no evidence or stop condition | NB5 builder exercise feeds `EditorFeedback` into repair and returns `EscalationTicket` on exhaustion | Can the learner distinguish repair from retry? |
| Capstone Security & Compliance Team | Independent security review across a typed team boundary | Development output can pass QA while retaining security risks | Validated `DevDeliverable` starts the Security Team, which returns `SecurityAuditResult` | Can the learner show the validated object, findings, and release decision? |
| CEO-Directed Project Planning | Human steering through TeamLog, not raw prompts | Human changes bypass commitments and downstream agents act on stale instructions | Optional NB10 updates `ProjectPlan` and `TeamCommitment` before the Coder acts | Can the learner show where natural language becomes governed state? |
| CrewAI Framework Bridge | Framework orchestration with explicit governance ownership | Teams adopt a framework and accidentally drop schema, policy, audit, and approval controls | `crewai_learning/README.md` teaches role clarity, context chains, process selection, guardrails, failure recovery, and clean delivery | Can the learner decide when to use custom orchestration, CrewAI, or a hybrid governed framework? |
| Homework A: Specialist Agent Skills | Specialist capability development | The team is well-governed but every specialist is mediocre | Specialist agents emit typed quality, test, security, and documentation artifacts | Can the learner prove each agent is good at its role, not merely present in the workflow? |
| Homework B: Production Controls | Human oversight, evaluation, cost control, and memory lifecycle | Agents act without approval, cannot be measured, overspend, or accumulate stale memory | Approval, benchmark, cache, and forgetting homework | Can the learner measure and control a deployed agent's behavior over time? |
| Homework C: Deployment and Operations | Operational accountability | The system works in notebooks but cannot be deployed, observed, sandboxed, or rolled back | Container, observability, sandbox, and version-control homework | Can the learner operate the system safely after it leaves the classroom? |

<a id="management-principle-matrix--notebook-exercise-narrative-standard"></a>

### Notebook Exercise Narrative Standard

The current notebook phase uses a consistent Andrew Ng-style teaching pattern:

| Element | Instructor Purpose | Learner Check |
| --- | --- | --- |
| The Story | Ground the technical pattern in a believable production failure | Can the learner explain what can go wrong in the real world? |
| Your Mission | Turn the failure into a focused implementation task | Can the learner change the system and produce evidence? |
| The Takeaway | Connect the implementation back to managing an AI workforce | Can the learner name the management principle, not just the code mechanic? |

Apply this standard to the three required labs and the two-team Capstone. The archived NB11 perimeter exercise is optional advanced material.

<a id="management-principle-matrix--instructor-rule"></a>

### Instructor Rule

For every lab, ask learners to answer in one sentence:

> What management failure does this technical pattern prevent?

If they cannot answer that, they have learned the code but not the course.

---

<a id="technical-implementation-playbook"></a>

## Technical scenarios and instructor Q&A

Use these instructor scenarios to explain how additional application boundaries extend the local teaching controls. The required course is the seven-notebook route in the [manifest](notebook_manifest.yml), supported by a six-slide deck. Archived MCP/A2A and optional FastAPI scenarios are advanced design references. They do not add required implementations, provider setup or course marks. The current tool-boundary lesson is [Lab 3](notebooks/03_lab_security.ipynb).

<a id="technical-implementation-playbook--delivery-pattern"></a>

### Delivery Pattern

For each scenario, show the naive failure, introduce the management control, then inspect the governed result and its limits. Ask four questions: which management principle is at stake, what business failure it prevents, what observable evidence tests it, and which familiar analogy explains it before code.

<a id="technical-implementation-playbook--instructor-qa-read-and-write-roles"></a>

### Instructor Q&A: Read and Write Roles

**Why not use one agent to write and check its own work?**

> Self-review can catch issues, but it is not an independent control: the same missed assumption can carry into the review. In this course, the Coder proposes a typed patch, a separately scoped QA role checks it and returns a structured report, and the Capstone Security Team audits the validated deliverable. LangChain's engineering guidance says read-heavy multi-agent systems tend to be easier to manage than systems that parallelize writes, because conflicting writes are harder to reconcile ([LangChain, “How and when to build multi-agent systems”](https://www.langchain.com/blog/how-and-when-to-build-multi-agent-systems)). Use this as a design observation, not a universal rule.

**Why is the Coder restricted instead of being given more tools to fix its own mistakes?**

> Each tool adds possible actions and side effects. Give a role only the permissions it needs, validate handoffs, bound retries, and escalate when the workflow reaches its limit. IBM's agent-security guidance discusses least privilege, validation, sandboxing, and human oversight for higher-risk actions ([IBM, “Agentic AI Security Guide”](https://www.ibm.com/think/insights/agentic-ai-security)).

**Are we learning to build autonomous coding agents like Devin?**

> No. We are learning to govern agent workflows through typed contracts, scoped tool access, independent checks, bounded repair, and escalation. Cognition describes Devin as using a shell, code editor, and browser in a sandboxed compute environment ([Cognition, “Introducing Devin”](https://cognition.com/blog/introducing-devin)); this course does not claim to reproduce that product or its infrastructure.

<a id="technical-implementation-playbook--1-mcp-zero-trust-tool-boundary"></a>

### 1. MCP: Zero-Trust Tool Boundary



<a id="technical-implementation-playbook--management-principle"></a>

#### Management Principle

Resource allocation and access control. A manager must decide who gets which tools, under what conditions, and with which data. Not every team member needs every tool.

<a id="technical-implementation-playbook--business-impact"></a>

#### Business Impact

Without this control, an external vendor agent could export restricted HR data or a resume parser could issue an offer. The failure mode is not a bad answer; it is a compliance breach, financial loss, or unauthorized business action.

<a id="technical-implementation-playbook--historical-advanced-files"></a>

#### Historical advanced files

- Supplementary prompt: [MCP tool governance](_archive/assignments/ex2_3_mcp_tool_governance.md)
- Archived starter: [governance policy](_archive/advanced_scaling/assignments/starter_code/ex4_governance_matrix_starter.py)
- Archived solution: [governance policy solution](_archive/advanced_scaling/assignments/starter_code/ex4_governance_matrix_solution.py)
- Archived notebook: [MCP tool gateway](_archive/03_mcp_tool_gateway.ipynb)
- Solution guide: [historical MCP reference](_archive/instructor/solutions/ex2_3_mcp_tool_governance_solution_guide.md)

<a id="technical-implementation-playbook--technical-implementation"></a>

#### Technical Implementation

Instructor scenario: The Rogue Agent Test.

```python
vendor = AgentIdentity(
    agent_id="vendor-001",
    organization="external_vendor",
    role="vendor_reporter",
    trust_tier=TrustTier.PUBLIC,
    allowed_tools={Tool.EXPORT_REPORT},
    public_key_ref="did:example:vendor-001",
)

gateway = ToolGateway()
request = ToolRequest(
    caller=vendor,
    tool=Tool.EXPORT_REPORT,
    args={"name": "restricted_hiring_audit"},
    data_sensitivity=TrustTier.RESTRICTED,
)

result = gateway.call(request)
assert result.success is False
assert gateway.audit_log[-1].allowed is False
```

<a id="technical-implementation-playbook--assessment-question"></a>

#### Assessment Question

Your QA agent needs to read test results but should never issue refunds or release offers. Design the tool policy. What happens if you accidentally give QA the high-impact tool but only confidential clearance?

Strong answer: the learner separates tool scope, role permission, trust tier, data sensitivity, and audit logging. They explain why any one check alone is insufficient.

<a id="technical-implementation-playbook--teaching-script"></a>

#### Teaching Script

In a human team, you do not give every contractor the keys to payroll, legal records, and production systems. In an AI team, you do not give the `resume_parser` the ability to issue offers. MCP gives tools a standard doorway; zero-trust policy decides who is allowed through that doorway.

<a id="technical-implementation-playbook--2-agentic-rag-and-theory-of-mind-governed-shared-memory"></a>

### 2. Agentic RAG and Theory of Mind: Governed Shared Memory



<a id="technical-implementation-playbook--management-principle-1"></a>

#### Management Principle

Context delegation and need-to-know memory. A manager ensures the right person can recover the right context at the right time, while preventing unnecessary exposure of sensitive information.

<a id="technical-implementation-playbook--business-impact-1"></a>

#### Business Impact

Without governed memory, agents either forget important constraints or over-share sensitive context. The coder may miss the PM's PostgreSQL requirement, while another agent may accidentally retrieve a production password.

<a id="technical-implementation-playbook--current-files"></a>

#### Current Files

- Learner prompt: `_archive/assignments/ex2_tom_memory.md`
- Starter/solution: `_archive/assignments/starter_code/ex2_memory_system_starter.py`
- Notebook: `_archive/02_shared_rag_memory.ipynb`

<a id="technical-implementation-playbook--technical-implementation-1"></a>

#### Technical Implementation

Instructor scenario: The Invisible Handoff.

```python
memory.add(MemoryRecord(
    author=Role.PM,
    visible_to={Role.CODER},
    sensitivity=Sensitivity.CONFIDENTIAL,
    tags={"architecture", "storage"},
    text="Use PostgreSQL for persistent storage.",
))

memory.add(MemoryRecord(
    author=Role.SECURITY,
    visible_to={Role.SECURITY},
    sensitivity=Sensitivity.RESTRICTED,
    tags={"password"},
    text="Production DB password: super_secret_123",
))

assert len(memory.search("password", Role.CODER)) == 0
assert len(memory.search("password", Role.SECURITY)) == 1
```

<a id="technical-implementation-playbook--assessment-question-1"></a>

#### Assessment Question

The PM knows the system must use PostgreSQL, but the coder receives only "build persistence." How should the coder discover the constraint without being handed every memory record? What should happen when the coder searches for "password"?

Strong answer: the learner designs visibility, sensitivity, tags, retrieval, and denial behavior. They explain that Theory of Mind is not unlimited mind-reading; it is authorized inference about what teammates know.

<a id="technical-implementation-playbook--teaching-script-1"></a>

#### Teaching Script

In a well-run human team, a project manager does not repeat every constraint in every meeting. The team has a shared source of truth. But that source of truth still has permissions. Agentic RAG is the shared source of truth; Theory of Mind is the agent knowing which teammate's knowledge should influence its next move.

<a id="technical-implementation-playbook--3-teamlog-collective-commitment-engine"></a>

### 3. TeamLog: Collective Commitment Engine



<a id="technical-implementation-playbook--management-principle-2"></a>

#### Management Principle

Mission alignment and global constraints. A manager must make team-level commitments stronger than local task incentives. Local success is not success if it violates the mission.

<a id="technical-implementation-playbook--business-impact-2"></a>

#### Business Impact

Without TeamLog commitments, a coder can satisfy a local ticket while breaking enterprise rules. For example, code may pass tests but call an external API even though the product must run offline for compliance or customer deployment reasons.

<a id="technical-implementation-playbook--current-files-1"></a>

#### Current Files

- Core implementation: `src/enterprise_agent_team.py`
- Design exercise: [governed agent roster](ASSIGNMENTS.md#foundational-architecture-design)
- Capstone: `assignments/starter_code/ex5_capstone_starter.py`

<a id="technical-implementation-playbook--technical-implementation-2"></a>

#### Technical Implementation

Instructor scenario: Scope Creep Prevention.

```python
commitment = TeamCommitment(
    owner=AgentRole.PRODUCT_MANAGER,
    commitment="All code must run offline. No external network calls.",
    visible_to={AgentRole.CODER, AgentRole.QA},
    sensitivity=TrustTier.CONFIDENTIAL,
)

coder = AgentIdentity(
    agent_id="coder-001",
    role=AgentRole.CODER,
    org_id="training",
    scopes={ToolName.CALL_EXTERNAL_API},
    clearance=TrustTier.CONFIDENTIAL,
)

request = ToolRequest(
    caller=coder,
    tool=ToolName.CALL_EXTERNAL_API,
    args={"url": "https://api.example.com"},
    data_sensitivity=TrustTier.CONFIDENTIAL,
)

check_teamlog_commitments(request, [commitment])
```

Expected result: `check_teamlog_commitments` raises `PermissionError` with the commitment text.

<a id="technical-implementation-playbook--assessment-question-2"></a>

#### Assessment Question

A coder produces a clever implementation that passes all tests but violates "No external network calls." Should QA approve it? Where should this rule live: in the prompt, in the tool policy, in memory, or as a TeamLog commitment?

Strong answer: the learner explains that global commitments must be explicit, visible to relevant roles, and enforced before tool execution or release.

<a id="technical-implementation-playbook--teaching-script-2"></a>

#### Teaching Script

In a human company, a brilliant engineer is still not allowed to ignore legal, security, or customer commitments. TeamLog is how we encode those team promises. It keeps the agent from saying, "My local task passed," when the actual team mission failed.

<a id="technical-implementation-playbook--4-chatdev-self-repair-bounded-quality-loop"></a>

### 4. ChatDev Self-Repair: Bounded Quality Loop



<a id="technical-implementation-playbook--management-principle-3"></a>

#### Management Principle

Quality control with bounded autonomy. A manager should allow workers to correct mistakes, but must define when repeated failure becomes an escalation.

<a id="technical-implementation-playbook--business-impact-3"></a>

#### Business Impact

Without a repair loop, broken first drafts ship. Without a retry budget, agents can loop forever, burn API credits, block releases, and hide the fact that human judgment is needed.

<a id="technical-implementation-playbook--current-files-2"></a>

#### Current Files

- Notebook: `_archive/05_self_repair_loop.ipynb`
- Capstone starter: `assignments/starter_code/ex5_capstone_starter.py`
- Capstone solution guide: `instructor/solutions/ex5_capstone_solution_guide.md`

<a id="technical-implementation-playbook--technical-implementation-3"></a>

#### Technical Implementation

Instructor scenario: The Infinite Loop Trap.

```python
summary = run_company("Create a slugify(text) utility with tests.", max_repairs=0)
assert summary.status in {"SHIPPED", "ESCALATED_TO_HUMAN"}
```

For a forced-failure variant, make `code()` keep returning an invalid implementation or make `run_tests()` always fail. With `max_repairs=2`, the system must stop after exactly 3 total attempts and return `status="ESCALATED_TO_HUMAN"`.

<a id="technical-implementation-playbook--assessment-question-3"></a>

#### Assessment Question

Your coding agent fails the same test three times. Should the system keep retrying, switch models, ask a human, or ship with a warning? What evidence should be preserved for the next reviewer?

Strong answer: the learner defines a retry budget, stores failure evidence, prevents silent shipping, and returns a typed escalation artifact.

<a id="technical-implementation-playbook--teaching-script-3"></a>

#### Teaching Script

A good engineering manager does not fire someone after the first failed test, but also does not let them work forever with no progress. ChatDev-style repair gives agents a chance to improve. The retry budget turns autonomy into managed autonomy.

<a id="technical-implementation-playbook--5-api-boundary-governance-perimeter-and-async-orchestration"></a>

### 5. API Boundary: Governance Perimeter and Async Orchestration



<a id="technical-implementation-playbook--management-principle-4"></a>

#### Management Principle

External intake governance. A manager must control how outside requests enter the team, who is allowed to request work, and how long-running work is tracked without blocking the requester.

<a id="technical-implementation-playbook--business-impact-4"></a>

#### Business Impact

Without an API boundary, messy webhooks, Slack commands, and A2A requests can hit internal agents directly. The result is schema drift, unauthorized high-risk work, blocked HTTP clients, and no reliable task status for external systems.

<a id="technical-implementation-playbook--current-files-3"></a>

#### Current Files

- Notebook: `extensions/08_api_boundaries_async_orchestration.ipynb`
- Historical API/A2A prompt: [archived OpenAPI contract](_archive/advanced_scaling/assignments/a2a_openapi_contract.md)
- Historical FastAPI implementation: [archived Capstone solution](_archive/advanced_scaling/assignments/starter_code/ex5_capstone_solution.py)

This API example is separate from the current [offline Capstone](notebooks/04_capstone.ipynb), which uses local Python adapters and requires no server or deployment.

<a id="technical-implementation-playbook--technical-implementation-4"></a>

#### Technical Implementation

Instructor scenario: The Customs Border.

```python
response = client.post(
    "/tasks",
    json={
        "github_issue_url": "https://github.com/org/repo/issues/42",
        "priority": "high",
        "requester_email": "pm@company.com",
    },
    headers={"Authorization": "Bearer sk-internal-admin"},
)
assert response.status_code == 202

blocked = client.post(
    "/tasks",
    json={
        "github_issue_url": "https://github.com/external/repo/issues/7",
        "priority": "high",
        "requester_email": "vendor@external.com",
    },
    headers={"Authorization": "Bearer sk-external-vendor"},
)
assert blocked.status_code == 403
```

<a id="technical-implementation-playbook--assessment-question-4"></a>

#### Assessment Question

A GitHub webhook, Slack command, and external vendor A2A call all request work from your agent team. Which fields are accepted at the API boundary, how is identity determined, and why should the endpoint return `202 Accepted` instead of waiting for the whole agent workflow to finish?

Strong answer: the learner maps API keys to identities, rejects unauthorized risk escalation, validates raw payloads into strict internal contracts, starts background work, and exposes polling through `GET /tasks/{task_id}`.

<a id="technical-implementation-playbook--teaching-script-4"></a>

#### Teaching Script

In a human company, the front desk does not let every visitor walk directly into engineering, legal, or finance. The API gateway is that front desk. It authenticates the visitor, checks what they are allowed to request, writes down the work order, and gives them a tracking number while the team does the work.

<a id="technical-implementation-playbook--6-basic-agent-governance-labs-logistics-weather-writer-qa-and-ceo"></a>

### 6. Basic Agent Governance Labs: Logistics Weather, Writer, QA, and CEO



<a id="technical-implementation-playbook--management-principle-5"></a>

#### Management Principle

Familiar agent examples should still teach managed autonomy. A logistics weather-risk agent, Writer Agent, QA Agent, or CEO interface becomes course-aligned only when it includes identity, typed contracts, governed tools, memory, bounded repair, A2A defense, or human approval.

<a id="technical-implementation-playbook--business-impact-5"></a>

#### Business Impact

Without this framing, learners confuse "agent can call an API" with "agent can be trusted in production." The business failures are familiar: leaked API keys, unbounded writing retries, prompt-injection acceptance, and raw human instructions bypassing TeamLog commitments.

<a id="technical-implementation-playbook--current-files-4"></a>

#### Current Files

- Handout: [supplemental governance practice](ASSIGNMENTS.md#basic-agent-governance-labs)
- NB1 exercise: `_archive/01_hello_multi_agent.ipynb`
- NB5 exercise: `_archive/05_self_repair_loop.ipynb`
- NB10 exercise: `extensions/10_vibe_coding_interface.ipynb`
- Optional archived network-boundary exercise: `_archive/advanced_scaling/notebooks/11_enterprise_a2a_perimeter.ipynb`
- Solution guide: `instructor/solutions/basic_agent_governance_labs_solution_guide.md`

<a id="technical-implementation-playbook--technical-implementation-5"></a>

#### Technical Implementation

Instructor scenario: The Builder Ladder.

| Lab | Naive Demo | Governance Upgrade | Evidence |
| --- | --- | --- | --- |
| Logistics Weather | Agent calls a weather API directly | Gateway hides API key, checks identity, validates `WeatherRequest` and `WeatherResponse` | Authorized call succeeds; external widget raises `PermissionError`; hallucinated fields fail validation |
| Writer | Writer retries until editor accepts | Editor emits typed feedback; loop stops with `EscalationTicket` | First draft fails; second uses feedback; forced failure escalates |
| QA | QA sends free-form test text | A2A gateway blocks prompt injection and exfiltration payloads | `SecurityIncidentTicket` plus Dead Letter Queue entry |
| CEO | Human prompt directly reaches coder | Manager converts language into `ProjectPlan` and `TeamCommitment` | Mid-flight MongoDB change is read from TeamLog |

<a id="technical-implementation-playbook--assessment-question-5"></a>

#### Assessment Question

Pick one familiar agent example and identify the management boundary. What data contract crosses the boundary? Who is authorized to call it? What happens when the request is invalid, unauthorized, or repeatedly failing?

Strong answer: the learner names the schema, the policy gate, the audit evidence, and the escalation path. They do not describe the lab as "just a tool call" or "just prompting."

<a id="technical-implementation-playbook--teaching-script-5"></a>

#### Teaching Script

Logistics weather, writing, QA, and CEO examples are intentionally simple. That is the point. We remove domain complexity so learners can see the management skeleton: identity, contracts, boundary, evidence, and stop condition. Once they can govern a weather-risk call, they are ready to govern a capstone tool call.

<a id="technical-implementation-playbook--advanced-expansion-roadmap"></a>

### Advanced Expansion Roadmap

The core course teaches managed agents. The advanced track teaches skilled and operated agents.

| Module | Purpose | Assignment File |
| --- | --- | --- |
| 7. Individual Agent Skill Development | Make each specialist good at its job. | `_archive/assignments/module7_individual_agent_skills.md` |
| 8. Production-Ready Agent Features | Add HITL, benchmarks, cost control, and long-term memory. | `_archive/assignments/module8_production_ready_agent_features.md` |
| 9. Agent Deployment & Operations | Deploy, observe, sandbox, and version agents. | `_archive/assignments/module9_deployment_operations.md` |

---

<a id="verification-pyramid"></a>

## Verification Pyramid for Managing Multi-Agent Teams

Use the [development workflow](DEVELOPMENT.md) to create a failing regression test before changing a behavior. Install `requirements/maintenance.txt` in Python 3.12. The required workshop remains three labs and one Capstone.

<a id="verification-pyramid--1-unit-tests-individual-rules"></a>

### 1. Unit tests: individual rules

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

<a id="verification-pyramid--2-integration-tests-handoffs-and-workflow"></a>

### 2. Integration tests: handoffs and workflow

```sh
python -m pytest tests -m integration -q
```

| Workflow | Tests |
| --- | --- |
| Typed task/patch/QA handoffs | `tests/test_handoffs.py` |
| Gateway authorization and TeamLog restrictions | `tests/test_intra_team_handoffs.py` |
| Complete local team flow and bounded repair | `tests/test_system.py`, `tests/test_ex5_capstone.py` |
| Hallucinated fields, overbroad authority, and a permanently failing Coder | `tests/test_adversarial_scenarios.py` |
| Historical bonus remains fixture-only when the old toggle is changed | `tests/test_capstone_bridge.py` |

The system tests are also marked `integration`, so the readiness gate includes them. The historical bridge-test filename remains, but its assertions now prove the bonus cannot enable provider calls.

<a id="verification-pyramid--3-curriculum-integration-real-jupyter-kernels"></a>

### 3. Curriculum integration: real Jupyter kernels

```sh
python -m pytest tests/test_notebooks.py tests/test_offline_runtime.py -m integration -v
```

`tests/test_notebooks.py` reads the root manifest and handouts. It exercises preflight, starter/partial/fixed states for the three labs (including both Lab 2 partial repairs), starter/fixed Capstone states, and the integrated factory/CI/CD rehearsals. A separate check inspects output cleanliness across core, extension, bonus, and archived notebooks.

The tests apply instructor-guide repairs only to in-memory copies. They verify raw grader scores, Manager decisions, removal of stale QA work, retry/cost bounds, failed-QA rejection before Security starts, and typed audit results. The scanner checks only the course's SQL/XSS teaching markers.

Each scenario uses a separate kernel with provider credentials omitted and runtime tripwires for live Crew execution and external DNS/connections. Dedicated negative tests deliberately trigger those guards and require a failure. Loopback connections remain available for Jupyter. The guards support verification of this path; they are not a production sandbox.

<a id="verification-pyramid--4-readiness-and-ci"></a>

### 4. Readiness and CI

Run the full gate before distribution or review:

```sh
python tools/check_readiness.py
```

It checks the Python version and exact direct dependency pins, runs `pip check`, then runs unit and integration stages. Any failed/error/skipped test, missing/empty report, timeout, or changed verification input makes the command fail.

Reports in `.test-results/readiness/` contain JUnit XML, executed copies, logs, environment versions, and input hashes. The [GitHub Actions workflow](.github/workflows/readiness.yml) runs the same command on Ubuntu and Windows. Local results and remote CI results are separate evidence.

Record the actual run in the [assessment compliance checklist](#assessment-compliance-checklist). Passing tests establish the stated deterministic workshop behaviors. They do not prove live LLM reliability, full vulnerability detection, or production deployment security.

<a id="verification-pyramid--review-that-still-needs-an-instructor"></a>

### Review that still needs an instructor

- Check learning objectives, instructions, and the marked TODOs against the solution guide.
- Review slide readability and the short learner decision/ADR explanations.
- Confirm classroom hardware, package availability, accessibility, and Paper ADR arrangements.
- Preserve the three `/15` lab graders, `/20` Capstone code rubric, and `/20` ADR rubric.

Optional extension notebooks receive cleanliness checks. Their full behavior, archived API/A2A lessons, and the archived nested CrewAI research project are outside this gate. The active [CrewAI bridge](crewai_learning/README.md) has fixture-driven and real-kernel coverage in `tests/test_crewai_reference.py`. Add explicit tests and dependencies before claiming readiness for other materials.

<a id="verification-pyramid--instructor-diagnosis-order"></a>

### Instructor diagnosis order

Inspect the contract, caller/tool authority, supplied context, and retry evidence before blaming the fixture output or extending the workflow. Use deterministic regressions to preserve each repaired behavior.

---

<a id="curriculum-maintenance-checklist"></a>

## Curriculum Maintenance Checklist

Use the [automated development workflow](DEVELOPMENT.md) throughout editing. Run its full readiness gate before releases and teaching, then use this checklist for curriculum and distribution review.

<a id="curriculum-maintenance-checklist--1-schema-synchronization"></a>

### 1. Schema Synchronization

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

<a id="curriculum-maintenance-checklist--2-optional-advanced-identity-and-tool-matrix"></a>

### 2. Optional Advanced Identity and Tool Matrix

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

<a id="curriculum-maintenance-checklist--3-notebook-hygiene"></a>

### 3. Notebook Hygiene

Checklist:

- [ ] Edit current handouts in place. If using `tools/build_core_notebooks.py`, run it on a private copy first and review its output against the current handouts before replacing them. Preserve supplied management actions and cell IDs.
- [ ] Clear outputs before commit.
- [ ] Search for absolute paths such as `/Users/` or `C:\\Users\\`.
- [ ] Confirm every core notebook sets `USE_LIVE_LLM = False` and contains no provider-call branch. The historical bonus must remain a fixture-only redirect; do not add provider execution or credential setup.
- [ ] In Python 3.12 with `requirements/maintenance.txt`, run `python -m pytest tests/test_notebooks.py -v`.

Commands:

```bash
rg "/Users/|C:\\\\Users\\\\" notebooks
python -m pytest tests/test_notebooks.py -v
```

<a id="curriculum-maintenance-checklist--4-assignment-and-rubric-alignment"></a>

### 4. Assignment and Rubric Alignment

Checklist:

- [ ] Every assignment has clear deliverables, constraints, and rubric weights.
- [ ] Every implementation-heavy assignment has starter code.
- [ ] Every core assignment has an instructor solution guide.
- [ ] [supplemental governance practice](ASSIGNMENTS.md#basic-agent-governance-labs) stays aligned with its local examples and the Capstone Security Team; the external A2A QA exercise stays archived.
- [ ] Required tests named in assignment text are represented in tests or instructor guidance.
- [ ] The [grading files](#grading) match the three `/15` lab graders scaled to `/20` each, Capstone code `/20`, and ADR `/20`. Formative exercises and optional extensions add no marks.

Notes:

- Keep the required course to three graded labs and one Capstone.
- The Capstone's cost-aware routing helper stays pre-written and ungraded. Do not turn it into a fourth lab or a router grading task.
- Optional homework tracks remain outside the required two-day path.

<a id="curriculum-maintenance-checklist--5-secret-and-key-scrubbing"></a>

### 5. Secret and Key Scrubbing

Checklist:

- [ ] No API keys in notebooks, docs, or starter files.
- [ ] `.env` is ignored and absent from the repo.
- [ ] All required notebooks, factory and the historical bonus contain no provider execution path.
- [ ] Placeholder keys are clearly fake, such as `sk-internal-admin` for local API identity tests.

Command:

```bash
rg -n "(sk-[A-Za-z0-9_-]{20,}|OPENAI_API_KEY=.*[A-Za-z0-9]{10,}|ANTHROPIC_API_KEY=.*[A-Za-z0-9]{10,}|api_key\\s*=\\s*['\\\"][A-Za-z0-9_-]{20,})" .
```

<a id="curriculum-maintenance-checklist--6-starter-code-vs-solution-drift"></a>

### 6. Starter Code vs. Solution Drift

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

<a id="curriculum-maintenance-checklist--7-release-hygiene"></a>

### 7. Release Hygiene

Checklist:

- [ ] No `__pycache__`, `.pytest_cache`, `.DS_Store`, or `.env` files.
- [ ] Markdown local links resolve.
- [ ] The master hub’s curated resources link to canonical sources.
- [ ] README and setup guide point to the current notebook and assignment map.
- [ ] `notebooks/` contains exactly the seven canonical handouts; `notebook_manifest.yml` stays at the repository root.
- [ ] The README hub links all nine topics to the seven required notebooks, consolidated assignment sections and curated resources. Check the hub anchors after any merge.

Commands:

```bash
find . -name "__pycache__" -o -name ".pytest_cache" -o -name ".DS_Store" -o -name ".env"
python tools/check_readiness.py
```

---

<a id="scope-alignment-verification"></a>

## Scope Alignment Verification

This scope reference describes the current seven-notebook course, its six-slide deck and local evidence boundaries. Historical verification lives in the assessment evidence section and archived originals.

<a id="scope-alignment-verification--deliverable-scope"></a>

### Deliverable scope

The two-day workshop teaches learners to manage **two cooperating multi-agent teams** through one typed boundary:

- **Development Team:** Engineering Manager, Coder, and QA Auditor.
- **Security & Compliance Team:** Security Manager and Pen Tester.
- **Inter-team handoff:** the Development Team's `DevDeliverable` is validated by Pydantic before the Security Team consumes it. The Security Team returns a typed `SecurityAuditResult`.

This is an intra-workshop inter-team handoff. Cross-organization A2A transport is advanced material archived under `_archive/advanced_scaling/` and is not part of the core learner path.

<a id="scope-alignment-verification--required-learner-path"></a>

### Required learner path

Use the [seven-notebook route and stable cell map](#course-manager-notebook-assignment-path). The foundation labs progress from contract to team to guardrails; Capstone validates Development-to-Security delivery, then factory and CI/CD add actual local artifacts and gated publication. Three raw `/15` lab scores scale to `/20` each; code `/20` and ADR `/20` complete `/100`. Routing, factory and CI/CD add no new marks.

<a id="scope-alignment-verification--academic-framing"></a>

### Academic framing

Theory of Mind and TeamLog explain role-specific context and shared commitments. TRINITY, Conductor, ChatDev, and Reflexion inform the discussion of worker/verifier feedback and bounded repair. The written guide labels access-list routing as a local Fugu-style pattern, not a hosted routing API. Cost-aware dynamic routing is a pre-written local policy in the Capstone, with illustrative costs and no coding task or grade. The sources are linked in the [README](README.md) and [Playbook](README.md#golden-path).

<a id="scope-alignment-verification--verification-record-and-earlier-rehearsal-notes"></a>

### Verification record and earlier rehearsal notes

Use the [verification pyramid](#verification-pyramid) and [assessment evidence](#assessment-compliance-checklist). Current completion requires current input hashes and successful command output. Earlier artifact reviews and setup timings are dated evidence for their own inputs. The current deck is six slides. A manifest entry, constructed Crew or green score does not establish unrestricted behavior, security or certification.

<a id="scope-alignment-verification--scope-controls"></a>

### Scope controls

- Preserve the required seven-notebook sequence, three graded labs, one Capstone and `/100` rubric.
- Keep the Capstone routing helper pre-written, deterministic and ungraded.
- Keep advanced HTTP/A2A, deployments and provider integrations outside the required runtime.
- Required labs, factory and CI/CD call no provider APIs and need no API keys; actual API cost is $0.00.
- Accept the Paper ADR route with the stated rubric; do not fabricate code evidence or full marks.
- Keep classroom timing private. Do not describe fixture scans as comprehensive security, a schema as truth/PII detection, or local publication as a hosted release.

---

<a id="assessment-compliance-checklist"></a>

## Assessment evidence and compliance boundaries

Use this section to record release evidence and explain its scope. [The verification pyramid](#verification-pyramid) defines the checks. The [rubric](#grading) defines learner marks. A passing course score is not a security, privacy or operational certification.

<a id="assessment-compliance-checklist--acceptance-audit---19-october-2026"></a>

### Historical acceptance audit: 19 October 2026

The archived original records a 19 October setup rehearsal: unchanged requirements installed in 57.927 seconds and JupyterLab served `/lab` after 63.976 seconds on one Mac. Its 122-test run, five-notebook layout, former provider bonus, older presentation hash and older link counts are historical. Those claims do not validate the current seven-notebook release. Physical printing was declined; the digital rubric remains the accepted delivery format.

For the current release, verify the seven notebooks, six-slide presentation, cleared learner outputs, exact rubric conversion, local links, fixture-only execution, factory denial/stale-evidence cases, and learner ZIP contents after consolidation.

<a id="assessment-compliance-checklist--current-readiness-evidence"></a>

### Current readiness evidence

Run `python tools/check_readiness.py` after editing and inspect `.test-results/readiness/summary.json`, its run-specific logs, JUnit reports and verification-input hashes. Do not label a previous run current merely because it passed.

The locally observed pre-consolidation run `20261021T040629Z-7267a2a8` reported **277 unit + 72 integration = 349 passed**, no failures/errors/skips, Python 3.12.3 on macOS 26.3 arm64, and clean dependencies. Its input SHA256 was `609637f665776e762542e406b706a9e8b8ee05b09b8111652cac6e190e666629`. This is a dated snapshot, not evidence for subsequent documentation or package edits. Retain the new run's actual result at release.

Local execution evidence does not imply remote Ubuntu/Windows CI ran, native PowerPoint hyperlink behavior was tested, every security issue was found, or a website was deployed to a remote host. Browser/source accessibility checks are bounded evidence rather than WCAG certification.

<a id="assessment-compliance-checklist--assessment-plan-100-marks"></a>

### Assessment plan: 100 marks

Use the single [marks table](#grading--marks) and [Paper ADR scoring anchors](#capstone-paper-adr-quick-sheet--instructor-scoring-anchors). Keep raw `/15` lab scores visible; convert each with `raw × 20 ÷ 15`. The final portfolio is `/100`. Factory/CI evidence is discussed with the Capstone without additional marks.

<a id="assessment-compliance-checklist--historical-verification-record-through-18-october-2026"></a>

### Historical verification record (through 18 October 2026)

Archived text records retain historical test, setup, grading, and alignment notes through 18 October. They recorded 112 local tests (73 unit, 39 integration) on 17 October and used earlier course artifacts. These records do not verify current files.

The substantive acceptance rules remain: invalid contracts block downstream work; Manager permissions/context are audited; stale QA inbox work is cleared; bounded repair records four maximum failing calls and escalation; failed QA is rejected before Security starts; tool scanning/approval authority is separate; and grading arithmetic distinguishes partial, zero and missing marks. Inspect the current tests and actual notebook results for each claim.

<a id="assessment-compliance-checklist--historical-automated-readiness-run-17-october-2026"></a>

### Historical automated readiness run (17 October 2026)

Run `20261017T090613Z-8d5290ed` used Python 3.12.3 on macOS 26.3 arm64 and reported 73 unit + 39 integration = 112 passed with exact direct pins and `pip check`. Its input SHA256 was `970852888845818efb502b030f21f9ecebb4fafc9dd50a3090ea9e86fe2c3ca7`. The discovered clearance defect was repaired by checking the full public/confidential/restricted ordering and all nine combinations. Rerun after changing an input.

The [CI workflow](.github/workflows/readiness.yml) is configured for Ubuntu and Windows. A local run and a remote workflow run are distinct evidence. See [DEVELOPMENT.md](DEVELOPMENT.md) for the maintenance route.

<a id="assessment-compliance-checklist--test-crosswalk"></a>

### Test crosswalk

| Outcome | Authoritative test location |
| --- | --- |
| Typed contracts and rejected handoff data | `tests/test_schemas.py`, `tests/test_handoffs.py`, Lab 1 grader |
| Manager tool/context/owner/current proposal | `tests/test_management_controls.py`, real Lab 2 scenarios in `tests/test_notebooks.py` |
| Retry, early stop, cost and escalation | `tests/test_management_controls.py`, `tests/test_adversarial_scenarios.py`, `tests/test_ex5_capstone.py` |
| Validated Dev-to-Security transition | `tests/test_ex5_capstone.py`, repaired Capstone kernel assertions |
| Historical bonus cannot activate providers | `tests/test_capstone_bridge.py`, `tests/test_offline_runtime.py` |
| Tool transparency and non-execution | `tests/test_skill_transparency.py` |
| Factory costs, checks, fixtures and publication | `tests/test_factory_costs.py`, `tests/test_factory_local_checks.py`, `tests/test_factory_harness.py`, `tests/test_factory_workflow.py` |
| Notebook/package hygiene and executed route | `tests/test_notebooks.py`, `tests/test_learner_pack.py`, `tests/test_offline_runtime.py` |
| Gate rejects incomplete/failed/skipped reports | `tests/test_readiness.py` |

These files establish only the cases and paths they exercise. Preserve scope statements when reporting a result.

<a id="assessment-compliance-checklist--score-record"></a>

### Score record

| Learner / cohort | Lab 1 raw /15 | Lab 1 /20 | Lab 2 raw /15 | Lab 2 /20 | Lab 3 raw /15 | Lab 3 /20 | Capstone code /20 | ADR /20 | Total /100 | Grade | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| | | | | | | | | | | | |

Grade bands: A 80–100; B 65–79; C 50–64; F below 50. The spreadsheet is the individual learner tracker; this table is a compact paper backup.

---

Private solution appendix. These are reference answers for optional or historical exercises; use the core solution guide for the current graded repairs.

<a id="basic-agent-governance-labs-solution-guide"></a>

## Supplemental Governance Practice Exercises: Solution Guide

Use this guide for optional, ungraded practice with the Logistics Weather, Writer, QA, and CEO-directed planning scenarios. The required course path remains three guided labs plus one Capstone.

<a id="basic-agent-governance-labs-solution-guide--strong-answer-indicators"></a>

### Strong Answer Indicators

- The learner uses Pydantic models for every boundary artifact instead of raw dictionaries.
- The learner separates agent identity from tool authorization.
- The learner keeps API keys and privileged actions inside gateways, never inside prompts.
- The learner records audit evidence for denied, repaired, or escalated paths.
- The learner can explain the management principle in one sentence.

<a id="basic-agent-governance-labs-solution-guide--optional-exercise-1-governed-logistics-weather-agent"></a>

### Optional Exercise 1: Governed Logistics Weather Agent

Expected evidence:

- `AgentIdentity(role="logistics_coordinator")` can call `get_weather`.
- `AgentIdentity(role="external_widget")` cannot call `get_weather`.
- `WeatherRequest` rejects unsupported units or extra fields.
- `WeatherResponse` includes `shipping_risk` and rejects invented fields.
- The API key is stored only in the gateway or environment-backed adapter.

Common mistakes:

1. Returning a loose `dict` instead of `WeatherResponse`.
2. Checking only `allowed_tools` but not the gateway policy.
3. Exposing the API key in an agent prompt or notebook output.
4. Letting the LLM invent fields such as `vibes` or `recommendation`.

<a id="basic-agent-governance-labs-solution-guide--optional-exercise-2-bounded-writer-agent"></a>

### Optional Exercise 2: Bounded Writer Agent

Expected evidence:

- The Writer reads `target_audience` from shared memory.
- The Editor returns `EditorFeedback`, not a string.
- The second attempt uses the previous feedback.
- Forced failure returns a typed `EscalationTicket`.
- The loop has a strict retry budget.

Common mistakes:

1. Treating repair as blind retry.
2. Losing editor feedback between attempts.
3. Allowing `while True` repair loops.
4. Returning `"failed"` instead of a typed escalation artifact.

<a id="basic-agent-governance-labs-solution-guide--optional-exercise-3-security--compliance-team-audit"></a>

### Optional Exercise 3: Security & Compliance Team Audit

Expected evidence:

- The Security Team receives a `DevDeliverable`, not raw unvalidated text.
- Pydantic rejects deliverables that did not pass QA.
- The receiving team revalidates the contract before inspecting the code.
- SQL/XSS indicators return a typed `SecurityAuditResult` with findings and `approved=False`.
- A clean, tested deliverable returns an approved result with an audit signature.

Common mistakes:

1. Starting the Security Team from raw coder text.
2. Ignoring the test-status field or team signature.
3. Returning a plain string instead of `SecurityAuditResult`.
4. Letting the Security Team rewrite or approve its own findings without a separate release decision.

<a id="basic-agent-governance-labs-solution-guide--optional-exercise-4-ceo-directed-project-planning"></a>

### Optional Exercise 4: CEO-Directed Project Planning

Expected evidence:

- The initial CEO instruction becomes a typed `ProjectPlan`.
- The database choice is stored as a `TeamCommitment`.
- The mid-flight MongoDB instruction updates TeamLog.
- The Coder reads TeamLog, not raw CEO text.
- A final `HumanReviewDecision` gates release.

Common mistakes:

1. Passing raw human text directly into the Coder.
2. Updating a local variable but not durable memory.
3. Omitting the human approval/rejection gate.
4. Passing unstructured intent to the Coder instead of governed project state.

---

<a id="ex1-solution-guide"></a>

## Ex1 Solution Guide: Agent Roster & SOPs



<a id="ex1-solution-guide--expected-architecture"></a>

### Expected Architecture

- Product Manager parses the GitHub issue into `TaskSpec`.
- Tech Lead or Manager decomposes the task into implementation steps.
- Coder produces `CodePatch`.
- QA runs tests and produces `TestResult`.
- Reviewer approves, repairs, or escalates through `ReviewDecision`.

<a id="ex1-solution-guide--strong-answer-indicators"></a>

### Strong Answer Indicators

- Agents have distinct roles, goals, and tools.
- SOP includes both happy path and failure path.
- QA failure routes back to Coder with error evidence.
- No agent has every tool.
- Handoffs are named artifacts, not vague messages.

<a id="ex1-solution-guide--common-mistakes"></a>

### Common Mistakes

- Giving all agents file, database, and execution tools.
- Omitting retry limits.
- Treating SOP as a paragraph rather than a sequence.
- No acceptance criteria before coding.

<a id="ex1-solution-guide--instructor-check"></a>

### Instructor Check

Ask: "Where is the first place a hallucinated field would be rejected?" If the learner cannot answer, their contract design is underspecified.

---

<a id="ex2-solution-guide"></a>

## Ex2 Solution Guide: Theory-of-Mind Memory System



<a id="ex2-solution-guide--expected-behavior"></a>

### Expected Behavior

The PM stores "Use PostgreSQL for persistent storage" in shared memory. The Coder receives only "Implement the user persistence layer" and must retrieve the PM's constraint before producing a `DesignPlan`.

<a id="ex2-solution-guide--minimal-correct-implementation"></a>

### Minimal Correct Implementation

- `MemoryRecord` has author, visible roles, sensitivity, tags, and text.
- `search(query, requester)` filters unauthorized records before matching.
- `DesignPlan.storage_choice` becomes `PostgreSQL` due to retrieved memory.
- A restricted record exists and is not returned to the Coder.

<a id="ex2-solution-guide--strong-answer-indicators"></a>

### Strong Answer Indicators

- The Coder cites or records which memory item influenced the design.
- Retrieval is tag/text based, not direct ID lookup.
- The reflection correctly distinguishes shared memory from Theory of Mind: memory stores evidence; ToM uses it to infer teammate intent.

<a id="ex2-solution-guide--common-mistakes"></a>

### Common Mistakes

- Hardcoding PostgreSQL in the Coder.
- Returning all memory before filtering.
- No sensitivity model.
- No demonstration that restricted memory is denied.

---

<a id="ex3-solution-guide"></a>

## Ex3 Solution Guide: RAG & MCP Architecture



<a id="ex3-solution-guide--expected-architecture"></a>

### Expected Architecture

- Separate memory domains for requirements, codebase, and operational data.
- MCP servers for GitHub, Jira, local file system, or database access.
- Policy gateway before every MCP call.
- Agents receive least-privilege tool scopes.

<a id="ex3-solution-guide--strong-answer-indicators"></a>

### Strong Answer Indicators

- Code RAG uses structure-aware chunking by function/class/file.
- Requirements RAG uses ticket and acceptance-criteria chunking.
- Tool matrix explicitly denies dangerous tools to non-authorized agents.
- Threat matrix includes prompt injection and malicious tool descriptions.

<a id="ex3-solution-guide--common-mistakes"></a>

### Common Mistakes

- Treating MCP as a security layer by itself.
- Giving the Coder database write access.
- No retrieval provenance.
- No policy for sensitive documents.

---

<a id="ex4-solution-guide"></a>

## Ex4 Solution Guide: Trust & Governance Matrix



<a id="ex4-solution-guide--expected-architecture"></a>

### Expected Architecture

The learner should model agents as identities with organization, role, trust tier, public key reference, allowed tools, and allowed message schemas.

<a id="ex4-solution-guide--strong-answer-indicators"></a>

### Strong Answer Indicators

- Vendor agent can export approved reports but cannot read restricted deployment logs.
- Every cross-org handoff has a typed schema.
- Denial examples are concrete: identity, requested tool, data class, policy reason.
- Threat mitigations map to specific controls, not generic "monitoring."

<a id="ex4-solution-guide--common-mistakes"></a>

### Common Mistakes

- No difference between confidential and restricted data.
- Trust is assigned by role name only.
- Vendor agents can read internal memory.
- Threat matrix omits context leakage.

<a id="ex4-solution-guide--instructor-check"></a>

### Instructor Check

Ask the learner to trace one denied request from agent identity to policy decision. A strong design can explain the denial in one sentence.

---

<a id="ex5-capstone-solution-guide"></a>

## Capstone Solution Guide

Use the [Core Notebook Solution Guide](instructor/solutions/core_notebook_solution_guide.md) for the current two-team Capstone. It matches the required `04_capstone.ipynb` notebook and its 20-point grader.

The former guide described a larger API-backed production architecture. That material is outside the required two-day course and has been removed from this solution path. Optional API-boundary material remains separate from the core Capstone.
