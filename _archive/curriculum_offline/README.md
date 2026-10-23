# Managing Multi-Agent Teams

<img src="slides/assets/un_volunteers_iyv26.png" alt="UN Volunteers and IYV26" width="320">

**UN Volunteers · Two-day workshop**

Start with one accountable agent, then add helpers when the task needs them. Learn to build a useful working brief, choose suitable tools, and supervise multi-agent workflows through typed handoffs and bounded retries. The workshop combines procurement and HR simulations with a software team exercise, then a Development-to-Security Capstone.

**Required practical work:** one ungraded preflight, three labs, and one Capstone. The supplied activities run locally with deterministic fixtures and require no model-provider API key.

[Navigation dashboard](#navigation-dashboard) · [Learner paths](#learner-paths) · [Practical sequence](#required-practical-sequence) · [Lab diagrams](#lab-diagrams-and-navigation) · [Slide index](#main-deck-slide-index) · [Schedule](PLAYBOOK.md#two-day-schedule)

## Navigation dashboard

Choose your next activity. Open notebooks in JupyterLab to run them; use the exercise brief and diagram alongside each lab.

| Activity | Open | Exercise, diagram, or reference |
| --- | --- | --- |
| **Start the workshop** | [Setup](SETUP.md) → [00 · Preflight](notebooks/00_sandbox_preflight.ipynb) | [Main deck](slides/managing_multi_agent_teams_workshop_v16.pptx) · [Two-day schedule](PLAYBOOK.md#two-day-schedule) |
| **Day 1 · Lab 1: Typed contracts** | [Run Lab 1](notebooks/01_lab_pydantic.ipynb) | [Exercise 03](assignments/assignment_03_architectural_supervision.md) · [Contract-flow diagram](resources/diagrams/lab1-contract-flow.svg) |
| **Day 1 · Lab 2: Team oversight** | [Run Lab 2](notebooks/02_lab_crewai.ipynb) | [Exercise 04](assignments/assignment_04_code_auditing.md) · [Team-audit diagram](resources/diagrams/lab2-team-audit.svg) |
| **Day 2 · Lab 3: Manager oversight** | [Run Lab 3](notebooks/03_lab_security.ipynb) | [Exercise 06](assignments/assignment_06_code_validation.md) · [Control and cell map](COURSE_MAP.md#control-and-cell-map) |
| **Day 2 · Capstone** | [Run the Capstone](notebooks/04_capstone.ipynb) | [Implementation and ADR brief](assignments/ex5_capstone_virtual_software_company.md) |
| **Check evidence and submit** | [Submission checklist](PLAYBOOK.md#submission-checklist) | [Assessment](#runtime-and-assessment) · [Grader coverage](COURSE_MAP.md#what-the-graders-actually-check) |
| **Review diagrams and standards** | [Diagram and standards guide](resources/diagrams/README.md) | [Course map](COURSE_MAP.md) · [Curriculum mind map](slides/managing_multi_agent_teams_mindmap.md) |

The optional [Live Software Factory guide](extensions/live_software_factory.md#choose-your-next-step) connects the labs to GitHub intake, specialist reviews, budgets, and deployment gates. Open its [architecture diagram](resources/diagrams/live-software-factory.svg), [local bootstrap script](extensions/software_factory/setup-local-factory.sh), or [Fix the Broken Pipeline exercise](extensions/live_software_factory.md#exercise-fix-the-broken-pipeline). For offline release practice, use the [Mock CI/CD notebook](extensions/11_mock_cicd_pipeline.ipynb). These follow-up activities are ungraded; live services still need implementation.

## What to teach

Teach the **21-slide main deck, the scheduled discussions, and the five notebooks below**. You do not need to teach every file in this repository.

| Material | How to use it |
| --- | --- |
| Main deck and [PLAYBOOK.md](PLAYBOOK.md) | Present the concepts and follow the two-day schedule. |
| `notebooks/00` through `04` | Run preflight, Labs 1–3, then the Capstone. These are the complete required practical route. |
| Eight briefs in the [lecture map](#interactive-syllabus-nine-un-mandated-lectures), simulations, and design guide | Use alongside the relevant slides or notebooks. They support the same course; they are not eight extra labs. |
| [COURSE_MAP.md](COURSE_MAP.md) and `resources/` | Consult for edit locations, evidence limits, and reading. No need to teach every reference. |
| `instructor/`, `tests/`, `tools/`, and [DEVELOPMENT.md](DEVELOPMENT.md) | Instructor preparation, grading, and repository maintenance. |
| `extensions/` and `crewai_learning/` | Optional follow-up study. Skip for core course delivery. |
| `_archive/` | Historical material. Do not teach it as part of the current course. |

**One learner install:** `python -m pip install -r requirements.txt` in an activated Python 3.12 environment. Specialist dependencies are grouped under `requirements/` for optional work and maintenance.

For a class handout, instructors can build a compact learner ZIP with [the packaging command](DEVELOPMENT.md#build-the-learner-handout). It includes the current deck, required notebooks and briefs, and supporting reading; it excludes solutions, optional notebooks, archives, tests, and local environments.

## Start here

1. Review slides **1–8** in the [main deck](slides/managing_multi_agent_teams_workshop_v16.pptx) and discuss the [procurement and HR/RAG simulations](assignments/workshop_simulations.md).
2. Follow [Setup](SETUP.md), then run [00 · Sandbox preflight](notebooks/00_sandbox_preflight.ipynb) in JupyterLab.
3. Complete **Lab 1, Lab 2, Lab 3, then the Capstone** using the [practical sequence](#required-practical-sequence).
4. Review the [submission checklist](PLAYBOOK.md#submission-checklist) and prepare your evidence and architecture decision record (ADR).

Use **Python 3.12** and the course requirements in the setup guide. The initial installation normally needs internet; after installation, the required exercises run offline. To work locally, [download the repository ZIP](https://github.com/W4sP4nx2/Managing-Multi-Agent-Teams/archive/refs/heads/main.zip) or clone the repository.

## Learner paths

Choose the row that describes your next task. These routes use the same workshop requirements.

| Your situation | Start with | Continue to |
| --- | --- | --- |
| **First time here** | [Start here](#start-here), then deck slides 1–8 | [Setup](SETUP.md) and the [required practical sequence](#required-practical-sequence) |
| **Returning to a lab** | Your current notebook in the [sequence below](#required-practical-sequence) | Rerun its cells in order, inspect the grader and decision note, then open the next notebook |
| **Reviewing the concepts** | [Slide index](#main-deck-slide-index) and [simulation walkthroughs](assignments/workshop_simulations.md) | [Framework comparison](resources/framework_comparison.md) and [reading library](resources/curated_resource_library.md); this review does not replace assessed work |
| **Setup is blocking progress** | [Setup troubleshooting](SETUP.md#troubleshooting) and instructor support | Continue the simulations while resolving setup; if the environment prevents Capstone execution, use the [Paper ADR route](assignments/ex5_capstone_virtual_software_company.md) |
| **Ready to submit** | [Assessment](#runtime-and-assessment) and [submission checklist](PLAYBOOK.md#submission-checklist) | Deck slide 21 for takeaways and transfer |
| **Exploring CrewAI execution** | Complete [Lab 2](notebooks/02_lab_crewai.ipynb), then open the [three-agent advanced reference](crewai_learning/README.md) | Run the offline failure proof and use [Assignment 09](assignments/assignment_09_framework_comparison.md) for comparison; no new marks |
| **Practicing release gates** | After the Capstone, open the [Mock CI/CD Pipeline](extensions/11_mock_cicd_pipeline.ipynb) | Inspect the blocked feature, resubmit its corrected description, and record an explicit Manager decision; optional and ungraded |
| **Planning a live factory** | After the Capstone, open the [Live Software Factory guide](extensions/live_software_factory.md) | Bootstrap the local hook exercise, then use the live implementation checklist; optional and ungraded |

**Using the navigation:** deck links open the PowerPoint file; slide numbers tell you where to go inside it. The deck footer links to this slide index and its practice map on slide 8. Keep the complete repository folder together so relative links to notebooks and briefs resolve. A notebook preview shows the material; open the local `.ipynb` in JupyterLab to run it. Use your viewer's Back command or the course links in supporting pages to return here.

<a id="click-through-course-journey"></a>

## Required practical sequence

You supervise a Manager–Coder–QA team in the labs. In the Capstone, you coordinate a handoff between Development and a separate Security & Compliance Team.

| Order | Deck | Activity | Completion evidence | Next step |
| ---: | ---: | --- | --- | --- |
| 0 | 1–3, 8 | [Sandbox preflight](notebooks/00_sandbox_preflight.ipynb) · [setup](SETUP.md) | Dependency, deterministic-mode, and workspace checks pass. Ungraded. | Lab 1 |
| 1 | 9–10 | [Lab 1: Context Engineering](notebooks/01_lab_pydantic.ipynb) · [brief](assignments/assignment_03_architectural_supervision.md) | Valid fixture accepted, malformed fixtures rejected, grader **15/15**, reflection complete. | Lab 2 |
| 2 | 11–12 | [Lab 2: Multi-Agent Management](notebooks/02_lab_crewai.ipynb) · [brief](assignments/assignment_04_code_auditing.md) | Tools and context repaired, grader **15/15**, Manager audit and local QA inbox inspected, decision note complete. | Lab 3 |
| 3 | 14–16 | [Lab 3: Manager Oversight](notebooks/03_lab_security.ipynb) · [brief](assignments/assignment_06_code_validation.md) | Unsafe input blocked, retry bound checked, grader **15/15**, escalation and decision note recorded. | Capstone |
| 4 | 13, 18–19, 21 | [Capstone: Development to Security](notebooks/04_capstone.ipynb) · [brief and ADR](assignments/ex5_capstone_virtual_software_company.md) | Validated handoff, scoped Security tools, typed audit evidence, and ADR/defense; Paper ADR fallback as specified in the brief. | [Submit and reflect](PLAYBOOK.md#submission-checklist) |

Complete the marked edits, rerun dependent cells, and explain the evidence before moving on. The [course map](COURSE_MAP.md) identifies edit locations and what each grader checks. The [exercise index](assignments/index.md) connects required work to topic briefs and optional study. Brief numbers are competency labels; **notebook numbers define the practical order**.

### Lab diagrams and navigation

Each lab below opens with a diagram, a text description, and links to its observe, repair, verify, and reflection steps. Use the [diagram guide](resources/diagrams/README.md) to compare the controls and their standards references.

| Lab | Diagram | Exercise and runnable notebook |
| --- | --- | --- |
| 1 · Typed contracts | [Input → validation → accept or reject](resources/diagrams/lab1-contract-flow.svg) | [Exercise 03](assignments/assignment_03_architectural_supervision.md) · [Run Lab 1](notebooks/01_lab_pydantic.ipynb) |
| 2 · Team oversight | [Roles → context → audit → local QA inbox](resources/diagrams/lab2-team-audit.svg) | [Exercise 04](assignments/assignment_04_code_auditing.md) · [Run Lab 2](notebooks/02_lab_crewai.ipynb) |

Labs 2–3 and the Capstone use `inspect_state` for readable fixture evidence and `safe_validate` for expected schema rejections. Lab 2 closes with a five-minute **Blind Agent Debug** task. Tool docstrings state Action, Input, Output, and Warning. See [DX and AX in practice](COURSE_MAP.md#enterprise-dx-and-ax) for the controls and evidence limits.

[Return to learner paths](#learner-paths)

## Interactive syllabus: nine UN-mandated lectures

All nine lectures use the same five core notebooks and **eight lightweight assignment briefs** linked below. Assignment numbers are competency labels; notebook numbers set the practical order. Lecture 4 shares Lab 3 rather than adding another assignment.

| Lecture | Topic | Open the activity |
| ---: | --- | --- |
| 1 | Strategic prompt engineering and spec-driven work | [Assignment 01: write a checkable specification](assignments/assignment_01_strategic_prompt_engineering.md) |
| 2 | AI workspace, Theory of Mind, and role-aware context | [Assignment 02: workspace and role context](assignments/assignment_02_ai_workspace_and_role_context.md) · [Preflight](notebooks/00_sandbox_preflight.ipynb) |
| 3 | Context engineering: intent to typed contract | [Lab 1](notebooks/01_lab_pydantic.ipynb) · [Assignment 03](assignments/assignment_03_architectural_supervision.md) |
| 4 | Agentic mechanics: tools and bounded control flow | [Lab 3: inspect the input gate and repair loop](notebooks/03_lab_security.ipynb); preview here, complete after Lab 2 |
| 5 | Code auditing: roles, TeamLog, and handoffs | [Lab 2](notebooks/02_lab_crewai.ipynb) · [Assignment 04](assignments/assignment_04_code_auditing.md) |
| 6 | Code validation: tool gates, repair budgets, and evaluation | [Lab 3](notebooks/03_lab_security.ipynb) · [Assignment 06](assignments/assignment_06_code_validation.md) |
| 7 | Context engineering and access-list routing | [Assignment 07: the Obsidian Vault analogy](assignments/assignment_07_context_engineering_access_lists.md#the-obsidian-vault-analogy) · [Lab 2 context injection](notebooks/02_lab_crewai.ipynb) |
| 8 | Debugging and AI-first SDLC | [Assignment 08: diagnose a workflow trace](assignments/assignment_08_debugging_sdlc.md) |
| 9 | Development-to-Security delivery and design defense | [Capstone](notebooks/04_capstone.ipynb) · [Capstone brief and ADR](assignments/ex5_capstone_virtual_software_company.md) |

Use the [detailed syllabus](assignments/assignment_syllabus.md#course-topic-map), [two-day schedule](PLAYBOOK.md#two-day-schedule), and [curated resource library](resources/curated_resource_library.md) alongside this map. The optional [live LLM bonus](extensions/bonus_live_demo.ipynb) is reserved for the **end of Day 2**, after required work and defenses, and adds no marks.

## Main deck slide index

[Open the current 21-slide deck](slides/managing_multi_agent_teams_workshop_v16.pptx). The titles below match the presentation. Slides 6–7 are formative simulations; slides 17 and 20 support ungraded framework literacy. The [agent-building guide](assignments/agent_building_design_guide.md) connects the design discussions to a short, ungraded checkpoint at the end of each notebook. The assessed work remains three labs and the Capstone.

| Slide | Title in the deck | Learner action or supporting material |
| ---: | --- | --- |
| 1 | Agenda: Building a Managed Agent Team | Follow the [practical sequence](#required-practical-sequence) and read the [starting brief](assignments/agent_building_design_guide.md#start-with-one-agent) |
| 2 | Starting with One Agent | Define the first task and justify a helper using the [start-with-one-agent prompt](assignments/agent_building_design_guide.md#start-with-one-agent); discuss in [preflight](notebooks/00_sandbox_preflight.ipynb) |
| 3 | What Changes When Agents Take Action | Identify required controls with the [starting guide](assignments/agent_building_design_guide.md#start-with-one-agent) and [MAS foundations](assignments/multi_agent_systems_foundations.md) |
| 4 | Types of Multiagent Systems | Classify goals, coordination, and capabilities using the [simulation walkthroughs](assignments/workshop_simulations.md) |
| 5 | Applications of Multiagent Systems | Identify a coordination risk in a [workshop use case](assignments/workshop_simulations.md) |
| 6 | Simulation: Automating Procurement | Trace the [procurement recommendation](assignments/workshop_simulations.md#simulation-1-automating-a-procurement-recommendation) and human approval |
| 7 | Governed HR Virtual Assistant (Multi-Agent RAG) | Trace the [HR/RAG example](assignments/workshop_simulations.md#simulation-2-enhancing-an-hr-virtual-assistant-with-rag) and check its sources |
| 8 | Three Labs and One Capstone | Follow [setup](SETUP.md), run [preflight](notebooks/00_sandbox_preflight.ipynb), then use the linked practice steps |
| 9 | Context Engineering: The Working Brief | Prepare a [context packet](assignments/agent_building_design_guide.md#context-engineering) for the [Lab 1 checkpoint](notebooks/01_lab_pydantic.ipynb) |
| 10 | Context Engineering: Typed Contracts | Complete [Lab 1](notebooks/01_lab_pydantic.ipynb) and its [brief](assignments/assignment_03_architectural_supervision.md) |
| 11 | One Main Agent, Specialist Helpers | Define a [helper's task and permissions](assignments/agent_building_design_guide.md#one-main-agent-and-specialist-helpers) in the [Lab 2 checkpoint](notebooks/02_lab_crewai.ipynb) |
| 12 | Multi-Agent Management: Manager's Audit | Complete [Lab 2](notebooks/02_lab_crewai.ipynb) and its [brief](assignments/assignment_04_code_auditing.md) |
| 13 | Choosing the Least Costly Adequate Option | Choose a route and [human pairing point](assignments/agent_building_design_guide.md#choosing-a-capability-and-pairing-with-the-human) for the [Capstone checkpoint](notebooks/04_capstone.ipynb) |
| 14 | Stable Tools, Loaded When Needed | Review the [stable-tool design](assignments/agent_building_design_guide.md#stable-tools-and-loading-on-demand) in the [Lab 3 checkpoint](notebooks/03_lab_security.ipynb) |
| 15 | Visible State Changes and Useful Errors | Propose an [actionable error and state receipt](assignments/agent_building_design_guide.md#state-changes-and-actionable-errors) in the [Lab 3 checkpoint](notebooks/03_lab_security.ipynb) |
| 16 | Manager Oversight: Code Validation | Complete [Lab 3](notebooks/03_lab_security.ipynb) and its [brief](assignments/assignment_06_code_validation.md) |
| 17 | Multi-Agent Framework Comparison | Compare workflow needs using the [framework reference](resources/framework_comparison.md#four-core-frameworks) |
| 18 | Capstone: Managing Team Boundaries | Complete the [Capstone notebook](notebooks/04_capstone.ipynb) and [ADR](assignments/ex5_capstone_virtual_software_company.md) |
| 19 | Assessment: Visible Criteria and Evidence | Review [grading and submission](PLAYBOOK.md#assessment-and-gradebook) and [grader evidence limits](COURSE_MAP.md#what-the-graders-actually-check) |
| 20 | Broader Framework Ecosystem | Explore the [ecosystem reference](resources/framework_comparison.md#broader-ecosystem) |
| 21 | Managing Multi-Agent Teams | Review the [four-branch mind map](slides/managing_multi_agent_teams_mindmap.md), connect the [takeaways](assignments/agent_building_design_guide.md#takeaways-and-evidence) to evidence, then use the [submission checklist](PLAYBOOK.md#submission-checklist) |

[Return to learner paths](#learner-paths) · [Return to the practical sequence](#required-practical-sequence)

## Learning outcomes

A **multiagent system (MAS)** contains agents that interact with one another and an environment. Their goals may be shared, competing, or mixed. One coordinated team already qualifies as a MAS; the Capstone adds a boundary between teams.

By the end of the workshop, you should be able to:

- Start with one agent, explain when a helper is useful, and distinguish MAS goals, coordination, and role capabilities.
- Prepare relevant context, choose the least costly adequate capability, and identify a human decision point.
- Propose stable tool interfaces, actionable errors, and reviewable state changes as design exercises.
- Trace a workflow through role decisions, evidence, and human approval.
- Specify a typed handoff and reject malformed fixtures before another task consumes them.
- Audit role tools and context, then explain the Manager's handoff decision.
- Check input gates and bounded retries, and record escalation when repair fails.
- Defend an inter-team contract using observed evidence and an ADR.
- Compare framework patterns for a use case, as an ungraded reference objective.

The [syllabus](assignments/assignment_syllabus.md) maps nine competency topics into the [two-day schedule](PLAYBOOK.md#two-day-schedule). The [course map](COURSE_MAP.md) connects outcomes to notebook controls and assessment evidence.

<a id="north-star-the-governance-shell"></a>

## Governance controls

| Risk | Workshop control | Evidence to inspect |
| --- | --- | --- |
| Malformed handoffs | **Architectural supervision:** validate a strict Pydantic contract before passing an artifact onward. | Lab 1 accepts valid fixtures and rejects the supplied malformed fixtures. |
| Lost context | **Explicit team context:** record decisions in TeamLog and pass relevant rules to the Coder. | Lab 2 shows the declared context dependency and Manager audit decision. |
| Excessive tool authority | **Scoped tools and input validation:** separate role permissions and gate tool requests. | Labs 2–3 and the Capstone inspect permissions and reject unsafe fixture input. |
| Unbounded repair | **Bounded autonomy:** stop after three retries following the initial attempt, then record escalation. | Lab 3 shows a maximum of four calls, simulated fixture cost, and a local escalation record. |

TeamLog is ordinary Python data passed between tasks. “Theory of Mind” is a teaching analogy. Schemas validate declared constraints, context makes information available, and tool lists restrict exposed custom tools. These controls do not establish factual truth, guarantee that a model follows instructions, or provide process isolation. The checks demonstrate behavior for supplied fixtures; production use requires further evaluation.

## Runtime and assessment

The required path uses **Python 3.12, JupyterLab, Pydantic, and CrewAI configurations**. Lab 2 constructs a Crew without calling `kickoff()`. The Capstone runs local Python adapters and separately constructs two Crews. Keep `USE_LIVE_LLM = False` in all core notebooks. Provider calls are isolated in the separate [end-of-Day-2 bonus](extensions/bonus_live_demo.ipynb). See [Setup](SETUP.md) for installation and [the course map](COURSE_MAP.md#one-development-team-then-a-security-team) for evidence limits.

| Assessed work | Course marks |
| --- | ---: |
| Lab 1 | 20 |
| Lab 2 | 20 |
| Lab 3 | 20 |
| Capstone implementation | 20 |
| Capstone ADR and defense | 20 |
| **Total** | **100** |

Each lab grader reports **/15**, converted to course marks with `raw_score × 20 ÷ 15`. Keep the raw result and required reflection or management decision note. Procurement and HR/RAG discussions, framework reading, and the agent-building design checkpoints add no marks. The checkpoints propose desktop/video/cloud helpers, tool discovery, durable state, and user-interaction tools; the local notebooks do not implement or execute those capabilities.

A sound **Paper ADR** is an accepted Capstone pass route when the environment prevents execution. Marks follow the [Capstone rubric](assignments/ex5_capstone_virtual_software_company.md); this fallback does not replace the three labs. Use the [assessment guidance](PLAYBOOK.md#assessment-and-gradebook) and [submission checklist](PLAYBOOK.md#submission-checklist) for complete requirements.

[Return to learner paths](#learner-paths)

## Optional Mock CI/CD Pipeline

After the Capstone, open [11 · Mock CI/CD Pipeline](extensions/11_mock_cicd_pipeline.ipynb) in JupyterLab and run the cells in order. It uses standard Python and the existing Pydantic installation, runs offline, and adds no course marks or required notebook.

The three-feature batch follows `REQUESTED`, `IN_PROGRESS`, `QA_PASSED`, `SECURITY_APPROVED`, and `DEPLOYED`, with `BLOCKED` for a failed gate. Development/QA and Security apply separate local policy checks. A typed Manager decision for the current description and revision is required before the simulated deployment state. Missing approval leaves a cleared feature at `SECURITY_APPROVED`.

For **Unblock the Pipeline**, inspect why `FEAT-002` stops, set `replacement_description` to `"Refactor database schema safely"`, and rerun the repair cell. Resubmission starts a new revision and clears prior gate evidence. Inspect the new QA and Security results, then set `approve_repaired_feature = True` to record your simulated Manager decision and run the proof cell. A denial blocks deployment. Changing the description alone cannot reuse earlier approvals.

The batch runner processes features sequentially to illustrate independent work items. `DEPLOYED` is a local simulation state: the notebook creates no real software build, concurrent workers, database query, or production deployment. Its fixed-marker checks demonstrate policy gates rather than complete security scanning. See [optional extensions](extensions/README.md) for the full study route.

The optional [Live Software Factory walkthrough](extensions/live_software_factory.md) maps these controls to GitHub intake, specialist reviewers, worktrees, budgets, and deployment gates. It includes a runnable local **Fix the Broken Pipeline** hook exercise and identifies the services still needed for live agents and deployment. Use it for post-course work or an instructor walkthrough after the assessed activities.

## Course materials

| Location | Purpose |
| --- | --- |
| [Main deck](slides/managing_multi_agent_teams_workshop_v16.pptx) | Current 21-slide presentation; use this version throughout the workshop |
| [PLAYBOOK.md](PLAYBOOK.md) | Schedule, learning sequence, grading, and submission |
| [SETUP.md](SETUP.md) | Installation, offline preparation, and troubleshooting |
| [COURSE_MAP.md](COURSE_MAP.md) | Notebook edit locations, controls, and evidence limits |
| [Assignments](assignments/index.md) | Simulations, lab briefs, and Capstone instructions |
| [Agent-building guide](assignments/agent_building_design_guide.md) | Formative prompts for starting small, context, helper roles, capability choice, and tool design |
| [Notebook manifest](notebook_manifest.yml) | Required notebook order |
| [Resources](resources/README.md) | Reading library and framework comparisons |
| [Extensions](extensions/README.md) | Optional post-course study outside the workshop assessment |
| [Mock CI/CD Pipeline](extensions/11_mock_cicd_pipeline.ipynb) | Optional offline feature lifecycle, resubmission, and explicit Manager approval exercise |
| [CrewAI advanced reference](crewai_learning/README.md) | Optional Manager–Coder–QA notebook: strict task outputs, three-attempt bound, and typed escalation; no new marks |
| [Archive](_archive/README.md) | Historical materials outside the required learner route |

### Teaching and research foundations

The course adapts the Stanford Teaching Commons AI Teaching Guide through functional, ethical, rhetorical, and pedagogical AI-literacy activities. These lenses supplement the engineering controls. See the [teaching-design alignment](instructor/stanford_teaching_guide_alignment.md) for the source guide, learning activities, and local adaptations.

The [curated reading library](resources/curated_resource_library.md) covers Theory of Mind, TEAMLOG, TRINITY, Conductor, ChatDev, and Reflexion. These readings provide research context for coordination and feedback; the workshop controls are local design choices.

### Instructors and maintainers

[Teaching and delivery guide](instructor/course_manager_notebook_assignment_path.md) · [Grading resources](instructor/GRADING.md) · [Development and readiness checks](DEVELOPMENT.md)

[Return to start](#start-here) · [Learner paths](#learner-paths) · [Main deck slide index](#main-deck-slide-index)
