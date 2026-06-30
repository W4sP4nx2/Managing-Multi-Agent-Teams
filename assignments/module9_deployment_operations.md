# Homework C: Deployment & Operations

## Mission

Move managed agent teams from notebooks into production operations: deployment, observability, secure execution, and version control.

Starter code: `assignments/starter_code/module9_deployment_operations_starter.py`

Instructor guide: `instructor/solutions/module9_solution_guide.md`

## Exercise 9.1: Containerize Your Agent

Prompt: Create a Docker deployment for a small agent API.

Deliverables:

- `Dockerfile` using `python:3.12-slim`.
- API entry point that exposes a health check and one agent action.
- Configuration file for model name, budget, and tool policy.

Technical constraints:

- Do not bake API keys into the image.
- Use environment variables for secrets.
- Container must start with a single documented command.

Rubric:

- Secure container structure: 35%
- Runnable API packaging: 35%
- Configuration hygiene: 20%
- Documentation: 10%

## Exercise 9.2: Observability Stack

Prompt: Implement `AgentObservability` for structured logs, traces, metrics, and alerts.

Deliverables:

- Structured log event for each agent action.
- Trace record for an end-to-end workflow.
- Metrics for latency, errors, cost, and repair attempts.
- Alert rule for repeated failures or budget exhaustion.

Technical constraints:

- Logs must include workflow ID, agent ID, action, result, and timestamp.
- Metrics must be machine-readable.
- Do not log secrets or restricted payload contents.

Rubric:

- Logging and tracing quality: 35%
- Useful metrics and alerts: 35%
- Privacy and redaction: 20%
- Operational clarity: 10%

## Exercise 9.3: Secure Code Sandbox

Prompt: Implement a `SecureSandbox.execute_untrusted_code` interface.

Deliverables:

- `ExecutionRequest` and `ExecutionResult` schemas.
- Timeout handling.
- Blocked network/filesystem behavior in design or implementation.
- Prompt-injection detection stub or classifier hook.

Technical constraints:

- Untrusted code must never run with broad host permissions in production.
- Timeout and failure states must be explicit.
- Captured stdout/stderr must be bounded.

Rubric:

- Isolation design: 40%
- Typed execution results: 25%
- Failure and timeout handling: 25%
- Prompt-injection awareness: 10%

## Exercise 9.4: Agent Configuration Version Control

Prompt: Implement `AgentVersionControl` for prompts, tools, model settings, and policy.

Deliverables:

- `AgentConfig` schema with prompt, tools, model parameters, and policy version.
- Version hash for each saved config.
- Rollback function and version diff.
- Demonstration of comparing two prompt/tool configurations.

Technical constraints:

- Version hash must change when prompt, tool set, or model parameters change.
- Rollback must validate the restored config.
- Diff must highlight prompt, tool, and policy changes.

Rubric:

- Versioning correctness: 35%
- Rollback safety: 25%
- Diff usefulness: 25%
- Deployment-readiness explanation: 15%
