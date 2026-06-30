import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const outPath = path.join(__dirname, "grading_rubrics.xlsx");
const previewPath = path.join(__dirname, "grading_rubrics_preview.png");

const assignments = [
  ["Assignment 01", "Agent Roster & SOPs", "Design", 100],
  ["Assignment 02", "Basic Agent Governance Labs", "Notebook/Code", 100],
  ["Assignment 03", "Type-Safe Handoffs", "Code", 100],
  ["Assignment 04", "Theory-of-Mind Memory", "Code/Design", 100],
  ["Assignment 05", "MCP Tool Governance", "Code", 100],
  ["Assignment 06", "RAG & MCP Architecture", "Design/Code", 100],
  ["Assignment 11", "Trust & Governance Matrix", "Design", 100],
  ["Assignment 12", "From Whisper to Shipped Code", "Build", 100],
  ["Assignment 13", "Virtual Software Company Capstone", "Build", 100],
  ["Homework A", "Specialist Agent Skills", "Advanced Build", 100],
  ["Homework B", "Production Controls", "Advanced Build", 100],
  ["Homework C", "Deployment & Operations", "Advanced Build", 100],
];

const rubricRows = [
  ["Assignment 01", "Schema and handoff clarity", 35, "Named artifacts and clear PM -> Coder -> QA -> Reviewer flow"],
  ["Assignment 01", "Tool governance and zero-trust reasoning", 35, "Least privilege tools and explicit denials"],
  ["Assignment 01", "Self-repair and alignment design", 30, "Bounded repair path and TeamLog-style commitment"],
  ["Assignment 02", "Schema and artifact contracts", 30, "Weather, draft, incident, plan, and commitment artifacts use strict Pydantic-style contracts"],
  ["Assignment 02", "Governance boundary enforcement", 35, "Gateway, retry budget, A2A perimeter, or TeamLog boundary blocks unsafe behavior"],
  ["Assignment 02", "Audit, repair, and escalation evidence", 25, "Denied, repaired, or escalated paths leave inspectable evidence"],
  ["Assignment 02", "Management explanation", 10, "Learner names the production failure each simple agent lab prevents"],
  ["Assignment 03", "Typed schema coverage", 35, "All handoffs use strict schemas rather than raw dictionaries"],
  ["Assignment 03", "Validation rejection evidence", 35, "Invalid enums, extra fields, or missing fields produce Pydantic errors"],
  ["Assignment 03", "Structured final report", 30, "Validated JSON output can be consumed by downstream agents"],
  ["Assignment 04", "Memory schema and access control", 35, "Visibility and sensitivity enforced before retrieval"],
  ["Assignment 04", "Theory-of-Mind retrieval behavior", 40, "Coder discovers hidden PM constraint through search"],
  ["Assignment 04", "Explanation and production reasoning", 25, "Connects memory to TeamLog and ToM"],
  ["Assignment 05", "Policy implementation", 40, "Allowed tools, trust tiers, and restricted data checks are enforced"],
  ["Assignment 05", "Denied audit evidence", 35, "Unauthorized calls are denied and logged with reasons"],
  ["Assignment 05", "Zero-trust explanation", 25, "Learner explains least privilege and external boundary risks"],
  ["Assignment 06", "Typed orchestration and routing", 40, "Agentic RAG/MCP architecture with clear contracts"],
  ["Assignment 06", "Security controls and MCP governance", 35, "Policy gate, tool scopes, threat mitigations"],
  ["Assignment 06", "Self-correction and test coverage", 25, "Evidence that invalid and unauthorized actions fail safely"],
  ["Assignment 11", "Zero-trust architecture completeness", 40, "Identity, trust tiers, denied paths, auditability"],
  ["Assignment 11", "Typed A2A and data governance", 35, "Schemas and classification for cross-org messages"],
  ["Assignment 11", "Threat analysis practicality", 25, "Specific mitigations for realistic risks"],
  ["Assignment 12", "Natural language to typed state", 20, "CEO prompt becomes ProjectPlan and TeamCommitment"],
  ["Assignment 12", "Dynamic scaffold quality", 20, "High-risk work inserts SecurityReviewer before release"],
  ["Assignment 12", "Debate and escalation behavior", 20, "Contention is structured and escalates when unresolved"],
  ["Assignment 12", "Mid-flight TeamLog pivot", 20, "Coder reads updated commitment rather than raw CEO text"],
  ["Assignment 12", "Human review and release evidence", 20, "Approval, rejection, and needs_changes paths are auditable"],
  ["Assignment 13", "Architecture and typed contracts", 30, "End-to-end graph and strict Pydantic artifacts"],
  ["Assignment 13", "Working implementation and test evidence", 30, "Runs, fails once, repairs, and ships or escalates"],
  ["Assignment 13", "Tool governance and zero-trust controls", 20, "Unauthorized tool and memory attempts are blocked"],
  ["Assignment 13", "Self-repair, routing, and memory quality", 15, "Bounded repair, route trace, useful failure memory"],
  ["Assignment 13", "PR summary clarity", 5, "Release artifact traces back to validated work"],
  ["Homework A", "Specialist schemas and typed outputs", 25, "Quality, test, security, and documentation agents emit strict artifacts"],
  ["Homework A", "Skill signal quality", 45, "Assessments and generated artifacts are useful, specific, and grounded in patches"],
  ["Homework A", "Failure and edge-case coverage", 20, "Strong, mediocre, unsafe, and edge-case examples are tested"],
  ["Homework A", "Production reasoning", 10, "Explains how skilled agents improve managed teams"],
  ["Homework B", "Human approval and safety gates", 25, "High-risk, high-cost, low-confidence, and restricted actions require approval"],
  ["Homework B", "Benchmark and evaluation rigor", 30, "Metrics compare configurations across accuracy, latency, cost, and hallucination rate"],
  ["Homework B", "Cost and memory lifecycle controls", 25, "Caching, budget enforcement, retrieval, and forgetting are implemented"],
  ["Homework B", "A2A OpenAPI contract quality", 15, "Network handoff uses strict OpenAPI schemas and API key security"],
  ["Homework B", "Auditability", 10, "Decisions are logged with enough evidence to debug"],
  ["Homework C", "Deployment packaging", 25, "Container/API/config separation is secure and runnable"],
  ["Homework C", "Observability quality", 30, "Logs, traces, metrics, and alerts expose workflow health"],
  ["Homework C", "Sandbox and security controls", 30, "Untrusted code execution is isolated, bounded, and typed"],
  ["Homework C", "Version control and rollback", 15, "Prompt/tool/model config versions can be compared and restored"],
];

const gradeRows = assignments.map(([id, title]) => [id, title, "", "", "", "", ""]);
const assignmentLastRow = assignments.length + 1;
const rubricLastRow = rubricRows.length + 1;

const workbook = Workbook.create();
const overview = workbook.worksheets.add("Overview");
const detailed = workbook.worksheets.add("Detailed Rubric");
const quick = workbook.worksheets.add("Quick Grade");

for (const sheet of [overview, detailed, quick]) {
  sheet.showGridLines = false;
}

overview.getRange("A1:D1").values = [["Assignment", "Focus", "Type", "Points"]];
overview.getRange(`A2:D${assignmentLastRow}`).values = assignments;
overview.getRange("A1:D1").format = { fill: "#111827", font: { bold: true, color: "#FFFFFF" } };
overview.getRange(`A1:D${assignmentLastRow}`).format.borders = { preset: "outside", style: "thin", color: "#CBD5E1" };
overview.getRange(`D2:D${assignmentLastRow}`).format.numberFormat = "0";
overview.getRange("A:D").format.autofitColumns();
overview.freezePanes.freezeRows(1);

detailed.getRange("A1:D1").values = [["Assignment", "Criterion", "Weight", "Excellent Evidence"]];
detailed.getRange(`A2:D${rubricLastRow}`).values = rubricRows;
detailed.getRange("A1:D1").format = { fill: "#0F766E", font: { bold: true, color: "#FFFFFF" } };
detailed.getRange(`A1:D${rubricLastRow}`).format.borders = { preset: "outside", style: "thin", color: "#CBD5E1" };
detailed.getRange(`C2:C${rubricLastRow}`).format.numberFormat = "0";
detailed.getRange("B:D").format.wrapText = true;
detailed.getRange("A:D").format.autofitColumns();
detailed.freezePanes.freezeRows(1);

quick.getRange("A1:G1").values = [["Assignment", "Focus", "Criterion 1", "Criterion 2", "Criterion 3+", "Total", "Notes"]];
quick.getRange(`A2:G${assignmentLastRow}`).values = gradeRows;
quick.getRange("F2").formulas = [["=SUM(C2:E2)"]];
quick.getRange(`F2:F${assignmentLastRow}`).fillDown();
quick.getRange("A1:G1").format = { fill: "#1D4ED8", font: { bold: true, color: "#FFFFFF" } };
quick.getRange(`A1:G${assignmentLastRow}`).format.borders = { preset: "outside", style: "thin", color: "#CBD5E1" };
quick.getRange(`C2:F${assignmentLastRow}`).format.numberFormat = "0";
quick.getRange(`G2:G${assignmentLastRow}`).format.wrapText = true;
quick.getRange("A:G").format.autofitColumns();
quick.freezePanes.freezeRows(1);
quick.getRange(`C2:E${assignmentLastRow}`).dataValidation = {
  rule: { type: "whole", operator: "between", formula1: 0, formula2: 100 },
};

const inspect = await workbook.inspect({
  kind: "sheet,table,formula",
  maxChars: 4000,
  tableMaxRows: 8,
  tableMaxCols: 7,
});
console.log(inspect.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

for (const sheetName of ["Overview", "Detailed Rubric", "Quick Grade"]) {
  const preview = await workbook.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
  const safeName = sheetName.toLowerCase().replaceAll(" ", "_");
  await fs.writeFile(path.join(__dirname, `grading_rubrics_${safeName}.png`), new Uint8Array(await preview.arrayBuffer()));
  if (sheetName === "Detailed Rubric") {
    await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));
  }
}

const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(outPath);
console.log(outPath);
