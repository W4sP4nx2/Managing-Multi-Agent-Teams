# Homework A Solution Guide: Specialist Agent Skills

## Strong Answer Indicators

- All outputs are Pydantic models, not raw dictionaries.
- Code quality scores are bounded from `0.0` to `1.0`.
- Security scanner checks hardcoded secrets, SQL injection patterns, `eval`, `exec`, subprocess usage, and unsafe imports.
- Test generator covers happy path, edge cases, negative cases, and sandbox notes.
- Documentation generator does not invent APIs outside the submitted patch.

## Common Mistakes

- Returning plain `dict` objects instead of typed artifacts.
- Treating all security findings as the same severity.
- Generating tests for functions that do not exist in the patch.
- Producing verbose docs that are not connected to the actual code change.

## Minimum Passing Evidence

- One safe patch and one unsafe patch.
- At least one generated test suite.
- At least one documentation bundle.
- Clear explanation of how each specialist agent improves the managed team.
