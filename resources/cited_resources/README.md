# 📊 Cited Resources & Schemas

This folder contains raw, machine-readable artifacts cited in the course papers, notebooks, and assignments.

## Current Assets

| File | Cited In | Purpose |
| :--- | :--- | :--- |
| [`hr_tool_policy_matrix.yaml`](./hr_tool_policy_matrix.yaml) | Ex4, Homework D | YAML policy matrix for zero-trust tool boundaries in HR workflows. |
| [`fugu_routing_costs.json`](./fugu_routing_costs.json) | NB6, Homework E | Mock cost and latency matrix for Fugu-style heterogeneous routing. |
| [`a2a_openapi_spec.yaml`](./a2a_openapi_spec.yaml) | Homework B | OpenAPI 3.0 contract for Agent-to-Agent security scanning. |

## Contribution Rules

- Prefer `.json`, `.yaml`, and `.csv` files that can be inspected in GitHub.
- Keep artifacts small enough to review in pull requests.
- Include schema versions when the structure may evolve.
- Do not store secrets, live API keys, production PII, or proprietary datasets.
