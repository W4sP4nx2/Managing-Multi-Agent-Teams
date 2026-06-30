# Homework B: Production Controls

## Mission

Add safety, evaluation, cost control, and memory lifecycle management to managed agent teams.

Starter code: `assignments/starter_code/module8_production_ready_features_starter.py`

Instructor guide: `instructor/solutions/module8_solution_guide.md`

## Exercise 8.1: Human-in-the-Loop Approval

Prompt: Implement `HumanApprovalGateway.requires_human_approval(action: AgentAction) -> bool`.

Deliverables:

- `AgentAction` schema with action type, estimated cost, confidence, data sensitivity, and rationale.
- `HumanDecision` schema with approved/rejected status and reviewer notes.
- Policy that requires approval for production deletion, high cost, low confidence, or restricted data access.

Technical constraints:

- Approval policy must be deterministic.
- Denied or pending actions must not execute downstream tools.
- Include an audit trail for approval decisions.

Rubric:

- HITL policy completeness: 40%
- Typed approval artifacts: 25%
- Safe execution gating: 25%
- Auditability: 10%

## Exercise 8.2: Agent Performance Benchmarks

Prompt: Implement `AgentBenchmark.measure_agent_performance(agent, tasks) -> Metrics`.

Deliverables:

- `Metrics` schema with accuracy, latency, cost, hallucination rate, and tool usage efficiency.
- A benchmark dataset with at least 10 tasks and expected outputs.
- A report comparing two agent configurations.

Technical constraints:

- Metrics must be reproducible in offline/mock mode.
- Hallucination checks must compare against expected fields or citations.
- Latency and cost can be simulated but must be consistently calculated.

Rubric:

- Metric design quality: 35%
- Reproducible benchmark harness: 35%
- Comparative analysis: 20%
- Clear recommendations: 10%

## Exercise 8.3: Cost-Aware Agent with Caching

Prompt: Implement `CostAwareAgent.generate_response(prompt: str) -> str`.

Deliverables:

- Response cache and cost tracker.
- Budget check before model invocation.
- Demonstration showing a cached call costs zero additional model spend.

Technical constraints:

- Cache key must include prompt and relevant model/config parameters.
- Budget failures must raise a typed error.
- Audit trail must record cache hit, cache miss, and budget denial.

Rubric:

- Cache correctness: 30%
- Budget enforcement: 30%
- Cost accounting: 25%
- Observability of decisions: 15%

## Exercise 8.4: Long-Term Memory with Forgetting

Prompt: Implement `LongTermMemory.store`, `retrieve`, and `forget`.

Deliverables:

- `AgentExperience` schema with task, outcome, value score, timestamp, and tags.
- Retrieval by keyword or embedding stand-in.
- Forgetting strategy for least-recent, low-value, or compressed memories.

Technical constraints:

- Restricted memories must not be returned to public agents.
- Forgetting must be explainable and testable.
- Memory bloat must be measurable before and after forgetting.

Rubric:

- Memory schema and retrieval quality: 30%
- Governance and sensitivity controls: 30%
- Forgetting strategy: 30%
- Measurement and explanation: 10%

## Exercise 8.5: A2A OpenAPI Contract

Prompt: Your Virtual Software Company needs to outsource `SECURITY_SCAN` to a third-party AI security agent hosted on another cloud. Design the REST API contract for that Agent-to-Agent handoff.

Deliverables:

- OpenAPI 3.0 YAML file for the external Security Agent.
- `POST /security-scan` endpoint.
- Request schema containing a strictly typed `CodePatch`.
- Response schema returning a strictly typed `SecurityReview`.
- API key authentication scheme.
- Example request and example response.
- Reflection explaining how OpenAPI enforces type-safe delegation across network boundaries the same way Pydantic enforces it inside Python.

Technical constraints:

- `CodePatch` must include files, rationale, and tests to run.
- `SecurityReview` must include approved status, findings, severity counts, and reviewer identity.
- The OpenAPI contract must reject unspecified fields through `additionalProperties: false` where appropriate.
- The API key must be defined in `components.securitySchemes`.

Rubric:

- OpenAPI schema correctness: 35%
- Type-safe A2A contract design: 30%
- Security/authentication design: 20%
- Reflection quality: 15%
