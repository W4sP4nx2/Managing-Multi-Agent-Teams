# Teaching-design alignment: Stanford Teaching Commons

**Purpose:** document how this workshop adapts the Stanford Teaching Commons' AI teaching and course-design guidance to a short, technical course on multi-agent systems. This is an independent local adaptation, not a Stanford-reviewed or Stanford-endorsed curriculum. Source pages checked 17 October 2026.

## Design commitments

The guide recommends intentional, course-specific choices about AI, attention to student success and workload, meaningful assignments with clear learning objectives, and human-centered AI literacy. This workshop uses those ideas to shape when learners see an answer, what they must decide, and what counts as evidence.

| Stanford AI-literacy lens | Workshop connection | Learner evidence |
| --- | --- | --- |
| **Functional** — how AI works and where it is limited | Define a multiagent system; distinguish a model response from orchestration, validation, and tool execution. | Trace roles and handoffs; explain what the deterministic fixture does and does not simulate. |
| **Ethical** — reliability, privacy, access, bias, and responsibility | Examine unsupported claims, source access, least privilege, simulated cost, and human approval. | Reject an unsafe or unsupported path; name a remaining risk and responsible decision-maker. |
| **Rhetorical** — use and critique human- and AI-generated language | Turn a natural-language request into testable requirements; evaluate whether a claim is supported by the requested evidence. | Revise a specification and justify which evidence supports or fails to support an output. |
| **Pedagogical** — use AI in ways that support learning | Keep required work deterministic and scaffolded; use prediction, practice, feedback, revision, and reflection before transfer. | Explain which control they changed, what feedback showed, and what they can transfer to a new case. |

The literacy domains overlap. They supplement the workshop's four engineering controls; they do not replace the technical pillar map.

## Learning cycle used in the workshop

Use the same short cycle in the simulations and notebooks:

1. **Connect:** start from a workplace scenario or learner experience; ask an open question before showing the model answer.
2. **Predict:** ask learners to identify the risk and expected evidence before they run a fixture.
3. **Practice:** give a bounded repair task with imports, context, and a visible starting state already supplied.
4. **Respond:** use the cell output, instructor hint, peer explanation, or grader message as formative feedback; invite a revision.
5. **Explain:** have the learner cite the observed evidence and state its limit. A green score alone is not the explanation.
6. **Transfer:** revisit the decision in the Capstone ADR and name a test, safeguard, or human decision needed in a new setting.

Treat deliberate starter failures as low-stakes cases for diagnosis. Do not grade speed, publicly rank learners by errors, or equate an uncaught exception with lack of ability. Offer solo or paired reasoning, a hint ladder, and an equivalent Paper ADR path when execution is inaccessible.

## Observable course outcomes

| Given… | Learners will be able to… | Evidence |
| --- | --- | --- |
| A short synthetic workflow | Identify its agents, environment, interactions, and one coordination risk. | Opening discussion or annotated role map. |
| A weak schema and valid/invalid fixtures | Repair a Pydantic contract that accepts the valid record and rejects both supplied defects. | Lab 1 grader and a brief explanation of one untested property. |
| A starter team configuration and audit trace | Repair Manager permissions and Coder context, then decide whether a typed proposal may enter the local QA inbox. | Lab 2 grader, `PASS_TO_QA`/`BLOCK` evidence, and a management note. |
| An unsafe tool request and an always-failing mock | Configure the input boundary and a three-retry ceiling; explain the four-call maximum and escalation result. | Lab 3 grader and observed call/cost/escalation record. |
| A Development-to-Security handoff | Gate the artifact, separate scan from approval, and defend one unresolved risk with a next-step recommendation. | Capstone evidence and the 20-point ADR. |

The outcomes use observable actions and named conditions. The rubric distinguishes structural validity from truth, configured context from proven model behavior, and local tool lists from operating-system isolation.

## Practice, feedback, and assessment

| Stage | Role in learning | Marks |
| --- | --- | ---: |
| Procurement and HR/RAG simulations | Low-stakes, open-ended discussion; learners inspect evidence and propose a decision before the facilitator reveals the worked example. | Formative only |
| Labs 1–3 | Scaffolded repair, deterministic re-run, grader feedback, and a short decision/evidence note. | 15 raw points per lab, scaled to 20 each |
| Capstone | Integrate the controls at a team boundary; inspect adversarial fixtures and explain residual risk. | Code /20 and ADR /20 |
| Paper ADR option | Preserve the reasoning outcome when a learner cannot run the environment; assess using the same stated ADR rubric. | ADR /20, with no implied code evidence |

Keep the criteria visible before learners begin. Give at least one chance to interpret feedback and revise before moving on. Accept a short written explanation, spoken explanation, or annotated workflow sketch for formative reflection, while retaining the same required code and rubric evidence for graded implementation.

## Suggested learner-facing AI-use policy

Adapt and publish a course policy that matches local institutional rules before delivery. A starting draft is:

> The required notebooks use local deterministic fixtures and do not need a model-provider account. You may use an AI assistant as a tutor to clarify concepts or interpret an error if your instructor permits it. Do not ask it to complete a graded TODO for you or submit generated code you cannot explain. Disclose substantial assistance, verify every suggestion against the notebook evidence, and never submit personal, confidential, or restricted data to an external service. Ask the instructor when a use is unclear.

The policy is meant to protect learner agency and make expectations predictable, not to imply that the local Stanford or another institution's policies apply here. Provide documentation, local examples, instructor help, and the Paper ADR path so access to a paid tool is never required.

## Where the design is implemented

- [README](../README.md): learner-facing AI-literacy frame, outcomes, and direct paths.
- [Workshop syllabus](../assignments/assignment_syllabus.md): observable outcomes, session sequence, and assessment alignment.
- [Teaching notes](teaching_notes.md): openers, facilitation moves, feedback, and distribution guidance.
- [Simulation walkthroughs](../assignments/workshop_simulations.md): predict/compare/discuss before revealing a deterministic decision.
- [Notebook manifest](../notebook_manifest.yml) and [Course Map](../COURSE_MAP.md): skill order, learner actions, and evidence.
- [21-slide main deck](../slides/managing_multi_agent_teams_workshop_v16.pptx): open questions, visible learner actions, agent-building design checkpoints, and end-of-course takeaways.
- [Notebook 1](../notebooks/01_lab_pydantic.ipynb), [Notebook 2](../notebooks/02_lab_crewai.ipynb), [Notebook 3](../notebooks/03_lab_security.ipynb), and [Capstone](../notebooks/04_capstone.ipynb): prediction, scaffolded repair, feedback, and reflection in Markdown instructions; code cells and graders remain the course fixtures.

## References

- [Artificial Intelligence Teaching Guide](https://teachingcommons.stanford.edu/teaching-guides/artificial-intelligence-teaching-guide), Stanford Teaching Commons.
- [Understanding AI Literacy](https://teachingcommons.stanford.edu/teaching-guides/artificial-intelligence-teaching-guide/understanding-ai-literacy), Stanford Teaching Commons.
- [Exploring the Pedagogical Uses of AI Chatbots](https://teachingcommons.stanford.edu/teaching-guides/artificial-intelligence-teaching-guide/exploring-pedagogical-uses-ai-chatbots), Stanford Teaching Commons.
- [Analyzing the Implications of AI for Your Course](https://teachingcommons.stanford.edu/teaching-guides/artificial-intelligence-teaching-guide/analyzing-implications-ai-your-course), Stanford Teaching Commons.
- [Integrating AI into Assignments](https://teachingcommons.stanford.edu/teaching-guides/artificial-intelligence-teaching-guide/integrating-ai-assignments), Stanford Teaching Commons.
- [Creating Learning Outcomes](https://teachingcommons.stanford.edu/teaching-guides/foundations-course-design/course-planning/creating-learning-outcomes), Stanford Teaching Commons.
- [Formative Assessment and Feedback](https://teachingcommons.stanford.edu/teaching-guides/foundations-course-design/feedback-and-assessment/formative-assessment-and-feedback) and [Increasing Student Engagement](https://teachingcommons.stanford.edu/teaching-guides/foundations-course-design/learning-activities/increasing-student-engagement), Stanford Teaching Commons.
