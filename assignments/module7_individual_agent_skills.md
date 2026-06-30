# Homework A: Specialist Agent Skills

## Mission

Build skilled specialist agents. The core course teaches learners how to govern a team; this module teaches learners how to make each team member good at its job.

Starter code: `assignments/starter_code/module7_individual_agent_skills_starter.py`

Instructor guide: `instructor/solutions/module7_solution_guide.md`

## Exercise 7.1: Code Quality Assessor

Prompt: Implement `assess_code_quality(patch: CodePatch) -> CodeQualityReport`.

Deliverables:

- `CodeQualityReport` Pydantic schema with security, testability, documentation, style, and edge-case scores.
- Deterministic checks for unsafe patterns, missing docstrings, missing tests, and brittle code.
- At least three test patches: strong, mediocre, and unsafe.

Technical constraints:

- Scores must be floats between `0.0` and `1.0`.
- Do not return raw dictionaries from the assessor.
- Findings must include actionable explanations, not only numeric scores.

Rubric:

- Schema quality and typed output: 30%
- Assessment signal quality: 40%
- Test cases and failure coverage: 20%
- Instructor-readable explanation: 10%

## Exercise 7.2: Test Generator Agent

Prompt: Implement `generate_test_suite(code_patch: CodePatch) -> TestSuite`.

Deliverables:

- `TestSuite` schema with unit, integration, edge-case, and performance test groups.
- Generated tests for at least one utility function and one API-style function.
- A short note explaining which tests should run in a secure sandbox.

Technical constraints:

- Test names must be stable and descriptive.
- Generated tests must reference files/functions present in `CodePatch`.
- Include at least one edge case and one negative test.

Rubric:

- Coverage of normal, edge, and failure cases: 40%
- Schema enforcement and typed artifacts: 25%
- Practical runnable test design: 25%
- Clear sandboxing note: 10%

## Exercise 7.3: Security Scanner Agent

Prompt: Implement `security_scan(patch: CodePatch) -> SecurityReport`.

Deliverables:

- `SecurityReport` schema with `critical`, `medium`, `low`, and `findings`.
- Checks for SQL injection patterns, hardcoded secrets, `eval`/`exec`, subprocess usage, and unsafe imports.
- Demonstration showing a safe patch approved and an unsafe patch rejected.

Technical constraints:

- Scanner must inspect all files in the patch.
- Critical findings must block release.
- The output must be deterministic for offline grading.

Rubric:

- Vulnerability coverage: 40%
- Severity classification: 25%
- Release-gate behavior: 25%
- Clear remediation guidance: 10%

## Exercise 7.4: Documentation Generator Agent

Prompt: Implement `generate_documentation(patch: CodePatch) -> DocumentationBundle`.

Deliverables:

- `DocumentationBundle` schema with README text, API docs, inline comment suggestions, and changelog.
- Documentation generated from patch contents and rationale.
- A release note that connects back to the original `TaskSpec`.

Technical constraints:

- Do not invent APIs that are not in the patch.
- Changelog must be concise and user-facing.
- Inline comments should be suggested only where complexity justifies them.

Rubric:

- Accuracy against the patch: 35%
- Completeness of docs bundle: 30%
- Release-note quality: 20%
- Restraint and clarity: 15%
