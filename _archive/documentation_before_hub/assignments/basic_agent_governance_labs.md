# Supplemental Governance Practice Exercises

> **Supporting reference material.** This is outside the required three labs and Capstone and adds no course marks. Follow the [current exercise index](index.md) for the assessed path. Historical NB/module labels belong to this supplementary material.

These optional, ungraded practice exercises are separate from the required course path, which remains three guided labs plus one Capstone. Logistics weather, writing, QA, and CEO-direction examples are familiar enough that learners can focus on managing agent behavior with contracts, boundaries, memory, and escalation.

## Optional Exercise 1: Governed Logistics Weather Agent

**Management Principle:** Tool access is a privilege, not a prompt instruction.

**Analogy:** The logistics coordinator asks for a weather risk check before planning a shipment. The MCP gateway is the operations desk: it checks the badge, calls the weather service with a private key, and returns a clean receipt.

**Prompt:** Build a logistics weather-risk assistant that can request weather only through a governed gateway.

**Deliverables:**
- `AgentIdentity` schema with `agent_id`, `role`, and `allowed_tools`.
- `WeatherRequest` schema with `city` and `units`.
- `WeatherResponse` schema with `city`, `temperature`, `condition`, and `shipping_risk`.
- `GovernedMCPGateway.call_tool()` that hides the API key, validates input, enforces scope, and returns a typed response.
- Three tests: authorized `logistics_coordinator` succeeds; unauthorized `external_widget` raises `PermissionError`; a hallucinated field fails schema validation.

**Rubric:**
- Schema enforcement and validation: 35%
- Zero-trust gateway policy: 40%
- Clear audit/test evidence: 25%

## Optional Exercise 2: Bounded Writer Agent

**Management Principle:** Feedback must be structured enough for repair.

**Analogy:** The writer is a junior engineer. The editor is a code reviewer. "Try again" is useless; typed feedback is actionable.

**Prompt:** Build a Researcher → Writer → Editor flow where the Writer reads audience context from shared memory and repairs the draft based on typed editor feedback.

**Deliverables:**
- `DraftSpec` schema.
- `EditorFeedback` schema.
- `SharedMemory` for target audience and last feedback.
- Bounded retry loop with `max_retries_allowed=2`.
- Typed `EscalationTicket` when the loop exhausts retries.

**Rubric:**
- Shared memory and Theory-of-Mind behavior: 30%
- Bounded repair loop correctness: 40%
- Typed escalation and audit trail: 30%

## Optional Exercise 3: Security & Compliance Team Audit

**Management Principle:** A second specialist team should audit only a validated deliverable and return typed evidence.

**Analogy:** The Development Team has completed its change. The Security & Compliance Team receives the approved handoff, checks for known risks, and records a separate release recommendation.

**Prompt:** Build a local Security-Team audit that accepts a Pydantic `DevDeliverable`, checks the code snippet for SQL injection and XSS indicators, and returns `SecurityAuditResult`.

**Deliverables:**
- `DevDeliverable` contract requiring passing tests and a Development-Team signature.
- `SecurityAuditResult` contract with approval, findings, and Security-Team signature.
- Receiving-boundary validation before the Security Team reads the code.
- Tests for rejected untested output, a clean deliverable, and SQL/XSS findings.

**Rubric:**
- Typed handoff and validation: 30%
- Security findings and safe decision: 40%
- Evidence and audit trail: 30%

## Optional Exercise 4: CEO-Directed Project Planning

**Management Principle:** Natural language can steer the team, but structured state governs the team.

**Analogy:** The CEO uses the steering wheel. TeamLog is the control cable. The engine room should never rely on raw spoken intent.

**Prompt:** Build a minimal governed planning session where a human directive becomes a typed project plan, a mid-flight change updates TeamLog, and the Coder reads governed memory instead of raw text.

**Deliverables:**
- `ProjectPlan` schema.
- `TeamCommitment` schema.
- `HumanReviewDecision` schema.
- Scripted session with initial instruction and mid-flight database change.
- Test proving the Coder uses the updated TeamLog commitment.

**Rubric:**
- Natural-language-to-schema mapping: 30%
- Commitment updates and memory routing: 35%
- Human approval/rejection gate: 35%
