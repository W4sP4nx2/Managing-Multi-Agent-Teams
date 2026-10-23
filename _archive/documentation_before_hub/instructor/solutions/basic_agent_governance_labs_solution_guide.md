# Supplemental Governance Practice Exercises: Solution Guide

Use this guide for optional, ungraded practice with the Logistics Weather, Writer, QA, and CEO-directed planning scenarios. The required course path remains three guided labs plus one Capstone.

## Strong Answer Indicators

- The learner uses Pydantic models for every boundary artifact instead of raw dictionaries.
- The learner separates agent identity from tool authorization.
- The learner keeps API keys and privileged actions inside gateways, never inside prompts.
- The learner records audit evidence for denied, repaired, or escalated paths.
- The learner can explain the management principle in one sentence.

## Optional Exercise 1: Governed Logistics Weather Agent

Expected evidence:

- `AgentIdentity(role="logistics_coordinator")` can call `get_weather`.
- `AgentIdentity(role="external_widget")` cannot call `get_weather`.
- `WeatherRequest` rejects unsupported units or extra fields.
- `WeatherResponse` includes `shipping_risk` and rejects invented fields.
- The API key is stored only in the gateway or environment-backed adapter.

Common mistakes:

1. Returning a loose `dict` instead of `WeatherResponse`.
2. Checking only `allowed_tools` but not the gateway policy.
3. Exposing the API key in an agent prompt or notebook output.
4. Letting the LLM invent fields such as `vibes` or `recommendation`.

## Optional Exercise 2: Bounded Writer Agent

Expected evidence:

- The Writer reads `target_audience` from shared memory.
- The Editor returns `EditorFeedback`, not a string.
- The second attempt uses the previous feedback.
- Forced failure returns a typed `EscalationTicket`.
- The loop has a strict retry budget.

Common mistakes:

1. Treating repair as blind retry.
2. Losing editor feedback between attempts.
3. Allowing `while True` repair loops.
4. Returning `"failed"` instead of a typed escalation artifact.

## Optional Exercise 3: Security & Compliance Team Audit

Expected evidence:

- The Security Team receives a `DevDeliverable`, not raw unvalidated text.
- Pydantic rejects deliverables that did not pass QA.
- The receiving team revalidates the contract before inspecting the code.
- SQL/XSS indicators return a typed `SecurityAuditResult` with findings and `approved=False`.
- A clean, tested deliverable returns an approved result with an audit signature.

Common mistakes:

1. Starting the Security Team from raw coder text.
2. Ignoring the test-status field or team signature.
3. Returning a plain string instead of `SecurityAuditResult`.
4. Letting the Security Team rewrite or approve its own findings without a separate release decision.

## Optional Exercise 4: CEO-Directed Project Planning

Expected evidence:

- The initial CEO instruction becomes a typed `ProjectPlan`.
- The database choice is stored as a `TeamCommitment`.
- The mid-flight MongoDB instruction updates TeamLog.
- The Coder reads TeamLog, not raw CEO text.
- A final `HumanReviewDecision` gates release.

Common mistakes:

1. Passing raw human text directly into the Coder.
2. Updating a local variable but not durable memory.
3. Omitting the human approval/rejection gate.
4. Passing unstructured intent to the Coder instead of governed project state.
