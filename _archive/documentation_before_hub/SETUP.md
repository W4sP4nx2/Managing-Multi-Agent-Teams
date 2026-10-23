# Course setup

[Course home](README.md) · [Playbook](PLAYBOOK.md) · [Factory guide](extensions/live_software_factory.md)

Use Python 3.12, Git, and JupyterLab. Run all commands from the repository root. Installation needs internet or a prepared package bundle. All course activities use deterministic local fixtures. There are no API calls, API keys, or provider charges.

## Create the environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyterlab
```

On Windows, activate `.venv\Scripts\Activate.ps1` in PowerShell. Select the environment's Python kernel in JupyterLab. Keep the repository folders together so notebook and exercise links resolve.

Run notebooks in order:

| Notebook | Purpose |
| --- | --- |
| [00 · Preflight](notebooks/00_sandbox_preflight.ipynb) | Check the environment |
| [01 · Typed contracts](notebooks/01_lab_pydantic.ipynb) | Repair the schema |
| [02 · Team oversight](notebooks/02_lab_crewai.ipynb) | Repair tools and context |
| [03 · Manager oversight](notebooks/03_lab_security.ipynb) | Bound repair and reject unsafe input |
| [04 · Capstone](notebooks/04_capstone.ipynb) | Validate the Development-to-Security handoff |
| [05 · Software Factory](notebooks/05_live_software_factory.ipynb) | Inspect role labels, simulated costs, human gates, and Git output |
| [06 · Local CI/CD](notebooks/06_local_cicd.ipynb) | Prove release checks and publication authorization |

## Verify the local factory

```bash
python orchestrator.py --check-only
python orchestrator.py --security-demo
python live_simulation_orchestrator.py
```

Default simulation uses typed pre-generated responses with actual API cost $0.00. Presentation delays make the collaboration visible. They are not real model thinking. The interactive run asks for each human decision. Use `python live_simulation_orchestrator.py --mode replay --delay-seconds 0 --workspace output/software-factory --no-input` to prove that unattended execution stops at approval rather than publishing.

After explicitly approving the final local publication, open the produced page:

```bash
open index.html
```

On other systems, use the browser's file-open command. No final approval means no newly published root page. Inspect the run's candidate and evidence in the workspace rather than assuming an old `index.html` belongs to the current run.

## Simulation profile and budget

No `.env` file or provider dependency installation is needed. Review [software_factory/simulation_config.json](software_factory/simulation_config.json) to inspect role labels, simulated charges, budget, and pacing.

| Simulated role | Illustrative model label | Simulated amount |
| --- | --- | ---: |
| Engineering Manager / Orchestrator | GPT-4 | $0.05 |
| Coder | Claude 3.5 | $0.15 |
| Security Reviewer | GPT-4 Turbo | $0.10 |
| UI/UX Reviewer | GPT-4 Vision | $0.10 |
| QA Auditor | GPT-3.5 | $0.05 |
| Human-authorized local publication | Local operation | $0.05 |
| **Plan total** | **Actual API cost: $0.00** | **$0.50 simulated** |

These historical model names are explanatory labels. No model engine runs and no price is a provider quote. Approve or deny the teaching amount at each requested gate. Denial, missing input, a failed bounded review, or insufficient simulated budget stops dependent actions.

The primary command has a configurable presentation delay:

```bash
python live_simulation_orchestrator.py --delay-seconds 1.5
```

For deterministic verification without pacing:

```bash
python live_simulation_orchestrator.py --mode replay --delay-seconds 0
```

`python orchestrator_with_approval.py` remains a compatible entry point. Simulation/replay are the available modes. A request for live mode fails with a clear message.

## Local CI/CD hook exercise

[Notebook 06](notebooks/06_local_cicd.ipynb) is the integrated local release lab. For the separate Semgrep hook repair, run the [bootstrap](extensions/software_factory/setup-local-factory.sh) only after Git, Bash, Python, and Semgrep are installed:

```bash
bash extensions/software_factory/setup-local-factory.sh
```

It creates a disposable repository and worktrees under the temporary directory and prints the next commands. It does not configure a GitHub remote or hosted deployment. A message trailer is a teaching convention; remote enforcement requires independent trusted CI and authenticated reviews.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Wrong kernel or missing module | Activate `.venv`, install the declared requirements, then select that interpreter in JupyterLab |
| An intentionally broken starter scores 0 | Repair the marked TODO, rerun dependent cells, and inspect the explanation |
| A command requests live mode | Use simulation or replay; live provider execution is intentionally unavailable |
| Budget denies a step | Inspect the simulated ledger and configured allowance; request a new teaching budget decision |
| Approval input is unavailable | Run in an interactive terminal; noninteractive operation must stop at the gate |
| Localhost sockets blocked by an executor | Run Jupyter in the authorized local terminal; the factory never needs outbound provider access |
| Semgrep missing | Use the notebook's local CI/CD evidence route; install and verify the scanner before the separate hook exercise |

For maintainer checks and packaging, see [DEVELOPMENT.md](DEVELOPMENT.md). [Dependency groups](requirements/README.md) explain core and maintenance installs.
