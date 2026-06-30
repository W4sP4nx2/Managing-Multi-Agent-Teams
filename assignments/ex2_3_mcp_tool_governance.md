# Exercise 2.3: MCP Tool Governance

## Mission

Build a zero-trust tool gateway where every agent tool call is authorized before execution.

## Business Problem

Customer service agents need tools: knowledge base lookup, customer profiles, refunds, security logs, and reports. Without governance, a support agent could issue refunds or a vendor could read restricted audit data.

## Required Tools

- `READ_PUBLIC_KB`
- `READ_CUSTOMER_PROFILE`
- `ISSUE_REFUND`
- `READ_SECURITY_LOGS`
- `EXPORT_REPORT`

## Deliverables

1. Implement `GovernancePolicy.authorize()` in `assignments/starter_code/ex4_governance_matrix_starter.py`.
2. Define sensitivity requirements for each tool.
3. Define role restrictions for each tool.
4. Implement a gateway that authorizes first and executes second.
5. Demonstrate at least two denied requests and two allowed requests.
6. Add an `AuditEvent` record for every request with `allowed=True` or `allowed=False`.

## Rogue Agent Test

Create a vendor identity with `trust_tier=TrustTier.PUBLIC`, `organization="external_vendor"`, and `allowed_tools={Tool.EXPORT_REPORT}`. Submit a `ToolRequest` for `Tool.EXPORT_REPORT` with `data_sensitivity=TrustTier.RESTRICTED`.

Expected result:

- `gateway.call(request).success` is `False`.
- The tool handler does not execute.
- `gateway.audit_log[-1].allowed` is `False`.
- The audit reason explains either clearance denial or the external organization boundary.

## Technical Constraints

- Every request must include caller identity, tool name, args, and data sensitivity.
- Tool scope, trust tier, role, and external organization checks must all be enforced.
- Denied requests must not execute the tool handler.
- The audit log must be structured data, not only printed text.

## Grading Rubric

- Correct zero-trust authorization logic: 45%
- Tool sensitivity and role model quality: 25%
- Working allowed/denied demonstrations: 15%
- Structured audit log with denial evidence: 15%
