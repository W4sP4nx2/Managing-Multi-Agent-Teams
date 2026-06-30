# Homework F Discussion Guide: Advanced Fugu Discussion

Homework F is optional conceptual material, not a graded implementation lab. Use it to help learners understand why Fugu is important without pretending they can reproduce an RL/evolutionary orchestrator in a short notebook.

## Discussion Goals

- Learners can explain the difference between heuristic routing and learned orchestration.
- Learners can identify what telemetry would be required to train or evaluate an orchestrator.
- Learners can critique dynamic scaffold generation, debate, topology adaptation, and workflow isolation as architecture patterns.
- Learners can say which parts of NB9 are teaching adapters rather than production Fugu.

## Strong Discussion Indicators

- Names the compute and benchmark requirements for training an orchestrator.
- Rejects the idea that an if/else rule is "learned" merely because it uses history.
- Explains why governance must come before optimization.
- Treats dynamic scaffolds and debate as management patterns that still need typed contracts and audit logs.
- Identifies rollback, evaluation, and human approval needs for adaptive orchestration.

## Common Misconceptions

- "A rule updated after ten failures is the same as RL." It is not. It is a teaching adapter.
- "More agents means better orchestration." Not necessarily; it can increase latency, cost, and coordination errors.
- "Debate automatically improves correctness." Debate only helps when disagreement is structured, evidence is preserved, and escalation is available.
- "Fugu should be a required coding lab." It should remain optional/conceptual in this course.

## Suggested Facilitation

1. Show NB6 as transparent heuristic routing.
2. Show NB9 as a conceptual bridge.
3. Ask learners what data would be required to train a real orchestrator.
4. Ask what could go wrong if an orchestrator updates policy without approval.
5. End by reconnecting to the core course: schemas, MCP governance, memory, repair, and auditability.
