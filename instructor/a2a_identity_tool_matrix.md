# A2A Identity and Tool Matrix

This is the matrix of truth for agent identity, trust tier, and tool scope across the course. Use it when updating notebooks, starter code, or tests.

## Core Software Team

| Role | Common Identifier | Trust Tier | Allowed Tools | Appears In |
| :--- | :--- | :--- | :--- | :--- |
| Product Manager | `product_manager`, `pm` | confidential | `search_memory` | `src/enterprise_agent_team.py`, Ex5, NB10 |
| Coder | `coder` | confidential | `search_memory`, `write_patch` | `src/enterprise_agent_team.py`, NB5, Ex5 |
| QA | `qa` | confidential | `search_memory`, `execute_tests`, `run_tests` | `src/enterprise_agent_team.py`, NB5, Ex5 |
| Security Reviewer | `security_reviewer`, `security` | restricted | `security_scan`, `read_security_logs`, `export_report` | Ex4, Ex5, Homework D |
| Release Manager | `release` | confidential | release summary only, no raw execution | Ex5 |
| Human | `human`, `ceo` | restricted decision authority | approval/rejection, escalation handling | NB10, Homework B, Homework D |

## HR Governance Team

| Role | Trust Tier | Allowed Tools | Denied Tools | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `resume_parser` | confidential | `READ_RESUME`, `READ_POLICY`, `REDACT_PII` | `ISSUE_OFFER`, `UPDATE_PAYROLL` | May extract PII but must quarantine before evaluation |
| `bias_checker` | confidential | `READ_POLICY`, `RUN_BIAS_CHECK`, `EVALUATE_CANDIDATE`, `EXPORT_REPORT` | `UPDATE_PAYROLL` | Must not receive unredacted PII |
| `hiring_manager` | confidential | `READ_RESUME`, `EXPORT_REPORT`, sometimes `ISSUE_OFFER` | restricted security logs | Offer actions should be gated by policy |
| `vendor_reporter` | public | `READ_POLICY`, limited `EXPORT_REPORT` | restricted data, `UPDATE_PAYROLL`, `EVALUATE_CANDIDATE` | External org boundary applies |
| `payroll_admin` | restricted | `UPDATE_PAYROLL` with human approval | direct agent-triggered payroll without approval | Used in HITL exercises |

## Marketing Team

| Role | Trust Tier | Allowed Tools | Governance Rule |
| :--- | :--- | :--- | :--- |
| Campaign Manager | confidential | routing request, campaign planning | Must pass budget preflight |
| Social Media Agent | confidential | draft generation | Cannot publish directly |
| Brand Safety Scanner | restricted | trademark list, policy scan | Restricted trademark memory must not leak |
| Publisher | restricted | `POST_TO_SOCIAL` | Requires passing `ReviewDecision.next_action == "publish"` |

## Canonical Trust Tiers

| Tier | Level | Use |
| :--- | :--- | :--- |
| `public` | 0 | External vendor, non-sensitive reference material |
| `confidential` | 1 | Internal task, candidate, campaign, and engineering context |
| `restricted` | 2 | Credentials, security logs, payroll, protected governance resources |

## Canonical Tool Names by Context

| Context | Tool Names |
| :--- | :--- |
| Software team | `SEARCH_MEMORY`, `WRITE_PATCH`, `EXECUTE_TESTS`, `READ_REPO`, `CALL_EXTERNAL_API` |
| Capstone starter | `SEARCH_MEMORY`, `WRITE_PATCH`, `RUN_TESTS`, `SECURITY_SCAN` |
| HR governance | `READ_RESUME`, `READ_POLICY`, `RUN_BIAS_CHECK`, `ISSUE_OFFER`, `READ_SECURITY_LOGS`, `EXPORT_REPORT`, `REDACT_PII`, `EVALUATE_CANDIDATE`, `UPDATE_PAYROLL` |
| Marketing | `ROUTE_CAMPAIGN_TASK`, `BRAND_SAFETY_SCAN`, `POST_TO_SOCIAL` |

## Drift Rules

- If a tool enum is renamed, update the gateway handler in the same edit.
- If a role string changes, update all tests that construct `AgentIdentity`.
- If a trust tier is added, update every tier ordering dictionary.
- If a notebook uses a simplified enum, say so in the markdown cell before the code.
