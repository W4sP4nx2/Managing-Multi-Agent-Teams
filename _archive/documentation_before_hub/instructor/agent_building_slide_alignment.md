# Agent-building slide and exercise alignment

Updated **20 October 2026**. Use the [current 21-slide deck](../slides/managing_multi_agent_teams_workshop_v16.pptx), [README slide index](../README.md#main-deck-slide-index), [curriculum mind map](../slides/managing_multi_agent_teams_mindmap.md), and [design guide](../assignments/agent_building_design_guide.md) together.

## Content crosswalk

| Requested topic | Slides | Learner connection |
| --- | --- | --- |
| Agenda, starting with one agent, and what changes when agents act | 1–3, 8 | Preflight checkpoint: define the artifact, allowed actions, stopping condition, and reason for a helper. |
| Context engineering | 9–10 | Lab 1 checkpoint: choose the relevant task, rule/source, and output contract; distinguish schema validity from truth. |
| Main agent with general, computer-use, video, and cloud coding helpers | 11–12 | Lab 2 checkpoint: bound one helper's input, output, permissions, and return check. |
| Cheapest adequate capability and one dedicated human-interaction channel | 13 | Capstone checkpoint: compare context/model knowledge, API/connector, web search, desktop, and asking the human; ask early when the decision belongs to the user. |
| Stable tools, loading only when needed, and clear unavailability | 14–15 | Lab 3 checkpoint: distinguish stable interfaces from deferred loading and execution-time availability. |
| Description plus schema below 4,000 characters | 14 | Lab 3 checkpoint: apply the workshop design budget; do not present it as a universal API limit. |
| Dedicated state-saving tools and actionable errors | 15–16 | Lab 3 checkpoint: propose a versioned state receipt and a supported next action. The guide explains when `read` or `shell` is appropriate. |
| Four-branch curriculum mind map | 21 | Core Philosophy, the four-step roadmap, Enterprise DX & AX, and Strategic Framework connect the Capstone checkpoint and ADR to observed evidence and a next decision. |
| Inspector helpers and clean expected errors | 12, 15–16, 18 | Labs 2–3 and Capstone: inspect fixture state and check `safe_validate` results before use. Lab 2 adds the five-minute Blind Agent Debug exercise. |
| Agent-First tool documentation | 14 | Read Action, Input, Output, and Warning alongside scoped tool lists and executable input gates. |

## Assessment and scope

The required sequence remains preflight, three labs, and the Development-to-Security Capstone. Each notebook retains its formative design checkpoint. The 20 October update adds small DX helpers, clearer tool docstrings, selected state inspection, and the Lab 2 debug task. Learner TODOs and grading rules remain unchanged. Course marks remain three labs × 20, Capstone implementation /20, and ADR/defense /20.

General/computer-use/video/cloud helper patterns, tool discovery, user-interaction tools, and durable state tools are design proposals. The supplied notebooks continue to use local deterministic fixtures. The capability ladder is an adequacy heuristic, not a measured price ranking.

## 18 October verification (historical)

The records below describe the earlier design-discussion update. Its hash and checks do not validate later DX/AX or mind-map changes. Current runtime evidence comes from a fresh run of the [readiness gate](../DEVELOPMENT.md).

- The README's 21 numbered titles match the presentation order and slide page numbers.
- All 51 internal slide links resolve to the intended agenda, practice map, teaching stage, or lab section. Each slide has Agenda, Practice, and Index navigation.
- The final audit passed 403 local documentation/notebook links and anchors, the README image path, and 45 local targets in the deck. It covered the curriculum, design guide, instructor records, and slides README.
- All five notebooks passed structural validation; comparison with the pre-edit copies confirmed preserved code cells and code positions.
- Presentation package, layout, font policy, native-table arithmetic, and first-party re-import checks passed. Four estimated table-height warnings were reviewed in the rendered slides.
- Independent visual QA inspected all 21 slides individually using LibreOffice renders and found no clipping or overlap. Native PowerPoint rendering and viewer-specific hyperlink behavior were not tested.
- Runtime tests were not rerun for these Markdown and presentation changes. Earlier readiness results remain historical evidence for their recorded inputs.

18 October deck SHA256: `711699860a2f7852523fbc6547e1b411e0d55778b060a3b40ef8324ee9b770f6`.

[Teaching notes](teaching_notes.md) · [Assessment checklist](assessment_compliance_checklist.md) · [Learner paths](../README.md#learner-paths)
