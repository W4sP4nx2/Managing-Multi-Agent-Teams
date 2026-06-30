# Solution Guide: Exercise 2.3 MCP Tool Governance

## Expected Behavior

The gateway must authorize every request before tool execution. At minimum, the policy checks:

- Tool is in caller `allowed_tools`.
- Caller trust tier is high enough for requested data sensitivity.
- Caller trust tier is high enough for the tool's required tier.
- Caller role is allowed for the tool.
- External organizations cannot access restricted data.
- Every request creates a structured audit event, including denied requests.

## Strong Answer Indicators

- Denied requests return a typed failure result and never execute handlers.
- Five tools have different sensitivity and role requirements.
- The demo includes at least two allowed and two denied requests.
- `gateway.audit_log` contains an `AuditEvent` for each request.
- The rogue vendor export test ends with `success=False` and `allowed=False`.

## Common Mistakes

1. **Checking only `allowed_tools`**
   - Wrong: allow a tool just because it appears in the caller scope.
   - Right: also check trust tier, data sensitivity, tool-required tier, role, and organization boundary.

2. **Executing tool logic before authorization**
   - Wrong: call the handler and then decide whether to redact the result.
   - Right: deny before the handler runs.

3. **Letting public vendors export restricted reports**
   - Wrong: `vendor_reporter` can call `EXPORT_REPORT` with restricted data.
   - Right: external organizations are denied restricted data even if they have a reporting tool.

4. **Confusing role permission with clearance**
   - Wrong: a `hiring_manager` can issue an offer with confidential clearance.
   - Right: high-impact tools such as `ISSUE_OFFER` require restricted clearance and the correct role.

5. **Printing denial text but still returning sensitive output**
   - Wrong: `success=False` but `output` contains the protected data.
   - Right: denied `ToolResult` has `output=None` and a clear error.

6. **No durable audit event**
   - Wrong: denial appears only as `print("denied")`.
   - Right: `AuditEvent(..., allowed=False, reason="...")` is appended before returning.

## Instructor File

`assignments/starter_code/ex4_governance_matrix_starter.py`
