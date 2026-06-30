# Verification Pyramid for Managing Multi-Agent Teams

This course is not verified by asking whether the agents produced a nice-looking answer. It is verified by proving that every agent boundary is typed, governed, observable, and bounded.

## Level 1: Unit Tests, Individual Agent Contracts

Management principle: each specialist must produce work in a form the next specialist can safely consume.

What to test:

- Pydantic schemas reject extra fields, unsafe paths, invalid enums, and weak acceptance criteria.
- Tool policies deny unauthorized tools before execution.
- Shared memory filters by sensitivity and requester clearance.
- Repair-loop data structures preserve enough failure context for the next attempt.
- Beginner governance labs validate their core contracts: `WeatherRequest`, `WeatherResponse`, `DraftSpec`, `EditorFeedback`, `SecurityIncidentTicket`, `ProjectPlan`, and `TeamCommitment`.

Representative command:

```bash
python -m pytest tests/test_schemas.py tests/test_tools.py tests/test_memory.py -v
```

## Level 2: Integration Tests, Agent-to-Agent Handoffs

Management principle: the handoff is the management surface. Raw text is not a contract.

What to test:

- PM output becomes a valid `TaskSpec`.
- Coder output becomes a valid `CodePatch`.
- QA receives a typed patch and returns a typed `TestResult`.
- Failures are returned as structured evidence instead of crashing the workflow.

Representative command:

```bash
python -m pytest tests/test_handoffs.py -v
```

## Level 3: System Tests, End-to-End Workflow

Management principle: a managed team must complete work, repair failures, and stop safely.

What to test:

- PM -> Coder -> QA -> Reviewer flow completes.
- ChatDev-style repair uses bounded retries.
- Fugu-style routing produces an auditable route trace.
- TeamLog commitments are present before release.
- Capstone baseline returns a `PullRequestSummary`, not an unstructured log.

Representative command:

```bash
python -m pytest tests/test_system.py tests/test_ex5_capstone.py -v
```

## Level 4: A2A and API Boundary Tests

Management principle: external systems are untrusted until converted into internal identities and typed requests.

What to test:

- MCP-shaped tool calls include caller identity, tool name, arguments, and data sensitivity.
- Tool gateways deny unauthorized calls.
- TeamLog commitments can override otherwise-scoped tools.
- API keys map to internal identities.
- FastAPI endpoints return `202 Accepted` for asynchronous work and `403 Forbidden` for governance violations.

Representative command:

```bash
python -m pytest tests/test_a2a_orchestration.py tests/test_api_boundary.py -v
```

## Level 5: Curriculum Execution Tests

Management principle: a learner should be able to run the material, not just read it.

What to test:

- Each notebook executes offline without API keys.
- Mock LLM adapters demonstrate invalid output rejection.
- Live LLM cells remain explicitly optional.
- No notebook depends on hidden local state.

Representative command:

```bash
python -m pytest tests/test_notebooks.py -v
```

## Exercise Verification Checklist

### Deliverables

- [ ] Clear problem statement.
- [ ] Specific, measurable deliverables.
- [ ] Technical constraints are explicit.
- [ ] Grading rubric is objective.

### Testability

- [ ] Can be graded automatically with unit or integration tests.
- [ ] Sample solution exists and passes all tests.
- [ ] Edge cases are covered.
- [ ] Invalid inputs are rejected.

### Basic Agent Governance Labs

- [ ] Logistics Weather Agent hides API keys inside a gateway and blocks unauthorized callers.
- [ ] Writer Agent consumes typed editor feedback and stops after its retry budget.
- [ ] QA Agent classifies adversarial A2A payloads and emits `SecurityIncidentTicket`.
- [ ] CEO Interface converts natural language into `ProjectPlan` and `TeamCommitment` before downstream execution.
- [ ] Each lab can answer: "What management boundary did we enforce?"

### A2A Alignment

- [ ] Tests agent-to-agent communication.
- [ ] Verifies governance boundaries.
- [ ] Checks schema enforcement.
- [ ] Validates repair or escalation paths.

## Notebook Verification Checklist

### Structure

- [ ] All code cells execute without errors.
- [ ] No unexpected `NotImplementedError` blocks remain in runnable cells.
- [ ] Markdown cells explain why the pattern matters for management.
- [ ] Each notebook has a clear learning objective.

### Functionality

- [ ] Mock LLM adapters work correctly.
- [ ] Schema validation catches invalid inputs.
- [ ] Tool policies block unauthorized access.
- [ ] Repair loops terminate.
- [ ] Memory search respects visibility rules.

### A2A Orchestration

- [ ] Agent identities are mapped explicitly.
- [ ] Tool requests include caller, tool, args, and sensitivity.
- [ ] Audit logs capture allowed and denied events.
- [ ] API status codes are correct.

### Production Readiness

- [ ] API keys are not hardcoded.
- [ ] Teaching placeholders that show fake API keys are explicitly labeled as mocks and never used for real calls.
- [ ] Environment variables are documented.
- [ ] Error handling is graceful.
- [ ] Logs or audit events are structured.

## Automated Testing Pipeline

Run the core suite:

```bash
python -m pytest tests/ -v
```

Run with coverage:

```bash
python -m pytest tests/ -v --cov=src --cov=assignments --cov-report=html
```

Run only A2A and API boundary checks:

```bash
python -m pytest tests/test_a2a_orchestration.py tests/test_api_boundary.py -v
```

Run with timeout protection:

```bash
python -m pytest tests/ -v --timeout=30
```

Optional production-readiness checks, if the tools are installed:

```bash
python -m black --check src assignments tests
python -m pytest --nbval notebooks/*.ipynb
git-secrets --scan
python -c "from src.enterprise_agent_team import run_virtual_software_company; print('Schemas OK')"
python -c "from assignments.starter_code.ex5_capstone_solution import app; print('API OK')"
```

## Instructor Rule

If a learner demo fails, diagnose in this order: schema contract, identity and tool scope, memory visibility, repair budget, then LLM behavior. The LLM is the least deterministic layer, so it should be debugged last.
