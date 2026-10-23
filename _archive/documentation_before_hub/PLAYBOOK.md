# Managing Multi-Agent Teams: Learner Playbook

[Course home](README.md) · [Dashboard](README.md#navigation-dashboard) · [Setup](SETUP.md) · [Course map](COURSE_MAP.md)

The course begins with repeatable local fixtures and continues into a deterministic Software Factory that builds a minimalist travel website. The same governance questions apply throughout: what may cross a boundary, which role may act, what evidence supports a decision, and when must a human approve the next step?

## Core course focus: managed team delivery

| Practice | Control | Inspect |
| --- | --- | --- |
| Lab 1 | Pydantic constraints before handoff | Valid and malformed data |
| Lab 2 | Manager, Coder, and QA duties with approved context | Tool lists, task dependencies, Manager audit |
| Lab 3 | Input validation and bounded repair | Calls, simulated cost, escalation |
| Capstone | Independent Development-to-Security boundary | Validated deliverable, scan, ADR |
| Factory | Illustrative role labels, simulated ledger, real Git candidate, staged human gates | Simulation label and actual $0.00, decisions and revision |
| Local CI/CD | Checks and human publication authorization | Candidate evidence, rejected changes, published file receipt |

## Learner path

1. Complete [setup](SETUP.md), then [preflight](notebooks/00_sandbox_preflight.ipynb).
2. Run [Lab 1](notebooks/01_lab_pydantic.ipynb), [Lab 2](notebooks/02_lab_crewai.ipynb), and [Lab 3](notebooks/03_lab_security.ipynb) in order. Repair only marked controls, rerun dependent cells, and explain the result.
3. Complete [the Capstone](notebooks/04_capstone.ipynb) and its [travel-site brief](assignments/ex5_capstone_virtual_software_company.md).
4. Operate [the factory lab](notebooks/05_live_software_factory.ipynb), then prove the gates in [local CI/CD](notebooks/06_local_cicd.ipynb).
5. Retain the artifacts in the [submission checklist](#submission-checklist).

Labs 00–04 remain deterministic with `USE_LIVE_LLM = False`. Notebooks 05/06 use simulation/replay fixtures and make no API calls. The [CrewAI learning bridge](crewai_learning/README.md) runs actual CrewAI tasks using fixture LLMs, which helps distinguish framework execution from a live model call.

## Your management decisions

In Lab 2, a failed audit leaves the local QA inbox empty. `PASS_TO_QA` admits a typed proposal but runs no QA Crew. In Lab 3, corrected controls record `ESCALATE_TO_HUMAN` after the initial attempt plus three retries. That four-call fixture stops at its illustrative $0.20 and grants no release permission.

The factory expands the Engineering Manager's responsibilities into a simulated orchestrator. Coder, Security, UI/UX, and QA each have an illustrative model label and typed fixture output. The terminal displays paced collaboration. This does not execute real model reasoning. Human decisions still control actual local file publication.

Human gates cover plan/spend, code build, security, UI/UX, QA, and final local publication. Denial, EOF, missing evidence, or a changed candidate stops the dependent action. An unattended `--no-input` run cannot approve itself. Inspect exactly which revision each report covers before proceeding.

## Model and cost decisions

Read [the simulation profile](software_factory/simulation_config.json) before running. The scenario assigns an illustrative historical model label to each role: GPT-4 to the orchestrator, Claude 3.5 to Coder, GPT-4 Turbo to Security, GPT-4 Vision to UI/UX, and GPT-3.5 to QA. These labels explain role-specific capability/cost decisions. They do not identify active engines or promise current model availability.

The default simulated plan totals $0.50: orchestrator $0.05, Coder $0.15, Security $0.10, UI/UX $0.10, QA $0.05, and local publication $0.05. The ledger checks the teaching allowance before work, records approved work that ran, and stops a step that would exceed the simulated budget. Actual API cost is always $0.00. No API key, network call, provider SDK, or billing account is required.

## Factory execution

From the repository root in the activated environment:

```bash
python orchestrator.py --check-only
python orchestrator.py --security-demo
python live_simulation_orchestrator.py
```

The default mode is simulation, with paced presentation delays. `--mode replay --delay-seconds 0` runs the same fixtures without pacing. Review the terminal collaboration and each requested gate. After final human approval, inspect the generated candidate repository, evidence, and local `index.html`. On macOS:

```bash
open index.html
```

For automated or noninteractive verification, use `--delay-seconds 0`. `--no-input` deliberately rejects approval rather than inventing a human decision. `--mode live` is unavailable.

Generated source lives under the separate factory workspace on a feature branch. The local published page is a reviewable output. Remote GitHub intake, protected branches, hosted deployments, and target-side health checks require their own configured service and evidence.

## Assessment and gradebook

| Component | Course marks | Evidence |
| --- | ---: | --- |
| Lab 1 | 20 | Valid and invalid schema fixtures, raw /15 result |
| Lab 2 | 20 | Manager tool/context repairs, audit and decision, raw /15 result |
| Lab 3 | 20 | Unsafe input rejection, bounded attempts, escalation, raw /15 result |
| Capstone implementation | 20 | Contract gate before Security, scoped tools, typed result |
| Capstone ADR and defense | 20 | Risk/architecture (6), controls/evidence (7), credible next step (7) |
| **Total** | **100** | |

Convert each lab with `raw_score × 20 ÷ 15`. The integrated factory and CI/CD labs provide required delivery evidence for the Capstone discussion without introducing a separate point scale. A simulation run demonstrates local policy behavior. The generated files, Git candidate, bounded checks, and explicit publication decision are real local evidence. Remote deployment is outside this demo.

## Capstone three-question ADR

1. What contract governs the Development-to-Security handoff and which malformed/failed-QA input does it reject?
2. Which role may write, review, test, approve spend, and authorize publication? Which evidence binds each decision to the current revision?
3. What risk remains in the travel-site factory, what did your tests establish, and what would you add before a hosted service?

Use [the ERD](resources/diagrams/capstone_factory_erd.md) to explain durable budget/accounting records separately from proposed travel-service entities. The current travel website is static and has no booking backend.

## Submission checklist

- Three repaired lab notebooks with raw grader results and management decision notes.
- Capstone notebook with validated handoff, scoped Security tools, typed audit result, and code score, or the agreed Paper ADR route.
- One-page ADR covering risk, controls, observed evidence, and next step.
- Factory evidence: role/model profile, execution mode, blocked malicious request, gate decisions, simulated budget ledger and actual $0.00, and candidate Git revision.
- Local CI/CD evidence: a clean candidate, at least one rejected unsafe/missing-evidence candidate, final publication decision, and the published file/receipt if approved.

No provider account is required. Use simulation or replay and state the evidence limit. A Paper ADR can explain blocked execution but must not invent unobserved model reasoning or remote deployment results.

## Standards and evidence limits

The [diagram and standards guide](resources/diagrams/README.md) maps selected exercises to least privilege, separation of duties, input validation, and reviewable release decisions. These are learning examples, not compliance certification. Pydantic validates declared structure, scanners can miss defects, a local hook can be bypassed, and a human approval applies only to the candidate actually reviewed.

[Return to dashboard](README.md#navigation-dashboard) · [Exercise index](assignments/index.md) · [Factory guide](extensions/live_software_factory.md)
