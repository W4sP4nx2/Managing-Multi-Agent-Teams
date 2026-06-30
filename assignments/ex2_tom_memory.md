# Ex2: Theory-of-Mind Memory System

## Prompt

Build a shared memory system where Agent A can record a constraint that Agent B must discover through memory retrieval before producing its output. The exercise simulates Theory of Mind: Agent B should infer what the PM knows and expects, instead of relying only on the immediate prompt.

## Scenario

A Product Manager records a hidden architectural constraint: "Use PostgreSQL for persistent storage." The Coder receives a vague task: "Implement the user persistence layer." The Coder must query shared memory, discover the hidden constraint, and produce a typed design plan that uses PostgreSQL.

## Deliverables

1. A `MemoryRecord` schema with author, visibility, sensitivity, tags, and text.
2. A `DesignPlan` schema with storage choice, rationale, risks, and follow-up questions.
3. A memory search function that filters by requester role and sensitivity.
4. A demonstration run where the Coder discovers the PostgreSQL constraint without receiving it in the direct prompt.
5. A short reflection explaining how this maps to TeamLog and Theory of Mind.

## Technical Constraints

- Use Pydantic or equivalent strict schema validation.
- Do not hardcode PostgreSQL inside the Coder function.
- Include at least one memory item the Coder is not authorized to read.
- Retrieval must use tags or text matching, not direct object access by ID.

## Grading Rubric

- Memory schema and access control: 35%
- Correct Theory-of-Mind behavior through retrieval: 40%
- Explanation and production reasoning: 25%
