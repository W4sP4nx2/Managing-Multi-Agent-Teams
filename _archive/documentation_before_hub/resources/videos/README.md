# 🎬 Video Index

> [!WARNING]
> **No `.mp4` files are stored in this repository.**
> Videos are hosted externally to ensure fast cloning and low repository bloat.
> This folder contains **Markdown transcripts**, **chapter timestamps**, and **key takeaways** for each video, allowing learners to search course content through GitHub search.

## Video Format Standard

Every video must have a corresponding `.md` file named `[module]_[topic].md`.

Example: `mod3_mcp_gateway_walkthrough.md`

```markdown
# Module 3: MCP Gateway Walkthrough

- **External Link:** [YouTube / Loom URL]
- **Duration:** 12:45

## ⏱️ Timestamps

- 00:00 - The Naive Approach: why raw tool calls fail
- 02:30 - Introducing the ToolPolicy schema
- 06:15 - Live demo: blocking the external vendor
- 10:00 - Audit logging and observability

## 🧠 Key Takeaways

1. The MCP Gateway is the customs border of your AI workforce.
2. Never trust the `role` string; always verify the `AgentIdentity` and `TrustTier`.
3. Audit logs are not decoration; they are the evidence trail.
```

## Current Video Notes

| File | Module | Purpose |
| :--- | :--- | :--- |
| [`tom_deep_dive_transcript.md`](./tom_deep_dive_transcript.md) | Module 2 | Placeholder transcript and timestamp plan for Theory-of-Mind memory. |
