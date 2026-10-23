# Capstone Paper ADR - Offline Fallback

Use this one-page worksheet when a learner cannot run the Capstone because of a device, package, power, or connectivity failure. No code execution is required. The learner may write by hand or type short answers. [Open the print-ready A4 PDF](../output/pdf/capstone_paper_adr_quick_sheet.pdf).

**Learner:** ______________________________  **Date:** ______________  **Case:** ______________________________

## Three questions

1. **Contract and architecture - 6 marks**  
   What risk does the Development-to-Security boundary address? Name the `DevDeliverable` fields and sketch how the Coordinator validates the handoff before Security starts.

   ____________________________________________________________________________________

   ____________________________________________________________________________________

   ____________________________________________________________________________________

2. **Governance and evidence - 7 marks**  
   Which tools may the Manager, Coder, QA, Pen Tester, and Security Manager roles use? What test or audit evidence would show that the handoff and role boundaries held? Label evidence as observed or proposed.

   ____________________________________________________________________________________

   ____________________________________________________________________________________

   ____________________________________________________________________________________

3. **Production next step - 7 marks**  
   What is the largest remaining risk, what concrete control would you add before production, and how would you check that the control works?

   ____________________________________________________________________________________

   ____________________________________________________________________________________

   ____________________________________________________________________________________

## Score

| Criterion | Marks |
| --- | ---: |
| Risk and architecture | ____ / 6 |
| Governance mapping and proof | ____ / 7 |
| Production next step | ____ / 7 |
| **Total** | **____ / 20** |

A sound, evidence-based ADR satisfies the Capstone fallback pass condition. Score the same 20-point rubric; the paper option is not an automatic full-mark award.

## Instructor scoring anchors

Award points for the quality of each explanation, including partial credit within each allocation.

| Question | Point allocations |
| --- | --- |
| 1 - Contract and architecture | Concrete handoff risk (2); correct `DevDeliverable` fields and validation rule (2); explains Development, Coordinator, and Security boundaries (2). |
| 2 - Governance and evidence | Development role/tool separation (2); Pen Tester scan access and Security Manager approval separation (2); suitable contract rejection and ordered audit evidence (2); distinguishes observed from proposed evidence (1). |
| 3 - Production next step | Specific remaining risk (2); control that addresses that risk with a credible rationale (3); practical verification or acceptance check (2). |

Expected contract fields are `code_snippet`, `unit_tests_passed`, and `dev_team_signature`. A failed QA result must stop the handoff before Security starts. A diagram or pseudo-code can express the boundary.

Record this sheet's score in **ADR & defense /20**. It awards ADR marks only. The fallback may satisfy the accepted Capstone pass route, but it does not create code execution evidence or code marks. If code could not be assessed, leave its score blank and record the reason or an explicitly agreed accommodation separately. The tracker leaves the course total blank while a required mark is missing.
