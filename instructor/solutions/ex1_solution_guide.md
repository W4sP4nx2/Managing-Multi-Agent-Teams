# Ex1 Solution Guide: Agent Roster & SOPs

## Expected Architecture

- Product Manager parses the GitHub issue into `TaskSpec`.
- Tech Lead or Manager decomposes the task into implementation steps.
- Coder produces `CodePatch`.
- QA runs tests and produces `TestResult`.
- Reviewer approves, repairs, or escalates through `ReviewDecision`.

## Strong Answer Indicators

- Agents have distinct roles, goals, and tools.
- SOP includes both happy path and failure path.
- QA failure routes back to Coder with error evidence.
- No agent has every tool.
- Handoffs are named artifacts, not vague messages.

## Common Mistakes

- Giving all agents file, database, and execution tools.
- Omitting retry limits.
- Treating SOP as a paragraph rather than a sequence.
- No acceptance criteria before coding.

## Instructor Check

Ask: "Where is the first place a hallucinated field would be rejected?" If the learner cannot answer, their contract design is underspecified.
