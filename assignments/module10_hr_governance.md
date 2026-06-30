# Homework D: HR Governance Track

## Mission

Build HR multi-agent workflows that can handle PII, protected-class proxy signals, compensation actions, and audit requirements without letting autonomous agents make irreversible decisions.

Starter code: `assignments/starter_code/module10_hr_governance_starter.py`

Instructor guide: `instructor/solutions/module10_solution_guide.md`

## Engineering Reality

HR agents process resumes, performance data, compensation records, protected-class proxies, and employment decisions. A hallucination, unredacted handoff, or over-scoped tool call is not a small model error. It is a compliance failure.

## Management Principle

High-stakes agent teams require separation of duties. The Resume Parser can extract information, the Bias Checker can evaluate anonymized evidence, and the Payroll or HRIS tool must sit behind explicit human approval.

## Exercise HR-1: PII Redaction and Bias-Check Pipeline

Prompt: Implement a governed HR handoff where resume parsing, PII redaction, and candidate evaluation are separated by strict Pydantic contracts and an MCP-style tool gateway.

### Scenario

The `ResumeParserAgent` extracts skills from a resume PDF. The `BiasCheckerAgent` evaluates the candidate. The parser accidentally includes the candidate's name and graduation year in the handoff, introducing illegal proxy-discrimination signals into the scoring model.

### The Trap

The naive pipeline sends the parser's raw output directly to `EVALUATE_CANDIDATE`. The model may score based on name, school year, age proxy, address, or other non-job-related signals.

### Engineer Task

Design a `CandidateProfile` schema that strictly separates `anonymized_skills` from `pii_quarantine`. Implement an MCP Tool Gateway rule: `EVALUATE_CANDIDATE` must reject any request where the payload contains unredacted PII.

Required schema shape:

```python
class CandidateProfile(StrictModel):
    candidate_id: str
    anonymized_skills: list[str]
    pii_quarantine: dict[str, str] = Field(default_factory=dict)
    redaction_complete: bool = False
```

Required policy behavior:

```python
class ToolPolicy:
    def authorize(self, request: ToolRequest) -> bool:
        if request.tool == ToolName.EVALUATE_CANDIDATE:
            profile = CandidateProfile.model_validate(request.args["profile"])
            if profile.pii_quarantine or not profile.redaction_complete:
                return False
        return True
```

### Deliverables

- `CandidateProfile` Pydantic schema with `anonymized_skills`, `pii_quarantine`, and `redaction_complete`.
- `ToolName.REDACT_PII` and `ToolName.EVALUATE_CANDIDATE` in the local MCP-style gateway.
- A `RedactPII` tool that moves names, emails, phone numbers, addresses, and graduation years into `pii_quarantine`.
- A `BiasCheckerAgent` that only receives profiles with `redaction_complete=True` and empty `pii_quarantine`.
- Unit test proving the parser's raw output is blocked at the MCP boundary.
- Integration test proving the parser can invoke `REDACT_PII`, then successfully hand off the cleaned profile.
- Audit log showing the denied raw evaluation and the later approved redacted evaluation.

### Technical Constraints

- Do not pass raw resume text to the evaluator.
- Do not silently drop PII; quarantine it for audit.
- The evaluator must reject unknown fields through `extra="forbid"`.
- `EVALUATE_CANDIDATE` must not execute if `pii_quarantine` is non-empty.
- The denial must be machine-checkable through `ToolResult.success=False` or a raised `PermissionError`.

### Required Tests

- `test_raw_candidate_profile_blocked_by_gateway`
- `test_redact_pii_tool_quarantines_protected_signals`
- `test_redacted_profile_can_be_evaluated`
- `test_audit_log_records_denied_and_allowed_events`

### Grading Rubric

- PII schema separation and strict validation: 30%
- MCP gateway denial and auditability: 30%
- Redaction tool behavior and test coverage: 25%
- Management explanation of bias-risk reduction: 15%

## Exercise HR-2: HITL Promotion Gateway

Prompt: Add a human-in-the-loop approval gate before an HR agent can trigger compensation or payroll-changing actions.

### Scenario

The `PerformanceAgent` analyzes metrics and recommends a promotion. The system must not autonomously trigger `UPDATE_PAYROLL`.

### The Trap

The naive workflow maps `next_action="promote"` directly to a payroll update tool. A model hallucination can become a compensation change.

### Engineer Task

Design a `HumanApprovalRequest` schema. When `ReviewDecision.next_action == "promote"`, the system must emit an approval request and pause the orchestration loop. The workflow may only resume if a mock human webhook returns `status="approved"`.

Required schema shape:

```python
class HumanApprovalRequest(StrictModel):
    request_id: str
    employee_id: str
    proposed_action: Literal["promote", "compensation_change"]
    rationale: str
    risk_level: Literal["medium", "high"]
    requested_by_agent: str
    status: Literal["pending", "approved", "rejected"] = "pending"
```

### Deliverables

- `ReviewDecision` schema with `next_action: Literal["no_action", "coach", "promote"]`.
- `HumanApprovalRequest` and `HumanDecision` schemas.
- State graph or explicit orchestration loop with states: `ANALYZE`, `REVIEW`, `PENDING_APPROVAL`, `APPROVED_EXECUTION`, `REJECTED`, `DONE`.
- Audit event created when execution is suspended.
- Mock webhook handler that accepts or rejects approval by `request_id`.
- Test proving `UPDATE_PAYROLL` is not called while approval is pending.
- Test proving the loop resumes only after `status="approved"`.

### Technical Constraints

- The payroll tool must require a human decision ID.
- Pending approval must be durable in a task store or approval store.
- Rejected approvals must terminate the payroll path.
- The audit trail must include the proposed action, approving human, timestamp, and final decision.
- The system must be deterministic in offline mode.

### Required Tests

- `test_promote_action_creates_approval_request`
- `test_payroll_tool_blocked_without_human_approval`
- `test_mock_human_webhook_approval_resumes_flow`
- `test_rejected_approval_terminates_payroll_path`

### Grading Rubric

- HITL state design and safe suspension: 35%
- Typed approval contracts and payroll gating: 30%
- Audit trail completeness: 20%
- Test coverage for approve and reject paths: 15%

## Instructor Delivery Pattern

Start with the naive path: raw resume output goes to evaluation, and `promote` goes straight to payroll. Then introduce the governance interventions: PII quarantine, bias-safe handoff, and human approval. End by showing the production reality: HR agents can assist, but policy and humans retain authority over sensitive data and irreversible actions.
