import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const instructorDir = path.dirname(fileURLToPath(import.meta.url));
const arg = process.argv.indexOf("--output-dir");
const outputDir = arg < 0 ? instructorDir : path.resolve(process.argv[arg + 1]);

// Formative lecture exercises and optional extensions do not add marks.
const components = [
  ["Lab 1", "Pydantic contracts", 15, 20],
  ["Lab 2", "CrewAI team handoff", 15, 20],
  ["Lab 3", "Tool gates and bounded repair", 15, 20],
  ["Capstone code", "Development-to-Security pipeline", 20, 20],
  ["Capstone ADR", "Risk, governance, and next step", 20, 20],
];

// Labs 1 and 2 each award separate five- and ten-point controls.
const rubricRows = [
  ["Lab 1", "Inclusive confidence range", "5 / 15", "Required typed fields and valid input pass; endpoints 0 and 1 pass; negative and 150.5 fail."],
  ["Lab 1", "Undeclared fields rejected", "10 / 15", "Required typed fields and valid input pass; the secret_backdoor extra field fails."],
  ["Lab 1", "Combined outcomes", "0, 5, 10, 15", "Neither control = 0; range only = 5; extras only = 10; both = 15. Invalid required shape = 0."],
  ["Lab 2", "Manager permissions", "5 / 15", "Manager has only approve_code_tool and delegation enabled."],
  ["Lab 2", "Architect context", "10 / 15", "Coder task context includes the actual architect_task object."],
  ["Lab 2", "Combined outcomes", "0, 5, 10, 15", "Neither control = 0; Manager only = 5; context only = 10; both = 15."],
  ["Lab 3", "Hostile input blocked", "4 / 15", "The supplied SQL-like payload is rejected before the dry-run tool."],
  ["Lab 3", "Safe input accepted", "3 / 15", "Numeric ID accepted; this credit requires the hostile-input gate to pass."],
  ["Lab 3", "Retry configuration", "3 / 15", "MAX_RETRIES is exactly 3."],
  ["Lab 3", "Termination and escalation", "3 / 15", "Initial attempt plus three retries ends after four calls with escalation."],
  ["Lab 3", "Mock budget bound", "2 / 15", "Simulated cost stops with the bounded loop."],
  ["Capstone code", "Separation of duties", "5 / 20", "Security Manager has approval only; Pen Tester has scan access only."],
  ["Capstone code", "Contract and Coordinator", "10 / 20", "Failed QA is rejected and validation is logged before Security starts."],
  ["Capstone code", "Typed audit result", "5 / 20", "The deterministic pipeline returns SecurityAuditResult."],
  ["Capstone ADR", "Risk and architecture", "6 / 20", "Identifies a concrete handoff risk and explains the two-team boundary."],
  ["Capstone ADR", "Governance and evidence", "7 / 20", "Connects contract, Coordinator gate, tool limits, and evidence."],
  ["Capstone ADR", "Next-step judgment", "7 / 20", "Names a credible production improvement and explains its value."],
];

const workbook = Workbook.create();
const overview = workbook.worksheets.add("Overview");
const detailed = workbook.worksheets.add("Detailed Rubric");
const quick = workbook.worksheets.add("Quick Grade");
function sheetStyle(sheet, range, header, color) {
  sheet.showGridLines = false;
  sheet.getRange(range).format.font = { name: "Arial", size: 11, color: "#111827" };
  sheet.getRange(range).format.verticalAlignment = "center";
  sheet.getRange(header).format = { fill: color, font: { name: "Arial", size: 11, bold: true, color: "#FFFFFF" }, horizontalAlignment: "center", verticalAlignment: "center", wrapText: true, rowHeight: 30 };
}
overview.getRange("A1:D1").values = [["Component", "Assessment", "Raw maximum", "Course marks"]];
overview.getRange("A2:D6").values = components;
overview.getRange("A7").values = [["Course total"]];
overview.getRange("D7").formulas = [["=SUM(D2:D6)"]];
overview.getRange("A9").values = [["Lab conversion: raw score × course maximum ÷ raw maximum."]];
overview.getRange("A10").values = [["Record each learner in assessment_score_tracker.xlsx."]];
overview.getRange("A11").values = [["Lecture exercises are formative and add no separate marks."]];
overview.getRange("A12").values = [["Sources: notebooks 01–04 and assignments/ex5_capstone_virtual_software_company.md."]];
sheetStyle(overview, "A1:D12", "A1:D1", "#111827");
overview.getRange("A:A").format.columnWidth = 22;
overview.getRange("B:B").format.columnWidth = 46;
overview.getRange("C:D").format.columnWidth = 19;
overview.getRange("A2:D7").format.rowHeight = 27;
overview.getRange("C2:D7").format.numberFormat = "0";
overview.getRange("A7:D7").format = { fill: "#E2E8F0", font: { bold: true } };
detailed.getRange("A1:D1").values = [["Component", "Criterion or score branch", "Raw points", "Evidence"]];
detailed.getRange(`A2:D${rubricRows.length + 1}`).values = rubricRows;
sheetStyle(detailed, `A1:D${rubricRows.length + 1}`, "A1:D1", "#0F766E");
detailed.getRange("A:A").format.columnWidth = 22;
detailed.getRange("B:B").format.columnWidth = 32;
detailed.getRange("C:C").format.columnWidth = 16;
detailed.getRange("D:D").format.columnWidth = 88;
detailed.getRange(`A2:D${rubricRows.length + 1}`).format.rowHeight = 36;
detailed.getRange(`B2:D${rubricRows.length + 1}`).format.wrapText = true;
detailed.freezePanes.freezeRows(1);
quick.getRange("A1:G1").values = [["Component", "Raw score", "Raw maximum", "Course maximum", "Course marks", "Assessor", "Comments"]];
quick.getRange("A2:G6").values = components.map(([name, , raw, marks]) => [name, null, raw, marks, null, null, null]);
for (let row = 2; row <= 6; row++) {
  quick.getRange(`E${row}`).formulas = [[`=IF(ISNUMBER(B${row}),B${row}*D${row}/C${row},"")`]];
  quick.getRange(`B${row}`).dataValidation = { rule: { type: "whole", operator: "between", formula1: 0, formula2: row <= 4 ? 15 : 20 } };
}
quick.getRange("A7").values = [["Total /100"]];
quick.getRange("E7").formulas = [["=IF(COUNT(B2:B6)<5,\"\",SUM(E2:E6))"]];
quick.getRange("A9").values = [["Enter the notebook raw scores. Yellow cells are editable."]];
quick.getRange("A10").values = [["ADR is assessed using the 6/7/7 rubric. Paper fallback uses the same rubric."]];
sheetStyle(quick, "A1:G10", "A1:G1", "#1D4ED8");
quick.getRange("A:A").format.columnWidth = 22;
quick.getRange("B:E").format.columnWidth = 19;
quick.getRange("F:F").format.columnWidth = 24;
quick.getRange("G:G").format.columnWidth = 45;
quick.getRange("A2:G7").format.rowHeight = 27;
quick.getRange("B2:B6").format.fill = "#FFF2CC";
quick.getRange("F2:G6").format.fill = "#FFF2CC";
quick.getRange("E2:E6").format.fill = "#EDF2F7";
quick.getRange("B2:D6").format.numberFormat = "0";
quick.getRange("E2:E7").format.numberFormat = "0.00";
quick.getRange("A7:G7").format = { fill: "#E2E8F0", font: { bold: true } };

// Change inputs to verify calculation, then restore the empty marking form.
for (const [raw, expected] of [[[15,15,15,20,20],100],[[5,5,7,10,10],42.666666666666664],[[0,0,0,0,0],0]]) {
  quick.getRange("B2:B6").values = raw.map(value => [value]);
  workbook.recalculate();
  const actual = quick.getRange("E7").values[0][0];
  if (typeof actual !== "number" || Math.abs(actual - expected) > 1e-8) throw new Error(`Score conversion failed: ${actual} != ${expected}`);
}
quick.getRange("B2:B6").clear({ applyTo: "contents" });
workbook.recalculate();
if (quick.getRange("E7").values[0][0] !== "") throw new Error("Incomplete grade must remain blank");
await fs.mkdir(outputDir, { recursive: true });
for (const sheet of [overview, detailed, quick]) {
  const preview = await workbook.render({ sheetName: sheet.name, autoCrop: "all", scale: 1, format: "png" });
  const safeName = sheet.name.toLowerCase().replaceAll(" ", "_");
  await fs.writeFile(path.join(outputDir, `grading_rubrics_${safeName}.png`), new Uint8Array(await preview.arrayBuffer()));
  if (sheet === detailed) await fs.writeFile(path.join(outputDir, "grading_rubrics_preview.png"), new Uint8Array(await preview.arrayBuffer()));
}
const errors = await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options: { useRegex: true, maxResults: 30 }, summary: "formula error scan" });
const inspect = await workbook.inspect({ kind: "sheet,formula", maxChars: 5000 });
await fs.writeFile(path.join(outputDir, "grading_rubrics.xlsx.inspect.ndjson"), inspect.ndjson + "\n" + errors.ndjson);
await (await SpreadsheetFile.exportXlsx(workbook)).save(path.join(outputDir, "grading_rubrics.xlsx"));
console.log(JSON.stringify({ output: path.join(outputDir, "grading_rubrics.xlsx"), conversionChecks: "max=100; partial=42.6667; zero=0; missing=blank", errors: errors.ndjson }));
