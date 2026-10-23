# CrewAI orchestration: advanced reference

**Optional reference; no new graded lab, submission, or course marks.**

Use the [three-agent reference notebook](../crewai_learning/01_Bridge_Sequential_Crew.ipynb) after [Lab 2](../notebooks/02_lab_crewai.ipynb). It connects to [Lecture 8: Debugging and SDLC](assignment_08_debugging_sdlc.md) and [Assignment 09: Framework Comparison](assignment_09_framework_comparison.md).

The example uses Manager, Coder, and QA; all tasks have strict output validation. A Python wrapper permits at most three total kickoffs and returns a typed escalation after three failures. Model responses and QA evidence are local fixtures; the real CrewAI execution and validation boundaries run with external networking blocked.

Follow [setup and verification](../crewai_learning/SETUP_AND_LEARNING_EXPERIENCE.md), then inspect the invalid-output, repeated-failure, and early-success results. Explain why the wrapper owns the bound and why a role named Manager does not itself enforce a stop.

The former seven-agent research crew, six-week outline, and Homework G exercises are [archived](../_archive/crewai_learning/README.md). They are not additional promises or requirements of this focused reference.

[Exercise index](index.md) · [Course learner paths](../README.md#learner-paths)
