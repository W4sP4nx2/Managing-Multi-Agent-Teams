# Learner Setup

[Course home](README.md) · [Learner paths](README.md#learner-paths) · [Slide index](README.md#main-deck-slide-index)

For the workshop sequence and schedule, see the [Playbook](PLAYBOOK.md). Use the compact learner ZIP supplied by your instructor, or [download the full repository ZIP](https://github.com/W4sP4nx2/Managing-Multi-Agent-Teams/archive/refs/heads/main.zip) or clone the repository with Git. Extract the ZIP before use. Open the extracted/cloned course folder in a terminal before creating the environment.

## Required setup

> **🔴 Python 3.12 is the maximum supported version for this workshop setup. Do not use Python 3.13 or newer.** The required CrewAI environment is tested with Python 3.12.

**Install only `requirements.txt` for the course.** It contains Pydantic, JupyterLab, the notebook kernel, CrewAI, and pytest. No additional requirements file, provider account, or API key is needed for the five required notebooks.

## Environment map

| Tool or platform | What it is | Where it runs | Learner use |
| --- | --- | --- | --- |
| JupyterLab | Interactive workspace | Local browser, backed by the activated `.venv` | Do the labs and Capstone in notebook cells; inspect outputs and validation errors. |
| CrewAI and Pydantic | Python libraries | Installed in `.venv` with `pip` | Import them in notebooks to define team roles and validate handoffs. |
| GitHub | Course repository | Hosted source repository | Download or clone the starter materials. Agents do not run on GitHub. |
| Terminal | Environment control | macOS/Linux shell or Windows PowerShell | Create/activate the environment, install packages, and start JupyterLab. |

**Learner rule:** work in JupyterLab, use CrewAI and Pydantic from Python, and use GitHub for course files. For required labs and the Capstone, keep `USE_LIVE_LLM = False`; no provider account or API key is needed.

These commands use `.venv` consistently. If you already have a working course environment, activate it and run the install command; there is no need to create it again.

### macOS / Linux

Run these four commands from the course folder root:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyter lab
```

### Windows PowerShell

Run these four commands from the course folder root:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m jupyter lab
```

In JupyterLab, open `notebooks/00_sandbox_preflight.ipynb`, run all cells, then follow [the required workshop manifest](notebook_manifest.yml). The `notebooks/` folder contains exactly five handouts: preflight, Labs 1–3, and the Capstone. Keep notebook outputs cleared in copies distributed to learners.

## Offline classroom use

The first package installation normally needs internet. For an offline classroom, install dependencies ahead of time or provide a wheel bundle/environment built for the learners' operating system and Python 3.12. After installation, the three labs and deterministic two-team Capstone can run without network access or provider keys.

## Optional packages

Skip extra packages during the required course. The [optional dependency guide](requirements/README.md) lists separate installs for maintainer verification, API-boundary examples, LangGraph experimentation, and the live-model bonus. These files are not included in the compact learner ZIP.

The [bonus live demonstration](extensions/bonus_live_demo.ipynb) is optional and reserved for the end of Day 2, after assessment. It requires separate provider configuration and may incur charges. Keep `USE_LIVE_LLM = False` in all required notebooks.

## Verification

Learners run the supplied notebook graders as described in the [Playbook](PLAYBOOK.md). The four-command workshop installation above is sufficient for the required activities.

Maintainers install the verification dependencies and run the automated readiness gate from the activated Python 3.12 environment:

```bash
python -m pip install -r requirements/maintenance.txt
python tools/check_readiness.py
```

See [DEVELOPMENT.md](DEVELOPMENT.md) for fast unit checks, notebook regression coverage, CI, and generated reports. Record the actual result in the [assessment compliance checklist](instructor/assessment_compliance_checklist.md).

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `python3.12` or `py -3.12` is not found | Python 3.12 is not installed | Install Python 3.12, then rerun the setup commands. |
| `ModuleNotFoundError` for a course package | Requirements were installed in another environment | Activate `.venv` in the course folder root and rerun `python -m pip install -r requirements.txt`. |
| Package download fails offline | The environment has not been preloaded | Connect for the initial install or ask the instructor for a matching wheel bundle/prepared environment. |
| Provider/API key error | An optional live-model cell was enabled | Keep live calls disabled for the required path, or use an instructor-configured provider outside the notebook. |

## Repository map

The compact learner ZIP contains the core materials. Optional and instructor folders below exist only in the full repository.

- `README.md`: course overview, learner paths, and slide index.
- `requirements.txt`: the only learner install file.
- `PLAYBOOK.md`: learner sequence, instructor schedule, grading, and guardrails.
- `notebooks/`: five required notebooks — open `00_sandbox_preflight.ipynb` first, then follow the sequence and manifest.
- `extensions/`: optional advanced notebooks outside the required workshop path.
- `_archive/`: older or replaced notebooks and advanced cross-organization A2A material.
- `assignments/`: Capstone brief and learner work.
- `instructor/`: checklist, grading tracker, and teaching references.

[Course home](README.md) · [Learner paths](README.md#learner-paths) · [Slide index](README.md#main-deck-slide-index)
