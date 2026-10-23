# Building a Managed Agent Team

[Course home](../README.md) · [Slide index](../README.md#main-deck-slide-index) · [Required exercises](index.md)

This guide supports the main deck's new design discussions. Use it with the seven-notebook course route. The additional prompts are formative: they add no packages, live calls, TODOs, or assessment marks. The course still assesses three labs and the Development-to-Security Capstone.

## Start with one agent

Write the task, expected artifact, evidence of success, allowed actions, and stopping condition before choosing an architecture. Give one main agent responsibility for the user conversation and final result. First attempt the task using the supplied context and a small tool set. Add a helper only when a distinct skill, independent check, or access boundary justifies the extra coordination.

An agent that can act needs more than a good prompt: role permissions, validated inputs and outputs, a retry or spend bound, and observable state changes. Additional agents create additional handoffs to inspect. The main agent remains accountable for integrating the results.

**Preflight discussion, slides 1–3 and 8:** choose a procurement, HR, or software task. Describe what one agent could do and name the first reason you would split off a helper. Running preflight only verifies the local environment.

## Context engineering

Context engineering selects the information available at the next decision. It includes the task and acceptance criteria, current rules, permitted tools, relevant source evidence, a concise state or decision record, and the required output contract. A large transcript is not automatically a useful working brief.

| Context element | Course example | Learner check |
| --- | --- | --- |
| Task and success criteria | Lab 1's valid and malformed research outputs | State what must pass and what must fail. |
| Output contract | `StrictResearchOutput` and the Capstone's `DevDeliverable` | Validate fields, constraints, and rejected input. |
| Relevant rules and state | Lab 2's TeamLog and `architect_task` context | Identify which rule reaches the Coder and why. |
| Permitted actions | Manager, Coder, QA, and Security tool lists | Separate writing, checking, and approval. |
| Source evidence | Synthetic HR policy snippets | Keep source IDs and refuse an unsupported claim. |
| Stop condition | Lab 3's bounded repair | Inspect the observed trace and escalation. |

Retrieved text and helper output are evidence to examine, not authority to change the task or permissions. Preserve source labels and uncertainty when passing context. Lab 1 checks representation and declared constraints; Lab 2 declares context availability. Neither proves a real model obeyed the rules.

**Lab 1 discussion, slides 9–10:** write a short working brief containing the task, one approved rule, expected output, and one item you would leave out. After the grader, identify a claim it did not verify.

## One main agent and specialist helpers

The main agent owns the user conversation, delegates bounded work, reviews the returned evidence, and assembles the final answer. A helper receives a specific task, necessary context, scoped tools, a return contract, and a budget. A helper does not inherit every permission of the main agent.

| Possible helper | Bounded task | Link to the course |
| --- | --- | --- |
| General helper | Summarize an approved source or compare supplied options | Procurement quote comparison or HR snippet review. |
| Computer-use helper | Inspect or operate a UI when an authorized connector cannot do the job | Discuss a proposed HR interface workflow; no desktop automation runs in the required labs. |
| Video helper | Extract evidence with timestamps from an authorized recording | Use the supplied [video transcript](../resources/videos/tom_deep_dive_transcript.md) for a reading exercise; no video-processing agent is supplied. |
| Cloud coding agent | Implement and test a bounded change in an isolated workspace | Compare with Lab 2's Coder/QA separation and the Capstone's typed deliverable. Required execution remains local. |

The actual Lab 2 configuration uses Manager, Coder, and QA roles. The Capstone adds Security roles. The four helper types above are design examples, not four new implemented agents or assignments.

**Lab 2 discussion, slides 11–12:** choose one helper, define its input and return artifact, and name a tool it must not receive. Explain what the main agent must check before using the result.

## Choosing a capability and pairing with the human

Choose the least costly option that can meet the evidence and quality requirement. Compare latency, tokens, service charges, reliability, and human effort; the order below is a starting heuristic, not a measured universal price ranking.

| Option | When it is adequate | Escalation condition |
| --- | --- | --- |
| What the model already knows and supplied context | Stable facts or reasoning over sufficient supplied evidence | Need current, private, missing, or verifiable source data. |
| API or connector | An authorized, structured interface exposes the required data or action | Required operation is unavailable or evidence is incomplete. |
| Web search | Current public information or a traceable public source is required | Evidence is behind an authorized app interface or remains insufficient. |
| Full desktop / computer use | The task requires a UI and a suitable connector cannot complete it | Missing permission, unsupported interaction, or an ambiguous decision. |
| Ask the human | A preference, missing fact, permission, or judgment belongs to the user | Wait for the answer before dependent work. |

**Ask early when needed.** Do not exhaust tools before asking a question only the human can answer. Pair at meaningful decisions. A dedicated `ask_user(question, options)` tool provides one structured channel for clarification and approval. This is an illustrative interface, not a package or function supplied by the notebooks.

**Capstone discussion, slides 13 and 18:** choose a capability for the request, state why it is adequate, and name the condition that would change the choice. The existing Fast/Expert routing fixture compares illustrative model costs. It does not benchmark connectors, search, desktop use, or human time.

## Stable tools and loading on demand

Keep tool names, descriptions, schemas, and ordering stable across turns of the workflow. Do not add or remove tools to represent temporary availability. Check authorization and current availability at execution time, and return an explicit result when a tool cannot run.

Load only the capabilities needed for the current task. With a deferred-tool platform, declare the catalog up front and discover selected definitions on demand; preserve the loading history. With a fixed tool interface, initialize the relevant backend only when called. These patterns separate a stable interface from the timing of loading. They do not grant new permissions.

**course size budget:** keep each tool's description plus serialized parameter schema below **4,000 characters**. This is a local design convention, not a universal API limit. Keep required fields, constraints, side effects, and error guidance precise; simplify the operation or split unrelated responsibilities if the budget is exceeded.

A useful tool contract states what the tool does, what it can change, valid arguments, the result shape, and the next action after an expected failure. Validate the inputs again in the application; a clear schema alone is not execution authorization.

## State changes and actionable errors

Use a dedicated state tool such as `save_state(task_id, expected_version, patch, reason)` for workflow state. Avoid hiding state writes in shell commands. Return the new version and a change receipt so a reviewer can see what changed, who requested it, and why. If an operation incurs a charge, record the cost and units separately. Validate the patch and reject stale versions rather than silently overwriting newer state. These names are proposed tool interfaces, not notebook functions.

A recoverable error should include a stable code, a plain-language reason, whether any state changed, and a supported next action. For example:

```json
{
  "ok": false,
  "code": "HELPER_ASLEEP",
  "message": "The agent is asleep; no task is running.",
  "state_changed": false,
  "next_action": "Use read_state to inspect its checkpoint, then resume_helper to continue."
}
```

If a runtime exposes `read` or `shell` for an idle helper's workspace, say what those tools can actually do: “Use read to inspect the saved file, or shell to run the authorized diagnostic.” A shell call does not automatically wake a helper or authorize a state write. Name only tools available to that runtime. For a tool that is unavailable now, return `TOOL_UNAVAILABLE` with the reason and a supported recovery step; do not make it disappear or report success.

**Lab 3 discussion, slides 14–16:** rewrite a vague failure as a useful error. Specify a state-change receipt for escalation. Compare the proposed interface with the notebook's in-memory oversight record: the notebook does not implement durable state storage, helper lifecycle controls, or billing.

## Takeaways and evidence

1. Start with one accountable main agent; justify each helper.
2. Give each decision a relevant working brief and typed return contract.
3. Select an adequate capability with a clear cost and evidence rationale; ask the human at decision points.
4. Keep tool interfaces stable, load only what is needed, and return useful errors.
5. Make state changes reviewable, bound repair, and check evidence before delivery.

At the end, point to the Lab 1 rejection evidence, Lab 2 audit and decision note, Lab 3 trace and escalation, and Capstone handoff and ADR. Name what remains a proposed design and what the supplied fixtures actually demonstrate. The [submission checklist](../PLAYBOOK.md#submission-checklist) and 100-mark rubric remain the assessment authority.

## Source notes

The architecture and cost ladder are course design guidance. The helper categories, dedicated user/state interfaces, actionable-error examples, and 4,000-character budget follow the requested course design; they are not claims about built-in notebook capabilities.

Official documentation checked on **18 October 2026**:

- [Orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration) distinguishes a manager retaining the final reply from a specialist taking over the conversation.
- [Tool search](https://developers.openai.com/api/docs/guides/tools-tool-search) describes deferred definitions and loading history; support depends on the platform and model.
- [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) describes stable tool definitions and ordering, callable-tool restrictions, and append-only loading.
- [Function calling](https://developers.openai.com/api/docs/guides/function-calling) explains names, descriptions, parameter schemas, and application-side handling of tool calls.

[Return to learner paths](../README.md#learner-paths) · [Return to slide index](../README.md#main-deck-slide-index)
