# Run and verify the CrewAI reference

[Reference home](README.md) · [Notebook](01_Bridge_Sequential_Crew.ipynb) · [Course setup](../SETUP.md)

This learning bridge uses the existing Python 3.12 course environment with CrewAI 1.15.23. The seven-agent research project's older environment is archived and is not used here. Installing dependencies needs internet or a prepared package bundle; executing the reference is offline.

## Run in JupyterLab

From the repository root, activate the environment described in [Setup](../SETUP.md), then run:

```bash
python -m pip install -r requirements.txt
python -m jupyterlab
```

Open `crewai_learning/01_Bridge_Sequential_Crew.ipynb` and run all cells in order. Select the course Python kernel. The notebook creates temporary CrewAI storage, disables telemetry, uses fixture LLMs, and blocks external network access around execution. It never needs a `.env` file or provider key.

Expected results:

- Exactly Manager, Coder, and QA agents; four tasks all declare an output model and callable guardrail.
- Malformed Coder output raises `ValidationError`; QA and review do not run.
- The failing tool raises three times; the wrapper returns `EscalationReport` with `ESCALATION_TRIGGERED`, `attempts: 3`, and three failure records.
- The valid fixture returns `ApprovedResult` after one attempt.

Restart the kernel and run all cells to repeat the complete demonstration. The failing-tool cell resets its counter before each run.

## Automated verification

Maintainers use the same pinned environment plus the existing test dependencies:

```bash
python -m pip install -r requirements/maintenance.txt
python tools/build_core_notebooks.py --check
python -m pytest tests/test_crewai_reference.py -q --notebook-artifacts=.test-results/crewai-reference
```

The tests run actual CrewAI tasks with local model fixtures and verify failure at every typed task boundary. They cover exact retry counts, fail-twice-then-pass recovery, early success, invalid QA/approval evidence, and a real Jupyter-kernel run. Kernel tests remove inherited provider credentials and block outbound networking. Jupyter still needs localhost sockets; a restricted executor must permit those local sockets.

For the full distribution gate, run `python tools/check_readiness.py`. The advanced reference is included in its source fingerprint and test collection while remaining alongside the seven-notebook course route without extra marks.

Executed notebook copies belong under ignored `.test-results/`. Distributed notebooks keep empty outputs and null execution counts. Edit [the source cells](../tools/notebook_sources/01_Bridge_Sequential_Crew.py), then regenerate using `python tools/build_core_notebooks.py`.

## Facilitation

Use the bridge after Lab 2 or during trace-diagnosis discussion. Predict the next task after malformed output, run the failure fixture, inspect the typed report, then explain the early-success case. Use [Assignment 09](../assignments/assignment_09_framework_comparison.md) to separate role/task orchestration from application-owned retry policy.

The third failure belongs to the tool; escalation belongs to the wrapper. Three attempts means at most three kickoffs, not four. The local escalation stub does not contact a human or grant approval for another run.

[Return to reference home](README.md) · [Learner paths](../README.md#learner-paths)

## Factory continuation

Run `python live_simulation_orchestrator.py` from the course root for paced deterministic collaboration, or add `--mode replay --delay-seconds 0` for fast rehearsal. No API key or provider setup is required. Explicit human gates control the real local publication. See [setup](../SETUP.md#simulation-profile-and-budget).
