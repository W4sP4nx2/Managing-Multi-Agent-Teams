"""Three-agent reference: real CrewAI tasks, fixture LLMs, Python-owned recovery.

Teaching entry point: open 01_Bridge_Sequential_Crew.ipynb in JupyterLab.
That notebook imports this module; running this file alone starts no demonstration.
The guided exercise is in ASSIGNMENTS.md under Assignment 09.

Use the course's pinned CrewAI 1.15.23 environment. Configure temporary
CREWAI_STORAGE_DIR and disable telemetry before importing CrewAI (see notebook).
No provider-backed execution or arbitrary generated-code execution is supplied.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Callable, Literal

from crewai import Agent, Crew, Process, Task
from crewai.llms.base_llm import BaseLLM
from crewai.tasks.task_output import TaskOutput
from crewai.tools import BaseTool
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, ValidationError

MAX_ATTEMPTS = 3  # Three total kickoffs, not an initial call plus three retries.
FIXTURE_CODE = "def add(a, b):\n    return a + b\n"


class StrictContract(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, revalidate_instances="always")


class WorkOrder(StrictContract):
    task_id: str = Field(min_length=1)
    spec: str = Field(min_length=1)


class CodePatch(StrictContract):
    task_id: str = Field(min_length=1)
    code: str = Field(min_length=1)


class QAReport(StrictContract):
    task_id: str = Field(min_length=1)
    passed: bool
    patch_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    checks: list[str] = Field(min_length=1)


class ManagerDecision(StrictContract):
    task_id: str = Field(min_length=1)
    status: Literal["approved", "needs_changes"]
    reason: str = Field(min_length=1)


class AttemptFailure(StrictContract):
    attempt: int = Field(ge=1, le=MAX_ATTEMPTS)
    error_type: str
    message: str


class EscalationReport(StrictContract):
    task_id: str
    status: Literal["escalated"] = "escalated"
    code: Literal["ESCALATION_TRIGGERED"] = "ESCALATION_TRIGGERED"
    attempts: Literal[3] = MAX_ATTEMPTS
    failures: list[AttemptFailure] = Field(min_length=3, max_length=3)
    next_action: str = "Human review required. Inspect failures before authorizing another run."


class ApprovedResult(StrictContract):
    status: Literal["approved"] = "approved"
    attempts: int = Field(ge=1, le=MAX_ATTEMPTS)
    patch: CodePatch
    qa: QAReport
    decision: ManagerDecision


class SimulatedInfrastructureError(RuntimeError):
    """Expected fixture failure, eligible for the bounded retry policy."""


class ReviewNeedsChanges(RuntimeError):
    """A structurally valid result failed an application acceptance check."""


def strict_guardrail(schema: type[StrictContract]):
    """Validate raw JSON before any model-based conversion or next task.

    ValidationError deliberately propagates to the caller. Returning TaskOutput
    with its validated model avoids CrewAI's fallback conversion/repair calls.
    """
    def validate(output: TaskOutput):
        output.pydantic = schema.model_validate_json(output.raw)
        return True, output
    return validate


class FixtureLLM(BaseLLM):
    """Scripted agent response at the LLM boundary; no network implementation."""
    _respond: Callable = PrivateAttr()

    def __init__(self, respond: Callable):
        super().__init__(model="offline/fixture", provider="offline")
        self._respond = respond

    def call(self, messages, **kwargs):
        # Run the real Agent/Task executor while substituting only its model.
        return "Final Answer: " + self._respond()

    def supports_function_calling(self) -> bool:
        return False


@dataclass
class FixtureState:
    code_tool: BaseTool | None = None
    overrides: dict[str, str] = field(default_factory=dict)
    trace: list[tuple[int, str]] = field(default_factory=list)
    kickoffs: int = 0
    feedback_received: list[list[dict]] = field(default_factory=list)


def build_crew(order: WorkOrder, state: FixtureState, attempt: int,
               feedback: list[AttemptFailure] | None = None) -> Crew:
    """Build a fresh three-agent/four-task graph for one bounded attempt.

    The fixture calls the Coder's injected tool once per Coder response. It does
    not simulate autonomous tool selection or CrewAI's native tool-repair loop.
    Manager writes a brief and reviews; Coder proposes; QA checks the fixture.
    """
    order = WorkOrder.model_validate(order)
    feedback_payload = [f.model_dump() for f in (feedback or [])]
    state.feedback_received.append(feedback_payload)
    tasks: dict[str, Task] = {}

    def respond(name):
        state.trace.append((attempt, name))
        if name in state.overrides:
            return state.overrides[name]
        if name == "brief":
            result = order
        elif name == "code":
            brief = tasks["brief"].output.pydantic
            code = state.code_tool.run(spec=brief.spec) if state.code_tool else FIXTURE_CODE
            result = CodePatch(task_id=brief.task_id, code=code)
        elif name == "qa":
            patch = tasks["code"].output.pydantic
            result = QAReport(task_id=patch.task_id, passed=patch.code == FIXTURE_CODE,
                              patch_sha256=sha256(patch.code.encode()).hexdigest(),
                              checks=["Exact match to the supplied add-function fixture; no code executed."])
        else:
            qa = tasks["qa"].output.pydantic
            result = ManagerDecision(task_id=qa.task_id,
                                     status="approved" if qa.passed else "needs_changes",
                                     reason="Inspect the typed QA fixture evidence.")
        return result.model_dump_json()

    # Manager is one Agent reused for two tasks, not a fourth agent.
    manager_calls = iter(("brief", "review"))
    manager = Agent(role="Manager", goal="Scope and review the work",
                    backstory="Owns the brief and approval; does not write code or run QA.",
                    llm=FixtureLLM(lambda: respond(next(manager_calls))), tools=[],
                    allow_delegation=False, max_iter=1, max_retry_limit=0, verbose=False)
    coder = Agent(role="Coder", goal="Propose a patch", backstory="Writes, but cannot approve.",
                  llm=FixtureLLM(lambda: respond("code")),
                  tools=[state.code_tool] if state.code_tool else [],
                  allow_delegation=False, max_iter=1, max_retry_limit=0, verbose=False)
    qa = Agent(role="QA", goal="Return independent check evidence",
               backstory="Checks the supplied fixture; cannot approve or change the patch.",
               llm=FixtureLLM(lambda: respond("qa")), tools=[],
               allow_delegation=False, max_iter=1, max_retry_limit=0, verbose=False)
    definitions = [
        ("brief", manager, WorkOrder, [], "Return the work order: " + order.model_dump_json()),
        ("code", coder, CodePatch, ["brief"], "Return a patch. Prior failure evidence: " + json.dumps(feedback_payload)),
        ("qa", qa, QAReport, ["code"], "Check the supplied patch fixture and return evidence."),
        ("review", manager, ManagerDecision, ["brief", "code", "qa"], "Review the QA evidence."),
    ]
    for name, agent, schema, dependencies, description in definitions:
        tasks[name] = Task(name=name, description=description, expected_output=f"{schema.__name__} JSON",
                           agent=agent, context=[tasks[n] for n in dependencies],
                           output_pydantic=schema, guardrail=strict_guardrail(schema),
                           guardrail_max_retries=0)
    return Crew(agents=[manager, coder, qa], tasks=list(tasks.values()),
                process=Process.sequential, verbose=False, tracing=False, memory=False, cache=False)


def escalate_to_human(order: WorkOrder, failures: list[AttemptFailure]) -> EscalationReport:
    """Return a review ticket locally. No email, chat message, or deployment runs."""
    return EscalationReport(task_id=order.task_id, failures=failures)


def run_team(order: WorkOrder, state: FixtureState) -> ApprovedResult | EscalationReport:
    """Retry recognized failures with at most three real Crew.kickoff calls.

    Each failed kickoff stops its task chain. Only the exceptions named below
    authorize another fresh attempt; unexpected exceptions propagate to callers.
    Successful task execution still needs matching evidence and both approvals.
    """
    order = WorkOrder.model_validate(order)
    failures: list[AttemptFailure] = []
    max_attempts = MAX_ATTEMPTS
    for attempt in range(1, max_attempts + 1):
        crew = build_crew(order, state, attempt, failures)
        state.kickoffs += 1
        try:
            result = crew.kickoff(inputs={"task_id": order.task_id})
            brief, patch, qa, decision = [t.pydantic for t in result.tasks_output]
            # Revalidate even model instances; a typed status alone is not approval.
            brief = WorkOrder.model_validate(brief)
            patch = CodePatch.model_validate(patch)
            qa = QAReport.model_validate(qa)
            decision = ManagerDecision.model_validate(decision)
            if any(item.task_id != order.task_id for item in (brief, patch, qa, decision)):
                raise ReviewNeedsChanges("A handoff belongs to another task.")
            if qa.patch_sha256 != sha256(patch.code.encode()).hexdigest():
                raise ReviewNeedsChanges("QA evidence does not match the current patch.")
            if not qa.passed or decision.status != "approved":
                raise ReviewNeedsChanges("QA or Manager requires changes; release blocked.")
            return ApprovedResult(attempts=attempt, patch=patch, qa=qa, decision=decision)
        except (ValidationError, SimulatedInfrastructureError, ReviewNeedsChanges) as error:
            failures.append(AttemptFailure(attempt=attempt, error_type=type(error).__name__,
                                           message=str(error)))
    return escalate_to_human(order, failures)
