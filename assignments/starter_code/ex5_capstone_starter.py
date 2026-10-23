"""Capstone starter: Virtual Software Company.

This is a minimal working baseline learners can run, inspect, and extend. It
maps directly to the production agentic lifecycle:

1. Planning: Engineering Manager turns the issue into a typed task and subtasks.
2. Execution: Senior Coder produces a patch; QA Auditor runs tests and security checks.
3. Learning: Repair loop stores failures and improves the next attempt.
4. Governance: Manager approves delivery or escalates unresolved risk.

WARNING: This file starts as a deterministic governance shell. The "agents"
below are mocked on purpose so the schemas, tool gateway, audit trail, and
repair loop are easy to test offline. In production, replace the deterministic
agent functions with LLM calls constrained by the same Pydantic contracts.
"""

from enum import Enum
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


class Role(str, Enum):
    MANAGER = "manager"
    PM = "manager"  # legacy alias for the same Manager role; it is not a fourth agent
    CODER = "coder"
    QA = "qa"
    SECURITY_MANAGER = "security_manager"
    PEN_TESTER = "pen_tester"


class Tool(str, Enum):
    SEARCH_MEMORY = "search_memory"
    WRITE_PATCH = "write_patch"
    RUN_TESTS = "run_tests"
    SECURITY_SCAN = "security_scan"
    AUDIT_DEV_DELIVERABLE = "audit_dev_deliverable"
    APPROVE_CODE = "approve_code"
    ESCALATE_TO_HUMAN = "escalate_to_human"


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


class DevDeliverable(StrictModel):
    """Validated Development-Team output handed to the Security Team."""

    code_snippet: str = Field(min_length=1)
    unit_tests_passed: bool
    dev_team_signature: str = Field(min_length=1)

    @field_validator("unit_tests_passed")
    @classmethod
    def tests_must_pass_before_handoff(cls, passed: bool) -> bool:
        if not passed:
            raise ValueError("The Security Team only accepts deliverables that passed unit tests")
        return passed


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


class SecurityAuditResult(StrictModel):
    approved: bool
    findings: list[str] = Field(default_factory=list)
    security_team_signature: str = Field(min_length=1)


class PullRequestSummary(StrictModel):
    status: Literal["SHIPPED", "ESCALATED_TO_HUMAN"]
    title: str
    body: str
    tests: list[str]
    risks: list[str]
    audit_trail: list[str] = Field(default_factory=list)
    dev_deliverable: DevDeliverable | None = None
    security_audit: SecurityAuditResult | None = None


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
            if request.caller.role != Role.QA:
                raise PermissionError("Only QA may run security checks")
            patch = CodePatch.model_validate(request.args["patch"])
            return {"security_review": security_scan(patch)}

        if request.tool == Tool.AUDIT_DEV_DELIVERABLE:
            if request.caller.role != Role.PEN_TESTER:
                raise PermissionError("Only the Pen Tester may audit a Development-Team deliverable")
            deliverable = DevDeliverable.model_validate(request.args["dev_deliverable"])
            return {"security_audit": security_team_audit(deliverable)}

        if request.tool == Tool.APPROVE_CODE:
            if request.caller.role != Role.MANAGER:
                raise PermissionError("Only the Manager may approve delivery")
            approved = bool(request.args.get("tests_passed") and request.args.get("security_approved"))
            return {"approved": approved}

        if request.tool == Tool.ESCALATE_TO_HUMAN:
            if request.caller.role != Role.MANAGER:
                raise PermissionError("Only the Manager may escalate to a human")
            return {"status": "ESCALATED_TO_HUMAN", "reason": str(request.args.get("reason", ""))}

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


def security_team_audit(deliverable: DevDeliverable) -> SecurityAuditResult:
    """Security-Team mock: inspect only the validated Development-Team artifact."""

    code = deliverable.code_snippet.lower()
    patterns = {
        "sql injection marker": ("drop table", "union select", "select * from"),
        "cross-site scripting marker": ("innerhtml", "document.write", "<script"),
    }
    findings = [
        f"Potential {label}: {marker}"
        for label, markers in patterns.items()
        for marker in markers
        if marker in code
    ]
    return SecurityAuditResult(
        approved=not findings,
        findings=findings,
        security_team_signature="Security & Compliance Team",
    )


def parse_issue(issue: str) -> TaskSpec:
    # [DETERMINISTIC MOCK] Engineering Manager planning behavior. In a real system, this calls an
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
    # [DETERMINISTIC MOCK] Manager planning behavior. In production, this is a
    # planning LLM constrained to list[SubTask].
    # LEARNER TASK: Expand this into the Engineering Manager's planning step.
    # The Manager should decompose the TaskSpec into SubTasks, assign owners,
    # and attach acceptance criteria to each subtask.
    return [
        SubTask(title="Implement utility", owner=Role.CODER, done_when=["slugify.py contains slugify"]),
        SubTask(title="Test behavior", owner=Role.QA, done_when=task.acceptance_criteria),
    ]


def route(task: TaskSpec) -> str:
    # [DETERMINISTIC MOCK] Starter route policy for local Python exercises.
    # LEARNER TASK: Replace this with your own transparent, typed policy for
    # cost, latency, and risk. This is an explicit local policy, not a learned
    # orchestration method or a hosted routing service.
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


def build_agent_identities() -> dict[Role, AgentIdentity]:
    """Return both teams' identities with separate tool scopes."""
    return {
        Role.MANAGER: AgentIdentity(
            role=Role.MANAGER,
            allowed_tools={Tool.APPROVE_CODE, Tool.ESCALATE_TO_HUMAN},
            trust_tier="confidential",
        ),
        Role.CODER: AgentIdentity(
            role=Role.CODER,
            allowed_tools={Tool.SEARCH_MEMORY, Tool.WRITE_PATCH},
            trust_tier="confidential",
        ),
        Role.QA: AgentIdentity(
            role=Role.QA,
            allowed_tools={Tool.SEARCH_MEMORY, Tool.RUN_TESTS, Tool.SECURITY_SCAN},
            trust_tier="confidential",
        ),
        Role.SECURITY_MANAGER: AgentIdentity(
            role=Role.SECURITY_MANAGER,
            allowed_tools={Tool.SEARCH_MEMORY},
            trust_tier="confidential",
        ),
        Role.PEN_TESTER: AgentIdentity(
            role=Role.PEN_TESTER,
            allowed_tools={Tool.AUDIT_DEV_DELIVERABLE},
            trust_tier="confidential",
        ),
    }


def run_company(issue: str, max_repairs: int = 2) -> PullRequestSummary:
    """
    Run a Development Team (Manager, Coder, QA), then pass its validated
    deliverable to the Security Team (Security Manager, Pen Tester).
    """
    task = parse_issue(issue)
    subtasks = decompose(task)
    route_choice = route(task)

    identities = build_agent_identities()

    gateway = ToolGateway()
    repair_memory: list[str] = []
    audit_trail = [
        f"Engineering Manager produced TaskSpec: {task.goal}",
        f"Engineering Manager produced {len(subtasks)} subtasks",
        f"Router selected {route_choice}",
    ]

    def escalate(reason: str, title: str, body: str, tests: list[str], risks: list[str]) -> PullRequestSummary:
        response = gateway.call(
            ToolRequest(
                caller=identities[Role.MANAGER],
                tool=Tool.ESCALATE_TO_HUMAN,
                args={"reason": reason},
                sensitivity="confidential",
            )
        )
        audit_trail.append(f"Engineering Manager escalated: {response['reason']}")
        return PullRequestSummary(
            status=response["status"],
            title=title,
            body=body,
            tests=tests,
            risks=risks,
            audit_trail=audit_trail,
        )

    final_patch: CodePatch | None = None
    final_test: TestResult | None = None
    final_security: SecurityReview | None = None
    final_dev_deliverable: DevDeliverable | None = None
    final_security_audit: SecurityAuditResult | None = None

    for attempt in range(max_repairs + 1):
        # Manager -> Coder -> QA happens inside this loop. The loop is the
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
                return escalate(
                    reason="Repair budget exhausted after QA failure.",
                    title="Escalation required: slugify utility",
                    body=(f"Repair budget exhausted. Task `{task.goal}` failed after {attempt + 1} attempts. "
                          f"Last failure: {test_result.log}"),
                    tests=[test_result.log],
                    risks=["Repair budget exhausted"],
                )
            continue

        # QA performs security checks as part of its validation duties; this is
        # a tool capability, not an additional Security Reviewer agent.
        security_payload = gateway.call(
            ToolRequest(
                caller=identities[Role.QA],
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
            dev_deliverable = DevDeliverable(
                code_snippet=patch.files.get("slugify.py", ""),
                unit_tests_passed=test_result.passed,
                dev_team_signature="Development Team: Manager/Coder/QA",
            )
            audit_trail.append("Development Team issued Pydantic DevDeliverable")
            security_payload = gateway.call(
                ToolRequest(
                    caller=identities[Role.PEN_TESTER],
                    tool=Tool.AUDIT_DEV_DELIVERABLE,
                    args={"dev_deliverable": dev_deliverable.model_dump(mode="json")},
                    sensitivity="confidential",
                )
            )
            security_audit: SecurityAuditResult = security_payload["security_audit"]
            audit_trail.append("Security Team received validated DevDeliverable")
            audit_trail.append(
                "Security Team approved deliverable"
                if security_audit.approved
                else f"Security Team rejected deliverable: {security_audit.findings}"
            )

            if not security_audit.approved:
                repair_memory.extend(security_audit.findings)
                if attempt >= max_repairs:
                    return escalate(
                        reason="Security Team repair budget exhausted.",
                        title="Escalation required: Security Team findings",
                        body=f"Task `{task.goal}` could not pass the Security Team audit.",
                        tests=[test_result.log],
                        risks=security_audit.findings,
                    )
                continue

            approval = gateway.call(
                ToolRequest(
                    caller=identities[Role.MANAGER],
                    tool=Tool.APPROVE_CODE,
                    args={"tests_passed": test_result.passed, "security_approved": security_audit.approved},
                    sensitivity="confidential",
                )
            )
            if not approval["approved"]:
                return escalate(
                    reason="Manager approval requirements were not met.",
                    title="Escalation required: approval gate",
                    body=f"Task `{task.goal}` did not pass the Manager approval gate.",
                    tests=[test_result.log],
                    risks=["Approval gate rejected delivery"],
                )
            audit_trail.append("Engineering Manager approved delivery")
            final_patch = patch
            final_test = test_result
            final_security = security_review
            final_dev_deliverable = dev_deliverable
            final_security_audit = security_audit
            break

        repair_memory.extend(security_review.findings)
        if attempt >= max_repairs:
            return escalate(
                reason="Security repair budget exhausted.",
                title="Escalation required: security findings",
                body=f"Task `{task.goal}` could not pass QA security checks.",
                tests=[test_result.log],
                risks=security_review.findings,
            )

    if (
        final_patch is None
        or final_test is None
        or final_security is None
        or final_dev_deliverable is None
        or final_security_audit is None
    ):
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
        dev_deliverable=final_dev_deliverable,
        security_audit=final_security_audit,
    )


# The required workshop stops at the deterministic team handoff above.
# The older FastAPI gateway solution is retained only as a historical supplement:
# _archive/advanced_scaling/assignments/starter_code/ex5_capstone_solution.py
# For optional API-boundary study, use the separate extensions/ notebook after
# completing the assessed labs and Capstone.


if __name__ == "__main__":
    demo_llm_schema_guard()
    print("\n=== Virtual Software Company run ===")
    print(run_company("Create a slugify(text) utility with tests.").model_dump_json(indent=2))
