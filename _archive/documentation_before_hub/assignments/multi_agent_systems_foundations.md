# Assignment 00A: Multi-Agent Systems Foundations

> **Supporting reference material.** This is outside the required three labs and Capstone and adds no course marks. Follow the [current exercise index](index.md) for the assessed path. Start with the [procurement and HR RAG course simulations](workshop_simulations.md) for the examples used in the main slides.

## Credits & Alignment

Source inspiration: [IBM's introduction to multi-agent systems](https://www.ibm.com/think/topics/multiagent-system), with academic foundations linked below.

This assignment develops the judgment needed to decide whether a task benefits from multiple agents, how those agents should interact, and which controls limit the relevant risks. Additional agents also introduce coordination and resource costs; their presence alone does not establish better results.

The required practical sequence remains [Lab 1: contracts](../notebooks/01_lab_pydantic.ipynb) → [Lab 2: team handoff](../notebooks/02_lab_crewai.ipynb) → [Lab 3: tool gates and bounded repair](../notebooks/03_lab_security.ipynb) → [Capstone: Development to Security](../notebooks/04_capstone.ipynb). This optional assignment adds no notebook prerequisites.

## Design Context

Before designing a `CodePatch` or a `DevDeliverable`, consider the system context.

A single agent can answer, summarize, and call tools. Tasks involving multiple specialties, conflicting goals, long-running state, security boundaries, or parallel work may benefit from separate roles, but should be compared against a simpler design.

A **multi-agent system (MAS)** requires multiple agents with some autonomy that interact within a shared task or environment. Multiple tool functions, model calls, or named steps do not by themselves establish autonomous interacting agents. The course's deterministic fixtures simulate selected coordination and validation behaviors; they do not demonstrate live agent reasoning.

A managed multi-agent team is like an airport control tower, newsroom, or software release room:

- Each specialist has a role.
- The shared plan is visible.
- Sensitive information is need-to-know.
- Tool access is governed.
- Disagreements are escalated.
- Failures leave evidence.

This assignment gives learners the vocabulary and judgment to choose the right team shape before they touch implementation.

## Learning Objectives

By the end, learners can:

1. Explain when specialization and coordination may justify multiple agents, and identify their additional costs.
2. Distinguish goal relationships (cooperative, competitive, mixed), coordination structures (hierarchical, peer-to-peer, hybrid), and capability distributions (homogeneous, heterogeneous).
3. Choose vertical, horizontal, or hybrid architecture for a business scenario.
4. Map interaction patterns to governance controls: schemas, memory visibility, tool authorization, repair loops, and audit trails.
5. Identify the management failure prevented by each technical pattern.

## Building Blocks

| Building Block | Analogy | Course Connection |
| --- | --- | --- |
| Single-Agent Trade-off | One employee handling product, security, QA, and release alone | Compare complexity and accountability before adding agents |
| Cooperative Agents | A relay team passing a baton | Typed handoffs and context chains |
| Competitive Agents | Two vendors bidding for a route | Debate records, arbitration, and human review |
| Mixed System | Ride dispatch balancing driver, rider, and platform incentives | Tool policy plus TeamLog commitments |
| Hierarchical System | Incident commander coordinating specialists | Development Manager, Coder, and QA configuration in [Lab 2](../notebooks/02_lab_crewai.ipynb) |
| Heterogeneous Team | Specialists with different jobs and tools | Coder and QA role/tool differences in Lab 2 |
| Expert Routing Policy | Routing a question to the appropriate service desk | The [Capstone](../notebooks/04_capstone.ipynb) has illustrative Fast/Expert records, not extra agents |
| Vertical Architecture | Control tower | API gateway, centralized policy, release approval |
| Horizontal Architecture | Peer review room | Optional design alternative; not a required cross-organization protocol |
| Hybrid Architecture | Manager sets goal; specialists choose methods | Compare with the Capstone's separate Development and Security configurations |

These rows describe different dimensions and can overlap: a system may be cooperative, hierarchical, and heterogeneous at the same time. Expert routing is a **workflow policy**, not another mutually exclusive MAS type. A router selecting among models or fixed records is not sufficient evidence of autonomous interacting agents. Neural **mixture-of-experts (MoE)** is a separate model architecture: a gating network selects neural subnetworks inside a model ([Shazeer et al., 2017](https://arxiv.org/abs/1701.06538)).

## Exercise 00A.1: The Single-Agent Stress Test

### Story

You hired one "super agent" to handle a software issue: read the GitHub ticket, design the feature, write code, test it, scan for security issues, and release it.

It works in a demo. Then the ticket includes a hidden constraint, an unsafe file path, a failing test, and a request from an external vendor.

### Mission

Write a short risk analysis showing what could fail, which controls could help, and whether each control needs another agent or can be implemented in ordinary code.

Use this table:

| Failure Pressure | Possible Failure | Control and Whether Another Agent Is Needed |
| --- | --- | --- |
| Specialization |  |  |
| Tool security |  |  |
| Hidden constraints |  |  |
| Test failure |  |  |
| External requester |  |  |

### Required Evidence

- At least five failure pressures.
- Each pressure maps to one course control: Pydantic schema, input/tool gate, role-specific context, bounded repair, route decision, or human review.
- One sentence explaining why "just improve the prompt" is not enough.

### Production Takeaway

Roles, boundaries, and accountability can support a complex workflow. Schemas, permissions, and retry limits remain useful in both single-agent and multi-agent designs.

## Exercise 00A.2: Classify The Interaction Pattern

### Story

You are the course architect reviewing proposed student projects. Some need agents to cooperate. Some need debate. Some need routing. Some need a manager.

### Mission

Describe each scenario on separate axes: **goals** (cooperative, competitive, mixed), **coordination** (hierarchical, peer-to-peer, hybrid), and **capabilities** (homogeneous, heterogeneous). Use **insufficient information** where the scenario does not establish an axis or the presence of multiple agents. Note any routing policy separately. Disagreement alone does not establish competitive goals; reviewers can disagree while pursuing the same objective.

| Scenario | Goals | Coordination | Capabilities | Evidence / Missing Information and Control |
| --- | --- | --- | --- | --- |
| PM -> Coder -> QA -> Security -> Release |  |  |  |  |
| Two reviewers disagree about whether a patch is safe |  |  |  |  |
| Marketing wants 500 copy variants under a fixed budget |  |  |  |  |
| External security agent sends a scan result over HTTP |  |  |  |  |
| CEO changes the database choice mid-workflow |  |  |  |  |
| Researcher, Writer, Editor, and Fact Checker build a report |  |  |  |  |
| A router sends simple tasks to cheap models and high-risk tasks to reasoning models |  |  |  |  |
| A vendor agent tries to export restricted logs |  |  |  |  |
| A QA agent red-teams an internal tool gateway |  |  |  |  |
| A manager creates a different workflow for low-risk and high-risk issues |  |  |  |  |

### Required Evidence

- Separate axis descriptions per scenario; mark unsupported classifications as insufficient information.
- A one-sentence justification.
- A matching governance control for each scenario.

### Production Takeaway

Goal relationships, coordination, and capabilities describe different design choices. Check evidence for each before choosing controls. Cross-organization communication is an optional scenario here, not a requirement of the course's local typed team handoff.

## Exercise 00A.3: Architecture Decision Matrix

### Story

A manager asks, "Should this be centralized, decentralized, or hybrid?"

That is not a style preference. It is a risk decision.

### Mission

Choose an architecture for each scenario:

- Vertical: centralized manager or policy gateway controls the flow.
- Horizontal: agents coordinate peer-to-peer.
- Hybrid: centralized governance with decentralized specialist execution.

| Scenario | Architecture | Why | Risk If Wrong |
| --- | --- | --- | --- |
| Internal software release with security approval |  |  |  |
| Peer agents collaboratively summarize public documents |  |  |  |
| Cross-organization payroll/security scan request |  |  |  |
| Logistics weather-risk workflow for shipments |  |  |  |
| CEO-driven Vibe Coding session with mid-flight changes |  |  |  |
| Research writing pipeline with strict final delivery format |  |  |  |

### Required Evidence

- Architecture choice for each scenario.
- One risk of choosing the wrong architecture.
- One current course artifact or control that supports the choice, such as a Lab 1 contract, Lab 2 task-context dependency, Lab 3 input gate or retry limit, or Capstone `DevDeliverable` boundary.

### Production Takeaway

Architecture determines where coordination decisions are made. Central control can simplify policy enforcement but creates a dependency; peer coordination distributes responsibility but adds agreement and communication challenges. Neither structure alone establishes safety or suitability.

## Exercise 00A.4: Build A Minimal Pattern Catalog

### Story

Your future team will ask, "What kind of multi-agent system are we building?"

You need a reusable catalog they can consult before coding.

### Mission

Create a one-page pattern catalog with six rows:

| Dimension / Policy | Example Description | Useful When | Risk / Control |
| --- | --- | --- | --- |
| Goal relationship | Cooperative |  |  |
| Goal relationship | Competitive |  |  |
| Goal relationship | Mixed |  |  |
| Coordination | Hierarchical; compare with peer-to-peer |  |  |
| Capabilities | Heterogeneous; compare with homogeneous |  |  |
| Workflow policy, not MAS type | Expert routing |  |  |

### Required Evidence

- Each row includes one concrete course scenario.
- Each row names at least one failure mode.
- Each row names a guardrail from the course.

### Production Takeaway

Pattern catalogs prevent architecture drift. They help teams choose a design because it fits the management problem, not because it sounds trendy.

## Exercise 00A.5: Failure Mode Map

### Story

Multi-agent systems fail differently from single-agent systems. One bad agent output can ripple through memory, tools, routing, and release.

### Mission

Build a failure mode map for a managed software team.

Use these failure classes:

- Agent malfunction.
- Coordination breakdown.
- Unpredictable behavior.
- Tool overreach.
- Memory leakage.
- Infinite repair loop.

| Failure Class | Example | Detection Signal | Mitigation |
| --- | --- | --- | --- |
| Agent malfunction |  |  |  |
| Coordination breakdown |  |  |  |
| Unpredictable behavior |  |  |  |
| Tool overreach |  |  |  |
| Memory leakage |  |  |  |
| Infinite repair loop |  |  |  |

### Required Evidence

- One detection signal per failure class.
- One mitigation per failure class.
- At least three mitigations must be typed artifacts, not prose policies.

### Production Takeaway

Failure is not an exception in multi-agent systems. It is part of the workflow. A managed team must detect, contain, repair, or escalate every predictable failure mode.

## Grading Rubric

| Criterion | Weight |
| --- | --- |
| Correct classification of interaction patterns and architectures | 30% |
| Clear mapping from management problem to technical guardrail | 30% |
| Production-quality failure analysis | 25% |
| Clear analogies and concise explanations | 15% |

## Submission Checklist

- [ ] Single-agent stress test is complete.
- [ ] Ten scenarios distinguish goal relationships, coordination, capabilities, and missing evidence.
- [ ] Six scenarios are mapped to vertical, horizontal, or hybrid architecture.
- [ ] Pattern catalog includes guardrails and failure modes.
- [ ] Failure mode map includes detection and mitigation.
- [ ] No healthcare diagnosis, trading execution, or ML-training task is introduced.

## References

- [Shoham and Leyton-Brown (2009), *Multiagent Systems*](https://www.masfoundations.org/): foundational treatment of autonomous entities with different information or interests, communication, and decision making.
- [Wooldridge and Jennings (1995), *Intelligent Agents: Theory and Practice*](https://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/ker95/ker95-html.html): agency, autonomy, and interaction. Agents are not limited to LLM-based implementations.
- [Lowe et al. (2017), *Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments*](https://arxiv.org/abs/1706.02275): a research example separating cooperative, competitive, and mixed settings; not a taxonomy of all coordination structures.
- [Shazeer et al. (2017), *The Sparsely-Gated Mixture-of-Experts Layer*](https://arxiv.org/abs/1701.06538): gated neural subnetworks within a model, distinct from autonomous interacting roles.

These sources supply concepts, not evidence that the course's particular configurations outperform a single agent or are ready for operational use.
