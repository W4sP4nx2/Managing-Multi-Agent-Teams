# Assignment 08: Debugging in the Agentic Age & SDLC Operations

**Maps to:** Lecture 8 — Debugging and AI-First SDLC · **Type:** Formative, pass/fail

## Objective

Use observable workflow evidence to find a failure point and explain which control should stop it.

## Task

1. In a local copy of the Capstone notebook, set both `dev_crew` and `security_crew` to `verbose=True` and identify the lines that enable execution logging. Keep `USE_LIVE_LLM = False`; do not call `Crew.kickoff()` for this assignment.
2. Analyze the deterministic scenario trace below. Identify a verification or permission failure, cite the line that proves it, and state one corrective action and the control that should block the failure.

```text
[Architect] TeamLog rule: user_id must be a string
[Coordinator] Coder task context: [] (architect_task missing)
[Coder] deterministic payload: {"user_id": 101, "operation": "create"}
[Pydantic] CodePatch rejected: user_id must be a strict string
[Coordinator] DevDeliverable validated; unit_tests_passed=True
[Security Manager] tools: approve_audit_tool, mock_pen_test_tool
[Pen Tester] tools: mock_pen_test_tool
[Pen Tester] finding: SQL injection marker detected
[Security Manager] decision: approved
[Local policy check] rejected: manager must not have mock_pen_test_tool
```

This is a **teaching fixture**, not a live CrewAI transcript. Verbose logs can show task execution and tool activity; they do not reveal an agent’s private chain-of-thought. The required classroom path makes no provider call.

## Submit

- The `verbose=True` configuration excerpt.
- A short note naming the risk, citing trace evidence, and explaining the permission or typed-result check that should block it.

## Pass/fail

- **Pass:** The learner identifies a concrete risk in the trace (excess scanner permission or approval contradicting the finding), cites evidence, and names a relevant verification or tool-permission control.
- **Revise:** The explanation is unsupported by the trace or claims that verbose mode exposes private reasoning.

## Lecture 8 reference discussion: choosing an orchestration pattern

For an executable, ungraded follow-up to Lab 2, open the [Manager–Coder–QA advanced reference](../crewai_learning/01_Bridge_Sequential_Crew.ipynb). It runs real CrewAI tasks with local fixture LLMs and external networking blocked. Observe strict-output rejection and exactly three tool failures followed by a typed escalation. Its Python wrapper owns recovery; the required classroom notebooks retain their existing no-kickoff boundary. Use [Assignment 09](assignment_09_framework_comparison.md) to discuss the framework/application split. This adds no submission or marks.

**Ungraded slide/reference discussion.** This section adds no submission or pass/fail criterion. Read the [framework comparison](../resources/framework_comparison.md#lecture-8-discussion-why-this-course-uses-crewai) alongside the presentation:

- **CrewAI:** The course uses visible Manager/Coder/QA roles, task context, and exposed tool lists to make separation of duties easy to inspect. The required demonstration uses deterministic fixtures rather than live team execution.
- **LangGraph:** Consider a future Capstone refactor when explicit state transitions, persistence, or recovery decisions become more complex. The [optional architecture design](../resources/framework_comparison.md#optional-capstone-architecture-extension-langgraph) illustrates this possibility; no refactor is assigned.
- **AutoGen:** Compare conversational coordination as a conversation-pattern reference. The official project now directs new users to Microsoft Agent Framework; current support matters in a production choice.
- **Microsoft Agent Framework:** Compare Python/.NET agent and explicit workflow coordination with the Capstone's team boundary. This remains reference reading, with no new package or coding requirement.
- **LlamaIndex:** Compare retrieval tools and document-oriented workflows using the HR/RAG simulation as context. It adds no retrieval implementation to this assignment.

Discussion focus: explain which orchestration need would change your framework choice, and which validation or authorization checks you would retain. The existing trace-analysis submission and assessment above remain the same.
