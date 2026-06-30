# Curated Resource Library: Managing Multi-Agent Teams

Mission: This library provides the theoretical spine and technical study material for the "Managing Multi-Agent Teams" course. It is organized by the Course Anatomy to help learners connect abstract research papers to the concrete Python architectures they are building.

## Repository Navigation

| Folder | Purpose | Best Practice |
| :--- | :--- | :--- |
| 📄 [`/papers/`](./papers/) | Canonical PDFs of cited research. | Prefer linking to arXiv. Use Git LFS for large PDFs. |
| 🎬 [`/videos/`](./videos/) | Transcripts, timestamps, and external links. | **Do not** commit `.mp4` files. Host externally and link here. |
| 📊 [`/cited_resources/`](./cited_resources/) | Raw schemas, datasets, and OpenAPI specs. | Store `.json`, `.yaml`, or `.csv` files referenced in papers. |

---

## 1. The Brain: Cognition, Alignment & Teamwork

*How agents reason about peers, form collective commitments, and maintain context.*

| Title | Source | Type | Why it Matters for this Course |
| :--- | :--- | :--- | :--- |
| **[Theory of Mind in Multi-Agent Collaboration](https://arxiv.org/abs/2310.10701)** | arXiv | Paper | Proves that agents must model peers' hidden beliefs to avoid misalignment. Maps to **NB2 (Shared Memory)**. |
| **[TeamLog: Formal Logical Theories of Teamwork](https://arxiv.org/abs/2402.01680)** | arXiv | Paper | Provides the math for "collective commitments." Maps to our **TeamLog Commitment Engine**. |

---

## 2. The Nervous System: Memory & Tool Governance

*How agents access the real world safely without leaking data or executing unauthorized actions.*

| Title | Source | Type | Why it Matters for this Course |
| :--- | :--- | :--- | :--- |
| **[Model Context Protocol (MCP) Specification](https://modelcontextprotocol.io/)** | Anthropic | Docs | The universal standard for agent-to-tool communication. Maps to **NB3 (MCP Gateway)**. |
| **[MCP: Landscape, Security Threats, and Future Research](https://arxiv.org/abs/2503.23278)** | arXiv | Paper | The definitive guide to MCP vulnerabilities. Maps to **Ex4 (Zero-Trust Governance)**. |
| **[Agentic RAG Examples](https://docs.llamaindex.ai/en/stable/examples/agent/)** | LlamaIndex | Docs | Practical patterns for routing queries across shared memory. |
| **Governed Logistics Weather Agent Lab** | [`/notebooks/01_hello_multi_agent.ipynb`](../notebooks/01_hello_multi_agent.ipynb) | Notebook exercise | Beginner-friendly MCP pattern: hide API keys inside a gateway, check identity, validate `WeatherRequest`, and return typed `WeatherResponse` with shipping risk. |

---

## 3. The Body: Execution Frameworks & Type-Safety

*How agents pass work to each other without hallucinating fields or breaking the pipeline.*

| Title | Source | Type | Why it Matters for this Course |
| :--- | :--- | :--- | :--- |
| **[Pydantic AI Documentation](https://ai.pydantic.dev/)** | Pydantic | Docs | Strict result types and type-safe agent delegation. Maps to **NB4 (Pydantic Contracts)**. |
| **[CrewAI Documentation](https://docs.crewai.com/)** | CrewAI | Docs | Production orchestration patterns for agents, tasks, crews, sequential/hierarchical processes, task context, guardrails, file outputs, runtime inputs, and coding-agent teams. Maps to the self-contained **CrewAI Learning Guide** in [`/crewai_learning/`](../crewai_learning/). |
| **[CrewAI Installation](https://docs.crewai.com/en/installation)** | CrewAI | Docs | Shows the local setup path for the CrewAI CLI and project execution. Use it in Homework G as an optional live setup path after the offline skeleton is designed. |
| **[CrewAI LLM Configuration](https://docs.crewai.com/en/concepts/llms#setting-up-your-llm)** | CrewAI | Docs | Explains provider/API-key setup. The course keeps this optional so individual learner configs do not block the exercises. |
| **[ChatDev: Communicative Agents for Software Dev](https://arxiv.org/abs/2307.07924)** | arXiv | Paper | The foundational "Virtual Software Company" pattern. Maps to **Ex5 (Capstone)**. |
| **[MetaGPT: Meta Programming for Multi-Agent Collab](https://arxiv.org/abs/2308.00352)** | arXiv | Paper | Proves that Standard Operating Procedures must be first-class artifacts. |

---

## 4. The Reflexes: Routing & Self-Repair

*How the system optimizes cost, handles failure, and knows when to escalate to a human.*

| Title | Source | Type | Why it Matters for this Course |
| :--- | :--- | :--- | :--- |
| **[Sakana Fugu Technical Report](https://arxiv.org/abs/2606.21228)** | Sakana AI | Paper | **Beyond simple routing:** teaches learned orchestration, dynamic scaffold generation, collective intelligence via debate, and adaptive topology selection. Maps to **NB6 (basic routing)** and **NB9 (advanced orchestration)**. |
| **[Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)** | arXiv | Paper | Foundational self-repair pattern: agents store verbal critiques in an episodic buffer to improve later attempts. Maps to **NB5 (Self-Repair)**. |
| **[Voyager: An Open-Ended Embodied Agent with LLMs](https://arxiv.org/abs/2305.16291)** | arXiv | Paper | Shows continuous improvement through a reusable skill library of verified behaviors. Maps to advanced memory, repair, and routing discussions. |
| **[LATS: Language Agent Tree Search](https://arxiv.org/abs/2310.04406)** | arXiv | Paper | Teaches structured exploration of multiple reasoning/repair paths before committing, a useful antidote to naive infinite retry loops. |
| **NB9: Advanced Fugu Orchestration** | [`/notebooks/09_advanced_fugu_orchestration.ipynb`](../notebooks/09_advanced_fugu_orchestration.ipynb) | Notebook | Implements dynamic scaffolds, debate moderation, adaptive topology, and simple history-based routing updates. |
| **[AutoGen: Enabling Next-Gen LLM Applications](https://arxiv.org/abs/2308.08155)** | Microsoft | Paper | Introduces conversable agents and GroupChat orchestration. |

> [!NOTE]
> **Scope clarification:** NB6 intentionally teaches transparent rule-based routing first. NB9 introduces teaching adapters for the broader Fugu paradigm: workflow generation, debate, and topology adaptation. The actual Fugu research direction involves learned orchestrator training; this course treats that as conceptual reading and design discussion, not a graded notebook implementation.

---

## 5. The Ecosystem: Enterprise Scale & Zero-Trust

*How multi-agent systems survive in production, across organizational boundaries.*

| Title | Source | Type | Why it Matters for this Course |
| :--- | :--- | :--- | :--- |
| **[The Internet of Agents (IoA) Whitepaper](https://outshift-headless-cms-s3.s3.us-east-2.amazonaws.com/Internet_of_Agents_Whitepaper.pdf)** | Cisco Outshift | PDF | Enterprise A2A interoperability, agent identity, and zero-trust governance. |
| **[Agent-to-Agent (A2A) Protocol](https://github.com/a2aproject/A2A)** | Google / GitHub | Docs/Code | Open standard for cross-organization agent communication, including Agent Cards, task management, and secure streaming. Maps to **NB11 (Enterprise A2A Perimeter)**. |
| **[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)** | OWASP | Security Guide | Industry baseline for AI security. Emphasize LLM01 Prompt Injection and LLM08 Excessive Agency for **Ex4** and **NB11**. |
| **[MCP: Landscape, Security Threats, and Future Research](https://arxiv.org/abs/2503.23278)** | arXiv | Paper | Read the cross-boundary data exfiltration sections before the A2A exercises. Connects MCP tool safety to network-bound agent communication. |
| **NB11: Enterprise A2A & Zero-Trust Perimeter** | [`/notebooks/11_enterprise_a2a_perimeter.ipynb`](../notebooks/11_enterprise_a2a_perimeter.ipynb) | Notebook | Implements cross-org identity checks, payload classification, schema drift detection, and a Dead Letter Queue for denied A2A messages. |
| **Adversarial QA Agent Lab** | [`/notebooks/11_enterprise_a2a_perimeter.ipynb`](../notebooks/11_enterprise_a2a_perimeter.ipynb) | Notebook exercise | Turns QA into a red-team A2A test: prompt injection and exfiltration payloads are blocked, ticketed, and quarantined. |
| **[AGNTCY Open Source Framework](https://github.com/agntcy)** | GitHub | Code | Emerging infrastructure for open, interoperable agent ecosystems. |
| **[LangGraph Documentation](https://langchain-ai.github.io/langgraph/)** | LangChain | Docs | Stateful routing, graph edges, cycles, and error-handling loops. |

---

## 🎓 6. Pacing & Pedagogy Materials

*How to teach this material effectively.*

- **[Multi AI Agent Systems with crewAI](https://www.deeplearning.ai/courses/multi-ai-agent-systems-with-crewai/)** (DeepLearning.AI): use for pacing the baseline collaboration module.
- **[AI Agentic Design Patterns with AutoGen](https://learn.deeplearning.ai/courses/agentic-ai/)** (DeepLearning.AI): use for teaching reflection, tool use, planning, and orchestration.

### Current Exercise Narrative Standard

The current notebook phase uses a consistent Andrew Ng-style exercise arc:

| Notebook | Exercise Story |
| :--- | :--- |
| **NB1** | A software-delivery team needs release readiness, risk review, and audit trails before agent output can be trusted. |
| **NB1 Builder Lab** | A Logistics Weather Agent is safe only when weather access goes through identity, gateway, and typed response contracts. |
| **NB2** | A growing architecture team needs governed shared memory without leaking secrets or blowing up context. |
| **NB3** | An HR agent tries to issue an offer without approval, showing why MCP-style governance matters. |
| **NB4** | A hallucinated handoff field crashes the pipeline, motivating Pydantic as the schema firewall. |
| **NB5** | A coder loops forever on broken code, motivating bounded autonomy and escalation. |
| **NB5 Builder Lab** | A Writer/Editor pair turns blind retry into typed feedback, memory, and escalation. |
| **NB6** | A marketing campaign burns budget by overusing reasoning models, motivating routing economics. |
| **NB8** | Slack, GitHub, and webhooks need a safe front door into the agent workforce. |
| **NB10** | A human CEO changes requirements mid-flight, motivating governed natural-language steering. |
| **NB10 Builder Lab** | Natural language becomes TeamLog state before downstream agents act. |
| **NB11** | Internal agents need to communicate with external agents without leaking PII, accepting schema drift, or losing auditability. |
| **NB11 Builder Lab** | An adversarial QA payload becomes a typed security incident instead of an unsafe conversation. |
| **CrewAI Learning Guide** | A self-contained academic research pipeline guide shows role design, context chains, process selection, guardrails, recovery patterns, and clean `.md` delivery. |

---

## 🔄 How to Contribute / Update this Library

If you are adding new research or videos to this course, follow this checklist:

- [ ] **For Papers:** Add the row to the correct anatomy table above. Link to arXiv or the canonical publisher. If a local PDF is required, place it in `/papers/` and use Git LFS when appropriate.
- [ ] **For Videos:** Create a new `.md` file in `/videos/` containing the external link, chapter timestamps, and a 3-bullet summary.
- [ ] **For Schemas/Datasets:** Place the `.json`, `.yaml`, or `.csv` in `/cited_resources/` and link it in the "Why it Matters" column.
