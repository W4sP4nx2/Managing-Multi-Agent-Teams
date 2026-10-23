# Course setup

[Course home](README.md) · [Playbook](README.md#golden-path) · [Factory guide](extensions/live_software_factory.md)

Use Python 3.12, Git, and JupyterLab. Run all commands from the repository root. Installation needs internet or a prepared package bundle. All course activities use deterministic local fixtures. There are no LLM or reasoning-model calls, API keys, or provider charges.

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
| [05 · Software Factory](notebooks/05_live_software_factory.ipynb) | Inspect the candidate page, review results, human gates, and Git output |
| [06 · Local CI/CD](notebooks/06_local_cicd.ipynb) | Prove release checks and publication authorization |

## Verify the local factory

```bash
python orchestrator.py --check-only
python orchestrator.py --security-demo
python live_simulation_orchestrator.py
```

The factory uses typed pre-generated responses and runs local checks and Git operations, with actual API cost $0.00. No `.env` file or configuration edits are needed. Presentation delays make the stages visible; they are not real model thinking. In the terminal, inspect the evidence and enter `yes` or `no` at six human gates: plan, code build, Security, UI/UX, QA, and local publication. Denial or missing input stops the next action.

For a faster rehearsal, add `--mode replay --delay-seconds 0` to the last command. Adding `--no-input` demonstrates that unattended execution stops at approval.

After explicitly approving the final local publication, open the produced page:

```bash
open index.html
```

On other systems, use the browser's file-open command. No final approval means no newly published root page. Inspect the run's candidate and evidence in the workspace rather than assuming an old `index.html` belongs to the current run.

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
| Approval input is unavailable | Run in an interactive terminal; noninteractive operation must stop at the gate |
| Localhost sockets blocked by an executor | Run Jupyter in the authorized local terminal; the factory never needs outbound provider access |
| Semgrep missing | Use the notebook's local CI/CD evidence route; install and verify the scanner before the separate hook exercise |

For maintainer checks and packaging, see [DEVELOPMENT.md](DEVELOPMENT.md). [Dependency groups](#dependency-profiles) explain core and maintenance installs.

<a id="dependency-profiles"></a>

<a id="dependency-profiles-course-and-maintainer-dependencies"></a>
## Course and maintainer dependencies

All learner activities, including the paced Software Factory simulation, use the root requirements:

```bash
python -m pip install -r requirements.txt
```

No API key, provider SDK install, or billing account is required. The factory uses pre-generated role outputs and local checks with actual API cost $0.00.

| Purpose | Install |
| --- | --- |
| Course notebooks and deterministic factory | `python -m pip install -r requirements.txt` |
| Maintainer verification and learner-package build | `python -m pip install -r requirements/maintenance.txt` |
| API-boundary reference | `python -m pip install -r requirements/api.txt` |
| LangGraph design experimentation | `python -m pip install -r requirements/langgraph.txt` |

`live-llm.txt` remains a compatibility alias to the core requirements and installs no additional provider libraries. Historical paid-provider prototypes are archived. The separate Semgrep hook exercise requires its installed scanner, as described in [setup](#local-cicd-hook-exercise). Framework design reading requires no extra package.
