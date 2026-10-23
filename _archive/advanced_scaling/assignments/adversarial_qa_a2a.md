# Archived Advanced Exercise: Adversarial QA over A2A

This extension sends an external Red Team payload across an organization boundary. It is not part of the two-day workshop. The core Capstone has a separate Security & Compliance Team inside one workflow and uses a Pydantic `DevDeliverable` handoff.

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
