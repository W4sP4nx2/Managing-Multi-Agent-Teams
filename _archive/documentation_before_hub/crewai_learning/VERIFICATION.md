# Three-agent reference verification

Verified **20 October 2026, Asia/Bangkok**. The [notebook](01_Bridge_Sequential_Crew.ipynb) is an optional reference for Lecture 8 and Assignment 09, alongside the seven required notebooks without extra marks.

| Requirement | Verified evidence |
| --- | --- |
| Three agents | Manager, Coder, QA; one Manager handles brief and review tasks. |
| Archive the old example | Seven-agent project moved under `_archive/crewai_learning/`; 14 source/configuration files retain their hashes. |
| Strict output for every task | WorkOrder, CodePatch, QAReport, and ManagerDecision; callable guards reject invalid JSON before the next task. Tests inject garbage at all four boundaries. |
| Hard maximum of three attempts | Python wrapper owns the bound; agent and guardrail retries are disabled. Fresh crew per attempt. |
| Third failure escalates | Actual notebook output: `Tool failures: 3 | kickoffs: 3 | stopped: True`; typed `EscalationReport` contains three failures and `ESCALATION_TRIGGERED`. |
| No downstream work after malformed output | `ValidationError` observed; QA and Manager review call counts remain zero. |
| Useful success path | Valid fixture succeeds after one kickoff; a separate test recovers after two tool failures. |
| Invalid approval cannot pass | Tests reject failed QA, stale patch evidence, mismatched task identity, and Manager rejection. |
| Offline notebook | Executed in a real Jupyter kernel with credentials removed and external network tripwires; zero external attempts and unhandled cell errors. |
| Navigation and scope | Active README paths, Lecture 8, Assignment 09, syllabus, course map, and manifest point to the ungraded reference. |

The full `python tools/check_readiness.py` gate passed: **95 unit + 46 integration = 141 tests**, with zero failures, errors, or skips. Exact requirement pins and `pip check` passed. Python 3.12.3; CrewAI 1.15.23; Pydantic 2.12.5; nbclient 0.10.2; nbformat 5.10.4.

Run ID: `20261019T185734Z-495da39a` (UTC timestamp). Verification source fingerprint: `bc68688ef31f5d4fea2f0f90b0dda356620258c3b58ec6d21288f3f0772f19b7`.

[Recorded evidence and hashes](audit_evidence/2026-10-20-reference.json) identify the checked sources. Local executed copies and detailed logs are under `.test-results/readiness/20261019T185734Z-495da39a/`; they are intentionally excluded from distribution. The handout's code outputs and execution counts remain empty.

These results concern the supplied fixture scenarios. The example uses sequential execution and a hierarchy of responsibilities, not native hierarchical delegation. QA compares the supplied fixture rather than running generated code. Live provider behavior and deployment readiness were not tested. The pinned CrewAI version emits deprecation warnings and an event-pairing diagnostic for intentionally raised validation errors; execution assertions still verify the stop behavior.

[Reference home](README.md) · [Run it yourself](SETUP_AND_LEARNING_EXPERIENCE.md) · [Course learner paths](../README.md#learner-paths)
