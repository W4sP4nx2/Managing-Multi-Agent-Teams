# Two-Day Course Delivery Readiness Checklist

Use this checklist with the canonical [course map](../COURSE_MAP.md), [Playbook](../PLAYBOOK.md), and [notebook manifest](../notebook_manifest.yml). The required path is three labs that construct a Development Team pattern, followed by a Capstone adding a Security & Compliance Team. Required execution uses local fixtures; CrewAI configurations are constructed without running live teams.

## Day 1 opening script

> Welcome. Before we write code, find the **Offline Deterministic Mode** cell in the preflight notebook. It sets `USE_LIVE_LLM = False`, so we verify roles, handoffs, schemas, and security gates with repeatable local inputs. The mock failures are fixtures, like stubs used to exercise software without calling production services. Every core notebook uses the same local mode. Optional live exploration is in a separate bonus at the end of Day 2; the local adversarial fixtures provide repeatable gate evidence.

All five core notebooks set `USE_LIVE_LLM = False` and contain no live-provider call path. The separate [bonus](../extensions/bonus_live_demo.ipynb) is optional and ungraded, and belongs only at the end of Day 2.

## Go/no-go checklist

1. **Clean install:** Remove the rehearsal `.venv`, follow the four commands in [SETUP.md](../SETUP.md) in Python 3.12, and record elapsed time and errors on a representative learner machine. The release target is a clean install in under five minutes; verify that target rather than assuming it. First-time package installation needs internet or a prepared package bundle.
2. **Automated gate:** Install `requirements/maintenance.txt` in the maintainer environment and run `python tools/check_readiness.py`. It executes preflight, broken/partial/repaired lab copies, and the Capstone through real Jupyter kernels without provider credentials. Inspect the generated summary and JUnit results. All required checks must pass without skips.
3. **Capstone handoff:** Keep `USE_LIVE_LLM = False`; confirm the local Development Team produces a validated `DevDeliverable`, the Security Team receives it automatically, and the notebook records a `SecurityAuditResult`.
4. **Grader sabotage:** In each lab, confirm the broken starter gives `0/15`, a partial repair earns its documented partial score, and a full repair gives `15/15`. Current reproducible examples: Lab 1 `0/5/15`, Lab 2 `0/5/10/15`, and Lab 3 `0/7/8/15` depending on which control is fixed.
5. **Output wipe:** Clear outputs and execution counts in distributed notebooks before saving the handout or committing it.

**Live-call note:** Open only [bonus_live_demo.ipynb](../extensions/bonus_live_demo.ipynb) for a provider-backed demonstration, after the Day 2 defenses and wrap-up. A provider-backed model is not guaranteed to hallucinate on cue, and structured-output adapters may repair or retry malformed responses. The deterministic adversarial fixture is the repeatable gate demonstration. Live calls may use paid quota.

Keep a repository ZIP or prepared environment/wheel bundle ready for low-connectivity classrooms. Record the gate's actual result in the [compliance checklist](assessment_compliance_checklist.md). The [development workflow](../DEVELOPMENT.md) defines the early unit-test cycle and CI checks. Print or open the Capstone ADR rubric and score tracker.

## Two-day delivery

| Day | Session | Evidence to look for |
| --- | --- | --- |
| Day 1 | Lecture: roles, shared context, Theory of Mind, and TeamLog | Learners explain which Architect rules the Coder needs and how task context makes them available. Availability does not prove obedience. |
| Day 1 | Lab 1: Pydantic contract | Grader reaches `15/15`; invalid data is rejected and valid data passes. |
| Day 1 | Lab 2: CrewAI Development Team | Structural grader checks Manager approval/delegation without writing and the Architect-task dependency in Coder context. Inspect supplied Coder/QA tool lists and the locally validated `CodePatch` separately; no TeamLog read event or QA run is executed. |
| Day 2 | Lecture: verification, bounded repair, and cost-aware routing | Learners explain the pre-written Capstone policy: low/medium complexity uses Fast, while high complexity uses Expert. Costs are illustrative; the router is not graded. |
| Day 2 | Lab 3: security and bounded repair | SQL-like input is blocked before the simulated tool; retries stop at three and escalate. |
| Day 2 | Capstone: Development Team → Security Team | Pydantic validates before the local Security adapter starts; separate Security tools and a typed audit result are recorded. The approval flag is an audit outcome, not a deployment/release action. Learners inspect the pre-written, ungraded routing example. |
| Day 2 | Defense or Paper ADR | Learner explains contract, permissions, risk, evidence, and next step. |
| End of Day 2 · optional | Separate live LLM bonus | Required submissions and grading are already complete. Run only the bonus notebook if provider/key setup, connectivity, and time permit. |

## Instructor guardrails

1. **Fill in the blank:** keep the workflow scaffolded; learners repair only the target control.
2. **Stop at green:** once a grader reports `15/15`, move on.
3. **Paper ADR fallback:** if execution is blocked, assess the one-page ADR using the same 20-point ADR rubric. A sound ADR is a Capstone pass route; it does not automatically receive full marks.

## Grade and submissions

- Collect the three lab notebooks and Capstone code evidence or Paper ADR.
- Record each raw lab score out of 15; the tracker converts each proportionally to 20 course marks.
- Grade Capstone code evidence /20 and the ADR/defense /20.
- Confirm the total is out of 100 and the score band is applied consistently.
- Give one concrete strength and one actionable next step.

## Readiness record

Record current repository-test counts and actual setup/deterministic-mode rehearsal results in [assessment_compliance_checklist.md](assessment_compliance_checklist.md). Distinguish checks that were run from steps that are only documented.
