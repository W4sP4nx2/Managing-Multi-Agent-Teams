# Ex4 Solution Guide: Trust & Governance Matrix

## Expected Architecture

The learner should model agents as identities with organization, role, trust tier, public key reference, allowed tools, and allowed message schemas.

## Strong Answer Indicators

- Vendor agent can export approved reports but cannot read restricted deployment logs.
- Every cross-org handoff has a typed schema.
- Denial examples are concrete: identity, requested tool, data class, policy reason.
- Threat mitigations map to specific controls, not generic "monitoring."

## Common Mistakes

- No difference between confidential and restricted data.
- Trust is assigned by role name only.
- Vendor agents can read internal memory.
- Threat matrix omits context leakage.

## Instructor Check

Ask the learner to trace one denied request from agent identity to policy decision. A strong design can explain the denial in one sentence.
