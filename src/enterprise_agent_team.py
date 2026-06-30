"""Production-style training template for managing a governed multi-agent team.

WARNING: This is a Deterministic Governance Shell. The agents are mocked to
ensure the Pydantic contracts, memory routing, MCP-shaped gateway, and repair
loop can be tested offline. In production, replace the deterministic agent
functions with LLM/framework calls constrained by these same schemas.

Run:
    python3 src/enterprise_agent_team.py

The local MCP gateway below is explicitly a teaching adapter. It mirrors the
shape of MCP tool discovery and tool calls so learners can run the module
offline. In production, replace LocalTrainingMcpGateway with the official MCP
Python SDK client/server transport and keep the same ToolRequest/ToolResult
contracts at the orchestration boundary.
"""

from __future__ import annotations

import json
import textwrap
from enum import Enum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


class AgentRole(str, Enum):
    PRODUCT_MANAGER = "product_manager"
    CODER = "coder"
    QA = "qa"
    SECURITY_REVIEWER = "security_reviewer"
    ROUTER = "router"


class ToolName(str, Enum):
    SEARCH_MEMORY = "search_memory"
    EXECUTE_TESTS = "execute_tests"
    READ_REPO = "read_repo"
    WRITE_PATCH = "write_patch"
    CALL_EXTERNAL_API = "call_external_api"


class TrustTier(str, Enum):
    PUBLIC = "public"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class StrictModel(BaseModel):
    """Base class forbids surprise fields, a common source of agent drift."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class AgentIdentity(StrictModel):
    agent_id: str
    role: AgentRole
    org_id: str
    scopes: set[ToolName]
    clearance: TrustTier


class TaskSpec(StrictModel):
    """The PM's typed contract for downstream agents."""

    task_id: str = Field(default_factory=lambda: f"task-{uuid4().hex[:8]}")
    goal: str = Field(min_length=8)
    acceptance_criteria: list[str] = Field(min_length=1)
    constraints: list[str] = Field(default_factory=list)
    risk_level: Literal["low", "medium", "high"] = "medium"

    @field_validator("acceptance_criteria")
    @classmethod
    def criteria_must_be_actionable(cls, value: list[str]) -> list[str]:
        if any(len(item.strip()) < 8 for item in value):
            raise ValueError("Each acceptance criterion must be actionable.")
        return value


class TeamCommitment(StrictModel):
    """TeamLog-inspired shared commitment."""

    owner: AgentRole
    commitment: str
    visible_to: set[AgentRole]
    sensitivity: TrustTier


class MemoryRecord(StrictModel):
    record_id: str = Field(default_factory=lambda: f"mem-{uuid4().hex[:8]}")
    text: str
    tags: set[str]
    sensitivity: TrustTier
    author: AgentRole


class CodeFile(StrictModel):
    path: str
    content: str

    @field_validator("path")
    @classmethod
    def path_must_be_relative_python(cls, value: str) -> str:
        if value.startswith("/") or ".." in value.split("/"):
            raise ValueError("Patch paths must be relative and cannot escape the repo.")
        if not value.endswith(".py"):
            raise ValueError("This training template only accepts Python files.")
        return value


class CodePatch(StrictModel):
    patch_id: str = Field(default_factory=lambda: f"patch-{uuid4().hex[:8]}")
    files: list[CodeFile] = Field(min_length=1)
    rationale: str = Field(min_length=12)
    tests_to_run: list[str] = Field(min_length=1)


class TestResult(StrictModel):
    passed: bool
    failing_tests: list[str] = Field(default_factory=list)
    log: str


class ReviewDecision(StrictModel):
    approved: bool
    reasons: list[str]
    next_action: Literal["ship", "repair", "escalate"]


class RouteDecision(StrictModel):
    """Fugu-style heterogeneous routing decision."""

    selected_worker: Literal["fast_small_model", "deep_reasoning_model", "security_specialist"]
    reason: str
    estimated_cost_class: Literal["low", "medium", "high"]


class ToolRequest(StrictModel):
    request_id: str = Field(default_factory=lambda: f"tool-{uuid4().hex[:8]}")
    caller: AgentIdentity
    tool: ToolName
    args: dict[str, Any]
    data_sensitivity: TrustTier


class ToolResult(StrictModel):
    request_id: str
    tool: ToolName
    ok: bool
    result: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class TeamState(StrictModel):
    task: TaskSpec | None = None
    commitments: list[TeamCommitment] = Field(default_factory=list)
    route_trace: list[RouteDecision] = Field(default_factory=list)
    patch: CodePatch | None = None
    test_result: TestResult | None = None
    review: ReviewDecision | None = None
    repair_attempts: int = 0


class SharedAgenticMemory:
    """Small agentic RAG stand-in: tag-aware, sensitivity-aware retrieval."""

    def __init__(self) -> None:
        self._records: list[MemoryRecord] = []

    def add(self, record: MemoryRecord) -> None:
        self._records.append(record)

    def search(self, query: str, requester: AgentIdentity) -> list[MemoryRecord]:
        query_terms = set(query.lower().split())
        visible: list[MemoryRecord] = []
        for record in self._records:
            if not self._can_read(requester.clearance, record.sensitivity):
                continue
            haystack = set(record.text.lower().split()) | {tag.lower() for tag in record.tags}
            if query_terms & haystack:
                visible.append(record)
        return visible

    @staticmethod
    def _can_read(clearance: TrustTier, sensitivity: TrustTier) -> bool:
        order = {
            TrustTier.PUBLIC: 0,
            TrustTier.CONFIDENTIAL: 1,
            TrustTier.RESTRICTED: 2,
        }
        return order[clearance] >= order[sensitivity]


class ToolPolicy:
    """Zero-trust authorization: every tool call is checked every time."""

    def authorize(self, request: ToolRequest) -> None:
        if request.tool not in request.caller.scopes:
            raise PermissionError(
                f"{request.caller.role} is not allowed to call {request.tool}."
            )
        if request.data_sensitivity == TrustTier.RESTRICTED and request.caller.clearance != TrustTier.RESTRICTED:
            raise PermissionError("Restricted data requires restricted clearance.")


def check_teamlog_commitments(
    request: ToolRequest,
    commitments: list[TeamCommitment],
) -> None:
    """Block tool calls that violate visible TeamLog commitments.

    TeamLog commitments are global mission constraints. They intentionally sit
    above an individual agent's local goal, so a tool can be in scope and still
    be denied when it violates a team-level promise.
    """

    for commitment in commitments:
        if request.caller.role not in commitment.visible_to:
            continue
        text = commitment.commitment.lower()
        if "no external" in text and request.tool == ToolName.CALL_EXTERNAL_API:
            raise PermissionError(
                f"Violation of TeamLog commitment: {commitment.commitment}"
            )


class LocalTrainingMcpGateway:
    """MCP-shaped local adapter for offline notebooks.

    Production replacement:
        - expose tools with mcp.server.fastmcp.FastMCP
        - connect with the MCP Python SDK client transport
        - keep ToolRequest and ToolResult as the application data contracts
    """

    def __init__(self, memory: SharedAgenticMemory, policy: ToolPolicy) -> None:
        self.memory = memory
        self.policy = policy

    def list_tools(self, caller: AgentIdentity) -> list[ToolName]:
        return sorted(caller.scopes, key=str)

    def call_tool(
        self,
        request: ToolRequest,
        commitments: list[TeamCommitment] | None = None,
    ) -> ToolResult:
        self.policy.authorize(request)
        check_teamlog_commitments(request, commitments or [])
        try:
            if request.tool == ToolName.SEARCH_MEMORY:
                records = self.memory.search(str(request.args["query"]), request.caller)
                return ToolResult(
                    request_id=request.request_id,
                    tool=request.tool,
                    ok=True,
                    result={"records": [record.model_dump(mode="json") for record in records]},
                )
            if request.tool == ToolName.EXECUTE_TESTS:
                result = run_python_patch_tests(CodePatch.model_validate(request.args["patch"]))
                return ToolResult(
                    request_id=request.request_id,
                    tool=request.tool,
                    ok=True,
                    result=result.model_dump(mode="json"),
                )
            raise ValueError(f"Tool {request.tool} exists in policy but has no handler.")
        except Exception as exc:
            return ToolResult(
                request_id=request.request_id,
                tool=request.tool,
                ok=False,
                error=str(exc),
            )


def run_python_patch_tests(patch: CodePatch) -> TestResult:
    """Run a tiny course-safe test harness.

    In production, execute untrusted code in an isolated container or remote
    sandbox. The important pattern is that QA receives a typed CodePatch and
    emits a typed TestResult; raw strings never become agent-to-agent contracts.
    """

    # [DETERMINISTIC MOCK] Replace with a sandboxed test runner in production.
    namespace: dict[str, Any] = {"__builtins__": {"abs": abs, "ValueError": ValueError}}
    try:
        for file in patch.files:
            exec(file.content, namespace, namespace)
        namespace["add"](2, 3)
        assert namespace["add"](2, 3) == 5, "add(2, 3) must return 5"
        assert namespace["add"](-2, 2) == 0, "add(-2, 2) must return 0"
    except Exception as exc:
        return TestResult(
            passed=False,
            failing_tests=["test_addition_contract"],
            log=f"{type(exc).__name__}: {exc}",
        )
    return TestResult(passed=True, log="All acceptance tests passed.")


def product_manager_parse_issue(issue: str) -> TaskSpec:
    """The PM turns vague vibe-coding input into an enforceable contract."""

    # [DETERMINISTIC MOCK] Replace with an LLM call constrained to TaskSpec.
    return TaskSpec(
        goal=f"Implement the requested behavior: {issue}",
        acceptance_criteria=[
            "Expose an add(a, b) Python function.",
            "Return correct sums for positive and negative integers.",
        ],
        constraints=["No filesystem access inside generated code.", "Keep implementation minimal."],
        risk_level="medium",
    )


def fugu_route(task: TaskSpec) -> RouteDecision:
    """Heterogeneous routing: choose model class by risk and complexity."""

    # [DETERMINISTIC MOCK] Replace with an observed model/router in production.
    complexity = len(task.acceptance_criteria) + len(task.constraints)
    if task.risk_level == "high":
        return RouteDecision(
            selected_worker="security_specialist",
            reason="High-risk task requires security specialist review.",
            estimated_cost_class="high",
        )
    if complexity >= 4:
        return RouteDecision(
            selected_worker="deep_reasoning_model",
            reason="Multiple constraints require deeper reasoning.",
            estimated_cost_class="medium",
        )
    return RouteDecision(
        selected_worker="fast_small_model",
        reason="Low-complexity task can use a fast worker.",
        estimated_cost_class="low",
    )


def coder_generate_patch(task: TaskSpec, repair_attempts: int, memories: list[MemoryRecord]) -> CodePatch:
    """Coder uses task contract plus TeamLog memory, never hidden globals."""

    # [DETERMINISTIC MOCK] Replace with an LLM/code agent constrained to CodePatch.
    failure_context = " ".join(record.text for record in memories)
    should_repair = repair_attempts > 0 or "AssertionError" in failure_context
    operator = "+" if should_repair else "-"
    return CodePatch(
        files=[
            CodeFile(
                path="team_math.py",
                content=textwrap.dedent(
                    f"""
                    def add(a, b):
                        \"\"\"Return the sum of two numbers.\"\"\"
                        return a {operator} b
                    """
                ).strip(),
            )
        ],
        rationale=(
            "Repairing failed QA contract with correct addition."
            if should_repair
            else "Initial implementation generated from the typed TaskSpec."
        ),
        tests_to_run=["test_addition_contract"],
    )


def reviewer_decide(test_result: TestResult) -> ReviewDecision:
    """ChatDev-style review gate routes failures back to the coder."""

    # [DETERMINISTIC MOCK] Replace with a reviewer agent if judgment is needed.
    if test_result.passed:
        return ReviewDecision(
            approved=True,
            reasons=["Patch satisfies all acceptance tests."],
            next_action="ship",
        )
    return ReviewDecision(
        approved=False,
        reasons=[f"QA failed: {test_result.log}"],
        next_action="repair",
    )


def run_virtual_software_company(issue: str) -> TeamState:
    """End-to-end flow: Brain -> Nervous System -> Body -> Reflexes -> Ecosystem."""

    pm = AgentIdentity(
        agent_id="pm-001",
        role=AgentRole.PRODUCT_MANAGER,
        org_id="training",
        scopes={ToolName.SEARCH_MEMORY},
        clearance=TrustTier.CONFIDENTIAL,
    )
    coder = AgentIdentity(
        agent_id="coder-001",
        role=AgentRole.CODER,
        org_id="training",
        scopes={ToolName.SEARCH_MEMORY, ToolName.WRITE_PATCH},
        clearance=TrustTier.CONFIDENTIAL,
    )
    qa = AgentIdentity(
        agent_id="qa-001",
        role=AgentRole.QA,
        org_id="training",
        scopes={ToolName.SEARCH_MEMORY, ToolName.EXECUTE_TESTS},
        clearance=TrustTier.CONFIDENTIAL,
    )

    state = TeamState()
    memory = SharedAgenticMemory()
    gateway = LocalTrainingMcpGateway(memory=memory, policy=ToolPolicy())

    state.task = product_manager_parse_issue(issue)
    state.commitments.append(
        TeamCommitment(
            owner=AgentRole.PRODUCT_MANAGER,
            commitment="All agents must satisfy the typed TaskSpec before shipping.",
            visible_to={AgentRole.CODER, AgentRole.QA, AgentRole.SECURITY_REVIEWER},
            sensitivity=TrustTier.CONFIDENTIAL,
        )
    )
    memory.add(
        MemoryRecord(
            text=json.dumps(state.task.model_dump(mode="json")),
            tags={"task", "acceptance", "teamlog"},
            sensitivity=TrustTier.CONFIDENTIAL,
            author=AgentRole.PRODUCT_MANAGER,
        )
    )

    state.route_trace.append(fugu_route(state.task))

    while state.repair_attempts <= 2:
        search_result = gateway.call_tool(
            ToolRequest(
                caller=coder,
                tool=ToolName.SEARCH_MEMORY,
                args={"query": "task acceptance AssertionError"},
                data_sensitivity=TrustTier.CONFIDENTIAL,
            )
        )
        memories = [
            MemoryRecord.model_validate(record)
            for record in search_result.result.get("records", [])
        ]
        state.patch = coder_generate_patch(state.task, state.repair_attempts, memories)

        tool_result = gateway.call_tool(
            ToolRequest(
                caller=qa,
                tool=ToolName.EXECUTE_TESTS,
                args={"patch": state.patch.model_dump(mode="json")},
                data_sensitivity=TrustTier.CONFIDENTIAL,
            )
        )
        if not tool_result.ok:
            raise RuntimeError(tool_result.error)
        state.test_result = TestResult.model_validate(tool_result.result)
        state.review = reviewer_decide(state.test_result)

        if state.review.next_action == "ship":
            return state

        memory.add(
            MemoryRecord(
                text=state.test_result.log,
                tags={"qa", "failure", "AssertionError"},
                sensitivity=TrustTier.CONFIDENTIAL,
                author=AgentRole.QA,
            )
        )
        state.repair_attempts += 1

    state.review = ReviewDecision(
        approved=False,
        reasons=["Repair budget exhausted."],
        next_action="escalate",
    )
    return state


def demonstrate_schema_enforcement() -> str:
    """Show learners that invalid inter-agent messages stop at the boundary."""

    try:
        CodePatch.model_validate(
            {
                "files": [{"path": "../escape.py", "content": "def add(a, b): return a + b"}],
                "rationale": "unsafe path",
                "tests_to_run": ["test_addition_contract"],
                "extra_field": "agent hallucination",
            }
        )
    except ValidationError as exc:
        return exc.errors()[0]["msg"]
    return "Unexpectedly accepted invalid patch."


if __name__ == "__main__":
    final_state = run_virtual_software_company("Create a safe add function for a shared utility module.")
    print(json.dumps(final_state.model_dump(mode="json"), indent=2))
    print("\nSchema enforcement demo:", demonstrate_schema_enforcement())
