# Homework B Solution Guide: Production Controls

## Strong Answer Indicators

- Human approval blocks high-risk actions before execution.
- Benchmarks include accuracy, latency, cost, hallucination rate, and tool usage efficiency.
- Cache keys include prompt and model/config parameters.
- Long-term memory retrieval respects sensitivity boundaries.
- Forgetting strategy is measurable and explainable.

## Common Mistakes

- Asking for human approval after executing the action.
- Simulating benchmark metrics without deterministic formulas.
- Caching responses without model/config context.
- Forgetting memories without recording why they were removed.

## Minimum Passing Evidence

- Approval and rejection examples.
- Cache hit, cache miss, and budget denial audit events.
- Benchmark comparison across two agent configurations.
- Memory retrieval plus forgetting demonstration.
