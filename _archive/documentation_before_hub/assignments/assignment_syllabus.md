# Course syllabus

[Course home](../README.md) · [Playbook](../PLAYBOOK.md) · [Exercise index](index.md)

## Course outcome

Specify and supervise a governed multi-agent workflow, repair selected controls, then operate a deterministic Software Factory that creates a minimalist travel website. Explain what the evidence proves and which claims remain unverified. All course execution is local, makes no provider calls, and has actual API cost $0.00.

## Measurable learning outcomes

| Given | Learner action | Evidence |
| --- | --- | --- |
| A weak contract and invalid data | Repair Pydantic constraints | Lab 1 valid/invalid fixtures and grader |
| Manager–Coder–QA configuration | Repair role tools and approved context | Lab 2 audit, inbox and decision |
| Unsafe input and failing tool | Reject input, bound retry, escalate | Lab 3 call/cost trace |
| Development artifact | Validate before Security starts | Capstone handoff order and typed result |
| Travel-site request and fixture roles | Apply human gates and simulated budget policy | Factory candidate, ledger and approvals |
| Local release candidate | Run bounded reviews and reject missing/stale evidence | CI/CD report and publication receipt |

## Course topic map

| Topic | Competency | Activity |
| ---: | --- | --- |
| 1 | Checkable specifications | [Assignment 01](assignment_01_strategic_prompt_engineering.md) |
| 2 | Workspace and role-aware context | [Assignment 02](assignment_02_ai_workspace_and_role_context.md) and preflight |
| 3 | Typed contracts | [Lab 1](../notebooks/01_lab_pydantic.ipynb) and [brief](assignment_03_architectural_supervision.md) |
| 4 | Tools and bounded control flow | [Lab 3](../notebooks/03_lab_security.ipynb) |
| 5 | Code auditing and separate duties | [Lab 2](../notebooks/02_lab_crewai.ipynb) and [brief](assignment_04_code_auditing.md) |
| 6 | Input validation and evaluation | [Lab 3 brief](assignment_06_code_validation.md), factory security checks |
| 7 | Authorized context selection | [Assignment 07](assignment_07_context_engineering_access_lists.md) |
| 8 | Debugging and SDLC | [Assignment 08](assignment_08_debugging_sdlc.md), [CrewAI bridge](../crewai_learning/README.md), local CI/CD |
| 9 | Managed software delivery | [Capstone](ex5_capstone_virtual_software_company.md), [factory](../notebooks/05_live_software_factory.ipynb), [CI/CD](../notebooks/06_local_cicd.ipynb) |

## Practice and feedback

Predict the next gate before running the fixture. Repair the marked control, inspect the output, explain its evidence limit, then transfer the decision to the travel-site factory. [The teaching-design alignment](../instructor/stanford_teaching_guide_alignment.md) documents the local instructional rationale.

The main [26-slide deck](../slides/managing_multi_agent_teams_workshop_v16.pptx) supports the full sequence. Foundation notebooks construct CrewAI configurations and validate fixtures. The CrewAI bridge executes actual Crew tasks with fixture LLMs. The factory presents pre-generated collaboration with paced delays and performs real local artifact, Git, review, and publication operations. Illustrative model labels do not run real model reasoning.

## Assessment

| Component | Marks |
| --- | ---: |
| Lab 1, raw /15 scaled to /20 | 20 |
| Lab 2, raw /15 scaled to /20 | 20 |
| Lab 3, raw /15 scaled to /20 | 20 |
| Capstone code | 20 |
| ADR and defense | 20 |
| **Total** | **100** |

Factory and CI/CD receipts are part of the delivery evidence used in the Capstone defense. No separate score is invented. See [the Capstone rubric](ex5_capstone_virtual_software_company.md#assessment-40-points) and [playbook](../PLAYBOOK.md#assessment-and-gradebook) for the Paper ADR route and evidence limits.
