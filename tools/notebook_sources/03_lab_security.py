# %% {"id": "03_guardrails_security_and_repair-00", "type": "markdown"}
# # Lab 3 — Manager Oversight: Code Validation and Bounded Repair
#
# [Course home](../README.md) · [Lab 2](02_lab_crewai.ipynb) · [Assignment 06](../ASSIGNMENTS.md#assignment-06-code-validation) · [Capstone](04_capstone.ipynb)
#
# ## What you interact with
#
# | Action | Your next step | Expected result |
# | --- | --- | --- |
# | **Run** | Run the starter input-gate and repair-loop cell, then the safe-input and oversight cells. | The weak gate accepts unsafe text; the oversized retry limit causes excessive mock attempts. |
# | **Edit** | Complete the `SecureToolInput` TODO and set `MAX_RETRIES = 3`. | Only numeric string IDs of 1–12 digits pass; the worker gets one initial attempt plus three retries. |
# | **Inspect** | Rerun the edited cell → safe control → oversight → grader. | Unsafe text never reaches the mock tool; the failing worker stops after four calls. |
# | **Finish** | Record `ESCALATE_TO_HUMAN` with its evidence and reach **15/15**. | Keep the notebook and decision note for Assignment 06, then open the Capstone. |
#
# You edit a Pydantic input gate and a bounded Python loop. `dry_run_database_lookup` appends to a Python list; it connects to no database and executes no SQL. `always_failing_mock` returns `False`. The dollar counter is an arithmetic teaching example with no API charge. No Crew, model, or human notification runs.
#
# **Predict:** which value should be rejected before the mock tool is called? How many calls should one initial attempt plus three retries produce?

# %% {"id": "03_guardrails_security_and_repair-01", "type": "markdown"}
# ## Observe both starter failures
#
# The weak model accepts the SQL-like string `123; DROP TABLE users; --`; the mock tool merely records it. The worker always fails, and `MAX_RETRIES = 100` permits 101 local attempts. These are deliberate starter defects.
#
# Run the next code cell once, then inspect the printed state before changing it. You will repair the validator and retry ceiling, not the tool, fixture, or grader.

# %% {"id": "lab3-exercise-flow", "type": "markdown", "diagram": "resources/diagrams/notebook-security-flow.svg"}
# ## Exercise flow
#
# ![Lab 3 exercise flow: validate the input before a mock lookup, run an initial mock attempt plus at most three retries, then inspect the stop-and-escalate evidence.](attachment:notebook-security-flow.svg)
#
# There are two local paths: the input gate either rejects the request or allows a mock lookup; the failing worker runs one initial attempt plus three retries, then records escalation. You edit the gate and retry limit in the next cell. After repair, rerun that cell → safe input → oversight → grader.

# %% {"id": "03_guardrails_security_and_repair-02", "type": "code"}
USE_LIVE_LLM = False

import re
import json
from pydantic import BaseModel, ConfigDict, ValidationError, field_validator


def inspect_state(step: str, data: dict):
    """DX: inspect synthetic or redacted state; never pass credentials or personal data."""
    print(f"\n🔍 INSPECTING: {step}")
    print(json.dumps(data, indent=2, default=str))
    print("─" * 40)


def safe_validate(schema, data):
    """DX: return a validated model or None; unexpected exceptions still propagate."""
    try:
        return schema.model_validate(data)
    except ValidationError as error:
        issue = error.errors(include_input=False, include_url=False)[0]
        field = ".".join(str(part) for part in issue["loc"]) or "<model>"
        # course validators use fixed policy messages; never include input values in them.
        reason = issue["msg"]
        print(f"🛑 GOVERNANCE BLOCK at {schema.__name__}: {reason} (Field: {field})")
        return None


malicious_tool_input = {"user_id": "123; DROP TABLE users; --"}
tool_call_log = []

def dry_run_database_lookup(user_id: str):
    """Action: record a local simulated user lookup after the input gate.
    Input: a validated numeric string user_id, 1 to 12 digits (for example, '123').
    Output: a dictionary with simulated status and user_id.
    Warning: caller must validate first; never pass SQL or raw unvalidated input.
    This teaching function connects to no database and enforces no gate itself.
    """
    tool_call_log.append(user_id)
    return {"status": "simulated", "user_id": user_id}

class SecureToolInput(BaseModel):
    # TODO: forbid extra fields and add a validator that allows a short numeric ID only.
    user_id: str

inspect_state("Input gate policy", {"contract": "numeric string, 1 to 12 digits", "sample": "SQL-like teaching input"})
unsafe_request = safe_validate(SecureToolInput, malicious_tool_input)
if unsafe_request is not None:
    unsafe_result = dry_run_database_lookup(unsafe_request.user_id)
    print("⚠️ VULNERABILITY: the weak schema accepted the injected value.")
else:
    print("✅ The gate rejected the unsafe input before any tool call.")

# Broken repair budget; set this to exactly 3 retries after the initial attempt.
MAX_RETRIES = 100
MOCK_COST_PER_CALL = 0.05

def always_failing_mock():
    return False

def run_repair_loop(max_retries: int):
    calls = 0
    simulated_cost = 0.0
    for attempt in range(max_retries + 1):
        calls += 1
        simulated_cost += MOCK_COST_PER_CALL
        if always_failing_mock():
            return {"calls": calls, "cost": simulated_cost, "escalated": False}
    return {"calls": calls, "cost": simulated_cost, "escalated": True}

repair_state = run_repair_loop(MAX_RETRIES)
inspect_state("Bounded repair result", repair_state)

# %% {"id": "03_guardrails_security_and_repair-03", "type": "markdown"}
# ## Repair and rerun
#
# In the preceding code cell:
#
# 1. Add `model_config = ConfigDict(extra="forbid")` to `SecureToolInput`.
# 2. Add `@field_validator("user_id")` and require a numeric string of **1–12 digits**. Reject all other values.
# 3. Set `MAX_RETRIES = 3`. The initial attempt plus three retries allows at most **four calls**, then escalation.
# 4. Rerun the edited cell first. It resets `tool_call_log` and `repair_state`. Then run the safe-input cell, oversight cell, and grader below.
#
# `safe_validate` returns `None` when validation fails; the caller must then skip the mock tool. The safe control `user_id="123"` must continue to pass. Inspect only synthetic or redacted inputs: `inspect_state` does not redact data.
#
# After the rerun, compare the observed count with your prediction. `ESCALATE_TO_HUMAN` means the controls stopped failed work; it does not mean the task succeeded or that a notification was sent.

# %% {"id": "03_guardrails_security_and_repair-04", "type": "code"}
# Safe control case. This remains a required check after the learner adds the validator.
safe_request = safe_validate(SecureToolInput, {"user_id": "123"})
if safe_request is not None:
    safe_result = dry_run_database_lookup(safe_request.user_id)
    inspect_state("Safe dry-run lookup", safe_result)
else:
    print("❌ Valid numeric ID was rejected; no tool call was made.")

# %% {"id": "lab3-management-oversight-instructions", "type": "markdown"}
# ## Inspect the supplied oversight check
#
# Run this cell after rerunning the repaired input/loop cell and the safe-input cell. Read every check before recording your decision.
#
# - `BLOCK_AND_REPAIR_CONTROLS`: at least one control still fails. Fix it and rerun the dependent cells.
# - `ESCALATE_TO_HUMAN`: the unsafe input is blocked and the always-failing worker stops after four calls. The displayed cost is **$0.20 simulated**, calculated as four × $0.05; actual API cost is **$0.00**.
#
# The oversight cell reads existing state. It makes no extra worker or tool calls and sends no message. A failed deliverable stays unapproved.

# %% {"id": "lab3-management-oversight", "type": "code"}
# MANAGEMENT OVERSIGHT — supplied; audit the always-failing scenario.
def management_oversight(state, call_log):
    try:
        SecureToolInput.model_validate(malicious_tool_input)
        hostile_rejected = False
    except ValidationError:
        hostile_rejected = True
    try:
        SecureToolInput.model_validate({"user_id": "123"})
        valid_accepted = True
    except ValidationError:
        valid_accepted = False

    checks = {
        "Unsafe input rejected": hostile_rejected,
        "Valid input still accepted": valid_accepted,
        "Unsafe value absent from tool calls": malicious_tool_input["user_id"] not in call_log,
        "Three retries configured": type(MAX_RETRIES) is int and MAX_RETRIES == 3,
        "Failing worker stopped after four calls": type(state.get("calls")) is int and state["calls"] == 4,
        "Simulated cost matches calls and budget": (
            type(state.get("cost")) in (int, float)
            and type(state.get("calls")) is int
            and 0 <= state["cost"] <= 4 * MOCK_COST_PER_CALL
            and round(state["cost"], 10) == round(state["calls"] * MOCK_COST_PER_CALL, 10)
        ),
        "Failure recorded escalation": state.get("escalated") is True,
    }
    return {"decision": "ESCALATE_TO_HUMAN" if all(checks.values())
            else "BLOCK_AND_REPAIR_CONTROLS", "checks": checks,
            "observed_calls": state.get("calls"), "simulated_cost": state.get("cost"),
            "release_approved": False}

manager_oversight = management_oversight(repair_state, tool_call_log)
manager_oversight_log = [manager_oversight]
inspect_state("Manager oversight", manager_oversight)
print("No extra worker/tool call or human notification was made by this action.")

# %% {"id": "lab3-manager-decision", "type": "markdown"}
# ### Record your oversight decision
#
# Complete this sentence after inspecting the evidence; no code changes are needed:
#
# **My decision:** BLOCK_AND_REPAIR_CONTROLS / ESCALATE_TO_HUMAN. **Evidence:** [unsafe-call result and attempt count]. **Next owner:** [learner repairing controls, or a human reviewer for the failed task].
#
# With corrected controls, expect no unsafe value in `tool_call_log`, four failed worker calls, and `ESCALATE_TO_HUMAN`. Retain the note and run the unchanged **/15** grader.
#
# **Reflection:** name one additional input that should fail validation. Explain why a mock lookup cannot establish the safety of a real database implementation.

# %% {"id": "03_guardrails_security_and_repair-05", "type": "markdown"}
# ## Auto-grader — Lab 3 (15 raw points)
#
# The grader awards points independently for hostile-input rejection, safe-input acceptance, a three-retry limit, bounded termination/escalation, and the mock budget counter. The gradebook scales `/15` to `/20`. At full credit, stop and move to the Capstone.
#
# After grading, return to your oversight note: cite one observed check, identify one untested edge case, and name who should own the next action.

# %% {"id": "03_guardrails_security_and_repair-06", "type": "code"}
# ==========================================
# AUTO-GRADER — LAB 3 (15 RAW POINTS)
# ==========================================
lab3_score = 0
lab3_results = []

try:
    SecureToolInput.model_validate(malicious_tool_input)
    hostile_blocked = False
except ValidationError:
    hostile_blocked = True

if hostile_blocked:
    lab3_score += 4
    lab3_results.append("✅ [4/4] SQL-like input rejected before the tool")
else:
    lab3_results.append("❌ [0/4] Validator accepted malicious input")

try:
    SecureToolInput.model_validate({"user_id": "123"})
    safe_accepted = True
except ValidationError:
    safe_accepted = False

if safe_accepted and hostile_blocked:
    lab3_score += 3
    lab3_results.append("✅ [3/3] Safe numeric ID accepted while unsafe input is blocked")
elif not safe_accepted:
    lab3_results.append("❌ [0/3] Safe numeric ID was rejected")
else:
    lab3_results.append("⏭️ [0/3] Safe-input credit unlocks after the hostile-input gate holds")

if MAX_RETRIES == 3:
    lab3_score += 3
    lab3_results.append("✅ [3/3] Retry limit is exactly three retries")
else:
    lab3_results.append("❌ [0/3] Set MAX_RETRIES to 3")

if repair_state["calls"] == 4 and repair_state["escalated"]:
    lab3_score += 3
    lab3_results.append("✅ [3/3] Four-call bound ends in escalation")
else:
    lab3_results.append("❌ [0/3] Rerun the loop with a three-retry limit")

if MAX_RETRIES == 3 and repair_state["calls"] == 4 and repair_state["cost"] <= 4 * MOCK_COST_PER_CALL:
    lab3_score += 2
    lab3_results.append("✅ [2/2] Simulated cost stops with the bounded loop")
else:
    lab3_results.append("❌ [0/2] Cost counter continued beyond the bounded loop")

print("\n".join(lab3_results))
print(f"LAB 3 SCORE: {lab3_score}/15")
if lab3_score == 15:
    print("✅ SUCCESS: 15/15 — stop here and move to the Capstone.")
else:
    print("⚠️ FAILED: fix the controls above, then rerun this grader.")

# %% {"id": "learner-navigation-03", "type": "markdown"}
# ## Continue or return
#
# After completing this notebook and inspecting its evidence, continue to [Capstone](04_capstone.ipynb).
#
# [Learner paths](../README.md#learner-paths) · [Slide index](../README.md#main-deck-slide-index) · [Practical sequence](../README.md#required-practical-sequence)
