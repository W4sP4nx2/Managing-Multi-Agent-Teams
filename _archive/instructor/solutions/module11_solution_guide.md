# Homework E Solution Guide: Marketing Orchestration Track

## NB6 Local Python Routing Reference

This reference is for instructors. Learners implement their own `choose_model()` in the optional homework. The classroom router is a local Python policy that compares complexity, risk, and simulated cost; it does not call a hosted router or train an orchestration model.

```python
def choose_model(self, analysis: TaskComplexity) -> tuple[ModelClass, str]:
    if analysis.risk_level == "high":
        return ModelClass.REASONING, "High-risk task requires deeper review"
    if analysis.requires_reasoning:
        return ModelClass.REASONING, "Task explicitly requires reasoning"
    if analysis.code_heavy:
        return ModelClass.CODE_SPECIALIST, "Code-heavy task uses a code specialist"
    if analysis.complexity == "simple":
        return ModelClass.FAST_CHEAP, "Simple task uses the fast, lower-cost class"
    return ModelClass.BALANCED, "Default to the balanced class"
```

The high-risk branch must precede low-cost shortcuts. If a learner adds `SECURITY_SPECIALIST`, update both the model registry and the in-notebook expected route for high-risk inputs.

## Strong Answer Indicators

- Bulk variation tasks route to `FAST_CHEAP`.
- Strategy and high-risk compliance tasks route to stronger models.
- Budget check happens before model dispatch.
- Brand safety scanner blocks unauthorized trademarks and false partnerships.
- Repair loop writes violation evidence to shared memory.

## Common Mistakes

- Tracking spend after the model call instead of before dispatch.
- Routing high-risk compliance tasks to cheap models because they are short.
- Publishing social drafts before brand safety approval.
- Returning scanner findings as unstructured strings.

## Minimum Passing Evidence

- Dynamic routing cost comparison against always-`REASONING`.
- `BudgetExhausted` result for over-budget dispatch.
- Unsafe draft blocked.
- Repaired draft approved and eligible for publishing.
