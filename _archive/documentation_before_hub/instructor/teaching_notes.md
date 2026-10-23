# Instructor Teaching Notes

Instructor preparation and delivery material is kept here. The learner route starts at the [README dashboard](../README.md), [course map](../COURSE_MAP.md), and [learner playbook](../PLAYBOOK.md).

Use the [notebook and assignment path](course_manager_notebook_assignment_path.md), [readiness checklist](course_delivery_readiness_checklist.md), [assessment compliance checklist](assessment_compliance_checklist.md), and [core solution guide](solutions/core_notebook_solution_guide.md) together. Preserve the TODOs in distributed learner notebooks.

The learner-facing approach adapts the [Stanford Teaching Commons AI Teaching Guide](stanford_teaching_guide_alignment.md). Review the [outcomes, four AI-literacy lenses, and policy draft](stanford_teaching_guide_alignment.md) before class; do not describe this local adaptation as Stanford endorsed.

## Facilitate the practice-and-feedback cycle

Use the same sequence in the slides, simulations, and notebook labs:

1. **Connect:** open with a short workplace or learner-relevant scenario. Invite several possible perspectives before narrowing to the course's fixed facts.
2. **Predict:** before revealing the simulation outcome or running a fixture, ask learners to write or discuss what might fail and what evidence they would expect.
3. **Practice:** give quiet think time first. Offer pair discussion as an option. The scaffold should include imports, fixture, code context, and grader; keep the learner's target control small and visible.
4. **Respond:** ask learners to read the rejection, trace, audit, or grader message as feedback. Give a hint before supplying an answer, then allow a revision.
5. **Explain:** ask “What did the check establish? What did it leave untested?” Accept a brief spoken explanation, a written sentence, or an annotated diagram for formative reflection.
6. **Transfer:** ask how the same decision changes when the input, authority, or stakeholder changes; collect the Capstone ADR as the summative reasoning artifact.

Frame a broken starter as a planned, low-stakes diagnostic case. Do not turn a visible failure into a public performance or use speed as a proxy for understanding. Give learners choice of working alone or with a partner, and use the Paper ADR route when the environment is a barrier. The graded code outcomes and rubric remain the same when the alternative route applies.

### Discussion prompts for the application slides

- **Procurement:** Before showing the recommendation in the walkthrough, ask which quote qualifies under all four rules, what evidence could change that choice, and which decision remains with a person.
- **HR/RAG:** Ask pairs to match each answer claim to a current, authorized snippet. Then ask what the assistant should do when the policy collection does not answer the question.
- **After a notebook grader:** Ask the learner to name one passed check, one boundary of the check, and one next test or review action.

## Facilitate the agent-building checkpoints

Use the [21-slide deck](../slides/managing_multi_agent_teams_workshop_v16.pptx) with the [design guide](../assignments/agent_building_design_guide.md). Keep each new prompt short and formative, using the Markdown checkpoint near the end of its notebook:

- **Preflight, slides 1–3 and 8:** ask for one task, one success criterion, and a reason a helper would be needed.
- **Lab 1, slides 9–10:** ask which rule, source, and output contract belong in the working brief, and what context should be omitted.
- **Lab 2, slides 11–12:** compare general, computer-use, video, and cloud coding helper designs with the actual Manager–Coder–QA configuration. Ask what the main agent must check on return.
- **Lab 3, slides 14–16:** keep tools stable across turns, explain loading only needed capabilities, and treat the description-plus-schema budget below 4,000 characters as a workshop convention. Ask for a recoverable error and a reviewable state receipt.
- **Capstone, slides 13, 18, and 21:** ask for the least costly adequate route and a decision needing human input through a dedicated user-interaction interface. Tie each takeaway to observed evidence or identify it as a proposed design.

The local notebooks do not execute desktop/video/cloud helpers, tool discovery, durable state storage, or user-interaction tools. The new prompts add no code edits, requirements, or marks. Preserve the existing grader and ADR criteria. A learner can answer aloud, in a short note, or with a small diagram.

## Day 1 opening: deterministic mode

> Before we write code, check the preflight notebook: `USE_LIVE_LLM = False` records our intended test mode. Engineers use mocks to check contracts and tool boundaries with predictable inputs, without spending money or relying on a live service. The five core notebooks make no provider calls. A live model is optional exploration in a separate bonus at the end of Day 2.

Each core notebook has its own `USE_LIVE_LLM = False` setting and contains no provider-call branch. Initial dependency installation needs internet or a prepared environment/package bundle. The readiness suite checks execution without provider credentials and with external networking blocked. Reserve [bonus_live_demo.ipynb](../extensions/bonus_live_demo.ipynb) for the end of Day 2 after required work and defenses.

## Why a native virtual environment?

> Docker is useful for packaging and deployment. This workshop uses a native Python virtual environment so class time focuses on contracts, role boundaries, verification, and bounded repair. Container deployment belongs to optional study. First-time package installation still needs internet or a prepared package bundle.

## Why separate Coder and QA roles?

> A separate QA role provides a distinct review step. The Coder proposes a typed patch; QA returns separate evidence. The course fixtures demonstrate the interface and permission pattern. They do not prove that a model is an independent or complete reviewer.

## Slide 17 script: universal patterns across frameworks

> The decision tree gives us a shortlist based on the dominant need. Clear task ownership points us toward CrewAI. Stateful branching and recovery point us toward LangGraph. Existing AutoGen applications give us conversation patterns to inspect. Document retrieval points us toward LlamaIndex. Python and .NET workflow integration gives us a reason to evaluate Microsoft Agent Framework. These are starting points, and capabilities overlap.
>
> The patterns we teach transfer across all of them. Pass explicit context and typed artifacts between roles. Give each tool only the authority it needs. Verify the result with evidence, bound retries and spending, and define when a human must approve or take over. A framework supplies abstractions. We still design and test those controls. CrewAI remains the only required framework in this workshop.

**Source note, checked 17 October 2026:** AutoGen's [GitHub metadata](https://api.github.com/repos/microsoft/autogen) reports `archived: false`, while its [README](https://github.com/microsoft/autogen#autogen) says Microsoft no longer maintains it and directs new users to [Microsoft Agent Framework](https://github.com/microsoft/agent-framework). Avoid claiming either active Microsoft development or a formal GitHub archive state from one signal alone. The [framework reference](../resources/framework_comparison.md#official-repository-and-name-check) records the official repositories for every framework on slides 17 and 20.

## Three classroom guardrails

1. **Provide the scaffold.** Keep imports, mocks, surrounding workflow, and grader intact. Learners repair only the marked control: field constraints, task context, role tools, input validation, or retry limits.
2. **Stop at green.** Once a lab reports `15/15`, move to the next activity. Retain the evidence and ask for the learner's explanation of its limits.
3. **Accept the Paper ADR route.** When execution is blocked by laptop, package, power, or connectivity problems, use the [print-ready ADR sheet](capstone_paper_adr_quick_sheet.md) and the stated /20 ADR rubric. Sound reasoning meets the Capstone pass condition; it does not automatically award full marks or create missing implementation evidence.

## Preparation and distribution

- Rehearse [SETUP.md](../SETUP.md) in Python 3.12.
- Make private rehearsal copies of notebooks and apply the [documented repairs](solutions/core_notebook_solution_guide.md).
- Compare broken, partial, and repaired grader results. Inspect the supplied demonstration cells separately from the scores.
- Rehearse the local Development-to-Security pipeline. Keep any provider-backed rehearsal in the separate bonus notebook.
- Run the current repository suite and record the actual environment and result in the [compliance checklist](assessment_compliance_checklist.md).
- Clear outputs and execution counts in distributed notebooks; preserve learner TODOs.
- Prepare a repository ZIP, a suitable local package bundle if needed, the ADR sheet, and the [score tracker](assessment_score_tracker.xlsx).

## Grading and feedback

1. Collect the three lab notebooks and Capstone evidence or Paper ADR.
2. Record each raw lab score /15; convert it to /20 with `raw_score × 20 ÷ 15`.
3. Record Capstone implementation /20 and ADR/defense /20 separately, including any fallback route.
4. Check the /100 total and give one concrete strength plus one practical next step that refers to observable evidence.

## Course maintenance and handover

1. Read the [course map](../COURSE_MAP.md), [learner schedule](delivery_schedule.md), and [syllabus](../assignments/assignment_syllabus.md). The [README](../README.md#main-deck-slide-index) lists current slide files and topics.
2. Confirm the five-notebook sequence and required packages using [SETUP.md](../SETUP.md) and the [manifest](../notebook_manifest.yml).
3. Rehearse broken, partial, and repaired copies with the [solution guide](solutions/core_notebook_solution_guide.md); a historical passing run does not verify a changed notebook.
4. Distinguish local fixtures from actual Crew execution. Lab 2 constructs configurations; Capstone cell 7 runs Python adapters, and cell 13 constructs two Crews. Only the separate optional bonus executes provider-backed CrewAI tasks.
5. After notebook changes, update cell IDs/numbers, manifest, solution guide, assessment descriptions, and slide links together.
6. Keep optional extensions and archived material outside the required learner path. Put teaching scripts and solution navigation in `instructor/`, not learner pages or projected slides.

## Optional-track delivery notes

These notes support post-course study; they add no required labs or marks.

### module10_hr_governance.md

Start with the naive path: raw resume output goes to evaluation, and `promote` goes straight to payroll. Then introduce the governance interventions: PII quarantine, bias-safe handoff, and human approval. End by showing the production reality: HR agents can assist, but policy and humans retain authority over sensitive data and irreversible actions.

### module11_marketing_orchestration.md

Start with the naive path: every task goes to the expensive model, and social posts publish immediately. Then introduce the interventions: cost-aware routing, budget preflight, brand-safety scanning, governed publish tools, and bounded repair. End with the production reality: marketing agents can scale creativity only when routing, spend, and brand policy are first-class system components.

### module12_advanced_orchestration.md

Teach this after NB6 and NB9. Be explicit:

"The Capstone shows a pre-written rule-based cost-aware router. NB6 and NB9 are optional extensions for learners who want to study more routing and workflow concepts. The required workshop does not train an orchestration model."

