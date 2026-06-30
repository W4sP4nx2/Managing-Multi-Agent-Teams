# Basic Agent Governance Labs Solution Guide

Use this guide to grade the Logistics Weather, Writer, QA, and CEO builder exercises. These are beginner-friendly scenarios, but they should still prove the learner understands managed multi-agent systems.

## Strong Answer Indicators

- The learner uses Pydantic models for every boundary artifact instead of raw dictionaries.
- The learner separates agent identity from tool authorization.
- The learner keeps API keys and privileged actions inside gateways, never inside prompts.
- The learner records audit evidence for denied, repaired, or escalated paths.
- The learner can explain the management principle in one sentence.

## Lab 1: Governed Logistics Weather Agent

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

## Lab 2: Bounded Writer Agent

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

## Lab 3: Adversarial QA Agent

Expected evidence:

- Normal internal functional tests are processed.
- Prompt-injection payloads are blocked.
- Data-exfiltration payloads are blocked.
- External red-team role violations are blocked.
- Each denial creates a `SecurityIncidentTicket` and Dead Letter Queue record.

Common mistakes:

1. Searching for only one exact malicious phrase.
2. Returning a plain string instead of `SecurityIncidentTicket`.
3. Blocking the payload but failing to preserve audit evidence.
4. Trusting `sender_org` without considering identity verification in the reflection.

## Lab 4: Vibe Coding CEO Interface

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
4. Treating Vibe Coding as free-form prompting rather than structured management.
