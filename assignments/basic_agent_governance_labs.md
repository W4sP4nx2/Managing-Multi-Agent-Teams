# Basic Agent Governance Labs

These labs look simple on purpose. Logistics weather, writing, QA, and CEO-direction examples are familiar enough that learners can focus on the real course objective: managing agent behavior with contracts, boundaries, memory, and escalation.

## Lab 1: Governed Logistics Weather Agent

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

## Lab 2: Bounded Writer Agent

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

## Lab 3: Adversarial QA Agent

**Management Principle:** A2A messages must be treated as untrusted external traffic.

**Analogy:** QA is not only clicking buttons. QA is the red team testing whether the city gate actually closes.

**Prompt:** Build an external Red Team QA agent that sends adversarial payloads to an internal defender gateway.

**Deliverables:**
- `AdversarialPayload` schema.
- `SecurityIncidentTicket` schema.
- `A2ADefenderGateway.process_request()` with prompt-injection, data-exfiltration, and role-violation checks.
- Dead Letter Queue entry for each denied message.
- Tests for one normal functional test and two blocked adversarial payloads.

**Rubric:**
- A2A contract design: 30%
- Threat classification and blocking: 40%
- Incident ticket and DLQ auditability: 30%

## Lab 4: Vibe Coding CEO Interface

**Management Principle:** Natural language can steer the team, but structured state governs the team.

**Analogy:** The CEO uses the steering wheel. TeamLog is the control cable. The engine room should never rely on raw spoken intent.

**Prompt:** Build a minimal Vibe Coding session where a human directive becomes a typed project plan, a mid-flight change updates TeamLog, and the Coder reads governed memory instead of raw text.

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
