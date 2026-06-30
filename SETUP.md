# Environment Setup Guide

## Required Software

- Python 3.10 or newer
- Git
- JupyterLab or VS Code with notebook support

## Recommended Python Setup

```bash
cd "/Users/lwinnaingkyaw/Documents/Training Managing Multi-Agent Teams"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Optional Production Packages

The notebooks include offline fallbacks so learners can run without API keys. FastAPI is included in `requirements.txt` for NB8. For live production integrations, install:

```bash
python -m pip install crewai chromadb pydantic-ai langgraph mcp pyautogen uvicorn
```

## API Keys

For workshop delivery, set only the provider keys you actually use:

```bash
export OPENAI_API_KEY="..."
export ANTHROPIC_API_KEY="..."
```

The default course notebooks are designed to run without live model calls. Live-model cells should be clearly marked by the instructor.

## Verification

Run the core implementation:

```bash
python3 src/enterprise_agent_team.py
```

Expected behavior:

- A first patch fails QA.
- The failure is written to shared memory.
- The coder repairs the patch.
- The final review ships.
- An unsafe schema example is rejected.

Run the automated verification pyramid:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/ -v --tb=short
python3 src/enterprise_agent_team.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/test_notebooks.py -v
```

Run the controlled Jupyter sandbox preflight before the learner sequence:

```bash
jupyter lab notebooks/00_sandbox_preflight.ipynb
```

Expected behavior:

- Required packages import successfully.
- `USE_LIVE_LLM` stays `False`.
- No API keys are required.
- The notebook confirms repository working directory markers.
- The notebook writes and cleans a small probe file in `/tmp`.

For coverage and timeout protection:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/ -v --cov=src --cov=assignments --cov-report=html --timeout=30
```

Optional notebook output validation, if `nbval` is installed:

```bash
cd notebooks
python3 -m pytest --nbval . --nbval-current-env
```

## Troubleshooting

| Symptom | Likely Cause | Fix |
| --- | --- | --- |
| `python: command not found` | System only exposes `python3` | Use `python3` in commands |
| `ModuleNotFoundError: pydantic` | Dependencies not installed | Run `python -m pip install -r requirements.txt` |
| `ModuleNotFoundError: fastapi` | NB8 dependency missing | Run `python -m pip install -r requirements.txt` |
| CrewAI/Chroma/MCP unavailable | Optional package not installed | Use notebook fallback or install optional packages |
| API key error | Live model cell was run | Set provider key or run offline fallback cells |

## Repository Tour

- `README.md`: learner-facing course overview, mission, module map, and success criteria
- `SETUP.md`: environment setup and verification path
- `slides/module_decks/`: six module-specific slide decks
- `notebooks/`: progressive practical notebooks
- `assignments/`: learner assignments and capstone
- `assignments/starter_code/`: scaffolds with TODOs
- `instructor/solutions/`: solution guides and grading support
- `instructor/verification_pyramid.md`: test strategy and instructor checklists
- `instructor/course_delivery_readiness_checklist.md`: course path and pre-push checklist
- `src/`: production-style core implementation
- `tests/`: automated verification suite
