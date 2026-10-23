# Capstone: a governed travel-site factory

[Course home](../README.md) · [Playbook](../PLAYBOOK.md) · [Capstone notebook](../notebooks/04_capstone.ipynb) · [Factory lab](../notebooks/05_live_software_factory.ipynb) · [Local CI/CD](../notebooks/06_local_cicd.ipynb)

## Product brief

Build a minimalist travel discovery website for a learner planning a short trip. The site needs a responsive navigation, clear hero/CTA, destination cards with useful text, and a clearly labeled contact section. It must not collect passwords, store credentials in browser storage, contact an unapproved endpoint, or claim to complete bookings. The delivered site is static HTML/CSS with local assets/behavior as supplied by the fixture.

The factory shows simulated Engineering Manager, Coder, Security, UI/UX, and QA collaboration using pre-generated outputs. It makes no API calls and costs $0.00 in actual API charges. Model names are illustrative labels. Delays represent presentation pacing rather than real model thinking.

## Contract and team boundary

First complete [notebook 04](../notebooks/04_capstone.ipynb):

1. Reject `DevDeliverable.unit_tests_passed=False` with a Pydantic validator.
2. Revalidate the Development deliverable before the Python Coordinator starts Security.
3. Keep the scanner with the Pen Tester and approval tool with the Security Manager.
4. Inspect `SecurityAuditResult`, validation order, and code grader.
5. Explain the largest remaining risk in your ADR.

The foundation notebook uses local Python adapters and separately constructs CrewAI configurations. It does not execute both Crews. A typed QA-status claim is not independent proof that tests passed.

## Factory and local release tasks

Continue into notebooks 05 and 06 using the same travel-site request. Run:

```bash
python orchestrator.py --check-only
python orchestrator.py --security-demo
python live_simulation_orchestrator.py
```

Inspect the pre-generated candidate before approving plan/spend, code build, Security, UI/UX, QA, and final local publication. The default simulated plan is $0.50 including the $0.05 publication step. Actual API cost stays $0.00. Reject the malicious request that stores passwords in `localStorage` and sends them over HTTP to an external endpoint.

Retain evidence for the exact candidate revision: generated source, security findings, bounded UI/QA checks, test-case results, simulated ledger, gate decisions, and Git commit. `open index.html` displays the real local file only after explicit final publication approval. The factory creates no hosted deployment or booking backend.

## Entity relationship diagram

Open the [editable ERD source](../resources/diagrams/capstone_factory_erd.md) or [diagram image](../resources/diagrams/capstone_factory_erd.svg). Use it to trace:

| Record | Relationship and purpose |
| --- | --- |
| Factory run | Owns the request hash, mode, branch, status, and configuration |
| Artifact | Belongs to a run and records source path, digest, and Git revision |
| Stage approval | Binds a human/fixture actor decision to a stage and subject digest |
| Review and QA case | Refer to the artifact actually checked, including failures and test evidence |
| Local publication | Refers to the approved artifact and final decision, with published path/digest |
| Factory event | Records the workflow stage and selected synthetic evidence |
| Simulated budget ledger | Reserves/settles teaching amounts with no provider bill |
| Proposed destination/itinerary content | Explains the travel product's domain; it does not imply a deployed database or booking service |

Explain why a changed artifact invalidates earlier review/approval evidence. Identify which records exist in SQLite and which travel-domain relationships are a future design.

## Assessment: 40 points

### Capstone code: 20 points

| Criterion | Points | Evidence |
| --- | ---: | --- |
| Separation of duties | 5 | Security Manager approval only, Pen Tester scan access |
| Contract and Coordinator handoff | 10 | Failed QA rejected, validation precedes Security start |
| Typed audit output | 5 | Pipeline returns `SecurityAuditResult` |

The notebook auto-grader displays the code score. Factory/CI/CD evidence supports the defense and adds no separate score.

### Architecture Decision Record: 20 points

1. **Risk:** which concrete handoff or publication risk matters most for this travel-site factory?
2. **Governance:** which contract, role permission, budget/gate decision, and revision evidence reduce that risk? What actually happened in your run?
3. **Next step:** what would a hosted service need before handling real travelers, inquiries, or payments, and why?

| Criterion | Points | Full-credit condition |
| --- | ---: | --- |
| Risk and architecture | 6 | Concrete travel/factory risk and clear team/data boundary |
| Governance mapping | 7 | Connects controls to observed contracts, checks, decisions, and revision evidence |
| Next-step judgment | 7 | Credible improvement with a reason and evidence needed to evaluate it |

When the learner's environment prevents execution, a sound one-page Paper ADR is an accepted fallback. Include schema pseudo-code, role tools, ERD relationships, and remaining risk/evidence/next step. The same /20 ADR rubric applies. A paper submission must not invent execution, API usage, security completeness, WCAG conformance, or deployment results.

## Optional architecture extension: a LangGraph state machine

This is reference design with no extra implementation or marks. Compare the [framework state/recovery reading](../resources/framework_comparison.md#optional-capstone-architecture-extension-langgraph) with the implemented deterministic Coordinator. A future graph could represent validated handoffs and human pauses explicitly. It is not part of the factory runtime.
