# Optional Design Fixtures

These small reference artifacts support optional homework designs. They are outside the [required notebook sequence](../../notebook_manifest.yml) and are not loaded by the required labs, Capstone, or current extension notebooks. A policy file alone does not enforce permissions; an implementation must read and apply its rules.

## Reference scope

| File | Optional context | Runtime status |
| :--- | :--- | :--- |
| [`hr_tool_policy_matrix.yaml`](hr_tool_policy_matrix.yaml) | [Homework D: HR design](../../_archive/assignments/module10_hr_governance.md) | Illustrative role/tier policy. No loader or policy enforcement is wired to this file. |
| [`cost_aware_routing_fixtures.json`](cost_aware_routing_fixtures.json) | [Homework E: campaign routing](../../_archive/assignments/module11_marketing_orchestration.md) | Synthetic marketing costs and latency. No current notebook reads this file; the Capstone uses its own Fast/Expert records with different fixture values. |
| [`a2a_openapi_spec.yaml`](a2a_openapi_spec.yaml) | [Homework B: API contract design](../../_archive/assignments/module8_production_ready_agent_features.md) | A separate cross-system HTTP contract reference, not the Capstone's in-process Pydantic handoff or a running endpoint. |

No extra package is needed to inspect these JSON/YAML files. A future YAML loader would need its own dependency and tests; no YAML dependency is added to the required installation.

## Contribution Rules

- Prefer `.json`, `.yaml`, and `.csv` files that can be inspected in GitHub.
- Keep artifacts small enough to review in pull requests.
- Include schema versions when the structure may evolve.
- Do not store secrets, live API keys, production PII, or proprietary datasets.
