---
marp: true
size: 16:9
paginate: true
theme: default
style: |
  section {
    background: #F8F9FA;
    color: #1E1E24;
    font-family: Arial, sans-serif;
    font-size: 28px;
    padding: 60px 72px;
  }
  h1 { font-size: 44px; line-height: 1.12; margin: 0 0 36px; }
  h2 { font-size: 34px; color: #0066FF; margin: 0 0 32px; }
  p { margin: 20px 0; }
  li { margin: 18px 0; }
  pre, code { font-family: Arial, sans-serif; background: transparent; color: #1E1E24; }
  pre { font-size: 26px; border: 1px solid #0066FF; padding: 22px; }
  pre:has(code.language-flow) { font-size: 28px; color: #0066FF; text-align: center; border: 0; padding: 24px 0; }
  section.contract { display: grid; grid-template-columns: 1.1fr 1fr; grid-template-rows: auto auto 1fr; column-gap: 48px; align-content: start; }
  section.contract h1, section.contract pre:first-of-type { grid-column: 1 / -1; }
  section.contract pre:nth-of-type(2) { grid-column: 1; align-self: start; margin: 16px 0; }
  section.contract ul { grid-column: 2; align-self: start; margin-top: 20px; padding-left: 1.2em; }
  section::after { color: #1E1E24; font-size: 16px; }
---

<!-- layout: cover -->
<!-- sources: ../README.md#golden-path; ../COURSE_MAP.md#seven-notebook-order -->

# Managing Multi-AI Teams:
## Orchestration to Production

Core stack: Python 3.12 · Pydantic · CrewAI · JupyterLab

```flow
Contracts → Roles → Gates → Evidence
```

Local fixtures · No LLM or reasoning-model calls · API cost $0.00

---

<!-- layout: flow-bullets -->
<!-- sources: ../notebooks/02_lab_crewai.ipynb; ../notebooks/03_lab_security.ipynb; ../notebooks/04_capstone.ipynb -->

# Architecture & Interaction Patterns

```flow
Roles → Rules → Handoffs → Evidence
```

- Roles assign work; rules gate actions; topology routes evidence.
- Compare independent, peer, centralized, and hybrid paths in Lab 2.
- Bound attempts; stop or repair using explicit failure evidence.

---

<!-- layout: contract -->
<!-- _class: contract -->
<!-- sources: ../notebooks/04_capstone.ipynb; ../ASSIGNMENTS.md#ex5-capstone-virtual-software-company -->

# Agent-to-Agent (A2A) Contract Handoffs

```flow
Development → Validate → Security
```

```python
DevDeliverable:
    code_snippet: str
    unit_tests_passed: bool
    dev_team_signature: str
```

- Reject malformed output and failed QA.
- Scoped memory; typed local API.
- Return SecurityAuditResult.

---

<!-- layout: review -->
<!-- sources: ../notebooks/02_lab_crewai.ipynb; ../ASSIGNMENTS.md#assignment-04-code-auditing; ../crewai_learning/01_Bridge_Sequential_Crew.ipynb -->

# Hands-On Lab: Code Review Pipeline

```oversight
Engineering Manager (oversight)
Coder | QA Auditor
```

- Remove Manager writing access and add architect_task to Coder context.
- Audit the typed patch; admit valid output to qa_inbox.
- Optional bridge: create a Crew, run kickoff, display Markdown.

---

<!-- layout: flow-bullets -->
<!-- sources: ../README.md#submission-checklist; ../ASSIGNMENTS.md#ex5-capstone-virtual-software-company; ../extensions/live_software_factory.md -->

# Hands-On Lab & Homework Deliverable

```flow
00 Preflight → 01–03 Labs → 04–06 Delivery
```

- Portfolio: three repaired labs + Capstone + ADR with interaction map.
- Factory / CI/CD: candidate revision + checks + gate decisions.
- Prove malfunction, conflicting evidence, stale state, and bounded repair.

---

<!-- layout: logistics -->
<!-- sources: ../SETUP.md; ../README.md#runtime-and-assessment; ../notebook_manifest.yml -->

# Environment & Execution Logistics

- Local: Python 3.12 + Git + JupyterLab at repository root.
- Git sync + dependency install before class; cloud setup is not supplied.
- Evaluation: 3 labs × 20 + Capstone 20 + ADR/defense 20 = 100.

Offline after setup · Existing dependencies · Assessment unchanged
