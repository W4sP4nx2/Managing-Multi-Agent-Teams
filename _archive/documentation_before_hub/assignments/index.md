# Course exercises

[Course home](../README.md) · [Playbook](../PLAYBOOK.md) · [Setup](../SETUP.md)

The course follows seven notebooks, from preflight to a deterministic Software Factory and local CI/CD. All execution uses local fixtures. Actual API cost is $0.00 and no API key is required.

| Order | Notebook and brief | Evidence |
| ---: | --- | --- |
| 0 | [Preflight](../notebooks/00_sandbox_preflight.ipynb) | Environment checks |
| 1 | [Typed contracts](../notebooks/01_lab_pydantic.ipynb) · [Exercise 03](assignment_03_architectural_supervision.md) | Valid/invalid fixtures and 15/15 |
| 2 | [Team oversight](../notebooks/02_lab_crewai.ipynb) · [Exercise 04](assignment_04_code_auditing.md) | Manager audit, scoped tools/context, decision and 15/15 |
| 3 | [Manager oversight](../notebooks/03_lab_security.ipynb) · [Exercise 06](assignment_06_code_validation.md) | Unsafe input block, bounded retry, escalation and 15/15 |
| 4 | [Capstone](../notebooks/04_capstone.ipynb) · [Brief and ADR](ex5_capstone_virtual_software_company.md) | Development-to-Security contract, code /20 and ADR /20 |
| 5 | [Software Factory Simulation](../notebooks/05_live_software_factory.ipynb) | Travel-site candidate, role fixtures, simulated ledger, human gate decisions |
| 6 | [Local CI/CD](../notebooks/06_local_cicd.ipynb) | Bounded checks, rejected unsafe/missing-evidence revision, explicit final local publication |

## Topic-linked briefs

| Topic | Activity |
| --- | --- |
| Specification | [01 · Checkable specification](assignment_01_strategic_prompt_engineering.md) |
| Workspace and context | [02 · Role-aware context](assignment_02_ai_workspace_and_role_context.md) |
| Contract | [03 · Typed handoffs](assignment_03_architectural_supervision.md) |
| Audit | [04 · Roles and evidence](assignment_04_code_auditing.md) |
| Validation | [06 · Input and repair controls](assignment_06_code_validation.md) |
| Context selection | [07 · Access lists](assignment_07_context_engineering_access_lists.md) |
| Debugging | [08 · Trace diagnosis](assignment_08_debugging_sdlc.md) |
| Delivery | [Travel-site Capstone](ex5_capstone_virtual_software_company.md) · [Factory guide](../extensions/live_software_factory.md) |

Use the [design checkpoints](agent_building_design_guide.md), [procurement and HR simulations](workshop_simulations.md), [CrewAI learning bridge](../crewai_learning/README.md), and [framework comparison](assignment_09_framework_comparison.md) alongside the relevant topic. The [Capstone ERD](../resources/diagrams/capstone_factory_erd.md) makes the factory records and proposed travel-domain relationships explicit.

## Assessment

Lab raw /15 results scale to /20 each. Capstone implementation is /20 and ADR/defense /20, making 100 marks. Factory and CI/CD evidence extends the Capstone discussion without an extra point scale. Read the [syllabus](assignment_syllabus.md) and [submission checklist](../PLAYBOOK.md#submission-checklist).

## Historical assignments

Superseded long-form assignments are retained in [the assignment archive](../_archive/assignments/README.md). They are excluded from the current course route. The current factory and local CI/CD labs replace the need to navigate multiple unrelated deployment/homework tracks.
