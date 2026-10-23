# Assessment files

| File | Use |
| --- | --- |
| [Grading rubric](grading_rubrics.xlsx) | Current five assessment components, notebook score branches, and a single-submission calculation sheet. |
| [Learner score tracker](assessment_score_tracker.xlsx) | Cohort record with raw lab scores, converted course marks, total, and grade. |
| [Assessment compliance checklist](assessment_compliance_checklist.md) | Release evidence and the scope of the automated checks. |
| [Capstone brief](../assignments/ex5_capstone_virtual_software_company.md) | Code criteria and the three-question ADR rubric. |
| [Paper ADR sheet](capstone_paper_adr_quick_sheet.md) and [print-ready PDF](../output/pdf/capstone_paper_adr_quick_sheet.pdf) | Accepted fallback with the same ADR rubric and 6/7/7 partial-credit anchors. |
| [Notebook solution guide](solutions/core_notebook_solution_guide.md) | Instructor repairs for the intentional broken starts. |

## Marks

| Component | Raw result | Course marks |
| --- | ---: | ---: |
| [Lab 1: Pydantic contract](../notebooks/01_lab_pydantic.ipynb) | /15 | /20 |
| [Lab 2: CrewAI team handoff](../notebooks/02_lab_crewai.ipynb) | /15 | /20 |
| [Lab 3: Tool gates and bounded repair](../notebooks/03_lab_security.ipynb) | /15 | /20 |
| [Capstone code](../notebooks/04_capstone.ipynb) | /20 | /20 |
| Capstone ADR and defense | /20 | /20 |
| **Total** | | **/100** |

Convert each lab with `raw score × 20 ÷ 15`. Keep the full precision in the tracker; formatting displays two decimals. Lecture exercises are formative and have no additional marks.

The Lab 1 and Lab 2 graders each award two independent controls worth 5 and 10 raw points, so the possible totals are 0, 5, 10, or 15. Lab 1 awards 5 for the inclusive confidence range and 10 for rejecting undeclared fields; both require the valid typed field shape. Lab 2 awards 5 for Manager permissions/delegation and 10 for the `architect_task` context dependency. The detailed rubric mirrors these allocations. Lab 2 does not measure a live Crew run or an executed TeamLog read. Lab 3 awards 4/3/3/3/2 raw points. Capstone code awards 5/10/5 and the ADR awards 6/7/7.

Enter raw results in the yellow tracker cells. Converted marks and totals calculate automatically. A missing component leaves the total and grade blank; an earned zero remains zero. Grade bands use the unrounded total: A at least 80, B at least 65 and below 80, C at least 50 and below 65, and F below 50.

Use the Paper ADR fallback according to the [playbook](../PLAYBOOK.md). Sound reasoning satisfies the fallback pass condition; it does not automatically earn full marks or fabricated code evidence. Enter the paper score in **ADR & defense /20**. If code could not be assessed, leave **Capstone code /20** blank, record the reason, and document any explicitly agreed accommodation separately. The tracker intentionally leaves the total blank until all five component marks are present.

The paper sheet divides the ADR rubric into 6 marks for risk and architecture, 7 for governance and evidence, and 7 for the next step. Each question has point allocations so instructors can award partial credit consistently.

## Rubric maintenance

The workbooks are stored in this `instructor/` directory.

The [rubric builder](build_grading_rubrics.mjs) regenerates `grading_rubrics.xlsx` and its previews with `@oai/artifact-tool`. It does not overwrite the cohort score tracker. Run it in a prepared artifact runtime, using `--output-dir` for a temporary review location before replacing the published rubric.

The [paper worksheet builder](../tools/build_paper_adr.py) regenerates the one-page A4 PDF using ReportLab. This is an instructor asset build step, separate from learner setup.
