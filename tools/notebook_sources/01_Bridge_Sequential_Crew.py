# %% {"id": "bridge-intro", "type": "markdown"}
# # Advanced reference: a bounded Manager–Coder–QA crew
#
# **Optional reference, no marks or new lab.** Follow [Lab 2](../notebooks/02_lab_crewai.ipynb) with this example for [Lecture 8](../ASSIGNMENTS.md#assignment-08-debugging-sdlc) and [Assignment 09: Framework Comparison](../ASSIGNMENTS.md#assignment-09-framework-comparison).
#
# **Teaching route:** follow the [guided read/run/explain exercise](../ASSIGNMENTS.md#assignment-09-guided-bridge-exercise). This notebook imports [coding_team.py](coding_team.py) in its setup cell; run the notebook cells to observe the lesson. Running that Python file alone starts no demonstration.
#
# This notebook runs real `Crew.kickoff()`, Agent executors, task context, and callable guardrails. Each agent uses a scripted local `FixtureLLM`; no trained language model or reasoning model runs, and no provider is called. Exactly three agents perform four tasks: Manager brief → Coder patch → QA evidence → Manager review. Python owns the retry budget and escalation.
#
# The responsibilities form a management hierarchy. Execution uses `Process.sequential`; this is not a demonstration of CrewAI's dynamic `Process.hierarchical` delegation. The production-oriented lesson is an enforced boundary with observable failures. The fixture does not establish production readiness or real code quality.
#
# | Your action | What you interact with | Evidence to inspect |
# | --- | --- | --- |
# | Run setup and inspect | Three CrewAI agents, four tasks, explicit context and strict output contracts | The printed task-to-schema mapping and Python retry wrapper |
# | Create and run a crew | Real sequential CrewAI execution with scripted local responses | Four recorded task calls and the final Manager task displayed as Markdown |
# | Run failure and recovery cases | Local invalid-output and failing-tool fixtures | Stopped downstream tasks, at most three attempts, and typed escalation or recovery |
# | Finish | Compare framework execution with application governance | Explain why a raw final-task result alone does not authorize approval |
#
# **Execution note:** Course execution uses no language model, reasoning model, API key, or hosted platform. Model-selection instructions in external videos do not apply here. Unchanged fixtures give the same task outputs; changing a fixture or tool changes the observed result. A future provider-backed implementation can vary for the same input and would need separate evaluation.
#
# **Predict:** If the Coder returns garbage or its tool always fails, which task must never run next?

# %% {"id": "bridge-setup", "type": "code"}
from pathlib import Path
import asyncio
import os
import sys
import tempfile

ROOT = next(p for p in (Path.cwd(), *Path.cwd().parents) if (p / "requirements.txt").exists())
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
USE_LIVE_LLM = False
runtime_directory = tempfile.TemporaryDirectory(prefix="crewai-reference-")
os.environ["CREWAI_STORAGE_DIR"] = runtime_directory.name
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TRACING_ENABLED"] = "false"
os.environ["CREWAI_TELEMETRY_ENABLED"] = "false"

from crewai_learning.offline import blocked_network
with blocked_network() as import_network_attempts:
    from crewai.tools import tool
    from pydantic import ValidationError
    from crewai_learning.coding_team import (
        MAX_ATTEMPTS, ApprovedResult, EscalationReport, FixtureState,
        SimulatedInfrastructureError, WorkOrder, build_crew, run_team,
    )
assert import_network_attempts == []
order = WorkOrder(task_id="add-001", spec="Propose a function that adds two numbers.")
print("Offline reference ready; maximum total attempts:", MAX_ATTEMPTS)

# %% {"id": "bridge-contracts", "type": "markdown"}
# ## Creating the Crew
#
# `build_crew(...)` creates the real `Crew` used below. It assigns three agents to four tasks and supplies each dependency through `Task.context`. The final constructor in [coding_team.py](coding_team.py) is:
#
# ```python
# Crew(
#     agents=[manager, coder, qa],
#     tasks=list(tasks.values()),
#     process=Process.sequential,
#     verbose=False,
#     tracing=False,
#     memory=False,
#     cache=False,
# )
# ```
#
# In the pinned course API, `verbose` is a Boolean. Keep `memory=False`: context is passed explicitly between these tasks, and the wrapper passes typed failure records between attempts. This example needs no embedding service, persistent CrewAI memory, or new dependency. Constructing a crew configures the workflow; `kickoff` executes it.
#
# ### Inspect the executable controls
#
# Every task declares `output_pydantic` and a callable guardrail. The guardrail calls `model_validate_json` with strict types and `extra="forbid"`; a `ValidationError` escapes before the next task can consume malformed output. Returning the validated TaskOutput avoids model-based conversion/repair.
#
# `max_retry_limit=0` and `guardrail_max_retries=0` disable nested agent and validation retries. The wrapper owns **three total attempts**, not an initial attempt plus three retries. A fresh crew on each attempt avoids reusing failed task outputs. Typed failure records are passed into the next Coder task.
#
# Jupyter already runs an event loop. `await asyncio.to_thread(...)` runs the synchronous CrewAI wrapper in a worker thread; it does not add retries or replace `crew.kickoff()`.
#
# Read the reusable implementation in [coding_team.py](coding_team.py). QA compares the patch with a supplied fixture; it does not execute generated code. The application checks task IDs, the patch hash, QA status, and Manager approval before returning success.

# %% {"id": "bridge-inspect", "type": "code"}
import inspect
with blocked_network() as inspection_network_attempts:
    example = build_crew(order, FixtureState(), attempt=1)
assert inspection_network_attempts == []
assert [agent.role for agent in example.agents] == ["Manager", "Coder", "QA"]
for task in example.tasks:
    assert task.output_pydantic is not None and task.guardrail is not None
    assert task.guardrail_max_retries == 0
    print(task.name, "->", task.output_pydantic.__name__)
print(inspect.getsource(run_team))

# %% {"id": "bridge-run-crew-heading", "type": "markdown"}
# ## Running the Crew
#
# Create a fresh fixture state, then call `crew.kickoff(inputs=...)`. This is the framework execution boundary. The local fixture reads the typed work order created in setup; no company research, web search, or sales workflow is needed to study orchestration.
#
# CrewAI returns a `CrewOutput`. Its `.raw` string is the final task's text; here that task returns a JSON Manager decision. `IPython.display.Markdown` accepts text, so display `result.raw` inside a Markdown code block. `Markdown(result)` would pass the result object rather than its text.
#
# This direct kickoff shows the framework result before the application's acceptance checks. The later `run_team(...)` examples also require matching task IDs, current patch evidence, successful QA, and Manager approval.

# %% {"id": "bridge-run-crew", "type": "code"}
from IPython.display import Markdown, display

kickoff_state = FixtureState()
with blocked_network() as kickoff_network_attempts:
    crew = build_crew(order, kickoff_state, attempt=1)
    result = await asyncio.to_thread(crew.kickoff, inputs={"task_id": order.task_id})
assert kickoff_network_attempts == []
assert [name for _, name in kickoff_state.trace] == ["brief", "code", "qa", "review"]
assert len(result.tasks_output) == 4
assert result.pydantic.status == "approved"
display(Markdown("### Final Crew task: Manager decision\n\n```json\n" + result.raw + "\n```"))
print("Framework completed four tasks; run_team supplies the application acceptance gate.")

# %% {"id": "bridge-garbage", "type": "markdown"}
# ## Exception handling: stop the current run
#
# An exception policy determines whether execution stops, a recognized failure is retried, or a report is returned. CrewAI does not guarantee that every exception is harmless or that downstream tasks always continue. In this course's pinned configuration, the strict guardrail raises and the direct kickoff stops. The notebook catches that expected exception so you can inspect the evidence and run the next example.
#
# The raw Coder response below is deliberately invalid JSON. This is one direct kickoff so you can observe the actual `ValidationError`; the bounded wrapper will handle repeated failures in the next example. QA and Manager review must not run.
#
# CrewAI 1.15.23 emits an event-pairing diagnostic when a guardrail raises `ValidationError`. The assertions below verify the exception and stopped task sequence; this diagnostic does not mean that the invalid result was accepted.

# %% {"id": "bridge-validation-proof", "type": "code"}
garbage = FixtureState(overrides={"code": "not a JSON patch"})
with blocked_network() as validation_network_attempts:
    try:
        await asyncio.to_thread(build_crew(order, garbage, attempt=1).kickoff)
    except ValidationError as error:
        validation_error_name = type(error).__name__
        print("Rejected:", validation_error_name)
    else:
        raise AssertionError("Malformed output escaped validation")
assert [name for _, name in garbage.trace] == ["brief", "code"]
assert validation_network_attempts == []
print("QA calls: 0; Manager review calls: 0")

# %% {"id": "bridge-hard-stop", "type": "markdown"}
# ## Governed continuation: retry recognized failures, then stop
#
# `run_team` catches only `ValidationError`, `SimulatedInfrastructureError`, and `ReviewNeedsChanges`. It records a failure and starts a fresh crew for the next bounded attempt. It never forwards invalid output to QA. After three total failed attempts, it returns `EscalationReport`; unexpected programming errors propagate instead of entering the retry loop.
#
# The mock tool **raises on every call**, including the third. Returning an escalation-shaped string from the tool would be a normal tool result and would not prove a third failure. The wrapper catches the third exception and calls `escalate_to_human`, which returns a local typed ticket. It does not message anyone.
#
# The Coder's fixture invokes this tool once per Coder response. This isolates the wrapper's guarantee from autonomous tool selection and native tool-repair behavior.

# %% {"id": "bridge-failing-tool", "type": "code"}
attempt_count = 0

@tool("failing_code_tool")
def failing_code_tool(spec: str) -> str:
    """Always fail to demonstrate deterministic escalation after three attempts."""
    global attempt_count
    attempt_count += 1
    raise SimulatedInfrastructureError("Simulated infrastructure error")

failing_state = FixtureState(code_tool=failing_code_tool)
with blocked_network() as failure_network_attempts:
    escalation = await asyncio.to_thread(run_team, order, failing_state)
assert isinstance(escalation, EscalationReport)
assert attempt_count == failing_state.kickoffs == escalation.attempts == 3
assert len(escalation.failures) == 3
assert all(name in {"brief", "code"} for _, name in failing_state.trace)
assert failure_network_attempts == []
print(escalation.model_dump_json(indent=2))
print("Tool failures:", attempt_count, "| kickoffs:", failing_state.kickoffs, "| stopped: True")

# %% {"id": "bridge-recovery-heading", "type": "markdown"}
# ## Observe recovery within the same bound
#
# This local tool fails twice and succeeds on its third call. Predict the task trace: attempts 1 and 2 end at Coder; attempt 3 reaches QA and Manager review. Inspect `feedback_received` to see earlier typed failures passed into the next attempt. This is application-owned recovery across fresh kickoffs, rather than continuing an invalid task chain.

# %% {"id": "bridge-recovery", "type": "code"}
from crewai_learning.coding_team import FIXTURE_CODE

recovery_count = 0

@tool("recovering_code_tool")
def recovering_code_tool(spec: str) -> str:
    """Fail twice, then return the supplied add-function fixture."""
    global recovery_count
    recovery_count += 1
    if recovery_count < MAX_ATTEMPTS:
        raise SimulatedInfrastructureError("Temporary local fixture failure")
    return FIXTURE_CODE

recovering_state = FixtureState(code_tool=recovering_code_tool)
with blocked_network() as recovery_network_attempts:
    recovered = await asyncio.to_thread(run_team, order, recovering_state)
assert recovery_network_attempts == []
assert isinstance(recovered, ApprovedResult)
assert recovered.attempts == recovering_state.kickoffs == recovery_count == 3
assert [len(items) for items in recovering_state.feedback_received] == [0, 1, 2]
assert recovering_state.trace == [(1, "brief"), (1, "code"), (2, "brief"), (2, "code"),
                                  (3, "brief"), (3, "code"), (3, "qa"), (3, "review")]
print("Recovered on attempt:", recovered.attempts, "| prior failures supplied:",
      len(recovering_state.feedback_received[-1]))

# %% {"id": "bridge-success-heading", "type": "markdown"}
# ## Prove success stops early
#
# A reject-everything system would pass the failure demonstration without being useful. The valid fixture must complete on attempt one and return the patch, QA evidence, and Manager decision.

# %% {"id": "bridge-success", "type": "code"}
successful_state = FixtureState()
with blocked_network() as success_network_attempts:
    approved = await asyncio.to_thread(run_team, order, successful_state)
assert isinstance(approved, ApprovedResult)
assert approved.attempts == successful_state.kickoffs == 1
assert approved.qa.passed and approved.decision.status == "approved"
assert success_network_attempts == []
print(approved.model_dump_json(indent=2))

# %% {"id": "bridge-takeaways", "type": "markdown"}
# ## Transfer to the curriculum
#
# - **Lab 2:** inspect role tools and context. Here, the same boundaries are followed through actual CrewAI execution with local model fixtures.
# - **Lecture 8:** diagnose the observed `ValidationError` and tool failure, then explain why the wrapper stops.
# - **Assignment 09:** CrewAI expresses roles, dependencies, and task validation; Python makes this example's retry count, exception policy, and escalation deterministic. Compare the direct `CrewOutput`, the three-failure escalation, third-attempt recovery, and first-attempt success. More complex state/recovery can motivate a Flow or graph, but requires its own tests.
#
# These scenarios prove the declared contracts and call bounds for supplied fixtures. They do not prove model obedience, operating-system isolation, real QA, live-provider retries, or safe deployment. Before live use, separately evaluate tool authorization, deadlines, cancellation, idempotency, persistent audit state, and provider behavior.
#
# [Reference home](README.md) · [Setup and verification](README.md#run-and-verify) · [Course learner paths](../README.md#learner-paths) · [Main slide index](../README.md#main-deck-slide-index)
