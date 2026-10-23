# Assignment 09: Framework Comparison

**Advanced reference discussion — ungraded, no submission or new lab.** This label connects the existing framework discussion to the working CrewAI example. It does not add a tenth assessed competency or change course marks.

Use the [three-agent notebook](../crewai_learning/01_Bridge_Sequential_Crew.ipynb) with the [framework comparison](../resources/framework_comparison.md) and [Lecture 8](assignment_08_debugging_sdlc.md).

| Inspect | CrewAI provides | This application enforces |
| --- | --- | --- |
| Manager, Coder, QA | Named agents, tasks, role tool lists, and context dependencies | Which role owns each task and whether evidence permits approval |
| Typed handoffs | `output_pydantic` and callable task guardrails | Strict JSON validation with no model-repair fallback |
| Failure recovery | Agent/task retry features, configured off in this reference | Three total `crew.kickoff()` attempts, typed feedback, and escalation |
| Stop decision | Structured task outputs | No success without matching task IDs, current-patch QA evidence, and Manager approval |

The notebook uses a sequential process and a hierarchy of responsibilities. It does not claim to test native hierarchical delegation. Its local fixture LLMs make failures reproducible while real CrewAI task execution runs.

After observing the three-failure escalation and one-attempt success, discuss which responsibilities would remain yours if you moved to a Flow or LangGraph state graph. Use the existing comparison reference for framework capabilities; no additional framework installation or implementation is required.

[Reference setup](../crewai_learning/SETUP_AND_LEARNING_EXPERIENCE.md) · [Exercise index](index.md) · [Learner paths](../README.md#learner-paths)
