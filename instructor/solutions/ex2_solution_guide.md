# Ex2 Solution Guide: Theory-of-Mind Memory System

## Expected Behavior

The PM stores "Use PostgreSQL for persistent storage" in shared memory. The Coder receives only "Implement the user persistence layer" and must retrieve the PM's constraint before producing a `DesignPlan`.

## Minimal Correct Implementation

- `MemoryRecord` has author, visible roles, sensitivity, tags, and text.
- `search(query, requester)` filters unauthorized records before matching.
- `DesignPlan.storage_choice` becomes `PostgreSQL` due to retrieved memory.
- A restricted record exists and is not returned to the Coder.

## Strong Answer Indicators

- The Coder cites or records which memory item influenced the design.
- Retrieval is tag/text based, not direct ID lookup.
- The reflection correctly distinguishes shared memory from Theory of Mind: memory stores evidence; ToM uses it to infer teammate intent.

## Common Mistakes

- Hardcoding PostgreSQL in the Coder.
- Returning all memory before filtering.
- No sensitivity model.
- No demonstration that restricted memory is denied.
