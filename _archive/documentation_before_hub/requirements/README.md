# Course and maintainer dependencies

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

`live-llm.txt` remains a compatibility alias to the core requirements and installs no additional provider libraries. Historical paid-provider prototypes are archived. The separate Semgrep hook exercise requires its installed scanner, as described in [setup](../SETUP.md#local-cicd-hook-exercise). Framework design reading requires no extra package.
