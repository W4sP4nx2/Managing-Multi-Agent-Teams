# Managing Multi-Agent Teams

<img src="slides/assets/un_volunteers_iyv26.png" alt="UN Volunteers and IYV26" width="320">

**UN Volunteers · Course**

Build a governed software team, then operate a deterministic Software Factory that creates a minimalist travel website. Begin with repeatable local fixtures, carry the same typed contracts into fixture-driven roles, and inspect simulated cost, security, review, Git, and publication evidence before approving the result.

[Navigation dashboard](#navigation-dashboard) · [Setup](SETUP.md) · [Learner playbook](PLAYBOOK.md) · [Diagrams and standards](resources/diagrams/README.md) · [Course map](COURSE_MAP.md) · [Slide index](#main-deck-slide-index)

## Navigation dashboard

Open notebooks in JupyterLab to run them. Follow the sequence through the factory and local CI/CD labs. The factory uses pre-generated outputs, paced terminal collaboration, real local files, and explicit human gates. It makes no API calls, needs no API keys, and has an actual API cost of $0.00.

| Stage | Run or read | Exercise, diagram, or evidence |
| --- | --- | --- |
| **Start** | [Setup](SETUP.md) · [00 · Preflight](notebooks/00_sandbox_preflight.ipynb) | [Main deck](slides/managing_multi_agent_teams_workshop_v16.pptx) · [Playbook](PLAYBOOK.md) |
| **Lab 1 · Typed contracts** | [01 · Run Lab 1](notebooks/01_lab_pydantic.ipynb) | [Exercise 03](assignments/assignment_03_architectural_supervision.md) · [Contract diagram](resources/diagrams/lab1-contract-flow.svg) |
| **Lab 2 · Team oversight** | [02 · Run Lab 2](notebooks/02_lab_crewai.ipynb) | [Exercise 04](assignments/assignment_04_code_auditing.md) · [Skill Transparency Matrix](assignments/assignment_04_code_auditing.md#skill-transparency--least-privilege) · [Team diagram](resources/diagrams/lab2-team-audit.svg) |
| **Lab 3 · Manager oversight** | [03 · Run Lab 3](notebooks/03_lab_security.ipynb) | [Exercise 06](assignments/assignment_06_code_validation.md) · [Control and cell map](COURSE_MAP.md#control-and-cell-map) |
| **Capstone · Development to Security** | [04 · Run the Capstone](notebooks/04_capstone.ipynb) | [Travel-site brief and ADR](assignments/ex5_capstone_virtual_software_company.md) · [Capstone ERD](resources/diagrams/capstone_factory_erd.md) · [ERD image](resources/diagrams/capstone_factory_erd.svg) |
| **Factory lab · Simulated collaboration** | [05 · Software Factory Simulation](notebooks/05_live_software_factory.ipynb) | [Factory execution guide](extensions/live_software_factory.md) · [Architecture](resources/diagrams/live-software-factory.svg) · [Simulation profile](software_factory/simulation_config.json) |
| **CI/CD lab · Local release gates** | [06 · Local CI/CD](notebooks/06_local_cicd.ipynb) | [Broken-pipeline exercise](extensions/live_software_factory.md#exercise-fix-the-broken-pipeline) · [Local bootstrap](extensions/software_factory/setup-local-factory.sh) |
| **CrewAI learning bridge** | [Run real CrewAI with local fixtures](crewai_learning/01_Bridge_Sequential_Crew.ipynb) | [CrewAI guide](crewai_learning/README.md) · [Setup and evidence](crewai_learning/SETUP_AND_LEARNING_EXPERIENCE.md) |
| **Review and submit** | [Submission checklist](PLAYBOOK.md#submission-checklist) | [Assessment](#runtime-and-assessment) · [Diagram and standards guide](resources/diagrams/README.md) |

## Start here

1. Read the [playbook](PLAYBOOK.md) and complete [setup](SETUP.md).
2. Run notebook 00, then Labs 1–3. Predict each failure, repair the marked control, and retain the evidence.
3. Complete the Capstone contract and ADR, then carry the travel-site brief into notebooks 05 and 06.
4. Run `python orchestrator.py --security-demo` and `python orchestrator.py --check-only` before the interactive simulation.
5. Run `python live_simulation_orchestrator.py` for paced collaboration and interactive approvals. Review the [simulation setup](SETUP.md#simulation-profile-and-budget) before approving.

After explicit final human approval, the factory publishes a local `index.html`. Open it with `open index.html` on macOS, or use your browser's file-open command. Local publication creates no remote deployment, GitHub branch protection, or hosted endpoint.

A [pre-generated reference preview](index.html) is included for immediate inspection. It matches the checked-in travel fixture and carries no human approval or release receipt; use the interactive run's evidence to establish a new approved publication.

## Learner paths

| Your next task | Open | Continue with |
| --- | --- | --- |
| First run | [Setup](SETUP.md) | [Practical sequence](#required-practical-sequence) |
| Return to an exercise | [Dashboard](#navigation-dashboard) | Rerun dependent cells and inspect evidence |
| Audit a role's tools | [Lab 2 skill matrix](assignments/assignment_04_code_auditing.md#skill-transparency--least-privilege) | Compare actual tools with the allowlist, repair the Manager, then rerun the matrix before configuring tasks |
| Trace a diagram to a control | [Diagrams and standards](resources/diagrams/README.md#standards-and-implementation-references) | Connect the contract and role boundaries to the evidence each lab produces |
| Understand role assignment | [Illustrative role/model profile](extensions/live_software_factory.md#role-model-and-cost-control) | Inspect [simulation_config.json](software_factory/simulation_config.json) and the simulated budget before approving |
| Investigate a block | [Factory guide](extensions/live_software_factory.md) | Identify the failed gate, candidate revision, evidence, and next owner |
| Review CrewAI mechanics | [CrewAI learning](crewai_learning/README.md) | Distinguish real Crew execution from pre-generated role presentation |
| Prepare submission | [Checklist](PLAYBOOK.md#submission-checklist) | Explain both successful controls and remaining risks |

<a id="click-through-course-journey"></a>

## Required practical sequence

| Order | Activity | Completion evidence |
| ---: | --- | --- |
| 0 | [Preflight](notebooks/00_sandbox_preflight.ipynb) | Environment and deterministic-mode checks |
| 1 | [Typed contracts](notebooks/01_lab_pydantic.ipynb) | Valid fixture accepted, invalid fixtures rejected, grader 15/15 |
| 2 | [Team oversight](notebooks/02_lab_crewai.ipynb) | Scoped tools/context, Manager audit, local QA inbox, grader 15/15 |
| 3 | [Manager oversight](notebooks/03_lab_security.ipynb) | Unsafe input blocked, bounded attempts, escalation, grader 15/15 |
| 4 | [Capstone](notebooks/04_capstone.ipynb) | Typed Development-to-Security gate, scoped tools, code /20, ADR /20 |
| 5 | [Software Factory](notebooks/05_live_software_factory.ipynb) | Malicious request blocks, simulation profile, simulated budget and per-stage approval evidence, candidate Git revision |
| 6 | [Local CI/CD](notebooks/06_local_cicd.ipynb) | Clean candidate passes, missing/stale evidence blocks, publication requires final human approval |

The factory and CI/CD are integrated course labs. Simulation and replay both use deterministic local fixtures. There is no live provider mode. The normal command adds presentation delays; automated checks use zero delay. Existing assessed code criteria retain the /100 rubric. Factory and CI/CD receipts extend the Capstone evidence and reasoning without adding invented grader points.

### Lab diagrams and navigation

Lab 1 and Lab 2 open with diagrams and observe, repair, verify, and reflection links. Open the [Lab 1 contract flow](resources/diagrams/README.md#lab-1-contract-before-handoff) or [Lab 2 role and audit flow](resources/diagrams/README.md#lab-2-roles-context-and-audit) for a diagram with a text explanation. The [standards guide](resources/diagrams/README.md#standards-and-implementation-references) maps each control to its reference and implementation limits.

In Lab 2, run the **Skill Transparency Matrix** immediately after agent definitions and before task configuration. Inspect the actual tools and their Action, Input, Output, and Warning metadata, repair the Manager's permissions, then rerun the matrix. See the [exercise instructions](assignments/assignment_04_code_auditing.md#skill-transparency--least-privilege).

The [Capstone ERD](resources/diagrams/capstone_factory_erd.md) connects factory records with the proposed travel domain. Travel entities describe a future service; the generated site is static and does not implement bookings or a customer database.

## Interactive syllabus: nine UN-mandated lectures

| Topic | Practice |
| ---: | --- |
| 1 · Strategic prompt engineering | [Checkable specification](assignments/assignment_01_strategic_prompt_engineering.md) |
| 2 · Workspace and role context | [Role-aware workspace](assignments/assignment_02_ai_workspace_and_role_context.md) |
| 3 · Typed context contracts | [Lab 1](notebooks/01_lab_pydantic.ipynb) |
| 4 · Tools and bounded control flow | [Lab 3](notebooks/03_lab_security.ipynb) |
| 5 · Code auditing and ownership | [Lab 2](notebooks/02_lab_crewai.ipynb) |
| 6 · Validation and evaluation | [Lab 3](notebooks/03_lab_security.ipynb) · [Factory security](notebooks/05_live_software_factory.ipynb) |
| 7 · Context and access lists | [Authorized context selection](assignments/assignment_07_context_engineering_access_lists.md) |
| 8 · Debugging and SDLC | [Trace diagnosis](assignments/assignment_08_debugging_sdlc.md) · [Local CI/CD](notebooks/06_local_cicd.ipynb) |
| 9 · Managed software delivery | [Capstone](assignments/ex5_capstone_virtual_software_company.md) · [Software Factory](extensions/live_software_factory.md) |

Use the [detailed syllabus](assignments/assignment_syllabus.md#course-topic-map), [exercise index](assignments/index.md), and [reading library](resources/curated_resource_library.md). Earlier advanced assignments and superseded decks are retained in [_archive](_archive/README.md).

## Main deck slide index

[Open the main deck](slides/managing_multi_agent_teams_workshop_v16.pptx). The historical filename remains stable for existing links. Titles below match the current 26-slide presentation.

| Slide | Title | Related activity |
| ---: | --- | --- |
| 1 | Agenda: Building a Managed Agent Team | [Course sequence](#required-practical-sequence) |
| 2 | Starting with One Agent | [Design guide](assignments/agent_building_design_guide.md) |
| 3 | What Changes When Agents Take Action | [Governance controls](PLAYBOOK.md#core-course-focus-managed-team-delivery) |
| 4 | Types of Multiagent Systems | [Foundations](assignments/multi_agent_systems_foundations.md) |
| 5 | Applications of Multiagent Systems | [Simulations](assignments/workshop_simulations.md) |
| 6 | Simulation: Automating Procurement | [Procurement exercise](assignments/workshop_simulations.md) |
| 7 | Governed HR Virtual Assistant (Multi-Agent RAG) | [HR exercise](assignments/workshop_simulations.md) |
| 8 | Course Practice and Evidence | [Seven-notebook route](#required-practical-sequence) |
| 9 | Context Engineering: The Working Brief | [Lab 1](notebooks/01_lab_pydantic.ipynb) |
| 10 | Context Engineering: Typed Contracts | [Lab 1](notebooks/01_lab_pydantic.ipynb) |
| 11 | One Main Agent, Specialist Helpers | [Lab 2](notebooks/02_lab_crewai.ipynb) |
| 12 | Multi-Agent Management: Manager's Audit | [Lab 2](notebooks/02_lab_crewai.ipynb) · [Skill matrix](assignments/assignment_04_code_auditing.md#skill-transparency--least-privilege) |
| 13 | Choosing the Least Costly Adequate Option | [Simulation profile](software_factory/simulation_config.json) |
| 14 | Stable Tools, Loaded When Needed | [Lab 3](notebooks/03_lab_security.ipynb) |
| 15 | Visible State Changes and Useful Errors | [Evidence map](COURSE_MAP.md) |
| 16 | Manager Oversight: Code Validation | [Lab 3](notebooks/03_lab_security.ipynb) |
| 17 | Multi-Agent Framework Comparison | [Framework comparison](resources/framework_comparison.md) |
| 18 | Capstone: Managing Team Boundaries | [Capstone brief](assignments/ex5_capstone_virtual_software_company.md) |
| 19 | Assessment: Visible Criteria and Evidence | [Assessment](PLAYBOOK.md#assessment-and-gradebook) |
| 20 | Broader Framework Ecosystem | [Framework reference](resources/framework_comparison.md) |
| 21 | Managing Multi-Agent Teams | [Mind map](slides/managing_multi_agent_teams_mindmap.md) |
| 22 | Live Software Factory | [Factory lab](notebooks/05_live_software_factory.ipynb) |
| 23 | Role Labels and Simulated Cost | [Profile and simulated budget](SETUP.md#simulation-profile-and-budget) |
| 24 | Human Approval and Security Blocks | [Security demonstration](extensions/live_software_factory.md#live-demo-execution) |
| 25 | Travel Site and Factory Data | [Capstone ERD](resources/diagrams/capstone_factory_erd.md) |
| 26 | Local CI/CD and Release Evidence | [CI/CD lab](notebooks/06_local_cicd.ipynb) |

## Learning outcomes

By the end of the course you can specify typed handoffs, scope role tools, bound retries, explain illustrative model labels for each role, check a simulated allowance and record completed work, and explain which human decision authorizes each next action. You can reject a malicious feature, connect evidence to a Git revision, and distinguish local publication from a remote deployment.

## North star: the Governance Shell

| Failure | Control | Evidence |
| --- | --- | --- |
| Malformed handoff | Strict Pydantic validation | Accepted/rejected fixtures |
| Forgotten rules | Explicit approved context | Task context and Manager audit |
| Excessive authority | Role-specific tools and input gates | Permission checks and blocked unsafe inputs |
| Runaway cost | Attempt limits and simulated budget checks | Simulation ledger and rejected over-budget step |
| Unreviewed release | Human gates bound to the candidate | Decisions, review reports, Git revision, publication receipt |

## Runtime and assessment

Python 3.12, JupyterLab, CrewAI configurations, and Pydantic support the foundations. The CrewAI learning bridge executes actual Crew tasks with local fixture LLMs. The factory harness validates pre-generated role outputs with Pydantic. GPT-4, Claude 3.5, GPT-4 Turbo, GPT-4 Vision, and GPT-3.5 are illustrative labels from the scenario. No engine runs behind these labels. Simulated thinking is a presentation delay and actual API cost stays $0.00.

Three lab raw scores (/15 each) scale to /20 each. Capstone implementation contributes /20 and ADR/defense /20, for 100 marks. Factory/CI/CD evidence supports the Capstone defense. A sound Paper ADR is available when execution is blocked, with the limits stated in the [brief](assignments/ex5_capstone_virtual_software_company.md).

Use [Setup](SETUP.md), [Playbook](PLAYBOOK.md), [Course map](COURSE_MAP.md), and [Development](DEVELOPMENT.md) for the appropriate level of detail. See [extensions](extensions/README.md) for legacy comparison material and [_archive](_archive/README.md) for historical content.
