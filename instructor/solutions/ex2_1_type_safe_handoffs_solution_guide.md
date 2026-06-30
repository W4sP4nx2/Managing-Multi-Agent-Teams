# Solution Guide: Exercise 2.1 Type-Safe Handoffs

## Expected Behavior

The customer-service crew should produce three validated artifacts:

- `TranscriptAnalysis`
- `QualityEvaluation`
- `FinalReport`

Each artifact must be a Pydantic model instance. Raw dictionaries are acceptable only as input to `model_validate()` during the invalid-output test.

## Strong Answer Indicators

- `extra="forbid"` rejects hallucinated fields.
- Sentiment, urgency, issue category, and recommended action are bounded with `Literal` or enums.
- Invalid output demonstrates multiple failures: bad enum, empty required list, and extra field.
- `FinalReportAgent` receives typed `TranscriptAnalysis` and `QualityEvaluation`, not raw text.

## Common Mistakes

1. **Returning `dict` instead of Pydantic models**
   - Wrong: `return {"sentiment": "positive"}`
   - Right: `return TranscriptAnalysis(sentiment="positive", ...)`

2. **Validating only the first handoff**
   - Wrong: `TranscriptAnalyzerAgent` returns a schema, but `QualityEvaluatorAgent` returns raw text.
   - Right: all three agents return typed schemas: `TranscriptAnalysis`, `QualityEvaluation`, and `FinalReport`.

3. **Allowing unbounded enums**
   - Wrong: `sentiment: str`
   - Right: `sentiment: Literal["positive", "neutral", "frustrated", "angry"]`

4. **Not demonstrating rejection**
   - Wrong: only showing a happy-path report.
   - Right: show `ValidationError` for invalid enum values, empty required lists, and extra fields.

5. **Letting the final report ignore upstream schema data**
   - Wrong: hardcoding a final response independent of the analysis and evaluation.
   - Right: derive `recommended_action`, notes, and audit trail from typed upstream artifacts.

## Instructor File

`assignments/starter_code/ex2_memory_system_starter.py`
