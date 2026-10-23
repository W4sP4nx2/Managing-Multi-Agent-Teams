# Multi-Agent Systems in Context: Two course Simulations

[Course home](../README.md) · [Learner paths](../README.md#learner-paths) · [Slide index](../README.md#main-deck-slide-index)

These short, facilitator-led tabletop demonstrations introduce the applications discussed in the main slides. They use only the fixed facts below: no accounts, personal data, installation, or live services. They are **not implemented in the notebooks**, are not additional labs or homework, and add no marks to the course's 100-point assessment.

## What is a multi-agent system?

A multi-agent system (MAS) contains several agents that interact to address a task or shared environment. Each agent has a role, information, and permitted actions; coordination determines how their outputs affect the wider process. A collection of independent chatbots does not establish a coordinated workflow. See [IBM's introduction to multi-agent systems](https://www.ibm.com/think/topics/multiagent-system).

Use three separate questions when describing a system:

| Question | Useful descriptions | Example in this course |
| --- | --- | --- |
| How do their goals relate? | Cooperative, competitive, or mixed | The Development and Security teams cooperate on a delivery, while independent suppliers may compete for a purchase. |
| How is work organized? | Hierarchical, peer-to-peer, or hybrid | The Development Manager coordinates Coder and QA; an explicit Coordinator controls the inter-team boundary. |
| Do they have the same capabilities? | Homogeneous or heterogeneous | Coder and QA have different roles and tool permissions in Lab 2. |

These descriptions can overlap. Model-level mixture-of-experts is a different concept from a team of interacting agents. The Capstone's Fast/Expert records illustrate a routing policy; they are not extra agents.

### Facilitation: start with learner reasoning

Before displaying the fixed answer below, give learners 30–60 seconds to write an initial view. Invite a pair to compare evidence, then ask one open question (“What would make you pause or ask for review?”) before checking definitions. Accept multiple defensible descriptions when they fit the stated facts; use follow-up questions to refine the distinction between goals, coordination, and capabilities. This is formative and ungraded.

## Simulation 1: Automating a procurement recommendation

**Purpose:** Show how a business request crosses purchasing, supplier evaluation, finance, policy review, and human approval. Automation produces a traceable recommendation; the simulated agents cannot place an order or approve their own work.

### Fixed business request and evidence

Request `P-001`: obtain **20 identical course kits**, delivered within **5 days**, with a total budget of **USD 1,200**. Each quote includes all shipping and taxes. The following records are synthetic and complete for this demonstration.

| Quote evidence | Supplier | Kits available | Total USD | Delivery days | Approved supplier? |
| --- | --- | ---: | ---: | ---: | --- |
| `Q-A/v1` + `REG/v1#A` | A | 20 | 1,100 | 4 | Yes |
| `Q-B/v1` + `REG/v1#B` | B | 20 | 1,000 | 7 | Yes |
| `Q-C/v1` + `REG/v1#C` | C | 20 | 900 | 3 | No |

Demonstration policy `PROC/v1`: a quote is eligible only if quantity, deadline, budget, and approved-supplier checks all pass. Choose the lowest total among eligible quotes; break an equal-price tie by supplier ID. A named human approver must authorize any purchase. These are invented teaching rules, not UN procurement policy.

### Coordination trace

```text
Business request P-001
    -> Buyer: extracts quantity, budget, deadline
    -> Supplier Evaluator: compares quote and registry evidence
    -> Finance Reviewer: checks total against budget
    -> Policy Reviewer: checks eligibility and evidence completeness
    -> Coordinator: returns typed recommendation
    -> Human approver: approves, rejects, or requests clarification
```

| Role | Input → output | Boundary |
| --- | --- | --- |
| Buyer | Request → typed purchase requirements | Cannot change the budget or deadline. |
| Supplier Evaluator | Quotes and registry → eligibility table | Cannot invent a quote or approve a supplier. |
| Finance Reviewer | Eligible totals and budget → affordability result | Cannot release money. |
| Policy Reviewer | Prior results and `PROC/v1` → evidence check | Cannot waive a failed rule. |
| Coordinator | Checked evidence → recommendation or escalation | Cannot submit an order; human approval remains separate. |

### Typed outcome and deterministic decisions

The proposed `ProcurementRecommendation` contract has these fields. This is a design record, not an extra model supplied by the repository.

| Field | Type / constraint |
| --- | --- |
| `request_id` | Nonempty string |
| `status` | `pending_human_approval` or `escalate` |
| `supplier_id` | Supplier ID, or null when escalated |
| `total_usd` | Positive integer, or null when escalated |
| `evidence_ids` | List of quote, registry, request, and policy versions used |
| `reasons` | Nonempty list of eligibility reasons or missing evidence |

Cross-field rules: a pending recommendation must identify an eligible supplier and complete evidence; an escalated outcome cannot authorize a purchase. Schema shape alone cannot establish that evidence is authentic or that the eligibility calculation is correct.

| Scenario | Calculation | Outcome |
| --- | --- | --- |
| Base: budget 1,200; deadline 5 days | A passes all four checks. B is late. C is not approved. | Recommend **A, USD 1,100**, pending human approval. Cite `P-001`, `Q-A/v1`, `REG/v1#A`, `PROC/v1`. |
| Budget changes to 1,000; deadline remains 5 days | A exceeds budget; B remains late; C remains unapproved. | **Escalate:** no eligible supplier. Human may revise the request; agents cannot silently relax a constraint. |
| Revised request: budget 1,000; deadline 7 days | B now passes all checks. | Recommend **B, USD 1,000**, pending human approval; retain the revised request version. |
| A's registry evidence is missing in the base case | A's approval status cannot be established; B and C still fail. | **Halt and request evidence.** Do not treat missing evidence as approval. |

**Visible evidence:** the request version, three-row eligibility table, selected evidence IDs, reason for each rejection, and a separate human decision record. A missing approval means no purchase occurs. Repeating a model call does not repair an invalid budget or missing authorization.

**Learner-first prompt:** cover the outcome column at first. Ask learners to apply the four rules, recommend a quote or escalation, and name the evidence they used. Then reveal the table and compare reasoning. Change the budget or deadline only after learners explain the base case; ask what changed and what must remain with a human approver.

## Simulation 2: Enhancing an HR virtual assistant with RAG

**Purpose:** Show how retrieval-augmented generation (RAG) supplies relevant policy text before an answer is drafted. RAG combines retrieval with generation; it does not itself require multiple agents. Here, separate Retriever, Answerer, and Reviewer roles demonstrate how a team can check access, citations, and unsupported claims. See [IBM's RAG explanation](https://www.ibm.com/think/topics/retrieval-augmented-generation) and the [original RAG paper](https://arxiv.org/abs/2005.11401).

### Synthetic policy collection

All records describe a fictional training organization. They are not UN volunteer entitlements, employment advice, or actual personnel records. The requester has `volunteer` access.

| Document / version / section | Status and access | Available policy snippet |
| --- | --- | --- |
| `HR-LEARN/v2/§2` | Current, approved; volunteers | “Volunteers may request up to 3 hours of optional learning time per month.” |
| `HR-BOOK/v1/§1` | Current, approved; volunteers | “Obtain coordinator confirmation before booking a learning session.” |
| `HR-LEARN/v1/§2` | Superseded; volunteers | Excluded from retrieval; it previously stated 1 hour. |
| `HR-REVIEW/v1` | Current; HR reviewers only | Restricted metadata entry; no text is supplied to this requester. |

### Coordination trace

```text
Policy question + requester access
    -> Retriever: current + approved + authorized + relevant snippets
    -> Answerer: draft only claims supported by returned snippets
    -> Reviewer: check each claim, citation, version, and access
    -> Cited answer OR abstention / authorized human referral
```

Retrieval applies access and version filters before supplying snippets to the Answerer. Retrieved content is evidence to inspect, not permission to change tools or instructions. The Reviewer checks whether the cited text actually supports the answer; the presence of a citation is insufficient.

### Typed outcome and deterministic decisions

Proposed `PolicyAnswer` fields: `question: str`, `status: Literal["answered", "abstain", "access_denied"]`, `answer: str | None`, `citations: list[DocumentCitation]`, and `reason: str | None`. Each `DocumentCitation` includes `document_id`, `version`, and `section`. An answered result requires supporting current authorized citations; an abstention or denial requires a reason. This contract is illustrative and is not implemented in the core notebooks.

| Question or changed evidence | Expected outcome |
| --- | --- |
| “How much optional learning time may I request, and what should I do before booking?” | **Answered:** “You may request up to 3 hours per month [`HR-LEARN/v2/§2`]. Obtain coordinator confirmation before booking [`HR-BOOK/v1/§1`].” Reviewer confirms both claims. |
| “Can unused learning time roll over?” | **Abstain:** none of the approved snippets establishes a rollover rule. Refer to the policy owner; do not infer one. |
| Only the superseded `HR-LEARN/v1` is returned | **Abstain:** a current approved source is missing. Do not answer “1 hour.” |
| “Show the HR-reviewer-only internal notes.” | **Access denied:** requester lacks the required access. Do not retrieve or reveal restricted text. |
| Draft says “You automatically receive 3 hours without approval.” | **Reviewer rejects:** the snippets say “may request” and require confirmation. Revise from evidence or abstain. |

**Visible evidence:** question, requester access category, retrieved document/version/section IDs, excluded-source reason, answer-to-source mapping, and Reviewer decision. Do not use real names, CVs, payroll, or individual employment decisions. An unresolved retrieval error can use a bounded retry; missing authority or unsupported policy remains a human referral.

**Learner-first prompt:** do not show the sample answer immediately. Ask learners to draft one sentence and point each claim to a current, authorized source. Have a partner flag any unsupported claim, then ask whether to answer, abstain, or refer. Reveal the expected response only after learners have stated their reasons.

## How these demonstrations connect to the required course

| Current course asset | Procurement connection | HR RAG connection |
| --- | --- | --- |
| [Lab 1: contracts](../notebooks/01_lab_pydantic.ipynb) | Declare recommendation fields and reject incomplete outcomes. | Declare answer status and citation metadata; test valid and invalid fixtures. |
| [Lab 2: team handoff](../notebooks/02_lab_crewai.ipynb) | Give each specialist the request and relevant prior results. | Separate retrieval, drafting, and review; provide only authorized evidence. |
| [Lab 3: tool gates and bounded repair](../notebooks/03_lab_security.ipynb) | Check actions and stop when evidence or approval is absent. | Enforce access at the retrieval boundary; stop unsupported answers and repeated failures. |
| [Capstone: Development to Security](../notebooks/04_capstone.ipynb) | A checked recommendation crossing into approval resembles a validated team boundary. | A drafted answer crossing into review resembles a validated team boundary. |

The notebook exercises implement software-delivery fixtures, not these procurement or HR workflows. Their controls illustrate patterns that could be adapted; passing the course checks does not certify either application for operational use.

Return to the [course dashboard](../README.md) or [resource library](../resources/curated_resource_library.md).

[Course home](../README.md) · [Learner paths](../README.md#learner-paths) · [Slide index](../README.md#main-deck-slide-index)
