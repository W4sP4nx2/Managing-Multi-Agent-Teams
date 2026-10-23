# Advanced Extension: A2A OpenAPI Contract

This network-boundary assignment is outside the two-day workshop and retained for optional advanced study. The core Capstone uses an intra-workshop Pydantic contract between the Development and Security teams.

## Exercise 8.5: A2A OpenAPI Contract

Prompt: Your Virtual Software Company needs to outsource `SECURITY_SCAN` to a third-party AI security agent hosted on another cloud. Design the REST API contract for that Agent-to-Agent handoff.

Deliverables:

- OpenAPI 3.0 YAML file for the external Security Agent.
- `POST /security-scan` endpoint.
- Request schema containing a strictly typed `CodePatch`.
- Response schema returning a strictly typed `SecurityReview`.
- API key authentication scheme.
- Example request and example response.
- Reflection explaining how OpenAPI enforces type-safe delegation across network boundaries the same way Pydantic enforces it inside Python.

Technical constraints:

- `CodePatch` must include files, rationale, and tests to run.
- `SecurityReview` must include approved status, findings, severity counts, and reviewer identity.
- The OpenAPI contract must reject unspecified fields through `additionalProperties: false` where appropriate.
- The API key must be defined in `components.securitySchemes`.

Rubric:

- OpenAPI schema correctness: 35%
- Type-safe A2A contract design: 30%
- Security/authentication design: 20%
- Reflection quality: 15%
