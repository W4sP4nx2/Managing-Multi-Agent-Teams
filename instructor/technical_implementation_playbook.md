# Instructor Technical Implementation Playbook

This playbook aligns the instructor narrative with the current runnable course files. Use it to teach the difference between a toy multi-agent demo and a managed AI workforce.

## Delivery Pattern

For every technical module, teach the same three-beat progression:

1. Naive approach: show the failure without governance.
2. Intervention: introduce the management pattern.
3. Production reality: run the governed implementation and show the failure handled safely.

Each scenario must answer four instructor questions:

- What management principle does this teach?
- What business impact does the principle prevent?
- How do we assess understanding of the principle?
- What analogy makes the principle obvious before code?

## 1. MCP: Zero-Trust Tool Boundary

### Management Principle

Resource allocation and access control. A manager must decide who gets which tools, under what conditions, and with which data. Not every team member needs every tool.

### Business Impact

Without this control, an external vendor agent could export restricted HR data or a resume parser could issue an offer. The failure mode is not a bad answer; it is a compliance breach, financial loss, or unauthorized business action.

### Current Files

- Learner prompt: `assignments/ex2_3_mcp_tool_governance.md`
- Runnable starter: `assignments/starter_code/ex4_governance_matrix_starter.py`
- Notebook: `notebooks/03_mcp_tool_gateway.ipynb`
- Solution guide: `instructor/solutions/ex2_3_mcp_tool_governance_solution_guide.md`

### Technical Implementation

Instructor scenario: The Rogue Agent Test.

```python
vendor = AgentIdentity(
    agent_id="vendor-001",
    organization="external_vendor",
    role="vendor_reporter",
    trust_tier=TrustTier.PUBLIC,
    allowed_tools={Tool.EXPORT_REPORT},
    public_key_ref="did:example:vendor-001",
)

gateway = ToolGateway()
request = ToolRequest(
    caller=vendor,
    tool=Tool.EXPORT_REPORT,
    args={"name": "restricted_hiring_audit"},
    data_sensitivity=TrustTier.RESTRICTED,
)

result = gateway.call(request)
assert result.success is False
assert gateway.audit_log[-1].allowed is False
```

### Assessment Question

Your QA agent needs to read test results but should never issue refunds or release offers. Design the tool policy. What happens if you accidentally give QA the high-impact tool but only confidential clearance?

Strong answer: the learner separates tool scope, role permission, trust tier, data sensitivity, and audit logging. They explain why any one check alone is insufficient.

### Teaching Script

In a human team, you do not give every contractor the keys to payroll, legal records, and production systems. In an AI team, you do not give the `resume_parser` the ability to issue offers. MCP gives tools a standard doorway; zero-trust policy decides who is allowed through that doorway.

## 2. Agentic RAG and Theory of Mind: Governed Shared Memory

### Management Principle

Context delegation and need-to-know memory. A manager ensures the right person can recover the right context at the right time, while preventing unnecessary exposure of sensitive information.

### Business Impact

Without governed memory, agents either forget important constraints or over-share sensitive context. The coder may miss the PM's PostgreSQL requirement, while another agent may accidentally retrieve a production password.

### Current Files

- Learner prompt: `assignments/ex2_tom_memory.md`
- Starter/solution: `assignments/starter_code/ex2_memory_system_starter.py`
- Notebook: `notebooks/02_shared_rag_memory.ipynb`

### Technical Implementation

Instructor scenario: The Invisible Handoff.

```python
memory.add(MemoryRecord(
    author=Role.PM,
    visible_to={Role.CODER},
    sensitivity=Sensitivity.CONFIDENTIAL,
    tags={"architecture", "storage"},
    text="Use PostgreSQL for persistent storage.",
))

memory.add(MemoryRecord(
    author=Role.SECURITY,
    visible_to={Role.SECURITY},
    sensitivity=Sensitivity.RESTRICTED,
    tags={"password"},
    text="Production DB password: super_secret_123",
))

assert len(memory.search("password", Role.CODER)) == 0
assert len(memory.search("password", Role.SECURITY)) == 1
```

### Assessment Question

The PM knows the system must use PostgreSQL, but the coder receives only "build persistence." How should the coder discover the constraint without being handed every memory record? What should happen when the coder searches for "password"?

Strong answer: the learner designs visibility, sensitivity, tags, retrieval, and denial behavior. They explain that Theory of Mind is not unlimited mind-reading; it is authorized inference about what teammates know.

### Teaching Script

In a well-run human team, a project manager does not repeat every constraint in every meeting. The team has a shared source of truth. But that source of truth still has permissions. Agentic RAG is the shared source of truth; Theory of Mind is the agent knowing which teammate's knowledge should influence its next move.

## 3. TeamLog: Collective Commitment Engine

### Management Principle

Mission alignment and global constraints. A manager must make team-level commitments stronger than local task incentives. Local success is not success if it violates the mission.

### Business Impact

Without TeamLog commitments, a coder can satisfy a local ticket while breaking enterprise rules. For example, code may pass tests but call an external API even though the product must run offline for compliance or customer deployment reasons.

### Current Files

- Core implementation: `src/enterprise_agent_team.py`
- Design exercise: `assignments/foundational_architecture_design.md`
- Capstone: `assignments/starter_code/ex5_capstone_starter.py`

### Technical Implementation

Instructor scenario: Scope Creep Prevention.

```python
commitment = TeamCommitment(
    owner=AgentRole.PRODUCT_MANAGER,
    commitment="All code must run offline. No external network calls.",
    visible_to={AgentRole.CODER, AgentRole.QA},
    sensitivity=TrustTier.CONFIDENTIAL,
)

coder = AgentIdentity(
    agent_id="coder-001",
    role=AgentRole.CODER,
    org_id="training",
    scopes={ToolName.CALL_EXTERNAL_API},
    clearance=TrustTier.CONFIDENTIAL,
)

request = ToolRequest(
    caller=coder,
    tool=ToolName.CALL_EXTERNAL_API,
    args={"url": "https://api.example.com"},
    data_sensitivity=TrustTier.CONFIDENTIAL,
)

check_teamlog_commitments(request, [commitment])
```

Expected result: `check_teamlog_commitments` raises `PermissionError` with the commitment text.

### Assessment Question

A coder produces a clever implementation that passes all tests but violates "No external network calls." Should QA approve it? Where should this rule live: in the prompt, in the tool policy, in memory, or as a TeamLog commitment?

Strong answer: the learner explains that global commitments must be explicit, visible to relevant roles, and enforced before tool execution or release.

### Teaching Script

In a human company, a brilliant engineer is still not allowed to ignore legal, security, or customer commitments. TeamLog is how we encode those team promises. It keeps the agent from saying, "My local task passed," when the actual team mission failed.

## 4. ChatDev Self-Repair: Bounded Quality Loop

### Management Principle

Quality control with bounded autonomy. A manager should allow workers to correct mistakes, but must define when repeated failure becomes an escalation.

### Business Impact

Without a repair loop, broken first drafts ship. Without a retry budget, agents can loop forever, burn API credits, block releases, and hide the fact that human judgment is needed.

### Current Files

- Notebook: `notebooks/05_self_repair_loop.ipynb`
- Capstone starter: `assignments/starter_code/ex5_capstone_starter.py`
- Capstone solution guide: `instructor/solutions/ex5_capstone_solution_guide.md`

### Technical Implementation

Instructor scenario: The Infinite Loop Trap.

```python
summary = run_company("Create a slugify(text) utility with tests.", max_repairs=0)
assert summary.status in {"SHIPPED", "ESCALATED_TO_HUMAN"}
```

For a forced-failure variant, make `code()` keep returning an invalid implementation or make `run_tests()` always fail. With `max_repairs=2`, the system must stop after exactly 3 total attempts and return `status="ESCALATED_TO_HUMAN"`.

### Assessment Question

Your coding agent fails the same test three times. Should the system keep retrying, switch models, ask a human, or ship with a warning? What evidence should be preserved for the next reviewer?

Strong answer: the learner defines a retry budget, stores failure evidence, prevents silent shipping, and returns a typed escalation artifact.

### Teaching Script

A good engineering manager does not fire someone after the first failed test, but also does not let them work forever with no progress. ChatDev-style repair gives agents a chance to improve. The retry budget turns autonomy into managed autonomy.

## 5. API Boundary: Governance Perimeter and Async Orchestration

### Management Principle

External intake governance. A manager must control how outside requests enter the team, who is allowed to request work, and how long-running work is tracked without blocking the requester.

### Business Impact

Without an API boundary, messy webhooks, Slack commands, and A2A requests can hit internal agents directly. The result is schema drift, unauthorized high-risk work, blocked HTTP clients, and no reliable task status for external systems.

### Current Files

- Notebook: `notebooks/08_api_boundaries_async_orchestration.ipynb`
- Capstone prompt: `assignments/ex5_capstone_virtual_software_company.md`
- Capstone starter TODO: `assignments/starter_code/ex5_capstone_starter.py`

### Technical Implementation

Instructor scenario: The Customs Border.

```python
response = client.post(
    "/tasks",
    json={
        "github_issue_url": "https://github.com/org/repo/issues/42",
        "priority": "high",
        "requester_email": "pm@company.com",
    },
    headers={"Authorization": "Bearer sk-internal-admin"},
)
assert response.status_code == 202

blocked = client.post(
    "/tasks",
    json={
        "github_issue_url": "https://github.com/external/repo/issues/7",
        "priority": "high",
        "requester_email": "vendor@external.com",
    },
    headers={"Authorization": "Bearer sk-external-vendor"},
)
assert blocked.status_code == 403
```

### Assessment Question

A GitHub webhook, Slack command, and external vendor A2A call all request work from your agent team. Which fields are accepted at the API boundary, how is identity determined, and why should the endpoint return `202 Accepted` instead of waiting for the whole agent workflow to finish?

Strong answer: the learner maps API keys to identities, rejects unauthorized risk escalation, validates raw payloads into strict internal contracts, starts background work, and exposes polling through `GET /tasks/{task_id}`.

### Teaching Script

In a human company, the front desk does not let every visitor walk directly into engineering, legal, or finance. The API gateway is that front desk. It authenticates the visitor, checks what they are allowed to request, writes down the work order, and gives them a tracking number while the team does the work.

## 6. Basic Agent Governance Labs: Logistics Weather, Writer, QA, and CEO

### Management Principle

Familiar agent examples should still teach managed autonomy. A logistics weather-risk agent, Writer Agent, QA Agent, or CEO interface becomes course-aligned only when it includes identity, typed contracts, governed tools, memory, bounded repair, A2A defense, or human approval.

### Business Impact

Without this framing, learners confuse "agent can call an API" with "agent can be trusted in production." The business failures are familiar: leaked API keys, unbounded writing retries, prompt-injection acceptance, and raw human instructions bypassing TeamLog commitments.

### Current Files

- Handout: `assignments/basic_agent_governance_labs.md`
- NB1 exercise: `notebooks/01_hello_multi_agent.ipynb`
- NB5 exercise: `notebooks/05_self_repair_loop.ipynb`
- NB10 exercise: `notebooks/10_vibe_coding_interface.ipynb`
- NB11 exercise: `notebooks/11_enterprise_a2a_perimeter.ipynb`
- Solution guide: `instructor/solutions/basic_agent_governance_labs_solution_guide.md`

### Technical Implementation

Instructor scenario: The Builder Ladder.

| Lab | Naive Demo | Governance Upgrade | Evidence |
| --- | --- | --- | --- |
| Logistics Weather | Agent calls a weather API directly | Gateway hides API key, checks identity, validates `WeatherRequest` and `WeatherResponse` | Authorized call succeeds; external widget raises `PermissionError`; hallucinated fields fail validation |
| Writer | Writer retries until editor accepts | Editor emits typed feedback; loop stops with `EscalationTicket` | First draft fails; second uses feedback; forced failure escalates |
| QA | QA sends free-form test text | A2A gateway blocks prompt injection and exfiltration payloads | `SecurityIncidentTicket` plus Dead Letter Queue entry |
| CEO | Human prompt directly reaches coder | Manager converts language into `ProjectPlan` and `TeamCommitment` | Mid-flight MongoDB change is read from TeamLog |

### Assessment Question

Pick one familiar agent example and identify the management boundary. What data contract crosses the boundary? Who is authorized to call it? What happens when the request is invalid, unauthorized, or repeatedly failing?

Strong answer: the learner names the schema, the policy gate, the audit evidence, and the escalation path. They do not describe the lab as "just a tool call" or "just prompting."

### Teaching Script

Logistics weather, writing, QA, and CEO examples are intentionally simple. That is the point. We remove domain complexity so learners can see the management skeleton: identity, contracts, boundary, evidence, and stop condition. Once they can govern a weather-risk call, they are ready to govern a capstone tool call.

## Advanced Expansion Roadmap

The core course teaches managed agents. The advanced track teaches skilled and operated agents.

| Module | Purpose | Assignment File |
| --- | --- | --- |
| 7. Individual Agent Skill Development | Make each specialist good at its job. | `assignments/module7_individual_agent_skills.md` |
| 8. Production-Ready Agent Features | Add HITL, benchmarks, cost control, and long-term memory. | `assignments/module8_production_ready_agent_features.md` |
| 9. Agent Deployment & Operations | Deploy, observe, sandbox, and version agents. | `assignments/module9_deployment_operations.md` |
