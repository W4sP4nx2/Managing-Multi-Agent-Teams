# Core Notebook Solution Guide

Instructor reference for the three graded labs and the two-team Capstone. The learner notebooks intentionally begin with one or more broken controls. The starter grader should therefore fail until learners repair the marked code. Apply these solutions, rerun the affected cells in order, then rerun the grader.

## Lab 1 — Pydantic contracts

Replace the TODO class in `01_lab_pydantic.ipynb` with:

```python
class StrictResearchOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    topic: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    findings: list[str]
```

Expected grader evidence: a valid score passes, `150.5` fails, and the undeclared `secret_backdoor` field fails. Score: **15/15**. Range-only repair earns **5/15**; extra-field-only repair earns **10/15**.

## Lab 2 — Multi-Agent Management: Manager audit

In `02_lab_crewai.ipynb`, make both marked configuration edits:

```python
tools=[approve_code_tool]
```

for the Manager's tools, and:

```python
context=[architect_task]
```

for `coder_task`. Keep `allow_delegation=True` on the Manager and keep the Coder and QA tool scopes unchanged. Rerun the configuration and deterministic demonstration cells. The Coder should receive the Architect context and return a valid `CodePatch`. The supplied Manager audit should record `PASS_TO_QA` with one typed proposal in `qa_inbox`. Ask for the decision/evidence/next-owner note. This does not execute QA or grant release approval. Score remains **15/15**. Permissions-only repair earns **5/15**; context-only repair earns **10/15**.

For the final **Blind Agent Debug** micro-task, the violated field is `generated_output.user_id`: `101` is an integer, while `CodePatch` requires a string. The missing dependency is `coder_task.context=[architect_task]`. Learners should repair the configuration and rerun the Coder demonstration, Manager gate, and grader rather than edit the historical failing trace. After both Lab 2 repairs, expect a string ID, a validated patch, and `PASS_TO_QA`. The task is formative and adds no points.

In Labs 2–3 and the Capstone, `safe_validate` returns `None` after expected schema rejection. Confirm that learner-facing examples guard the return value before downstream use. Preserve raw raising validation at the Coordinator and other receiving boundaries; readable errors do not replace fail-closed enforcement.

## Lab 3 — Manager Oversight: Code Validation

Replace the TODO `SecureToolInput` with a strict model that accepts only short numeric IDs:

```python
class SecureToolInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: str

    @field_validator("user_id")
    @classmethod
    def require_short_numeric_id(cls, value: str) -> str:
        if not re.fullmatch(r"\d{1,12}", value):
            raise ValueError("user_id must contain 1 to 12 digits")
        return value
```

Set:

```python
MAX_RETRIES = 3
```

Rerun the cell that calculates `repair_state`. The loop performs four calls total at most: one initial attempt and three retries, then it escalates. The dry-run tool never connects to a database. The supplied oversight action should record `ESCALATE_TO_HUMAN`, no release approval, four failed calls, and $0.20 simulated cost. Ask for the oversight decision note; no notification is sent. Score remains **15/15**.

## Capstone — Development to Security handoff

In `04_capstone.ipynb`, add the failed-QA validator to `DevDeliverable`:

```python
    @field_validator("unit_tests_passed")
    @classmethod
    def require_passing_tests(cls, value: bool) -> bool:
        if not value:
            raise ValueError("Development Team QA must pass before Security review")
        return value
```

Replace `coordinate_handoff` so it validates and records the contract before Security starts:

```python
def coordinate_handoff(candidate: DevDeliverable) -> SecurityAuditResult:
    validated = DevDeliverable.model_validate(candidate.model_dump())
    COORDINATOR_LOG.append("Coordinator validated DevDeliverable")
    COORDINATOR_LOG.append("Security Team started")
    return run_security_team(validated)
```

Keep the Security Manager's approval tool and remove its scanner tool:

```python
tools=[approve_audit_tool]
```

The Pen Tester keeps `tools=[mock_pen_test_tool]`. Rerun the deterministic pipeline after clearing `COORDINATOR_LOG`, then rerun the grader. It should verify failed-QA rejection, validation-before-start ordering, separate tools, and a typed `SecurityAuditResult`. Score: **20/20**. No CrewAI kickoff or provider call is needed for this deterministic grader.

## Expected starter and repaired scores

The shipped learner notebooks are intentionally broken at the marked settings. Their grader is expected to report a failing or partial score before learner changes. With the complete repairs above, Lab 1, Lab 2, and Lab 3 should each report **15/15**, and the Capstone code grader should report **20/20**.
