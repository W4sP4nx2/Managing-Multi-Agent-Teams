# Instructor demo: deterministic Software Factory

This private facilitation script targets a five-minute demonstration. Learner pages use competency order without classroom timings. Run locally before presenting and retain actual evidence. The command makes no API calls, needs no API keys, and incurs $0.00 in API charges.

## Preparation

Activate the course environment. Run `python orchestrator.py --check-only` and `python orchestrator.py --security-demo`. Keep a terminal and browser visible. Choose a disposable factory workspace so the candidate and decisions belong to this demonstration.

## Five-minute walkthrough

| Time | Instructor action | Evidence to discuss |
| --- | --- | --- |
| 0:00–0:40 | Show the travel-site request, role labels, and profile. State that outputs are fixtures and delays are presentation pacing. | Actual API cost $0.00. Simulated plan $0.50. |
| 0:40–1:10 | Run `python live_simulation_orchestrator.py --delay-seconds 1.5`. Review and approve plan/spend. | Human decision binds the configured teaching budget. |
| 1:10–2:00 | Inspect the typed plan, approve preparing the Coder fixture, then inspect its generated page source. | Actual local files in an isolated Git worktree. |
| 2:00–3:05 | Explain and approve each bounded Security, UI/UX, and QA action, then inspect its result before continuing. | A failed result blocks the next stage; avoid claiming no vulnerabilities or full WCAG conformance. |
| 3:05–3:40 | Review the final artifact/revision and approve local publication. Run `open index.html`. | Real local page, receipt/digest, no hosted deployment. |
| 3:40–4:25 | Run `python orchestrator.py --security-demo`. Show password storage, insecure HTTP, and exfiltration findings. | Malicious request blocks with no publication. |
| 4:25–5:00 | Connect contracts to Lab 1, role separation to Lab 2, attempt/budget gates to Lab 3, and evidence to the ERD/CI/CD lab. | Learners name the failed gate and next accountable owner. |

If discussion takes longer, shorten pacing with `--delay-seconds 0`; do not bypass gates. `--no-input` must stop at approval. A fixture actor injected by automated tests is test evidence, not a human approval. The optional recording is a capture of this deterministic run and must retain the simulation label.
