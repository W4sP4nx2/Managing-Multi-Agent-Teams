# Development and automated readiness

This is the maintainer workflow for the **three foundation labs, a Capstone, and integrated factory/CI-CD labs**. Learner setup and assessment stay in [SETUP.md](SETUP.md) and [the master hub](README.md#golden-path).

## Install the verification environment

Use **Python 3.12** in a virtual environment, then install:

```sh
python -m pip install -r requirements/maintenance.txt
```

This adds notebook execution and manifest readers to the course packages. It uses no provider account, API key, paid model, or local LLM. Installation needs internet or a prepared package bundle.

## Work in small verified changes

1. Turn the scenario or reported defect into an automated test before changing behavior. Use a unit test for an isolated rule and an integration test for a handoff or notebook workflow.
2. Run the smallest affected test and confirm it fails for the expected reason. Repair the implementation and rerun it.
3. Run fast checks during editing:

   ```sh
   python -m pytest tests -m unit -q
   ```

4. Before distributing the course or requesting review, run the complete gate:

   ```sh
   python tools/check_readiness.py
   ```

The gate checks Python and exact direct dependency pins, runs `pip check`, then runs unit tests before integration tests. It fails on a test failure, error, skip, missing/empty report, timeout, or a change to verification inputs during the run. `--stage unit` and `--stage integration` run individual stages; only the default `all` run covers full readiness. Every new test must have exactly one `unit` or `integration` marker so the gate cannot silently omit it.

## What the checks cover

| Layer | Automated evidence |
| --- | --- |
| Unit | Pydantic contracts, path rejection, memory visibility, all nine clearance combinations, Manager permissions/context/payload checks, bounded repair, cost/escalation evidence, and the readiness command's failure behavior. |
| Integration | Existing component and end-to-end flows, adversarial coder behavior, real Jupyter execution of all seven required notebooks, grader state transitions, stale QA inbox reset, typed Dev-to-Security validation order, and SQL/XSS teaching-marker rejection. |
| Historical demo link | `extensions/bonus_live_demo.ipynb` redirects to the deterministic factory. Tests force its old flag both ways and reject provider imports; there is no paid execution branch. |
| Mock CI/CD extension | Contract, gate-order, explicit approval, stale-evidence, resubmission, and replay unit checks, plus real offline Jupyter execution of starter, waiting, denied, and repaired/approved notebook states. |
| Distribution | The root `notebook_manifest.yml` resolves the seven handouts; `notebooks/` contains exactly those files. Distributed notebook outputs remain empty, execution does not modify handouts, and learner-pack links include the Lab 1–2 diagram assets. |
| CI | Pull requests, pushes, and manual dispatch run the same gate on Ubuntu and Windows with Python 3.12. Reports upload even on failure. |

The notebook tests read the **actual handouts** and apply the instructor guide's repairs to in-memory copies. Each execution starts a separate Jupyter kernel using the verification environment's Python. Provider credentials are omitted. Live Crew entry points, external DNS/connections, and interactive prompts fail the run. A separate test deliberately triggers these tripwires so an ineffective guard cannot produce a misleading green result. Local loopback ports are required for Jupyter itself.

Expected raw scores are assertions, including the intentionally broken starts:

| Notebook | Starter | Partial repairs | Complete repair |
| --- | ---: | --- | ---: |
| Lab 1 | 0/15 | Range only: 5/15; extra-field rejection only: 10/15 | 15/15 |
| Lab 2 | 0/15 | Permissions only: 5/15; context only: 10/15 | 15/15 |
| Lab 3 | 0/15 | Input only: 7/15; retry bound only: 8/15 | 15/15 |
| Capstone code | 5/20 | — | 20/20 |

Keep source notebooks broken at the intended TODOs. Do not save executed tests or solutions into learner files.

## Reports and delivery decision

The command writes `.test-results/readiness/summary.json` and a separate directory per run containing stage logs, JUnit XML, executed notebook copies, and the environment/source fingerprint. These generated files are ignored by Git. In CI, download the `readiness-<OS>` artifact to inspect failures. A past green report describes only its recorded inputs and environment; rerun after changes.

Passing this gate supports **distribution of the deterministic course**. It does not establish live model reliability, production security, deployment hosting, or complete SQL/XSS detection. The teaching scanners are marker checks, and simulated QA/cost evidence remains simulated. All distributed notebooks, including archived lessons, receive output-cleanliness checks. The factory receives actual temporary Git/worktree and publication tests, denial/stale-evidence tests, exact simulated-budget checks, and declarative QA execution. The historical bonus has no provider branch. The [CrewAI advanced reference](crewai_learning/README.md) receives fixture-driven unit tests and real Jupyter-kernel execution with outbound networking blocked; its code and notebook are included in the verification fingerprint. The [Mock CI/CD extension](extensions/11_mock_cicd_pipeline.ipynb) receives contract/gate tests and offline Jupyter execution; its source and notebook are also fingerprinted. Other optional and archived lessons do not receive full execution coverage. The archived seven-agent research project remains outside the execution gate.

GitHub Actions runs after the workflow reaches GitHub. Local success does not prove the remote Ubuntu/Windows jobs have run. Require the resulting readiness checks in repository branch protection if you want GitHub to block merges; that repository setting is separate from this workflow file.

## Audit active curriculum links

Run the default offline check before distribution:

```sh
python tools/audit_links.py check
```

The scope follows the learner-package file list, required and advanced-reference notebook manifest entries, current root guides, and active instructor references. Archived content, environments, and generated reports are excluded as audit sources. A link into an archive still has its destination and fragment checked. Notebook Markdown is checked at its distributed location; repairs update the maintained source before regenerating the affected handout. Code examples and illustrative URLs are excluded.

An explicit external check records time-dependent HTTP observations and writes JSON plus a readable report:

```sh
python tools/audit_links.py check --external --report output/link-audit.json
```

Inspect the classifications, proposed repairs, and unverified URLs. Apply the recorded repair set without making new network requests:

```sh
python tools/audit_links.py apply --from-report output/link-audit.json
python tools/audit_links.py check
```

Apply rejects stale source hashes. Valid paths, anchors, and successful redirects remain unchanged. Confirmed missing local references and permanently unavailable external links lose their wrappers while useful labels remain. Ambiguous mappings and transient network failures remain reported for review. A clean report causes no content writes. The command uses no LLM or provider API.

## Rebuild the six-slide deck and executive brief

The canonical deck content is [Marp Markdown](slides/managing_multi_agent_teams_6_slides.md). Its builder, `tools/build_compact_deck.mjs`, reads that source and creates the editable PowerPoint in `slides/` and matching PDF in `pdf/`. The root `pdf/` folder is the canonical location for PDF exports. Use the Codex bundled Node runtime and set `CODEX_RUNTIME_NODE_MODULES`, `CODEX_RUNTIME_PYTHON`, and `CODEX_PRESENTATIONS_SKILL_DIR` to the paths returned by the workspace dependency loader and the installed presentation skill. The builder uses the bundled presentation tooling and LibreOffice PDF conversion; it does not install dependencies.

```sh
node tools/build_compact_deck.mjs
```

The [leadership brief source](leadership/executive_brief.md) is maintained separately. Render it with a Python environment containing ReportLab and pypdf, using the bundled workspace Python when available:

```sh
python tools/build_executive_brief.py
```

Arial is embedded in the executive PDF. On other platforms, pass `--font-dir` pointing to a licensed Arial installation containing the regular and bold faces. Confirm six deck slides, six slide-PDF pages, and one A4 executive page, then inspect every rendered page. Keep the executive PDF outside the learner ZIP. Keep the exported deck PDF, executive brief, and Paper ADR quick sheet together in the root `pdf/` folder.

## Build the learner handout

Build a handout only when you need a ZIP to share. The generated `dist/` folder is optional, is not used by the course runtime or notebooks, and can be deleted. The command below recreates it from the source files.

After the readiness gate passes, run:

```sh
python tools/build_learner_pack.py
```

Share `dist/managing-multi-agent-teams-learner.zip`. The ZIP contains the current deck, seven clean course notebooks, the CrewAI bridge, the consolidated assignment book, simulations, course/setup/assessment documents, and supporting references. It preserves the directory structure used by slide and notebook links. Extract it before starting JupyterLab.

The builder uses an explicit file list and excludes the root instructor playbook, instructor solutions, test machinery, optional notebooks, archives, old decks, provider credentials, and local environments. Links to excluded material become plain text marked “full repository”; the package explains that these are optional or instructor references. The package's notebook manifest lists only the required sequence. A build report records file hashes and sizes in `dist/learner-pack-manifest.json`.

Every required notebook embeds its exercise SVG in a Markdown attachment; the factory notebook also embeds the ERD. The [diagram guide](README.md#diagram-guide) and editable SVG sources remain available. When changing an attached diagram, rebuild the notebooks from their cell sources. The [Software Factory guide](extensions/live_software_factory.md), runtime modules, fixture assets, offline configuration, CrewAI bridge, and ERD are included so extracted learners can run the whole route. The readiness fingerprint tracks factory modules, fixture/config files, diagrams, and documentation. The automated gate performs local publication with clearly named fixture actors; it never requests a provider or remote deployment.

The full repository retains optional learning and maintenance materials. `.venv/`, `venv/`, `.test-results/`, caches, and an archived local virtual environment account for most local disk usage; they are ignored by Git and excluded from the handout. They are not lessons. Building the handout does not delete these local files or historical sources.
