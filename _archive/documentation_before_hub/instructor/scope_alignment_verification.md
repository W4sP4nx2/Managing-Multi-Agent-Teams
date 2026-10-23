# Scope Alignment Verification

Last updated: 2026-10-18

## Deliverable scope

The two-day workshop teaches learners to manage **two cooperating multi-agent teams** through one typed boundary:

- **Development Team:** Engineering Manager, Coder, and QA Auditor.
- **Security & Compliance Team:** Security Manager and Pen Tester.
- **Inter-team handoff:** the Development Team's `DevDeliverable` is validated by Pydantic before the Security Team consumes it. The Security Team returns a typed `SecurityAuditResult`.

This is an intra-workshop inter-team handoff. Cross-organization A2A transport is advanced material archived under `_archive/advanced_scaling/` and is not part of the core learner path.

## Required learner path

| Step | Core asset | Required evidence |
| --- | --- | --- |
| 1. The Contract | `notebooks/01_lab_pydantic.ipynb` | Bad mock output is rejected; valid data is accepted; grader reports up to 15 raw points. |
| 2. The Team | `notebooks/02_lab_crewai.ipynb` | CrewAI Development Team roles and tools are separated; TeamLog shows the Coder read the Architect rules; typed `CodePatch` reaches QA. |
| 3. The Guardrails | `notebooks/03_lab_security.ipynb` | Malicious input is rejected; repair stops at three retries and escalates. |
| 4. The Delivery | `notebooks/04_capstone.ipynb` | Validated `DevDeliverable` starts the Security Team and yields a typed audit result; learners inspect a pre-written, ungraded cost-aware routing helper. |

The score model is three labs × 20 marks after converting each raw `/15` grader, plus Capstone code `/20` and ADR/defense `/20`, for `/100` total. The routing helper is a reference example and carries no marks.

## Academic framing

Theory of Mind and TeamLog explain role-specific context and shared commitments. TRINITY, Conductor, ChatDev, and Reflexion inform the discussion of worker/verifier feedback and bounded repair. The deck labels access-list routing as a local Fugu-style pattern, not a hosted routing API. Cost-aware dynamic routing is a pre-written local policy in the Capstone, with illustrative costs and no coding task or grade. The sources are linked in the [README](../README.md) and [Playbook](../PLAYBOOK.md).

## Verification record and earlier rehearsal notes

Use the [assessment compliance checklist](assessment_compliance_checklist.md) for current command output, environment, and release results. The older deck and installation notes below are dated snapshots, not proof that the current dependency profile or handouts have passed. Do not carry their counts into a new release.

| Check | Current evidence |
| --- | --- |
| Repository tests | Record the latest `python tools/check_readiness.py` result in the [compliance checklist](assessment_compliance_checklist.md); historical test counts do not verify the current files. |
| Three grader sabotage runs | Rehearse Lab 1 0/5/15, Lab 2 0/5/10/15, and Lab 3 0/7/8/15. Record the current gate result in the [compliance checklist](assessment_compliance_checklist.md). |
| Required notebook execution | The current gate must execute all five Golden Path notebooks with credentials removed and external connections blocked. Retain the current kernel results in the [compliance checklist](assessment_compliance_checklist.md). |
| Automatic Development-to-Security transition | `tests/test_ex5_capstone.py` exercises local adapters and contract validation before Security starts. `tests/test_capstone_bridge.py` now checks the separate structured-output bonus with a fake SDK; it does not execute Crews. |
| Notebook handout outputs | Clear outputs and execution counts across all `.ipynb` files, including extensions and archives, then inspect the current JSON audit; old notebook counts are not a release check. |
| Historical v14 deck review | **Superseded:** the prior v14 review documented its 14-slide count, framework comparison on slide 10, and terminology correction on slide 13. Those notes apply to the prior file. |
| Historical v15 deck count and teaching-design review | **Superseded:** the 2026-10-17 review of the pre-navigation v15 snapshot recorded 14 slides. Slide 1 opens with the Vibe Coding vs. Governed Engineering comparison; slide 5 uses the Knowledge, Drafting, and Compliance roles, Pydantic citation contract, and instructor no-source escalation reveal; slide 6 shows Code `/20` + ADR `/20`. Teaching-design edits add learner prediction, decisions, evidence checks, reflection, transfer, and a transparent `/15` to `/20` assessment conversion. Updated slides were rendered and reviewed; independent QA rechecked slides 1, 4–6, 8, 9, 12, and 14 with no visible fit issues or collisions. Slides 2, 10, and 13 are unchanged from v14. SHA256: `d475a7d307da7b7dbb47ac3e1638952acd63e1e06615f1d65def71f9b9cef110`. |
| Active v16 deck and curriculum alignment | **Pass (2026-10-18):** the current 21-slide deck adds the agenda, one-agent starting point, working brief, specialist helpers, capability choice, stable tools, state/error design, and final takeaways. README titles match the deck; all 51 internal slide links and 360 scoped local documentation/notebook links passed. Five new formative Markdown checkpoints preserve notebook code and marks. Independent visual QA reviewed all slides. See the [alignment record](agent_building_slide_alignment.md) for the final hash and validation boundaries. |
| Earlier learner setup rehearsal | A prior dependency profile installed on this Mac in 85 seconds using Python 3.12.3, and JupyterLab launched. Rehearse the current four-command setup in a fresh `.venv` and record elapsed time; that earlier result does not verify today's profile. |
| Offline execution | The current gate removes provider credentials and blocks external connections while running required notebook scenarios. Initial package installation needs internet or a prepared bundle. |
| Grade arithmetic | **Pass:** tracker scales the three raw `/15` lab scores to `/20`, requires all five scored components for a total, and caps the course at `/100`. A maximum-score sample recalculated to 100/A with no formula errors. |
| Course sitemap | The [interactive syllabus](../README.md#interactive-syllabus-nine-un-mandated-lectures) links nine lectures to five Golden Path notebooks and eight briefs. The separate bonus is scheduled at the end of Day 2; optional study and archives add no core work or marks. |
| NIST/CISA alignment | **Pass (conceptual):** Playbook maps Lab 2 to AC-5/AC-6, Lab 3 to SI-10, and links joint CISA/NCSC secure-AI lifecycle guidance; it makes no certification claim. |

## Scope controls

- Core materials stay within a two-day delivery, three required labs, and one two-team Capstone.
- The Capstone routing helper stays pre-written, deterministic, and ungraded.
- FastAPI/HTTPX, LangGraph, and provider SDKs remain optional extension dependencies.
- Groq is not required for Jupyter, the labs, repository checks, or deterministic Capstone execution.
- The Paper ADR is an accepted Capstone pass route, graded with the stated rubric; it does not guarantee full marks.
