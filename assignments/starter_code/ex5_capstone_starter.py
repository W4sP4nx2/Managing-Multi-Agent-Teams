"""Capstone starter: Virtual Software Company.

This is a minimal working baseline learners can run, inspect, and extend. It
maps directly to the production agentic lifecycle:

1. Perception: PM ingests the raw issue and extracts requirements.
2. Reasoning: Tech Lead decomposes requirements into subtasks.
3. Execution: Coder and QA produce code, tests, and feedback.
4. Learning: Repair loop stores failures and improves the next attempt.
5. Governance: Security and Release enforce compliance before output.

WARNING: This file starts as a deterministic governance shell. The "agents"
below are mocked on purpose so the schemas, tool gateway, audit trail, and
repair loop are easy to test offline. In production, replace the deterministic
agent functions with LLM calls constrained by the same Pydantic contracts.
"""

from enum import Enum
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


class Role(str, Enum):
    PM = "pm"
    TECH_LEAD = "tech_lead"
    CODER = "coder"
    QA = "qa"
    SECURITY = "security"
    RELEASE = "release"


class Tool(str, Enum):
    SEARCH_MEMORY = "search_memory"
    WRITE_PATCH = "write_patch"
    RUN_TESTS = "run_tests"
    SECURITY_SCAN = "security_scan"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TaskSpec(StrictModel):
    goal: str
    acceptance_criteria: list[str] = Field(min_length=1)
    risk: Literal["low", "medium", "high"]


class SubTask(StrictModel):
    title: str
    owner: Role
    done_when: list[str] = Field(min_length=1)


class CodePatch(StrictModel):
    files: dict[str, str]
    rationale: str
    tests_to_run: list[str] = Field(min_length=1)

    @field_validator("files")
    @classmethod
    def paths_are_relative(cls, files: dict[str, str]) -> dict[str, str]:
        for path in files:
            if path.startswith("/") or ".." in path.split("/"):
                raise ValueError(f"Unsafe patch path: {path}")
        return files


def mock_llm_code_patch_payload(task: str, attempt: int = 0) -> dict[str, Any]:
    """Teaching adapter for the missing LLM layer.

    A real LLM is nondeterministic and may return extra fields, unsafe paths, or
    malformed structures. This mock simulates that failure offline so learners
    can see Pydantic catch the hallucination before the orchestration loop uses
    the output.
    """

    if attempt == 0:
        return {
            "files": {"../escape.py": "print('hack')"},
            "rationale": f"I am adding a config file for: {task}",
            "tests_to_run": ["test_config"],
            "hallucinated_field": "I am an LLM and I made this up.",
        }
    return {
        "files": {"slugify.py": 'def slugify(text):\n    return "-".join(text.lower().split())\n'},
        "rationale": "Fixed unsafe path and removed hallucinated fields after schema feedback.",
        "tests_to_run": ["test_slugify_spaces", "test_slugify_lowercase"],
    }


def demo_llm_schema_guard() -> None:
    """Show messy LLM JSON being rejected, then repaired."""

    print("=== Mock LLM Adapter: schema guard demo ===")
    try:
        CodePatch.model_validate(mock_llm_code_patch_payload("Create slugify utility", attempt=0))
    except ValidationError as exc:
        print("Pydantic rejected the first LLM output:")
        for error in exc.errors():
            print(f"- {error['loc']}: {error['msg']}")
        print("Triggering LLM repair with validation feedback...\n")

    repaired_patch = CodePatch.model_validate(
        mock_llm_code_patch_payload("validation feedback: unsafe path and extra field", attempt=1)
    )
    print("Repaired LLM output validated:")
    print(repaired_patch.model_dump_json(indent=2))


class TestResult(StrictModel):
    passed: bool
    log: str
    failing_tests: list[str] = Field(default_factory=list)


class SecurityReview(StrictModel):
    approved: bool
    findings: list[str] = Field(default_factory=list)


class PullRequestSummary(StrictModel):
    status: Literal["SHIPPED", "ESCALATED_TO_HUMAN"]
    title: str
    body: str
    tests: list[str]
    risks: list[str]
    audit_trail: list[str] = Field(default_factory=list)


class AgentIdentity(StrictModel):
    role: Role
    allowed_tools: set[Tool]
    trust_tier: str


class ToolRequest(StrictModel):
    caller: AgentIdentity
    tool: Tool
    args: dict[str, Any]
    sensitivity: str


class ToolGateway:
    def call(self, request: ToolRequest) -> dict[str, Any]:
        # [DETERMINISTIC MOCK] This is an MCP-shaped gateway, not a real MCP
        # transport. Keep the authorization pattern when replacing it with MCP.
        if request.tool not in request.caller.allowed_tools:
            raise PermissionError(f"{request.caller.role.value} cannot use {request.tool.value}")

        if request.tool == Tool.WRITE_PATCH:
            if request.caller.role != Role.CODER:
                raise PermissionError("Only the coder may submit patches")
            patch = CodePatch.model_validate(request.args["patch"])
            return {"status": "patch accepted", "patch": patch}

        if request.tool == Tool.RUN_TESTS:
            if request.caller.role != Role.QA:
                raise PermissionError("Only QA may run tests")
            patch = CodePatch.model_validate(request.args["patch"])
            return {"test_result": run_tests(patch)}

        if request.tool == Tool.SECURITY_SCAN:
            if request.caller.role != Role.SECURITY:
                raise PermissionError("Only security may scan patches")
            patch = CodePatch.model_validate(request.args["patch"])
            return {"security_review": security_scan(patch)}

        if request.tool == Tool.SEARCH_MEMORY:
            query = str(request.args.get("query", "")).lower()
            memory = request.args.get("memory", [])
            return {"matches": [item for item in memory if query in item.lower()]}

        raise ValueError(f"Unknown tool: {request.tool}")


def run_tests(patch: CodePatch) -> TestResult:
    """QA tool: execute the submitted utility in a tiny local test harness."""

    # [DETERMINISTIC MOCK] In production, run tests in an isolated sandbox with
    # resource limits. The teaching goal is the typed CodePatch -> TestResult
    # handoff, not this tiny executor.
    namespace: dict[str, Any] = {"__builtins__": {}}
    try:
        source = patch.files["slugify.py"]
        exec(source, namespace, namespace)
        slugify = namespace["slugify"]
        assert slugify("Hello World") == "hello-world", "spaces must become hyphens"
        assert slugify("Already") == "already", "single tokens must remain lowercase"
        assert slugify("multi   space") == "multi-space", "repeated whitespace must collapse"
    except Exception as exc:
        return TestResult(
            passed=False,
            log=f"{type(exc).__name__}: {exc}",
            failing_tests=["test_slugify_contract"],
        )

    return TestResult(passed=True, log="All slugify tests passed")


def security_scan(patch: CodePatch) -> SecurityReview:
    """Security tool: block obviously unsafe code patterns before release."""

    # [DETERMINISTIC MOCK] Replace with SAST, dependency, secrets, and policy
    # scanners. Keep the same SecurityReview contract at the boundary.
    unsafe_tokens = ["open(", "eval(", "exec(", "__import__", "subprocess", "os."]
    findings = [
        f"Unsafe token found: {token}"
        for content in patch.files.values()
        for token in unsafe_tokens
        if token in content
    ]
    return SecurityReview(approved=not findings, findings=findings)


def parse_issue(issue: str) -> TaskSpec:
    # [DETERMINISTIC MOCK] PM agent behavior. In a real system, this calls an
    # LLM with response_model=TaskSpec. For this exercise, implement rule-based
    # extraction from the issue string or integrate a live LLM if keys are
    # available. Do not return static filler data.
    issue_lower = issue.lower()
    risk: Literal["low", "medium", "high"] = "medium"
    if any(term in issue_lower for term in ["auth", "payment", "pii", "secret", "security"]):
        risk = "high"
    elif any(term in issue_lower for term in ["docs", "typo", "format", "readme"]):
        risk = "low"

    return TaskSpec(
        goal=issue,
        acceptance_criteria=[
            "Expose slugify(text)",
            "Lowercase text",
            "Replace whitespace with hyphens",
            "Include passing tests",
        ],
        risk=risk,
    )


def decompose(task: TaskSpec) -> list[SubTask]:
    # [DETERMINISTIC MOCK] Tech Lead agent behavior. In production, this is a
    # planning LLM constrained to list[SubTask].
    # LEARNER TASK: Expand this into a real Tech Lead agent.
    # The Tech Lead should decompose the TaskSpec into SubTasks, assign owners,
    # and attach acceptance criteria to each subtask.
    return [
        SubTask(title="Implement utility", owner=Role.CODER, done_when=["slugify.py contains slugify"]),
        SubTask(title="Test behavior", owner=Role.QA, done_when=task.acceptance_criteria),
        SubTask(title="Review safety", owner=Role.SECURITY, done_when=["No unsafe imports or filesystem access"]),
    ]


def route(task: TaskSpec) -> str:
    # [DETERMINISTIC MOCK] Fugu-style routing behavior. In production, this can
    # be learned/observed routing across model classes with cost and latency.
    # LEARNER TASK: Replace this rule-based router with a Fugu-style router.
    # Add task complexity, estimated cost, latency, and model-class selection.
    if task.risk == "high":
        return "reasoning_model"
    if len(task.acceptance_criteria) >= 4:
        return "code_specialist"
    return "fast_model"


def code(task: TaskSpec, feedback: list[str]) -> CodePatch:
    # [DETERMINISTIC MOCK] Coder agent behavior. In production, this calls an
    # LLM/code model and validates the raw JSON or tool output as CodePatch.
    if feedback:
        implementation = 'def slugify(text):\n    return "-".join(text.lower().split())\n'
        rationale = "Fixed slug replacement after QA feedback"
    else:
        implementation = "def slugify(text):\n    return text.lower()\n"
        rationale = "Initial implementation, intentionally incomplete until QA feedback"

    return CodePatch(
        files={"slugify.py": implementation},
        rationale=rationale,
        tests_to_run=["test_slugify_spaces", "test_slugify_lowercase"],
    )


def run_company(issue: str, max_repairs: int = 2) -> PullRequestSummary:
    """
    Orchestrates the Agentic Lifecycle for a Virtual Software Company:
    1. Perception (PM): Ingests raw issue, extracts requirements.
    2. Reasoning (Tech Lead): Decomposes into sub-tasks, plans execution.
    3. Execution (Coder/QA): Writes code, runs tests, gathers feedback.
    4. Learning (Repair Loop): Evaluates outcome, refines strategy via memory.
    5. Governance (Security/Release): Enforces compliance before final output.
    """
    task = parse_issue(issue)
    subtasks = decompose(task)
    route_choice = route(task)

    identities = {
        # LEARNER TASK: Add PM, Tech Lead, and Release identities, then enforce
        # that each stage can only call the tools it owns.
        Role.CODER: AgentIdentity(
            role=Role.CODER,
            allowed_tools={Tool.WRITE_PATCH, Tool.SEARCH_MEMORY},
            trust_tier="confidential",
        ),
        Role.QA: AgentIdentity(
            role=Role.QA,
            allowed_tools={Tool.RUN_TESTS, Tool.SEARCH_MEMORY},
            trust_tier="confidential",
        ),
        Role.SECURITY: AgentIdentity(
            role=Role.SECURITY,
            allowed_tools={Tool.SECURITY_SCAN, Tool.SEARCH_MEMORY},
            trust_tier="restricted",
        ),
    }

    gateway = ToolGateway()
    repair_memory: list[str] = []
    audit_trail = [
        f"PM produced TaskSpec: {task.goal}",
        f"Tech Lead produced {len(subtasks)} subtasks",
        f"Router selected {route_choice}",
    ]

    final_patch: CodePatch | None = None
    final_test: TestResult | None = None
    final_security: SecurityReview | None = None

    for attempt in range(max_repairs + 1):
        # PM -> Tech Lead -> Coder happens before this loop. The loop is the
        # ChatDev-style repair reflex: Coder submits, QA tests, feedback goes
        # back into memory, and the next Coder attempt uses that evidence.
        patch = code(task, feedback=repair_memory)
        audit_trail.append(f"Coder attempt {attempt + 1}: {patch.rationale}")

        gateway.call(
            ToolRequest(
                caller=identities[Role.CODER],
                tool=Tool.WRITE_PATCH,
                args={"patch": patch.model_dump(mode="json")},
                sensitivity="confidential",
            )
        )

        test_payload = gateway.call(
            ToolRequest(
                caller=identities[Role.QA],
                tool=Tool.RUN_TESTS,
                args={"patch": patch.model_dump(mode="json")},
                sensitivity="confidential",
            )
        )
        test_result: TestResult = test_payload["test_result"]
        audit_trail.append(f"QA attempt {attempt + 1}: {test_result.log}")

        if not test_result.passed:
            repair_memory.append(test_result.log)
            if attempt >= max_repairs:
                audit_trail.append("Repair budget exhausted; escalating to human reviewer")
                return PullRequestSummary(
                    status="ESCALATED_TO_HUMAN",
                    title="Escalation required: slugify utility",
                    body=(
                        f"Repair budget exhausted. Task `{task.goal}` failed after {attempt + 1} attempts. "
                        f"Last failure: {test_result.log}"
                    ),
                    tests=[test_result.log],
                    risks=["Repair budget exhausted"],
                    audit_trail=audit_trail,
                )
            continue

        # LEARNER TASK: Add more governed tools here, such as linting,
        # dependency scanning, or documentation generation. Each tool should be
        # authorized through ToolGateway before it can run.
        security_payload = gateway.call(
            ToolRequest(
                caller=identities[Role.SECURITY],
                tool=Tool.SECURITY_SCAN,
                args={"patch": patch.model_dump(mode="json")},
                sensitivity="confidential",
            )
        )
        security_review: SecurityReview = security_payload["security_review"]
        audit_trail.append(
            "Security approved patch"
            if security_review.approved
            else f"Security rejected patch: {security_review.findings}"
        )

        if security_review.approved:
            final_patch = patch
            final_test = test_result
            final_security = security_review
            break

        repair_memory.extend(security_review.findings)
        if attempt >= max_repairs:
            audit_trail.append("Security repair budget exhausted; escalating")
            return PullRequestSummary(
                status="ESCALATED_TO_HUMAN",
                title="Escalation required: security findings",
                body=f"Task `{task.goal}` could not pass security review.",
                tests=[test_result.log],
                risks=security_review.findings,
                audit_trail=audit_trail,
            )

    if final_patch is None or final_test is None or final_security is None:
        raise RuntimeError("Orchestration ended without release or escalation")

    return PullRequestSummary(
        status="SHIPPED",
        title="Add slugify utility",
        body=(
            f"Parsed task: {task.goal}\n"
            f"Route: {route_choice}\n"
            f"Subtasks: {[subtask.title for subtask in subtasks]}\n"
            f"Final patch rationale: {final_patch.rationale}"
        ),
        tests=[final_test.log],
        risks=final_security.findings or ["No security findings"],
        audit_trail=audit_trail,
    )


# LEARNER TASK: Wrap `run_company()` in a FastAPI gateway.
# Required API layer:
# - POST /tasks accepts raw external JSON from a GitHub webhook, Slack command,
#   or Jira ticket and returns 202 Accepted plus a task_id.
# - GET /tasks/{task_id} returns PENDING, RUNNING, SHIPPED, or ESCALATED status.
# - Map the incoming X-API-Key or Authorization header to an AgentIdentity.
# - Reject external_vendor identities that request high-risk work or restricted
#   memory access.
# - Run the orchestration in a BackgroundTask or simulated async worker.


if __name__ == "__main__":
    demo_llm_schema_guard()
    print("\n=== Virtual Software Company run ===")
    print(run_company("Create a slugify(text) utility with tests.").model_dump_json(indent=2))
