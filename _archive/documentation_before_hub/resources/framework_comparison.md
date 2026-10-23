# Multi-Agent Framework Comparison

[Course home](../README.md) · [Learner paths](../README.md#learner-paths) · [Slide index](../README.md#main-deck-slide-index)

**Slides and reference reading · Reviewed 17 October 2026**

**Learning objective — Multi-Agent Framework Literacy:** Compare CrewAI (role-based teams), LangGraph (state-machine workflows), AutoGen (conversational agents), and Microsoft Agent Framework (agents and explicit workflows). LlamaIndex adds a retrieval-oriented reference example.

Use this comparison with the [main presentation](../slides/managing_multi_agent_teams_workshop_v16.pptx). It adds no exercise, homework, installation step, or assessment mark. The required practical work continues to use the existing CrewAI configurations and deterministic fixtures in [Labs 1–3 and the Capstone](../assignments/index.md).

## What counts as a multi-agent system?

A coordinated Manager, Coder, and QA can form a multi-agent system: agents interact to complete a task. Multiple independent teams, vendors, or frameworks are **not required**. The course's Development-to-Security Capstone demonstrates a further boundary between two teams; it is one possible organization of a MAS. See [MAS foundations](../assignments/multi_agent_systems_foundations.md).

Frameworks, agent SDKs, orchestration runtimes, and visual automation products overlap, but they are different kinds of tools. The tables identify their main abstractions rather than ranking every product on one scale. Their features and deployment options change; consult the linked primary documentation before adopting one.

<a id="four-core-frameworks"></a>

## Framework shortlist

The use cases below are starting points for comparison. Each framework supports more than its shortest description suggests.

| Framework | Architecture and core mechanics | Typical fit and audience | Controls available to the application | Limitations to assess | Course example or reference connection |
| --- | --- | --- | --- | --- | --- |
| **CrewAI** | Role-based agents execute tasks in sequential or hierarchical Crews. | Teams whose roles, delegation, and task deliverables are easy to describe; Python application builders. | Task `context`, `output_pydantic`, role/task tool lists, and output guardrails. | A declared role is not enforced intent; an exposed tool list is not a sandbox. Complex state transitions may need explicit Flow/application design. | **Implemented:** Lab 2 constructs the Development Crew; the Capstone constructs Development and Security Crews. Required runs use local fixtures/adapters. [Processes](https://docs.crewai.com/en/concepts/processes) · [Tasks](https://docs.crewai.com/en/concepts/tasks) |
| **LangGraph** | Explicit state graph with nodes, edges, branches, and cycles. | Workflows needing inspectable transitions, persistence, and resume; engineers designing orchestration state. | Conditional routing, checkpoints, interrupts for human review, and developer-defined validation. | The application must design state, reducers, recovery, and side-effect handling. A `TypedDict` state declaration does not perform runtime validation. | **Conceptual alternative:** The Capstone's validation → Security decision can be represented as graph nodes. No refactor is assigned. [Overview](https://docs.langchain.com/oss/python/langgraph/overview) · [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api) |
| **AutoGen** | Message-based agents and teams; AgentChat provides group-conversation patterns over an event-driven core. | Understanding conversational coordination and existing AutoGen applications; developers and researchers. | Speaker selection, termination conditions, human participation, and separately configured code executors. | Conversation needs explicit contracts and stopping rules. A local executor runs on the host; Docker isolation must be configured and reviewed. Review the current maintenance notice and the source discrepancy below before adoption. | **Reference only:** Compare a conversation team with Lab 2's task dependencies; no AutoGen exercise. [AgentChat](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html) · [Executors](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/components/command-line-code-executors.html) |
| **LlamaIndex Agents** | Tool-using agents and agent workflows; retrieval/query engines can be exposed as tools. | Document-grounded assistants and retrieval-heavy workflows; data and application engineers. | Explicit tools, workflow state/events, human-review patterns, and structured outputs. | Retrieval quality, source freshness, access rules, and answer evaluation remain application responsibilities. It also supports general orchestration beyond RAG. | **Reference only:** Relate the HR/RAG tabletop simulation to retrieval tools. No LlamaIndex notebook or package is required. [Agents](https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/) · [Building an agent](https://developers.llamaindex.ai/python/framework/understanding/agent/) |
| **Microsoft Agent Framework** | Agents plus explicit graph workflows, including sequential, concurrent, and handoff patterns. | Python and .NET applications needing agent/workflow orchestration and integrations; application and enterprise engineers. | Sessions, middleware, checkpoints, tool policies, and human-review workflows. | The application still supplies authorization, validation, and safe handling of side effects. Check the chosen language and package version. | **Reference only:** Another way to express the Capstone's explicit team boundary. [Official repository](https://github.com/microsoft/agent-framework) · [Overview](https://learn.microsoft.com/agent-framework/overview) |

## Lecture 8 discussion: why this course uses CrewAI

The optional [three-agent advanced reference](../crewai_learning/01_Bridge_Sequential_Crew.ipynb) adds executable evidence to this discussion: real CrewAI tasks with local fixture LLMs, strict output rejection, three bounded attempts, and typed escalation. It uses sequential execution with Manager/Coder/QA responsibilities; native hierarchical delegation is not tested. [Assignment 09](../assignments/assignment_09_framework_comparison.md) maps the example to this comparison without adding graded work.

The course chooses CrewAI because named Manager/Coder/QA roles, task dependencies, and tool lists make role separation visible in a small classroom example. This is a teaching choice, not a claim that CrewAI is the only framework with typed output or role controls. The required lab constructs the configuration and checks local fixtures. [CrewAI processes](https://docs.crewai.com/en/concepts/processes)

For a future version with more branches, persistent workflow state, and recovery decisions, LangGraph offers an explicit graph model to evaluate. AutoGen illustrates conversational coordination, subject to the maintenance/source caveat below. LlamaIndex provides a retrieval-oriented comparison for the HR/RAG example. Microsoft Agent Framework provides a comparison for Python/.NET agent and workflow orchestration. These comparisons add no implementation task.

Use this discussion in [Lecture 8](../assignments/assignment_08_debugging_sdlc.md) without adding graded work: which need would justify a different orchestration model, and which contract, tool, and evidence checks would transfer?

## Optional Capstone architecture extension: LangGraph

**Reference/design only — no required homework, coding, marks, or installation.** This is a possible future architecture, not a feature in the current [Capstone notebook](../notebooks/04_capstone.ipynb).

```text
START → Development → Validate DevDeliverable
                          ├─ valid → Security & Compliance → Inspect audit → END
                          └─ invalid → Reject / escalate → END
```

The **Workflow Coordinator** is the routing policy between these stages; it need not be another LLM agent. A prospective state record could carry the request, candidate deliverable, validated artifact, audit result, status, and evidence events. A validation node executes Pydantic checks before a conditional edge permits Security to start. The graph describes control flow; it does not itself verify that the Development Team's QA-status claim is truthful. Independent test evidence remains necessary. [LangGraph graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)

If recovery requirements grow, the design could use a configured checkpointer to retain workflow state and an interrupt to wait for human input. The application still defines rejection/retry budgets, storage access, and safe repetition of external actions. A graph drawn on a slide supplies none of those implementations. [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) · [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)

Development and Security could remain CrewAI-based components behind these graph stages in a future design; changing the coordinator does not require replacing every team. That integration is an architectural possibility to investigate, not a tested cross-framework adapter supplied by this repository. The [Capstone brief](../assignments/ex5_capstone_virtual_software_company.md#optional-architecture-extension-a-langgraph-state-machine) and [extension index](../extensions/README.md#optional-capstone-architecture-reading) link here for optional reading.

## Broader ecosystem

These products illustrate additional abstractions and deployment choices. The fit/audience descriptions are teaching interpretations of the documented capabilities, not guaranteed outcomes.

| Product and type | Architecture and core mechanics | Typical fit and audience | Controls available to the application | Limitations to assess | Course connection and primary reading |
| --- | --- | --- | --- | --- | --- |
| **Google ADK** — agent/workflow framework | LLM agents, subagents, tools, shared state, and workflows. | Multi-step applications, including Google model/cloud integrations; application and cloud engineers. | Configurable routing, tool authentication, and action confirmations. | Orchestration does not validate business truth. Workflow APIs vary by ADK language/version; consult current guidance. | **Reference only:** Compare role/context routing with Lab 2. [Agents](https://adk.dev/agents/) · [Safety](https://adk.dev/safety/) |
| **Claude Agent SDK** — agent SDK/harness | Embeds Claude Code's agent loop and context management; Python/TypeScript, subagents, tools, sessions, and hooks. | Code, file, and tool-driven applications; software and automation engineers. | Tool permissions, approval callbacks, and hooks; execution isolation must also be configured. | A permission callback is not a complete sandbox. Operated SDK processes and hosted managed-agent services have different deployment boundaries. | **Reference only:** Compare tool permissions and role-specific context. [Overview](https://code.claude.com/docs/en/agent-sdk/overview) · [Permissions](https://code.claude.com/docs/en/agent-sdk/permissions) |
| **MetaGPT** — role/SOP framework | Software-team roles coordinate requirements, design, and code artifacts through standard operating procedures. | Studying software-team automation and artifact handoffs; architects and researchers. | Configurable roles, actions, and workflow; artifact review remains necessary. | SOPs and role prompts do not establish secure tool permissions or correct code. Runtime compatibility differs from this course environment. | **Reference only:** Relate product/architect/engineer artifacts to a typed handoff. [Project](https://github.com/FoundationAgents/MetaGPT#software-company-as-multi-agent-system) · [Configuration](https://docs.deepwisdom.ai/main/en/guide/get_started/configuration.html) |
| **Pydantic AI** — typed Python agent framework | Model-agnostic agents with Pydantic-validated output, typed tools, and dependency injection. | Typed service integrations and data contracts; Python/backend engineers. | Output validators, tool argument validation, and explicit dependencies. | Passing validation establishes declared constraints, not factual accuracy or correct code. Pydantic AI is a separate agent library from installed Pydantic. | **Reference only:** Compare the Lab 1 contract with an agent framework's output model. [Overview](https://pydantic.dev/docs/ai/overview/) · [Output](https://pydantic.dev/docs/ai/core-concepts/output/) |
| **n8n** — visual workflow automation platform | Connected nodes and branches integrate services; an AI Agent selects from connected tools. | Operational integrations and approval flows; automation builders and operations teams. | Credentials, validation nodes, and human review on selected tools. | A workflow canvas does not itself enforce safe actions. Review node permissions, data flow, and retry effects. | **Reference only:** Visual counterpart to the validate → act → review pattern. [Workflows](https://docs.n8n.io/build/understand-workflows.md) · [Human review for tools](https://docs.n8n.io/build/integrate-ai/ai-examples/human-in-the-loop-for-tools.md) |
| **OpenClaw** — self-hosted assistant gateway/runtime | Routes channel messages to configured agents with separate workspaces, sessions, and state. | Channel-connected assistants and agent routing; self-hosting and automation practitioners. | Agent bindings, tool policies, approvals, and configurable sandboxing. | A workspace is a working directory, not a hard sandbox. Local gateway hosting does not imply every model call stays local. | **Reference only:** Compare routing and tool boundaries. [Multi-agent routing](https://docs.openclaw.ai/concepts/multi-agent) · [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing) |

**AutoGen maintenance and source note, 17 October 2026:** The GitHub API reports `archived: false`. The repository's prominent README notice says Microsoft no longer actively maintains the project or provides fixes/support, describes the project as archived, and directs new users to Microsoft Agent Framework. These signals conflict. Slide 17 uses the neutral name **AutoGen** and limits its selection example to existing systems or conversation-pattern study. Check the current maintenance policy before adoption. A recent push or an old release date does not establish active support. [GitHub repository metadata](https://api.github.com/repos/microsoft/autogen) · [README notice](https://github.com/microsoft/autogen#autogen) · [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)

## Official repository and name check

The official repositories below were checked on **17 October 2026**; they now support slides 17 and 20. This verifies the names and source links, not production suitability or a support guarantee.

| Slide label | Official repository |
| --- | --- |
| CrewAI | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) |
| LangGraph | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) |
| AutoGen | [microsoft/autogen](https://github.com/microsoft/autogen) |
| LlamaIndex | [run-llama/llama_index](https://github.com/run-llama/llama_index) |
| Microsoft Agent Framework | [microsoft/agent-framework](https://github.com/microsoft/agent-framework) |
| Google ADK (Agent Development Kit) | [google/adk-python](https://github.com/google/adk-python) |
| Claude Agent SDK | [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) |
| MetaGPT | [FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT) |
| Pydantic AI | [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) |
| n8n | [n8n-io/n8n](https://github.com/n8n-io/n8n) |
| OpenClaw | [openclaw/openclaw](https://github.com/openclaw/openclaw) |

## Production decision starting points

These are design heuristics, not exclusive winners or verified performance rankings. Several tools can implement the same pattern.

1. **Clear roles and task deliverables:** Evaluate CrewAI's Crews and output models. Verify the actual tool permissions and downstream acceptance checks.
2. **Explicit branching, retries, persistence, or resume:** Evaluate LangGraph's state and transition model. Define retry budgets and safe handling of repeated side effects.
3. **Conversational negotiation or group critique:** Study AutoGen's conversation patterns and migration guidance; compare supported alternatives before starting a new deployment.
4. **Queries across documents and retrieval tools:** Evaluate LlamaIndex's retrieval and agent abstractions. Test permissions, retrieval relevance, freshness, and source-grounded answers.
5. **Python/.NET agent and workflow integration:** Evaluate Microsoft Agent Framework's agents, explicit workflows, and integrations. Implement application authorization and approval boundaries.

Before choosing, compare the team's language and operating skills, required integrations, hosting/data boundaries, current support, observability, and representative task results. Measure quality, latency, cost, and failure recovery on the intended workload. Choosing a framework alone establishes none of these outcomes.

## Cross-framework pattern: a contract with executable checks

| Transferable principle | What to implement and inspect |
| --- | --- |
| **Validate data at boundaries** | Execute a validator such as Pydantic on incoming and outgoing data. Python's `TypedDict` describes expected keys and types for type checking; it does **not** enforce them at runtime. LangGraph can use Pydantic state or explicit validation where appropriate. [Python typing](https://docs.python.org/3/library/typing.html#typing.TypedDict) · [LangGraph schemas](https://docs.langchain.com/oss/python/langgraph/graph-api#schema) |
| **Check meaning as well as structure** | A valid object can contain a false test-status claim or an incorrect answer. Validate the schema, then inspect independent evidence and task-specific tests. CrewAI's `output_pydantic` requests a typed result; callers still handle failed conversion and invalid content. [CrewAI task outputs](https://docs.crewai.com/en/concepts/tasks#task-output) · [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/) |
| **Restrict tool access and effects** | Limit exposed tools, validate arguments, and authorize each consequential action in the tool/service. Use appropriate process/container isolation for untrusted execution. Tool lists and role prompts are not OS security boundaries. [AutoGen executor environments](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/components/command-line-code-executors.html) |
| **Bound autonomy and escalate** | Specify attempts, time/cost budgets, terminal states, and a human-review route in executable control flow. A timeout, a retry budget, and human approval solve different problems. |
| **Retain an audit trail** | Record relevant inputs, routing decisions, validation outcomes, tool calls, and final evidence with suitable access/redaction. Logs support inspection; they are not proof of private model reasoning or universal correctness. |

## Course vocabulary: same three labs

| Course term | Existing activity | What the learner can claim from the evidence |
| --- | --- | --- |
| **Context Engineering — Lab 1** | Define the typed artifact and constraints before downstream use; connect these specifications to the relevant task context in Lab 2. | The supplied valid/invalid fixtures show whether declared constraints are enforced. A schema does not establish factual truth. |
| **Multi-Agent Management / Code Auditing — Lab 2** | Inspect role tools/context and run the supplied Manager audit before admitting a typed proposal to the local QA inbox. | The required grader checks those configuration repairs; the local fixture demonstrates typed output. It does not execute a live Crew or establish OS isolation. |
| **Manager Oversight / Code Validation — Lab 3** | Repair the input gate and retry loop; run the supplied oversight record and cite evidence for escalation. | The supplied unsafe input is blocked and the failing mock stops after one initial attempt plus three retries. This does not prove comprehensive security. |
| **Strategic Prompt Engineering — Labs 1–2** | Express requirements, role responsibilities, context dependencies, and expected outputs precisely. | Better instructions and relevant context support execution. Runtime validation and tests are still needed; neither prompts nor schemas eliminate hallucinations. |

The [course map](../COURSE_MAP.md) records the exact notebook edits and grader coverage. Framework literacy transfers these design questions to other tools; it does not change the three required labs, the Capstone, or their grading.

[Course home](../README.md) · [Learner paths](../README.md#learner-paths) · [Slide index](../README.md#main-deck-slide-index)
