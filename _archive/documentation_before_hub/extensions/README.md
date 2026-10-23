# Factory and supporting simulations

[Course home](../README.md) · [Playbook](../PLAYBOOK.md) · [Setup](../SETUP.md)

The deterministic Software Factory and local CI/CD are integrated into the course, through [notebook 05](../notebooks/05_live_software_factory.ipynb) and [notebook 06](../notebooks/06_local_cicd.ipynb). The guide keeps its historical path for stable links.

| Open | Purpose |
| --- | --- |
| [Factory execution guide](live_software_factory.md) | Simulated role collaboration, explicit human gates, actual local artifacts and $0.00 API cost |
| [Factory architecture](../resources/diagrams/live-software-factory.svg) | Role handoffs and release boundaries |
| [Capstone ERD](../resources/diagrams/capstone_factory_erd.md) | Persisted evidence and proposed travel-domain records |
| [Local hook bootstrap](software_factory/setup-local-factory.sh) | Disposable staged-scan/message-hook exercise |
| [Earlier mock CI/CD notebook](11_mock_cicd_pipeline.ipynb) | Comparison state-machine simulation, not the current release route |
| [Historical structured-output reference](bonus_live_demo.ipynb) | Fixture-only comparison material |

The current course requires no provider account, API key, or paid SDK setup. Old provider prototypes and unrelated advanced assignments belong in [_archive](../_archive/README.md). Local publication creates a file; it does not configure GitHub protection or a remote production environment.

## Optional Capstone architecture reading

The [LangGraph state/recovery comparison](../resources/framework_comparison.md#optional-capstone-architecture-extension-langgraph) is a design reference. It adds no required package or implementation. The current factory remains deterministic local Python.
