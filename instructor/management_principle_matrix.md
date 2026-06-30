# Management Principle Matrix

Use this matrix to keep the course anchored on managing multi-agent teams, not merely implementing agent code.

| Scenario | Management Principle | Business Impact If Missing | Code Evidence | Assessment Question |
| --- | --- | --- | --- | --- |
| MCP Zero-Trust Tool Boundary | Resource allocation and least-privilege access | Unauthorized tools can trigger refunds, offers, exports, or restricted data leaks | `ToolGateway.call()` denies the rogue vendor and appends `AuditEvent(allowed=False)` | Can the learner design a tool policy where QA can read test results but cannot issue refunds or offers? |
| Agentic RAG and Theory of Mind | Context delegation with need-to-know memory | Agents forget constraints or retrieve sensitive secrets they should not see | Coder retrieves PostgreSQL constraint but receives 0 password records | Can the learner explain how an agent discovers teammate knowledge without seeing all memory? |
| TeamLog Collective Commitment | Mission alignment and global constraint enforcement | Agents pass local tasks while violating enterprise rules such as offline-only execution | `check_teamlog_commitments()` blocks `CALL_EXTERNAL_API` under a no-network commitment | Can the learner decide where global rules belong and prove they override local agent goals? |
| ChatDev Bounded Self-Repair | Quality control with bounded autonomy | Broken code ships, or agents loop forever and burn budget | `run_company()` returns `PullRequestSummary(status="SHIPPED" or "ESCALATED_TO_HUMAN")` | Can the learner define when to retry, when to switch strategy, and when to escalate? |
| Fugu Dynamic Routing | Work allocation by risk, complexity, latency, and cost | Every task goes to an expensive model, or high-risk tasks go to weak workers | NB6 logs `RouteTraceRecord` and cost savings versus static reasoning routing | Can the learner justify why a task used fast, code-specialist, balanced, or reasoning workers? |
| API Boundary and Async Orchestration | External intake governance and non-blocking work management | Messy webhooks hit internal agents directly, or slow workflows block HTTP clients | NB8 maps API keys to identity, returns `202 Accepted`, and exposes `GET /tasks/{task_id}` polling | Can the learner explain why the API gateway is the governance perimeter? |
| Enterprise A2A Perimeter | Cross-organization trust negotiation and message quarantine | Internal agents can leak PII to vendors, accept schema drift, or send restricted data to the public internet | NB11 blocks PII and hallucinated schemas, then writes denials to a Dead Letter Queue | Can the learner explain why A2A messages need identity, classification, schema checks, and audit trails? |
| Governed Logistics Weather Agent | Tool access through a least-privilege gateway | API keys leak into prompts or unauthorized widgets call privileged tools such as shipment cancellation | NB1 builder exercise validates `WeatherRequest`, returns `WeatherResponse`, and blocks `external_widget` | Can the learner explain why even a simple weather-risk call belongs behind a gateway? |
| Bounded Writer Agent | Structured feedback and retry budgets | Writer/editor loops become blind retries with no evidence or stop condition | NB5 builder exercise feeds `EditorFeedback` into repair and returns `EscalationTicket` on exhaustion | Can the learner distinguish repair from retry? |
| Adversarial QA Agent | A2A defense and incident escalation | External QA payloads inject prompts, exfiltrate data, or bypass role boundaries | NB11 builder exercise returns `SecurityIncidentTicket` and quarantines denied payloads | Can the learner classify a malicious payload without debating with it? |
| Vibe Coding CEO Builder | Human steering through TeamLog, not raw prompts | Human changes bypass commitments and downstream agents act on stale instructions | NB10 builder exercise updates `ProjectPlan` and `TeamCommitment` before the Coder acts | Can the learner show where natural language becomes governed state? |
| CrewAI Framework Bridge | Framework orchestration with explicit governance ownership | Teams adopt a framework and accidentally drop schema, policy, audit, and approval controls | `crewai_learning/README.md` teaches role clarity, context chains, process selection, guardrails, failure recovery, and clean delivery | Can the learner decide when to use custom orchestration, CrewAI, or a hybrid governed framework? |
| Homework A: Specialist Agent Skills | Specialist capability development | The team is well-governed but every specialist is mediocre | Specialist agents emit typed quality, test, security, and documentation artifacts | Can the learner prove each agent is good at its role, not merely present in the workflow? |
| Homework B: Production Controls | Human oversight, evaluation, cost control, and memory lifecycle | Agents act without approval, cannot be measured, overspend, or accumulate stale memory | Approval, benchmark, cache, and forgetting homework | Can the learner measure and control a deployed agent's behavior over time? |
| Homework C: Deployment and Operations | Operational accountability | The system works in notebooks but cannot be deployed, observed, sandboxed, or rolled back | Container, observability, sandbox, and version-control homework | Can the learner operate the system safely after it leaves the classroom? |

## Notebook Exercise Narrative Standard

The current notebook phase uses a consistent Andrew Ng-style teaching pattern:

| Element | Instructor Purpose | Learner Check |
| --- | --- | --- |
| The Story | Ground the technical pattern in a believable production failure | Can the learner explain what can go wrong in the real world? |
| Your Mission | Turn the failure into a focused implementation task | Can the learner change the system and produce evidence? |
| The Takeaway | Connect the implementation back to managing an AI workforce | Can the learner name the management principle, not just the code mechanic? |

Apply this standard to NB1, NB2, NB3, NB4, NB5, NB6, NB8, and NB10. NB11 uses the same management principle standard, but its exercise section is framed as an enterprise perimeter and red-team lab.

## Instructor Rule

For every lab, ask learners to answer in one sentence:

> What management failure does this technical pattern prevent?

If they cannot answer that, they have learned the code but not the course.
