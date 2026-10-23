# Curated Resource Library: course Topics

Optional references paired with the course topics. The course uses one [26-slide main presentation](../slides/managing_multi_agent_teams_workshop_v16.pptx); the nine competency topic numbers below are not slide numbers or separate decks. The core lessons use JupyterLab, deterministic fixtures, and the repository’s local checks; learners do not need a paid coding assistant or provider account.

Follow the [learner dashboard](../README.md#click-through-course-journey) for slides and exercises. These readings explain concepts; they do not add labs, homework, or marks to the required course.

## Teaching design and AI literacy

The course's learner-centered sequence is informed by the [Stanford Teaching Commons Artificial Intelligence Teaching Guide](https://teachingcommons.stanford.edu/teaching-guides/artificial-intelligence-teaching-guide), including its [four-domain AI literacy framework](https://teachingcommons.stanford.edu/teaching-guides/artificial-intelligence-teaching-guide/understanding-ai-literacy) and guidance on [meaningful assignments, objectives, and student perspectives](https://teachingcommons.stanford.edu/teaching-guides/artificial-intelligence-teaching-guide/integrating-ai-assignments). The local course adapts these ideas to deterministic software labs; Stanford did not review or endorse this curriculum. See the [alignment note](../instructor/stanford_teaching_guide_alignment.md) for implementation details and additional sources.

## Framework literacy: presentation reference

The [multi-agent framework comparison](framework_comparison.md) compares CrewAI, LangGraph, AutoGen, LlamaIndex, and Microsoft Agent Framework, then surveys Google ADK, Claude Agent SDK, MetaGPT, Pydantic AI, n8n, and OpenClaw. It includes primary documentation, current support caveats, and decision heuristics. This is slides/reference material only: no new framework exercise, homework, package, or marks. One coordinated team can be a MAS; multiple teams or frameworks are not a prerequisite.

## Start here: Multi-Agent Systems, Applications & RAG

Read the main deck's **slides 1–7** first, then use the matching references here:

| Main slides | Focus | Companion material |
| --- | --- | --- |
| 1–2 | Agenda and starting with one agent | [Agent-building guide](../assignments/agent_building_design_guide.md#start-with-one-agent) |
| 3–5 | MAS definition, types, and applications | IBM MAS introduction below; [simulation introduction](../assignments/workshop_simulations.md#what-is-a-multi-agent-system) |
| 6 | Procurement recommendation | [Procurement simulation](../assignments/workshop_simulations.md#simulation-1-automating-a-procurement-recommendation) |
| 7 | HR policy assistant with RAG | IBM RAG reading below; [HR simulation](../assignments/workshop_simulations.md#simulation-2-enhancing-an-hr-virtual-assistant-with-rag) |

- **Definition and system types:** [What is a multi-agent system?](https://www.ibm.com/think/topics/multiagent-system) (IBM) introduces interacting agents, organization patterns, applications, and coordination challenges. Cooperative/competitive goals, hierarchical/peer organization, and homogeneous/heterogeneous capabilities describe different dimensions; they are not mutually exclusive categories.
- **RAG foundation:** [What is retrieval-augmented generation?](https://www.ibm.com/think/topics/retrieval-augmented-generation) (IBM) explains retrieving external knowledge before generating a response. The original research is [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) (Lewis et al., 2020). Retrieval and citations support review; they do not guarantee truth or access control.
- **course applications:** [Procurement and HR policy RAG simulations](../assignments/workshop_simulations.md) provide fixed facts, role diagrams, typed outcome designs, and expected decisions. These are ungraded tabletop demonstrations linked to the existing three labs and Capstone, not implemented notebooks or new installation requirements.
- **Scope:** A RAG workflow can use one agent or several. Routing among model-level experts is not itself a multi-agent team; the Capstone's Fast/Expert records are routing targets, not additional agents.

## Agent-building discussions

The [design guide](../assignments/agent_building_design_guide.md) connects working briefs (slide 9), helper roles (11), capability choice and human pairing (13), stable tools (14), state changes and errors (15), and takeaways (21) to the notebook checkpoints. Its [source notes](../assignments/agent_building_design_guide.md#source-notes) distinguish course conventions from platform documentation. The prompts are ungraded; the required notebooks do not implement these proposed desktop/video/cloud, tool-discovery, durable-state, or user-interaction capabilities.

## Required practical route

After the opening simulations, follow the [exercise index](../assignments/index.md): **preflight → Lab 1 → Lab 2 → Lab 3 → Capstone**. Main deck slides 8–21 explain this route. Background readings below support those tasks; they do not create extra graded work. The older short theory decks are archived and are not required reading.

## Topics 1–2: AI Orchestration, Workspace & Strategic Prompt Engineering

- **Course connection:** [Assignment 01](../assignments/assignment_01_strategic_prompt_engineering.md) and [Assignment 02](../assignments/assignment_02_ai_workspace_and_role_context.md) turn an informal request into explicit constraints and a role-aware handoff.
- **Article:** [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) (Anthropic) — practical guidance on choosing workflows and agents, designing tools, and keeping agent systems understandable.
- **Concept:** Context Engineering — curate the instructions, tools, memory, and task history passed to an agent. See Anthropic’s [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).

## Topics 3–5: Contracts, Team Memory & Code Auditing

- **Pydantic:** [Field constraints](https://docs.pydantic.dev/latest/concepts/fields/) and [model configuration](https://docs.pydantic.dev/latest/concepts/config/) — the validation rules repaired in [Lab 1](../notebooks/01_lab_pydantic.ipynb).
- **CrewAI:** [Tasks, context, and structured output](https://docs.crewai.com/en/concepts/tasks), [agent configuration](https://docs.crewai.com/en/concepts/agents), and [custom tools](https://docs.crewai.com/en/learn/create-custom-tools) — the task graph and tool lists inspected in [Lab 2](../notebooks/02_lab_crewai.ipynb). The required lab constructs the Crew and validates a local fixture; it does not execute CrewAI tasks.
- **Research context:** [Theory of Mind for Multi-Agent Collaboration via Large Language Models](https://aclanthology.org/2023.emnlp-main.13/) informs the discussion of role-specific information; [ChatDev](https://aclanthology.org/2024.acl-long.810/) and [MetaGPT](https://proceedings.iclr.cc/paper_files/paper/2024/hash/6507b115562bb0a305f1958ccc87355a-Abstract-Conference.html) provide examples of specialized software-team roles. These works motivate discussion; they do not prove this course’s exact topology.
- **Shared commitments:** [TEAMLOG in Action: a Case Study in Teamwork](https://www.comsis.org/pdf.php?id=244-0912) (ComSIS, 2010) studies a formal model of team information and commitments. The notebook's `team_log` dictionary is a small teaching analogy, not an implementation of TEAMLOG's logic.

## Topic 6: Safety Nets, Tool Validation & Evals

- **Agent evaluation:** [Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (Anthropic) — approaches to evaluating multi-step agent behavior.
- **Security:** [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — security risks to discuss alongside the local input-validation exercise.
- **Tool protocol:** [Model Context Protocol specification](https://modelcontextprotocol.io/specification) — background for the notebook’s MCP-style tool-boundary example; the local exercise is not a complete MCP server.
- **Course connection:** [Lab 3](../notebooks/03_lab_security.ipynb) uses a dry-run input gate and a fixed retry budget. Its checks cover supplied fixtures, not comprehensive injection resistance or production security.

## Topics 7–8: Context, Debugging & SDLC

- **Context engineering:** Anthropic’s [context engineering article](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) complements [Assignment 07's access-list exercise](../assignments/assignment_07_context_engineering_access_lists.md).
- **Debugging evidence:** Use the deterministic scenario trace in [Assignment 08](../assignments/assignment_08_debugging_sdlc.md). It is a teaching fixture, not a live trace and not model reasoning.
- **Coordination research:** [TRINITY: An Evolved LLM Coordinator](https://arxiv.org/abs/2512.04695) assigns Thinker, Worker, and Verifier roles; [Learning to Orchestrate Agents in Natural Language with the Conductor](https://arxiv.org/abs/2512.04388) studies learned communication topologies. The course's Fugu-style discussion adapts explicit routing and context selection as inspectable Python policies. It neither calls a hosted Fugu endpoint nor trains either research system.
- **Further reading:** The [resource index](README.md) separates optional references from the required exercise route.

## Topic 9: Capstone & Orchestration

- **Research context:** [ChatDev](https://aclanthology.org/2024.acl-long.810/) describes a multi-agent software-development organization.
- **Tool boundary:** The [MCP specification](https://modelcontextprotocol.io/specification) provides further reading on agent-to-tool interfaces.
- **Course implementation:** The [Capstone](../notebooks/04_capstone.ipynb) passes a validated `DevDeliverable` between local Development and Security adapters. It constructs two CrewAI configurations separately. Continue through the [deterministic factory](../notebooks/05_live_software_factory.ipynb) and [local CI/CD](../notebooks/06_local_cicd.ipynb): no provider calls or keys are required. The main notebook's Fast/Expert routing costs are self-contained teaching values and do not load the [optional marketing fixture](cited_resources/cost_aware_routing_fixtures.json).

## Resource notes

- The course’s `output_pydantic` setting requests a structured CrewAI result and Pydantic validates it; it does not guarantee that a model will always follow the contract.
- A schema validates declared fields and constraints; it does not prove that a generated claim is true. Task context makes information available; an executed trace or targeted check is needed to establish how it was used.
- `verbose=True` can expose execution and tool logs; it does not expose private chain-of-thought.
