# Lab diagrams and control guide

[Course home](../../README.md#lab-diagrams-and-navigation) · [Exercise index](../../assignments/index.md) · [Course map](../../COURSE_MAP.md#control-and-cell-map)

Use a diagram to trace who supplies an artifact, where it is checked, and what may happen next. Then open the notebook and run its cells in order. The diagrams use named boxes, directional arrows, and explicit acceptance/block labels; meaning is available in text as well as color.

| Order | Open and navigate | Evidence to explain |
| --- | --- | --- |
| 1 | [Lab 1 notebook](../../notebooks/01_lab_pydantic.ipynb) · [Exercise 03](../../assignments/assignment_03_architectural_supervision.md) | Why the weak schema accepts the fixture, how the repaired contract rejects defects, and why valid data still passes. |
| 2 | [Lab 2 notebook](../../notebooks/02_lab_crewai.ipynb) · [Exercise 04](../../assignments/assignment_04_code_auditing.md) | Who may write, how rules reach the Coder, and why only a passing audit admits a typed proposal to the local QA inbox. |

## Lab 1: contract before handoff

![Lab 1 contract gate; the text description follows.](lab1-contract-flow.svg)

The delivery manager defines required fields, a confidence range, and a rule rejecting undeclared fields. A local fixture represents untrusted model output. The weak schema accepts a bad score and silently drops the extra field. The learner repairs `StrictResearchOutput`; the grader checks valid and malformed probes. Valid input can pass the contract; malformed input is rejected. A passing schema establishes the declared data constraints. Reviewers still need evidence that the findings are correct.

## Lab 2: roles, context, and audit

![Lab 2 role and audit flow; the text description follows.](lab2-team-audit.svg)

The human delivery manager supervises an Engineering Manager, Coder, and QA Auditor. Approved rules in `team_log` feed `architect_task`, a task artifact. The learner supplies that dependency to `coder_task` and removes the Manager's writing tool. The local Coder fixture becomes a proposed `CodePatch`. The supplied audit checks tools, task ownership, context, output contracts, and payload validity. A failed check blocks the handoff and clears the local QA inbox; a pass admits one typed patch. The QA task and `QAReport` are configured for later verification. The required exercise executes the fixture and audit locally.

## Standards and implementation references

These are teaching mappings to selected engineering controls. A passing lab supplies the evidence described below; a production assessment needs evidence from the deployed system.

| Principle | Course application | Reference and limit |
| --- | --- | --- |
| Validate an artifact before use | Lab 1 checks field declarations, the inclusive range, and extra fields; Lab 2 validates `CodePatch`. | [Pydantic field constraints](https://docs.pydantic.dev/latest/concepts/fields/) and [extra-field configuration](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.extra). Representation checks do not establish factual or code correctness. |
| Explicit context dependencies | Lab 2 supplies `[architect_task]` to the Coder and `[coder_task]` to QA. | [CrewAI tasks](https://docs.crewai.com/en/concepts/tasks). Task context makes prior output available; a live run would need additional evidence of rule adherence. |
| Least privilege and separation of duties | The Manager reviews, the Coder writes, and QA verifies through separate custom tool lists. | Selected concepts from AC-6 and AC-5 in [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final). Framework tool lists require process and credential isolation in a live factory. |
| Input validation | Reject malformed payloads at the contract boundary before the next role consumes them. | Conceptual mapping to NIST SI-10 in the same publication; schema validation covers only the declared checks. |
| Accessible complex diagrams | Both lab diagrams have short image descriptions, adjacent text equivalents, and labeled outcomes. SVG sources include a title and description. | [W3C WAI guidance for complex images](https://www.w3.org/WAI/tutorials/images/complex/). These features support accessibility; full WCAG conformance requires testing the complete delivery surface. |

## Transfer to the Software Factory

Continue through [05 · Software Factory Simulation](../../notebooks/05_live_software_factory.ipynb) and [06 · Local CI/CD](../../notebooks/06_local_cicd.ipynb). These integrated labs use pre-generated role outputs, simulated budget amounts, explicit human gates, and actual local files/Git operations. There are no API calls or API keys and actual API cost is $0.00. Open [the factory guide](../../extensions/live_software_factory.md), [architecture](live-software-factory.svg), and [Capstone ERD](capstone_factory_erd.md).

[Lab 1](../../notebooks/01_lab_pydantic.ipynb) · [Lab 2](../../notebooks/02_lab_crewai.ipynb) · [Lab 3](../../notebooks/03_lab_security.ipynb) · [Capstone](../../notebooks/04_capstone.ipynb) · [Factory](../../notebooks/05_live_software_factory.ipynb) · [CI/CD](../../notebooks/06_local_cicd.ipynb)
