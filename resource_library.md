# Curated Resource Library: Managing Multi-Agent Teams

> [!NOTE]
> The GitHub-optimized version of this library now lives in `resources/README.md`.
> Use that folder for searchable video transcripts, cited schemas, and paper notes.

## Essential Papers And Research

### The Brain: Cognition, Alignment, Teamwork

- **Theory of Mind in Multi-Agent Collaboration via LLMs**  
  https://arxiv.org/abs/2310.10701  
  Why read it: shows how agents can reason about teammates' hidden beliefs, constraints, and intentions.

- **TeamLog: Formal Logical Theories of Teamwork**  
  https://arxiv.org/abs/2402.01680  
  Why read it: gives the formal basis for collective commitments, not just isolated task execution.

### The Nervous System: Memory And Tools

- **Model Context Protocol: Landscape, Security Threats, and Future Research Directions**  
  https://arxiv.org/abs/2503.23278  
  Why read it: reframes MCP as a governed tool lifecycle with concrete security risks and guardrails.

- **Model Context Protocol Python SDK**  
  https://github.com/modelcontextprotocol/python-sdk  
  Why read it: official implementation path for standardized agent-to-tool communication.

- **LlamaIndex Agentic RAG Examples**  
  https://docs.llamaindex.ai/en/stable/examples/agent/  
  Why read it: practical patterns for routing questions across shared memory and specialized indexes.

- **Course Builder Lab: Governed Logistics Weather Agent**  
  `notebooks/01_hello_multi_agent.ipynb` and `assignments/basic_agent_governance_labs.md`  
  Why read it: turns a familiar API-calling logistics agent into a zero-trust gateway exercise with typed request and response schemas.

### The Body: Execution Frameworks

- **ChatDev: Communicative Agents for Software Development**  
  https://arxiv.org/abs/2307.07924  
  Why read it: foundational "virtual software company" pattern for vibe coding with PM, coder, reviewer, and tester agents.

- **AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation**  
  https://arxiv.org/abs/2308.08155  
  Why read it: introduces conversable agents and GroupChat orchestration.

- **MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework**  
  https://arxiv.org/abs/2308.00352  
  Why read it: makes Standard Operating Procedures first-class artifacts.

- **CrewAI Documentation**  
  https://docs.crewai.com/  
  Why read it: production orchestration patterns for agents, tasks, crews, context chains, guardrails, persistent outputs, dynamic inputs, coding-agent teams, and hierarchical delegation. Maps to the self-contained CrewAI guide in `crewai_learning/README.md`.

- **CrewAI Installation and LLM Configuration**  
  https://docs.crewai.com/en/installation  
  https://docs.crewai.com/en/concepts/llms#setting-up-your-llm  
  Why read it: shows the Python/CLI and API-key setup path. In this course, live setup is optional; the required exercise is the governed offline coding-agent skeleton.

- **AutoGen Documentation**  
  https://microsoft.github.io/autogen/  
  Why read it: production-oriented multi-agent conversation and group chat patterns.

- **LangGraph Documentation**  
  https://langchain-ai.github.io/langgraph/  
  Why read it: stateful routing, graph edges, cycles, and error-handling loops.

- **Pydantic AI Documentation**  
  https://ai.pydantic.dev/  
  Why read it: strict result types, dependencies, and type-safe agent delegation.

- **Course Builder Lab: Vibe Coding CEO Interface**  
  `notebooks/10_vibe_coding_interface.ipynb` and `assignments/basic_agent_governance_labs.md`  
  Why read it: shows how human natural language becomes typed project state and TeamLog commitments before downstream agents act.

### The Reflexes: Routing And Self-Repair

- **Sakana Fugu Technical Report**  
  https://arxiv.org/abs/2606.21228  
  Why read it: introduces orchestrator-as-a-model routing across heterogeneous LLMs.

- **Course Builder Lab: Bounded Writer Agent**  
  `notebooks/05_self_repair_loop.ipynb` and `assignments/basic_agent_governance_labs.md`  
  Why read it: translates self-repair from code generation into a familiar writer/editor loop with typed feedback and escalation.

### The Ecosystem: Enterprise Scale

- **Internet of Agents Whitepaper, Cisco Outshift**  
  https://outshift-headless-cms-s3.s3.us-east-2.amazonaws.com/Internet_of_Agents_Whitepaper.pdf  
  Why read it: enterprise A2A interoperability, agent identity, discovery, and zero-trust governance.

- **AGNTCY Open Source Framework**  
  https://github.com/agntcy  
  Why read it: emerging infrastructure for open, interoperable agent ecosystems.

- **Course Builder Lab: Adversarial QA Agent**  
  `notebooks/11_enterprise_a2a_perimeter.ipynb` and `assignments/basic_agent_governance_labs.md`  
  Why read it: turns QA into a red-team A2A perimeter exercise with typed incident tickets and quarantined messages.

## DeepLearning.AI Teaching Materials

- Multi AI Agent Systems with crewAI: https://www.deeplearning.ai/courses/multi-ai-agent-systems-with-crewai/
- AI Agentic Design Patterns with AutoGen: https://learn.deeplearning.ai/courses/agentic-ai/

## Instructor Use

Use the papers as the theory spine, the framework documentation as implementation support, and the DeepLearning.AI courses as pacing models: first build intuition, then show the architecture, then make the learner implement a small but real version.
