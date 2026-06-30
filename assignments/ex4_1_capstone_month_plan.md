# Exercise 4.1 Capstone: Production AI Workforce

## Mission

Ship a production-style multi-agent system as an API with typed contracts, governed tools, shared memory, self-repair, routing, audit logs, and monitoring.

## Monthly Build Plan

### Week 1: Agents + Schemas

- Define roles and responsibilities.
- Implement all Pydantic handoff schemas.
- Add invalid-output tests for every schema.
- Produce a happy-path run with typed artifacts.

### Week 2: Memory + Governance

- Add shared memory for decisions, failures, and constraints.
- Implement a zero-trust tool gateway.
- Prove unauthorized tool calls and memory reads are denied.
- Add audit logs for all tool and memory access.

### Week 3: Self-Repair + Routing

- Add bounded retry loop.
- Store repair evidence in memory.
- Implement dynamic routing by complexity, risk, or cost.
- Prove a first failure repairs successfully or escalates.

### Week 4: Deployment + Monitoring

- Expose the system as an API.
- Add structured request/response models.
- Add route, tool, repair, and schema-failure logs.
- Record a demo showing typed contracts, governance, repair, routing, and auditability.

## Success Metric

The final system should show the difference between a demo and a managed workforce:

- Demo: agents pass text and generate a report.
- Production: agents exchange typed artifacts, use governed tools, consult shared memory, repair failures, route dynamically, and leave an audit trail.
