"""Instructor capstone solution: Virtual Software Company.

Run:
    python3 assignments/starter_code/ex5_capstone_solution.py
"""

import asyncio
from enum import Enum
from typing import Any, Literal
from uuid import uuid4

from fastapi import BackgroundTasks, Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator


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

    @model_validator(mode="after")
    def paths_are_safe(self):
        for path in self.files:
            if path.startswith("/") or ".." in path.split("/"):
                raise ValueError(f"Unsafe patch path: {path}")
        return self


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


class AgentIdentity(StrictModel):
    role: Role
    allowed_tools: set[Tool]
    trust_tier: Literal["public", "confidential", "restricted"]


class ToolRequest(StrictModel):
    caller: AgentIdentity
    tool: Tool
    args: dict[str, Any]
    sensitivity: Literal["public", "confidential", "restricted"]


class MemoryRecord(StrictModel):
    text: str
    visible_to: set[Role]
    sensitivity: Literal["public", "confidential", "restricted"]
    tags: set[str] = Field(default_factory=set)


class SharedMemory:
    LEVELS = {"public": 0, "confidential": 1, "restricted": 2}

    def __init__(self) -> None:
        self.records: list[MemoryRecord] = []

    def add(self, record: MemoryRecord) -> None:
        self.records.append(record)

    def search(self, query: str, requester: AgentIdentity) -> list[MemoryRecord]:
        results: list[MemoryRecord] = []
        for record in self.records:
            if requester.role not in record.visible_to:
                continue
            if self.LEVELS[requester.trust_tier] < self.LEVELS[record.sensitivity]:
                continue
            if query.lower() in record.text.lower() or query.lower() in {tag.lower() for tag in record.tags}:
                results.append(record)
        return results


class ToolGateway:
    LEVELS = {"public": 0, "confidential": 1, "restricted": 2}

    def call(self, request: ToolRequest) -> dict[str, Any]:
        if request.tool not in request.caller.allowed_tools:
            raise PermissionError(f"{request.caller.role.value} cannot use {request.tool.value}")
        if self.LEVELS[request.caller.trust_tier] < self.LEVELS[request.sensitivity]:
            raise PermissionError("Insufficient clearance for requested data")

        if request.tool == Tool.RUN_TESTS:
            if request.caller.role != Role.QA:
                raise PermissionError("Only QA can run tests")
            return {"test_result": run_tests(CodePatch.model_validate(request.args["patch"]))}

        if request.tool == Tool.SECURITY_SCAN:
            if request.caller.role != Role.SECURITY:
                raise PermissionError("Only Security can run scans")
            return {"security_review": security_scan(CodePatch.model_validate(request.args["patch"]))}

        if request.tool == Tool.WRITE_PATCH:
            if request.caller.role != Role.CODER:
                raise PermissionError("Only Coder can write patches")
            return {"status": "patch accepted"}

        if request.tool == Tool.SEARCH_MEMORY:
            return {"status": "use SharedMemory.search directly in this instructor solution"}

        raise ValueError(f"Unknown tool: {request.tool}")


def parse_issue(issue: str) -> TaskSpec:
    return TaskSpec(
        goal=issue,
        acceptance_criteria=[
            "Expose slugify(text)",
            "Lowercase text",
            "Replace whitespace with hyphens",
            "Include passing tests",
        ],
        risk="medium",
    )


def decompose(task: TaskSpec) -> list[SubTask]:
    return [
        SubTask(title="Implement utility", owner=Role.CODER, done_when=["slugify.py contains slugify"]),
        SubTask(title="Test behavior", owner=Role.QA, done_when=task.acceptance_criteria),
        SubTask(title="Review safety", owner=Role.SECURITY, done_when=["No unsafe imports or filesystem access"]),
    ]


def route(task: TaskSpec) -> str:
    if task.risk == "high":
        return "reasoning_model"
    if len(task.acceptance_criteria) >= 4:
        return "code_specialist"
    return "fast_model"


def code(task: TaskSpec, feedback: list[str]) -> CodePatch:
    if feedback:
        implementation = 'def slugify(text):\n    return "-".join(text.lower().split())\n'
        rationale = "Fixed slug replacement after QA failure"
    else:
        implementation = "def slugify(text):\n    return text.lower()\n"
        rationale = "Initial implementation, likely incomplete"

    return CodePatch(
        files={"slugify.py": implementation},
        rationale=rationale,
        tests_to_run=["test_slugify_spaces", "test_slugify_lowercase"],
    )


def run_tests(patch: CodePatch) -> TestResult:
    namespace: dict[str, Any] = {"__builtins__": {}}
    try:
        exec(patch.files["slugify.py"], namespace, namespace)
        assert namespace["slugify"]("Hello World") == "hello-world"
        assert namespace["slugify"]("Already") == "already"
    except Exception as exc:
        return TestResult(
            passed=False,
            log=f"{type(exc).__name__}: {exc}",
            failing_tests=["test_slugify_spaces"],
        )
    return TestResult(passed=True, log="All tests passed")


def security_scan(patch: CodePatch) -> SecurityReview:
    unsafe = ["open(", "exec(", "eval(", "subprocess", "os."]
    findings = [
        f"Unsafe token found: {token}"
        for content in patch.files.values()
        for token in unsafe
        if token in content
    ]
    return SecurityReview(approved=not findings, findings=findings)


def run_company(issue: str, max_repairs: int = 2) -> PullRequestSummary:
    identities = {
        Role.CODER: AgentIdentity(role=Role.CODER, allowed_tools={Tool.WRITE_PATCH}, trust_tier="confidential"),
        Role.QA: AgentIdentity(role=Role.QA, allowed_tools={Tool.RUN_TESTS}, trust_tier="confidential"),
        Role.SECURITY: AgentIdentity(role=Role.SECURITY, allowed_tools={Tool.SECURITY_SCAN}, trust_tier="restricted"),
    }
    gateway = ToolGateway()
    memory = SharedMemory()

    task = parse_issue(issue)
    subtasks = decompose(task)
    route_choice = route(task)
    memory.add(
        MemoryRecord(
            text=f"Task route: {route_choice}",
            visible_to={Role.CODER, Role.QA, Role.SECURITY, Role.RELEASE},
            sensitivity="confidential",
            tags={"route"},
        )
    )

    feedback: list[str] = []
    final_patch: CodePatch | None = None
    final_test: TestResult | None = None
    final_security: SecurityReview | None = None

    for attempt in range(max_repairs + 1):
        patch = code(task, feedback)
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
        memory.add(
            MemoryRecord(
                text=f"Attempt {attempt}: {test_result.log}",
                visible_to={Role.CODER, Role.QA, Role.SECURITY},
                sensitivity="confidential",
                tags={"test", "repair"},
            )
        )

        if test_result.passed:
            security_payload = gateway.call(
                ToolRequest(
                    caller=identities[Role.SECURITY],
                    tool=Tool.SECURITY_SCAN,
                    args={"patch": patch.model_dump(mode="json")},
                    sensitivity="confidential",
                )
            )
            security_review: SecurityReview = security_payload["security_review"]
            if security_review.approved:
                final_patch = patch
                final_test = test_result
                final_security = security_review
                break
            feedback.extend(security_review.findings)
        else:
            feedback.append(test_result.log)
    else:
        return PullRequestSummary(
            status="ESCALATED_TO_HUMAN",
            title="Escalation required: slugify utility",
            body=f"Repair budget exhausted for `{task.goal}` after {max_repairs + 1} attempts.",
            tests=feedback or ["No passing tests"],
            risks=["Repair budget exhausted"],
        )

    assert final_patch is not None
    assert final_test is not None
    assert final_security is not None

    return PullRequestSummary(
        status="SHIPPED",
        title="Add slugify utility",
        body=(
            f"Implements `{task.goal}` using route `{route_choice}`. "
            f"Subtasks completed: {[subtask.title for subtask in subtasks]}. "
            f"Final rationale: {final_patch.rationale}."
        ),
        tests=[final_test.log],
        risks=final_security.findings or ["No security findings"],
    )


app = FastAPI(title="Virtual Software Company Capstone API")


class ExternalTaskRequest(StrictModel):
    source: Literal["github", "slack", "jira", "a2a"] = "github"
    issue: str
    risk: Literal["low", "medium", "high"] = "medium"
    requester: str


class ApiCallerIdentity(StrictModel):
    organization: Literal["internal", "external_vendor"]
    role: Literal["product_manager", "vendor_reporter"]
    trust_tier: Literal["public", "confidential"]


class TaskStatusResponse(StrictModel):
    task_id: str
    status: Literal["PENDING", "RUNNING", "SHIPPED", "ESCALATED"]
    pull_request_summary: dict[str, Any] | None = None


task_store: dict[str, dict[str, Any]] = {}


def get_api_identity(x_api_key: str = Header(default="", alias="X-API-Key")) -> ApiCallerIdentity:
    if x_api_key == "sk-internal-admin":
        return ApiCallerIdentity(
            organization="internal",
            role="product_manager",
            trust_tier="confidential",
        )
    if x_api_key == "sk-external-vendor":
        return ApiCallerIdentity(
            organization="external_vendor",
            role="vendor_reporter",
            trust_tier="public",
        )
    raise HTTPException(status_code=401, detail="Invalid API key")


async def run_company_background(task_id: str, request: ExternalTaskRequest) -> None:
    task_store[task_id]["status"] = "RUNNING"
    await asyncio.sleep(0.01)
    summary = run_company(request.issue)
    task_store[task_id]["status"] = "SHIPPED" if summary.status == "SHIPPED" else "ESCALATED"
    task_store[task_id]["pull_request_summary"] = summary.model_dump(mode="json")


@app.post("/tasks", response_model=TaskStatusResponse, status_code=202)
async def create_task(
    request: ExternalTaskRequest,
    background_tasks: BackgroundTasks,
    identity: ApiCallerIdentity = Depends(get_api_identity),
) -> dict[str, Any]:
    if identity.organization == "external_vendor" and request.risk == "high":
        raise HTTPException(status_code=403, detail="External vendors cannot request high-risk work")

    task_id = f"task-{uuid4().hex[:8]}"
    task_store[task_id] = {
        "task_id": task_id,
        "status": "PENDING",
        "pull_request_summary": None,
    }
    background_tasks.add_task(run_company_background, task_id, request)
    return task_store[task_id]


@app.get("/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task(task_id: str) -> dict[str, Any]:
    if task_id not in task_store:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_store[task_id]


def demo_controls() -> None:
    gateway = ToolGateway()
    coder = AgentIdentity(role=Role.CODER, allowed_tools={Tool.WRITE_PATCH}, trust_tier="confidential")
    try:
        gateway.call(
            ToolRequest(
                caller=coder,
                tool=Tool.RUN_TESTS,
                args={},
                sensitivity="confidential",
            )
        )
    except PermissionError as exc:
        print("Unauthorized tool blocked:", exc)

    memory = SharedMemory()
    memory.add(
        MemoryRecord(
            text="Restricted deployment secret",
            visible_to={Role.SECURITY},
            sensitivity="restricted",
            tags={"secret"},
        )
    )
    print("Coder secret search:", memory.search("secret", coder))

    try:
        CodePatch(files={"../escape.py": "print(1)"}, rationale="bad", tests_to_run=["test"])
    except ValidationError as exc:
        print("Unsafe patch blocked:", exc.errors()[0]["msg"])


if __name__ == "__main__":
    demo_controls()
    print(run_company("Create a slugify(text) utility with tests.").model_dump_json(indent=2))
