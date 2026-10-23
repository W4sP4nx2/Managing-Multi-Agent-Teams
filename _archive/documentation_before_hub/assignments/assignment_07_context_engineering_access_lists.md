# Assignment 07: Context Engineering and Access Lists

**Maps to:** Lecture 7 — Context Engineering and Access List Routing · **Type:** Formative, pass/fail

## Objective

Choose which prior artifacts each role may read, preserving useful evidence while excluding irrelevant or sensitive history.

## The Obsidian Vault analogy

Think of an **Obsidian Vault** as a folder of linked Markdown notes: project rules, approved requirements, decisions, and examples. A colleague can work in your preferred style by reading the relevant notes before starting. You do not retrain that colleague for every project; you supply the working context.

Context injection gives an agent the same kind of project-specific customization. Select the authorized notes for the current role and inject them into its task context. This can produce the *fine-tuned customization* learners want **without model training or changing model weights**. It is context engineering, not technical fine-tuning: behavior still depends on the supplied context, and irrelevant or stale notes can make it worse.

In [Lab 2](../notebooks/02_lab_crewai.ipynb), `team_log` is our tiny vault of approved rules and `architect_task` carries the selected brief. Setting `coder_task.context=[architect_task]` makes that brief available to the Coder. The notebook uses local Python data and does not install or connect to Obsidian. The deterministic fixture demonstrates the context dependency; it does not prove that a live model will follow every note. Use the access lists below to decide which notes each role should receive.

## Task

Use this task-artifact list:

| Artifact | Contents |
| --- | --- |
| `architect_spec` | Contract and acceptance rules for the task. |
| `approved_requirements` | Requirements confirmed by the Manager. |
| `coder_patch` | The Coder's proposed code change. |
| `acceptance_tests` | Checks QA must run against the contract. |
| `provider_secret` | A private API credential unrelated to the task. |
| `old_unrelated_log` | A previous task's stale output. |

Write a small access list for the **Coder** and **QA**. Choose the artifacts each role needs, then give one sentence explaining each role's view. Identify one artifact that must be excluded and explain why.

## Submit

- One role-specific access list for the Coder and one for QA.
- A brief reason for one inclusion and one exclusion.

## Pass/fail

- **Pass:** The Coder receives the specification and approved requirements; QA receives the patch and acceptance tests; secrets and stale unrelated output are excluded; the choices are explained.
- **Revise:** Either role lacks evidence needed for its task, or sensitive/unrelated data is included without justification.

This is a local reasoning exercise. It uses no Fugu service, external API, provider account, or live model call.
