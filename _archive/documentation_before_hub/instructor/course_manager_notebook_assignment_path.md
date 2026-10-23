# Instructor Notebook and Assignment Path

Start with the canonical [COURSE_MAP.md](../COURSE_MAP.md) for the purpose, exact notebook cell IDs, learner edits and grader coverage. The [teaching notes](teaching_notes.md) contain scripts, preparation, and handover guidance. This page maps the seven-notebook course route: preflight, three labs, the Capstone, the deterministic Software Factory, and local CI/CD.

| Order | Notebook or brief | Instructor focus | Required evidence |
| --- | --- | --- | --- |
| 0 | [Preflight](../notebooks/00_sandbox_preflight.ipynb) | Confirm dependencies, deterministic mode, notebook kernel, and repository-root workspace. | Preflight completes without provider credentials. |
| 1 | [Lab 1](../notebooks/01_lab_pydantic.ipynb) · [Assignment 03](../assignments/assignment_03_architectural_supervision.md) | Repair the weak Pydantic data contract. | Supplied invalid output is rejected and valid data passes; grader 15/15. |
| 2 | [Lab 2](../notebooks/02_lab_crewai.ipynb) · [Assignment 04](../assignments/assignment_04_code_auditing.md) | Inspect the Skill Transparency Matrix before task setup, then repair the Manager's tools and Coder's Architect-task dependency. | Structural grader 15/15; inspect the local typed `CodePatch` fixture separately. |
| 3 | [Lab 3](../notebooks/03_lab_security.ipynb) · [Assignment 06](../assignments/assignment_06_code_validation.md) | Combine unsafe-input validation and bounded retries. | SQL-like fixture blocked; one initial call plus three retries, then escalation; grader 15/15. |
| 4 | [Capstone notebook](../notebooks/04_capstone.ipynb) · [brief and ADR](../assignments/ex5_capstone_virtual_software_company.md) | Connect deterministic Development and Security adapters through `DevDeliverable`; inspect the separate Crew configurations. | Failed QA rejected, validation precedes Security start, separate Security tools, typed audit result; grader 20/20 and ADR /20, or sound Paper ADR fallback. |
| 5 | [Software Factory Simulation](../notebooks/05_live_software_factory.ipynb) | Review fixture roles, simulated budget, bounded checks, and human gates. | Candidate revision, review reports, ledger and decisions; actual API cost $0.00. |
| 6 | [Local CI/CD](../notebooks/06_local_cicd.ipynb) | Reject missing/stale evidence and require final local publication approval. | Exact-candidate checks, failure evidence, and matching local file/receipt when approved. |

## Skill Transparency Matrix in Lab 2

Slide 12 and the notebook expose configured authority before the learner creates tasks. Markdown cell `lab2-skill-transparency-guide` explains the management decision. Code cell `lab2-skill-transparency` follows the actual Engineering Manager, Coder, and QA Agent definitions and precedes `lab2-task-configuration`.

`build_skill_transparency` reads each Agent's current tools and their actual name/description metadata. The displayed columns are **Role**, **Actual tools**, **Allowed tools**, and **Least privilege**. Each detail exposes **Action, Input, Output, Warning** from the configured tool description. The cell does not call tools, change permissions, train a model, or run a Crew.

The starter Manager exposes writing and approval, so its least-privilege result is false. After the learner removes its writing tool, rerunning the matrix should show the exact approval-only allowlist and a true result. Coder retains the writing tool; QA retains `run_tests_tool`. The check requires exact names with no duplicates. A row that merely omits an excess tool from a printed list would hide the defect; inspect the actual Agent object instead.

Ask the learner which excess permission they found, which role still owns writing, and what evidence supports the repair. Tool descriptions help an agent choose an action. The framework's configured tool list controls exposure inside that framework, while OS permissions, credentials, process isolation, and independent production policy require separate controls.

## Executive-brief evidence audit

| Module | What the course establishes | Boundary to explain |
| --- | --- | --- |
| 1 · Contracts | Declared Pydantic fields, range/extra-field constraints, and supplied rejection probes | A schema does not establish truth, eliminate hallucinations, or detect arbitrary PII without explicit rules. |
| 2 · Team | Actual tool metadata, role allowlists, task-context declarations, and local audit/inbox behavior | Available context does not prove a real model follows a rule; the foundation lab executes fixtures. |
| 3 · Guardrails | Supplied unsafe-input rejection, bounded mock call count, cost fixture, and escalation record | Selected fixtures do not prove complete injection defense or unrestricted production cost control. |
| 4 · Capstone and factory | Validated Development-to-Security adapter handoff, role separation, actual local files/Git/review evidence, and explicit publication gates | The Capstone uses local Python adapters rather than running both Crews. Publication is local, not a hosted production deployment. |

The deterministic factory supports repeatable local demonstrations after dependency setup. Its actual API cost is $0.00. Fixture checks provide evidence about those cases, with no general guarantee of reliability, security, privacy compliance, or enterprise readiness. Retain the /100 portfolio rubric without treating a score as certification.

## Team boundary

Labs teach the Engineering Manager, Coder, and QA pattern. The Capstone adds a Security Manager and Pen Tester. The required workflow runs ordinary Python adapters, while separate CrewAI objects model the teams. All foundation notebooks keep `USE_LIVE_LLM = False`. The factory and CI/CD use deterministic fixtures with actual API cost $0.00 and no API keys. Dependencies need installation before offline execution; the historical bonus is a fixture-only reference. The archive at [`_archive/advanced_scaling/`](../_archive/advanced_scaling/README.md) retains network A2A material outside the learner path.

Lab 2 context makes Architect rules available; it does not prove a model followed them. Its tool lists are framework permissions, not OS isolation. Its QA tool and the Capstone scanner are fixtures, not real test/scanning services. Use [the course map's evidence limits](../COURSE_MAP.md#what-the-graders-actually-check) when briefing another instructor.

## Grading

Each lab auto-grader reports `/15`; the assessment tracker converts raw lab scores to `/20`. Capstone code is `/20`; ADR and defense are `/20`. See [the compliance checklist](assessment_compliance_checklist.md) for readiness and test evidence.

## Preparation and maintenance resources

- [Teaching notes and course maintenance](teaching_notes.md)
- [Core notebook solution guide](solutions/core_notebook_solution_guide.md)
- [Delivery readiness checklist](course_delivery_readiness_checklist.md)
- [Grading files and usage](GRADING.md)
- [Assessment compliance checklist](assessment_compliance_checklist.md) · [Score tracker](assessment_score_tracker.xlsx)
- [Archived materials](../_archive/README.md)
