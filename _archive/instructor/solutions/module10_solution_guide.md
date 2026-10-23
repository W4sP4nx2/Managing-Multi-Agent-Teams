# Homework D Solution Guide: HR Governance Track

## Strong Answer Indicators

- `CandidateProfile` separates anonymized skills from `pii_quarantine`.
- `EVALUATE_CANDIDATE` rejects profiles with non-empty PII quarantine.
- Redaction preserves quarantined PII for audit instead of deleting it silently.
- Promotion and payroll actions require a typed human approval request.

## Common Mistakes

- Passing raw resume text to the evaluator.
- Dropping PII with no audit record.
- Letting `next_action="promote"` call payroll directly.
- Treating graduation year as harmless even though it can be an age proxy.

## Minimum Passing Evidence

- Raw parser output blocked at MCP boundary.
- Redacted profile accepted after PII quarantine is empty.
- Pending approval blocks payroll.
- Approved mock webhook resumes execution.
