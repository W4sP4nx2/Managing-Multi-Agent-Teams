# %% {"id": "6d5e52e3", "type": "markdown"}
# # Lab 2 — Multi-Agent Management: Code Auditing and Team Oversight
#
# [Course home](../README.md) · [Lab 1](01_lab_pydantic.ipynb) · [Assignment 04](../ASSIGNMENTS.md#assignment-04-code-auditing) · [Lab 3](03_lab_security.ipynb)
#
# **Navigate:** [Team map](#lab2-team-map) → [Two repairs](#lab2-repairs) → [Skill transparency](#lab2-skill-transparency) → [Local fixture](#lab2-fixture) → [Audit](#lab2-audit) → [Decision](#lab2-decision) → [Grader](#lab2-grader) → [Debug trace](#lab2-debug) → [Collaboration patterns](#lab2-collaboration-patterns).
#
# ## What you interact with
#
# | Action | Your next step | Expected result |
# | --- | --- | --- |
# | **Run** | Run agent configuration → tool matrix → task configuration → Coder fixture → audit. | The starter Manager has excess tools, the Coder lacks context, and the audit returns `BLOCK`. |
# | **Edit** | Repair **TODO 1** in `manager_agent.tools` and **TODO 2** in `coder_task.context`. | The Manager has only the review tool; the Coder receives `[architect_task]`. |
# | **Inspect** | Rerun that full sequence, then read every audit check and `qa_inbox`. | The tool matrix matches all role allowlists; the audit returns `PASS_TO_QA` with one typed proposal. |
# | **Finish** | Record the decision, run the unchanged grader for **15/15**, and inspect the debug trace. | Keep the notebook and decision note for Assignment 04, then open Lab 3. |
#
# You construct real CrewAI `Agent`, `Task`, and `Crew` objects, then inspect them using supplied local fixtures and Python checks. This notebook never calls `crew.kickoff()`: no model runs, no tool is executed by an agent, and the QA task does not run. `PASS_TO_QA` only places a validated proposal in a Python list for this exercise.

# %% {"id": "lab2-team-map", "type": "markdown", "diagram": "resources/diagrams/lab2-team-audit.svg"}
# <a id="lab2-team-map"></a>
# ## Team map and the path you will run
#
# ![Lab 2 role boundaries and local audit flow: inspect declared tools and task context, repair two settings, and gate the local Coder payload into qa_inbox.](attachment:lab2-team-audit.svg)
#
# **Read the diagram:** you supervise the Manager–Coder–QA configuration. The Coder alone has the writing tool; the Manager has the review tool; QA has the sample-testing tool. `architect_task` carries rules from `team_log`; it is a prior task, not another agent. Dashed arrows describe configured relationships. Solid arrows describe the local exercise: synthetic payload → configuration and `CodePatch` audit → `qa_inbox`.
#
# **Next actions:** run agent configuration → tool matrix → task configuration → fixture → audit. Inspect the block, edit the two TODOs, and rerun that same sequence. `BLOCK` keeps the inbox empty; `PASS_TO_QA` admits one typed proposal. Neither outcome executes QA, Git, or a deployment.
#
# [Go to the two repairs](#lab2-repairs) · [Assignment evidence](../ASSIGNMENTS.md#assignment-04-code-auditing-submit)

# %% {"id": "a5fc9282", "type": "markdown"}
# <a id="lab2-repairs"></a>
# ## Make the two configuration repairs
#
# The Manager coordinates and reviews. The Coder proposes code. QA is configured to verify it separately. The approved rule lives in `team_log`, and `architect_task` carries it as prior-task context.
#
# 1. **TODO 1 — agent configuration:** change the Manager to `tools=[approve_code_tool]` and retain delegation. Leave the Coder and QA tool lists unchanged.
# 2. **TODO 2 — task configuration:** change `coder_task.context` to `[architect_task]`.
#
# First run the starter cells to observe the failure. After editing, rerun agent configuration → tool matrix → task configuration → fixture → audit. Then record your decision and run the grader.
#
# CrewAI `Task.context` contains prior `Task` objects. Here, the local fixture checks whether the dependency is present and selects a valid or invalid sample payload. This shows context wiring; it cannot prove that a model understood or followed the rules.

# %% {"id": "read-write-roles", "type": "markdown"}
# ### Inspect the role boundaries
#
# | Role | Declared custom tool | What it represents in this notebook |
# | --- | --- | --- |
# | Engineering Manager | `approve_code_tool` | A review acknowledgement placeholder. |
# | Senior Coder | `write_code_tool` | A draft acknowledgement placeholder; it writes no files. |
# | QA Auditor | `run_tests_tool` | Sample evidence; it runs no test commands. |
#
# Treat the Coder payload as an untrusted proposal. Pydantic checks its declared structure, while the audit checks role tool lists and task dependencies. The tools are supplied local teaching placeholders. The next matrix inspects their actual metadata without calling them.

# %% {"id": "88df3214", "type": "code"}
USE_LIVE_LLM = False

import json
from pydantic import BaseModel, ConfigDict, Field, ValidationError
import os
import tempfile
from pathlib import Path
os.environ.setdefault("CREWAI_STORAGE_DIR", str(Path(tempfile.gettempdir()) / "crewai_training_lab2"))
from crewai import Agent, Crew, Process, Task
from crewai.tools import tool


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


class StrictContract(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ArchitectBrief(StrictContract):
    rules: list[str] = Field(min_length=1)


class CodePatch(StrictContract):
    user_id: str = Field(strict=True)
    operation: str


class QAReport(StrictContract):
    passed: bool
    evidence: str = Field(min_length=1)


@tool("write_code_tool")
def write_code_tool(spec: str) -> str:
    """Action: draft a local implementation placeholder for the Coder.
    Input: an approved implementation specification as a string.
    Output: a draft acknowledgement string.
    Warning: writes no files; does not test or approve code. Pass no secrets.
    """
    return f"Draft prepared for: {spec}"


@tool("approve_code_tool")
def approve_code_tool(summary: str) -> str:
    """Action: record the Manager's local review placeholder.
    Input: a summary of the proposal and independent review evidence.
    Output: a review acknowledgement string.
    Warning: approves no real code or release; never use it as test evidence.
    """
    return f"Review recorded for: {summary}"


@tool("run_tests_tool")
def run_tests_tool(target: str) -> str:
    """Action: return sample verification evidence for the QA Auditor.
    Input: a named local verification target as a string.
    Output: a sample QA evidence string.
    Warning: runs no commands or real tests; cannot write or approve code.
    """
    return f"Sample QA evidence for {target}; inspect locally before release."


# The shared blackboard contains the Architect's policy.
team_log = {
    "architect_rules": ["user_id must be a string", "Use no network or file access."],
}

# START BROKEN: the Manager can write code, violating separation of duties.
manager_agent = Agent(
    role="Engineering Manager",
    goal="Delegate work and approve or escalate the result.",
    backstory="You govern the delivery process; the Coder owns implementation.",
    tools=[write_code_tool, approve_code_tool],  # TODO 1: remove write_code_tool; repaired target: tools=[approve_code_tool]
    allow_delegation=True,
)

coder_agent = Agent(
    role="Senior Coder",
    goal="Implement the request within the Architect's rules.",
    backstory="You write code and do not approve or test your own work.",
    tools=[write_code_tool],
    allow_delegation=False,
)

qa_agent = Agent(
    role="QA Auditor",
    goal="Run the requested checks and report evidence.",
    backstory="You test the Coder's work and do not modify or approve it.",
    tools=[run_tests_tool],
    allow_delegation=False,
)

# %% {"id": "lab2-skill-transparency-guide", "type": "markdown"}
# <a id="lab2-skill-transparency"></a>
# ## Skill Transparency & Least Privilege
#
# Before assigning tasks, inspect the **custom tools actually declared on each agent**. Here, a skill means an exposed tool capability and its description; it is not model training or fine-tuning. Each tool's docstring declares **Action, Input, Output, and Warning** so a delivery manager can see its purpose, data boundary, result, and limits.
#
# | Role | Expected custom-tool allowlist | Responsibility |
# | --- | --- | --- |
# | Engineering Manager | `approve_code_tool` | Coordinate and record review; delegate implementation. |
# | Senior Coder | `write_code_tool` | Draft a proposal; do not approve or verify your own change. |
# | QA Auditor | `run_tests_tool` | Read / Verify the proposal and return sample evidence; do not write or approve. |
#
# Run the supplied **Skill Transparency Matrix** below. It reads each current `Agent.tools` list and prints the actual tool descriptions, including every Warning. The starter Manager has an extra writing capability, so its least-privilege result must be **False**. After TODO 1, rerun the agent definitions and this matrix: the Manager should have only its review tool and show **True**. Coder and QA should retain separate Write and Read / Verify capabilities. The display does not change tools or repair either TODO.
#
# **Interpret the evidence:** True means the declared custom-tool names match this exercise's allowlist exactly. It does not establish OS isolation, reveal every framework-added runtime capability, execute a tool, prove a model followed a rule, or authorize a release. Read the descriptions: these tools are local placeholders, and the QA tool runs no actual tests. Task context and typed handoffs are inspected separately by the supplied audit gate.
#
# Continue with **task configuration**, then the local fixture and audit. After either repair, rerun the agent definitions, matrix, task configuration, fixture, and audit in order. No Crew kickoff or external service is needed.

# %% {"id": "lab2-skill-transparency", "type": "code"}
def build_skill_transparency(role_agents, expected_tools):
    """Inspect declared custom-tool metadata without calling or changing tools."""
    rows = []
    for role, agent in role_agents.items():
        declared = list(getattr(agent, "tools", None) or [])
        actual_names = [getattr(item, "name", "<unnamed>") for item in declared]
        allowed_names = list(expected_tools[role])
        rows.append({
            "role": role,
            "allowed_tools": allowed_names,
            "actual_tools": actual_names,
            "least_privilege": (
                len(actual_names) == len(set(actual_names))
                and set(actual_names) == set(allowed_names)
            ),
            "skill_details": [
                {"name": getattr(item, "name", "<unnamed>"),
                 "description": getattr(item, "description", "") or "No description supplied."}
                for item in declared
            ],
        })
    return rows


skill_transparency_matrix = build_skill_transparency(
    {"Engineering Manager": manager_agent, "Senior Coder": coder_agent, "QA Auditor": qa_agent},
    {"Engineering Manager": ["approve_code_tool"],
     "Senior Coder": ["write_code_tool"],
     "QA Auditor": ["run_tests_tool"]},
)

print("SKILL TRANSPARENCY MATRIX — declared custom tools")
print(f"{'Role':<22} | {'Actual tools':<36} | {'Allowed tools':<22} | Least privilege")
print("-" * 108)
for row in skill_transparency_matrix:
    actual = ", ".join(row["actual_tools"]) or "(none)"
    allowed = ", ".join(row["allowed_tools"]) or "(none)"
    print(f"{row['role']:<22} | {actual:<36} | {allowed:<22} | {row['least_privilege']}")

for row in skill_transparency_matrix:
    for skill in row["skill_details"]:
        print(f"\n{row['role']} → {skill['name']}\n{skill['description']}")
print("\nMetadata inspection only: no tools executed, no permissions changed, no model call.")

# %% {"id": "lab2-task-configuration", "type": "code"}
# This prior task publishes the TeamLog rules as typed context for downstream work.
architect_task = Task(
    description=f"Publish the approved implementation rules: {team_log['architect_rules']}",
    expected_output="An ArchitectBrief containing the approved rules.",
    output_pydantic=ArchitectBrief,
)

# START BROKEN: without this dependency, the Coder has no TeamLog context.
coder_task = Task(
    description="Create a user record. Follow the Architect's rules in your task context.",
    expected_output="A CodePatch with the user_id and operation.",
    agent=coder_agent,
    context=[],  # TODO 2: use [architect_task]
    output_pydantic=CodePatch,
)

qa_task = Task(
    description="Test the Coder's patch and report evidence.",
    expected_output="A structured QAReport.",
    agent=qa_agent,
    context=[coder_task],
    output_pydantic=QAReport,
)

# CrewAI's hierarchy manager coordinates the two worker agents.
# The Architect task runs first; coder_task explicitly depends on its output.
crew = Crew(
    agents=[coder_agent, qa_agent],
    tasks=[architect_task, coder_task, qa_task],
    process=Process.hierarchical,
    manager_agent=manager_agent,
    verbose=False,
)

inspect_state("Team configuration", {
    "process": crew.process,
    "architect_rules": team_log["architect_rules"],
    "manager_tools": [item.name for item in manager_agent.tools],
    "coder_has_architect_context": architect_task in (coder_task.context or []),
    "coder_output_contract": coder_task.output_pydantic.__name__,
})
print("Configuration constructed; no Crew kickoff or model call was made.")

# %% {"id": "60e17e84", "type": "markdown"}
# <a id="lab2-fixture"></a>
# ## Observe the broken contract
#
# This local fixture stands in for one deterministic Coder response. If the task has the Architect’s context, the mock follows the rule. If the context is missing, the mock returns an integer `user_id`. `CodePatch` requires a strict string, so Pydantic rejects the broken starter with a `ValidationError`.
#
# `inspect_state` exposes the synthetic proposal; `safe_validate` displays a compact governance block and returns `None` for the expected contract rejection. Callers must check that result before using it. The helper shows a field path and policy message, omitting raw rejected input. Keep validator messages free of secrets. Only inspect synthetic or explicitly redacted state: the inspector does not redact data for you.
#
# After you wire the context, rerun it to see the valid typed object. The failure is local and repeatable; it does not call CrewAI or an API. Internal audit/grader checks still enforce their own boundaries; these display helpers grant no permissions.

# %% {"id": "38b0ca66", "type": "code"}
has_architect_context = architect_task in (coder_task.context or [])
mock_coder_output = {
    "user_id": "101" if has_architect_context else 101,
    "operation": "create",
}
inspect_state("Coder Output", mock_coder_output)
validated_patch = safe_validate(CodePatch, mock_coder_output)
if validated_patch is None:
    if has_architect_context:
        raise RuntimeError("The contextualized Coder fixture unexpectedly violated CodePatch.")
    print("Expected rejection: repair the missing Architect context before the QA handoff.")
else:
    inspect_state("Validated CodePatch", validated_patch.model_dump())

# %% {"id": "lab2-manager-audit-instructions", "type": "markdown"}
# <a id="lab2-audit"></a>
# ## Manager's Audit Action: control the QA handoff
#
# Run the supplied gate after agent configuration, the skill matrix, task configuration, and the Coder fixture. As delivery manager, inspect **every check**, then record whether the patch may enter the local QA inbox and cite one piece of evidence.
#
# - **BLOCK:** keep the inbox empty; repair the failed control and rerun the dependent cells.
# - **PASS_TO_QA:** the configuration and local payload meet this exercise's checks. QA may review the typed proposal. This is not test success or release approval.
#
# This action is formative and adds no points. The helper revalidates the current `mock_coder_output`; it does not trust a previously saved `validated_patch`.
#
# **Discuss after inspection:** what exactly does `PASS_TO_QA` authorize in this notebook, and what does it not authorize? Use one observed check to support your answer.

# %% {"id": "lab2-manager-audit-gate", "type": "code"}
# MANAGER'S AUDIT GATE — supplied; inspect its evidence, no new TODO.
def manager_audit_gate(manager, coder, qa, brief_task, implementation_task,
                       review_task, candidate):
    def tools_of(agent):
        return {item.name for item in (getattr(agent, "tools", None) or [])}

    checks = {
        "Manager reviews and delegates only": (
            tools_of(manager) == {"approve_code_tool"}
            and bool(getattr(manager, "allow_delegation", False))
        ),
        "Coder has writing only": tools_of(coder) == {"write_code_tool"},
        "QA has testing only": tools_of(qa) == {"run_tests_tool"},
        "Task owners match their roles": (
            getattr(implementation_task, "agent", None) is coder
            and getattr(review_task, "agent", None) is qa
        ),
        "Coder receives Architect context": any(
            task is brief_task for task in (implementation_task.context or [])
        ),
        "Typed Coder-to-QA dependency": (
            implementation_task.output_pydantic is CodePatch
            and review_task.output_pydantic is QAReport
            and any(task is implementation_task for task in (review_task.context or []))
        ),
    }
    try:
        raw_candidate = candidate.model_dump() if isinstance(candidate, BaseModel) else candidate
        patch = CodePatch.model_validate(raw_candidate)
    except ValidationError as exc:
        patch = None
        checks["Current Coder payload validates"] = False
        payload_evidence = exc.errors(include_input=False, include_url=False)[0]["type"]
    else:
        checks["Current Coder payload validates"] = True
        payload_evidence = patch.model_dump()

    allowed = all(checks.values())
    audit = {"decision": "PASS_TO_QA" if allowed else "BLOCK",
             "checks": checks, "payload_evidence": payload_evidence}
    return audit, patch if allowed else None

manager_audit, patch_for_qa = manager_audit_gate(
    manager_agent, coder_agent, qa_agent, architect_task, coder_task,
    qa_task, mock_coder_output,
)
# Reset on every run: a previous accepted patch cannot remain in this inbox.
qa_inbox = [] if patch_for_qa is None else [patch_for_qa]
management_log = [{"actor": "Learner as delivery manager", **manager_audit,
                   "qa_inbox_count": len(qa_inbox)}]
inspect_state("Manager audit and QA handoff", {
    **manager_audit,
    "qa_inbox": [patch.model_dump() for patch in qa_inbox],
})
print("Configuration/fixture audit only; no QA task, test command, or release ran.")

# %% {"id": "lab2-manager-audit-decision", "type": "markdown"}
# <a id="lab2-decision"></a>
# ### Record your management decision
#
# Complete this sentence after inspecting the audit (no code changes):
#
# **My decision:** BLOCK / PASS_TO_QA. **Evidence:** [name a check and its observed value]. **Next owner:** [Coder for repair, or QA for review].
#
# Keep this note with the notebook. After the two code repairs, the expected action is `PASS_TO_QA` with one typed proposal in `qa_inbox`; the /15 grader remains unchanged.
#
# **Reflection:** name one condition that would change your decision, and one QA action still needed after a pass. A spoken answer, written sentence, or annotated role map is fine for this formative reflection.

# %% {"id": "c45bcbc4", "type": "markdown"}
# <a id="lab2-grader"></a>
# ## Auto-grader — Lab 2 (15 raw points)
#
# Run this cell after editing and rerunning agent configuration → skill matrix → task configuration → fixture → audit. The grader checks the two governance repairs and reports the missing control. It is safe to run on the broken starter.
#
# - **0/15:** Both controls are still broken.
# - **5/15:** Manager SoD is fixed; the Coder still lacks `architect_task` context.
# - **10/15:** Architect context is fixed; the Manager still has an overbroad tool scope.
# - **15/15:** Both controls are correct. The course gradebook scales this raw score to 20 marks.
#
# After the grader reports a score, return to the decision note and explain one limit of that score. A passing configuration check is not test success or release approval.

# %% {"id": "84aaa3ad", "type": "code"}
# AUTO-GRADER — LAB 2 (15 RAW POINTS)
manager = globals().get("manager_agent")
coder_task_for_grade = globals().get("coder_task")
architect_task_for_grade = globals().get("architect_task")
manager_tool_names = {getattr(item, "name", "")
                      for item in (getattr(manager, "tools", None) or [])}
manager_sod_ok = (
    manager is not None
    and manager_tool_names == {"approve_code_tool"}
    and bool(getattr(manager, "allow_delegation", False))
)
context_tasks = getattr(coder_task_for_grade, "context", None) or []
teamlog_context_ok = (
    coder_task_for_grade is not None
    and architect_task_for_grade is not None
    and any(task is architect_task_for_grade for task in context_tasks)
)
lab2_score = (5 if manager_sod_ok else 0) + (10 if teamlog_context_ok else 0)
print(f"{'✅' if manager_sod_ok else '❌'} [{5 if manager_sod_ok else 0}/5] Manager approval/delegation only")
print(f"{'✅' if teamlog_context_ok else '❌'} [{10 if teamlog_context_ok else 0}/10] Architect context reaches Coder")
if not manager_sod_ok:
    print("Set Manager tools=[approve_code_tool] and keep allow_delegation=True.")
if not teamlog_context_ok:
    print("Set coder_task.context=[architect_task].")
print(f"LAB 2 SCORE: {lab2_score}/15")
if lab2_score == 15:
    print("✅ SUCCESS: 15/15 — complete the Blind Agent Debug below, then move to Lab 3.")

# %% {"id": "lab2-blind-agent-debug-instructions", "type": "markdown"}
# <a id="lab2-debug"></a>
# ## DX Exercise: The "Blind Agent" Debug · 5 minutes (ungraded)
#
# The historical fixture below records a Coder that missed the Architect’s rule. Compare the received context and generated output with the strict `CodePatch` contract above.
#
# 1. Read the Inspector log and identify the field, its observed type, and the required type.
# 2. Trace the missing rule to the **earlier task configuration cell**: `coder_task.context` must contain `[architect_task]`. Confirm `team_log` supplies the rule. Do not weaken `CodePatch` or fix only the generated value.
# 3. If that configuration is still broken, repair it; if already fixed for the grader, explain how your existing repair addresses this trace. Rerun agent configuration → skill matrix → task configuration → Coder fixture → audit → grader. Expect a string `"101"`; QA receives it only when the Manager's permissions also pass.
#
# This historical log deliberately stays broken after your repair. Compare it with the current `Coder Output` and audit above. Context makes the rule available; only validation and independent review provide evidence about the output. No extra code or marks are required.

# %% {"id": "lab2-blind-agent-debug", "type": "code"}
failing_agent_trace = {
    "agent_role": "Senior Coder",
    "context_received": [],
    "generated_output": {"user_id": 101, "operation": "create"},
}
inspect_state("Failing Coder Trace (historical fixture)", failing_agent_trace)
blocked_debug_patch = safe_validate(CodePatch, failing_agent_trace["generated_output"])
if blocked_debug_patch is not None:
    raise AssertionError("The strict user_id contract must reject this historical fixture.")
print("BLOCK: historical output stays outside the QA inbox; inspect the context repair above.")

# %% {"id": "lab2-live-factory-mapping", "type": "markdown"}
# <a id="lab2-live-mapping"></a>
# ## Connect this evidence to the later factory lab
#
# You have checked declared tools, task context, and one local payload. The later [Software Factory notebook](05_live_software_factory.ipynb) adds actual local Git changes, checks, and a publication approval flow using supplied artifacts.
#
# For your decision note, name one action still needed after `PASS_TO_QA`. Independent QA is a suitable answer: this notebook configured that role but did not execute its task.
#
# [Back to team map](#lab2-team-map) · [Assignment evidence](../ASSIGNMENTS.md#assignment-04-code-auditing-submit)

# %% {"id": "lab2-collaboration-patterns", "type": "markdown", "diagram": "resources/diagrams/notebook-collaboration-patterns.svg"}
# <a id="lab2-collaboration-patterns"></a>
# ## Compare collaboration patterns · 5 minutes (ungraded)
#
# Three different questions describe a team. **Role based collaboration** assigns responsibilities and tools, such as Coder proposes and QA verifies. **Rule based collaboration** defines conditions for a handoff, such as “all required checks pass and the packet is valid.” **Architecture** determines who receives evidence and makes that decision. A multi-agent team can combine roles, rules, and any suitable routing architecture; a role description alone does not enforce its rules.
#
# ![Four local routing models: independent private reports, decentralized peer exchange, a centralized coordinator, and hybrid local gates with a central policy gate.](attachment:notebook-collaboration-patterns.svg)
#
# | Architecture | Where evidence goes | Who decides in this exercise? |
# | --- | --- | --- |
# | Independent | Each worker keeps its own report. | Each reports readiness; there is no shared handoff decision or coordination. |
# | Decentralized | Every peer receives the other peers' reports. | Each applies the same rule; all must agree before handoff. No central manager decides. |
# | Centralized | Specialists report to one coordinator. | The coordinator applies the rule to all reports and the packet. |
# | Hybrid | Each specialist gates its own work, then reports to the coordinator. | Local specialists can veto; central policy also requires a valid packet. |
#
# The cell below is a small **Python routing model**, separate from the configured CrewAI objects above. Boolean values stand in for completed specialist checks; dictionaries stand in for messages. Nothing runs concurrently, calls an LLM or reasoning model, invokes tools, or approves a real release. The peer example assumes all three reports are available; it is not a distributed consensus protocol.
#
# **Run:** inspect the missing Security readiness and the four decisions. **Edit:** set `pattern_checks["Security"]` to `True` in the input dictionary, then rerun: the three coordinated models allow the next review, while independent workers still have no shared decision. Next set `pattern_packet_valid = False`: every coordinated model must block again. **Inspect:** compare `deciders`, `local_ready`, and `peer_inboxes` to explain where the same rule runs. **Finish:** restore Security to `False` and the packet to `True`; rerun. The fixed proof cases at the end must pass in every variation. This adds no marks or submission.

# %% {"id": "lab2-collaboration-comparison", "type": "code"}
# Local routing comparison only: these are records, not executing agents.
def compare_collaboration(checks, packet_valid=True):
    roles = ("Coder", "QA", "Security")
    if set(checks) != set(roles) or any(type(value) is not bool for value in checks.values()):
        raise ValueError("Supply one Boolean readiness report for each required role.")
    if type(packet_valid) is not bool:
        raise ValueError("Packet validity must be a Boolean.")

    local_ready = {role: checks[role] for role in roles}
    peer_inboxes = {
        role: {peer: checks[peer] for peer in roles if peer != role}
        for role in roles
    }
    peer_votes = {
        role: packet_valid and local_ready[role] and all(peer_inboxes[role].values())
        for role in roles
    }
    coordinator_allows = packet_valid and all(checks.values())
    local_gates_allow = all(local_ready.values())
    hybrid_allows = packet_valid and local_gates_allow

    return {
        "independent": {
            "decision": "NO_SHARED_DECISION", "deciders": list(roles),
            "local_ready": local_ready,
        },
        "decentralized": {
            "decision": "HANDOFF" if all(peer_votes.values()) else "BLOCK",
            "deciders": list(roles), "peer_inboxes": peer_inboxes,
            "peer_votes": peer_votes,
        },
        "centralized": {
            "decision": "HANDOFF" if coordinator_allows else "BLOCK",
            "deciders": ["Coordinator"], "received_reports": dict(checks),
        },
        "hybrid": {
            "decision": "HANDOFF" if hybrid_allows else "BLOCK",
            "deciders": [*roles, "Coordinator"], "local_ready": local_ready,
            "central_packet_valid": packet_valid,
        },
    }


# EDIT these two inputs, inspect the records, then restore this starter case.
pattern_checks = {"Coder": True, "QA": True, "Security": False}
pattern_packet_valid = True
pattern_results = compare_collaboration(pattern_checks, pattern_packet_valid)
for name, evidence in pattern_results.items():
    print(f"\n{name.upper()}: {evidence['decision']}")
    print(json.dumps(evidence, indent=2))

# Fixed proof cases stay unchanged when you experiment with the inputs above.
for proof_checks, proof_packet, expected in (
    ({"Coder": True, "QA": True, "Security": False}, True, "BLOCK"),
    ({"Coder": True, "QA": True, "Security": True}, True, "HANDOFF"),
    ({"Coder": True, "QA": True, "Security": True}, False, "BLOCK"),
):
    proof = compare_collaboration(proof_checks, proof_packet)
    assert proof["independent"]["decision"] == "NO_SHARED_DECISION"
    assert all(proof[name]["decision"] == expected
               for name in ("decentralized", "centralized", "hybrid"))
print("\nProofs passed: missing readiness and invalid packets block every coordinated route.")
print("HANDOFF means next review in this local model; it never means release approval.")

# %% {"id": "lab2-collaboration-reflection", "type": "markdown"}
# **Explain the result:** changing the topology did not change the acceptance rule. The decentralized example copies each report to two peers; the centralized example sends each report to one coordinator. This changes the evidence paths and decision owners, even when their decisions match. The hybrid example combines local vetoes with a central policy check. Choose one route for your capstone interaction map and name who blocks a failed handoff; this reflection adds no submission.
#
# **Framework bridge:** the CrewAI hierarchy configured earlier is a centralized coordination pattern. The separate [bridge notebook](../crewai_learning/01_Bridge_Sequential_Crew.ipynb) runs an actual sequential Crew using local fixture responses. Neither configuring a hierarchy nor running this dictionary exercise proves that an autonomous team followed its policy.

# %% {"id": "learner-navigation-02", "type": "markdown"}
# ## Continue or return
#
# After completing this notebook and inspecting its evidence, continue to [Lab 3](03_lab_security.ipynb).
#
# **Optional follow-up:** use the [CrewAI bridge notebook](../crewai_learning/01_Bridge_Sequential_Crew.ipynb) and [guided Assignment 09 exercise](../ASSIGNMENTS.md#assignment-09-guided-bridge-exercise) to trace this configuration pattern through actual CrewAI execution. The notebook imports [coding_team.py](../crewai_learning/coding_team.py) and demonstrates rejected output, three-attempt escalation, and early success with local fixture responses. This adds no marks or submission.
#
# [Learner paths](../README.md#learner-paths) · [Slide index](../README.md#main-deck-slide-index) · [Practical sequence](../README.md#required-practical-sequence)
