#!/usr/bin/env node
/** Build the editable six-slide deck and PDF from the authoritative Marp source.
 * Run with the bundled Node runtime and CODEX_RUNTIME_NODE_MODULES set to its
 * node_modules directory. Optional: --build-dir DIR --output-pptx FILE --output-pdf FILE.
 */
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { spawnSync } from "node:child_process";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const runtime = process.env.CODEX_RUNTIME_NODE_MODULES;
if (!runtime) throw new Error("Set CODEX_RUNTIME_NODE_MODULES to the bundled runtime node_modules directory.");
// The skill's first-party import validator runs a subprocess using this name.
process.env.RUNTIME_NODE_MODULES ??= runtime;
const runtimePython = process.env.CODEX_RUNTIME_PYTHON;
if (!runtimePython) throw new Error("Set CODEX_RUNTIME_PYTHON to the bundled Python executable.");
const skill = process.env.CODEX_PRESENTATIONS_SKILL_DIR;
if (!skill) throw new Error("Set CODEX_PRESENTATIONS_SKILL_DIR to the installed presentations skill directory.");
const arg = (name, fallback) => {
  const i = process.argv.indexOf(name);
  if (i < 0) return fallback;
  if (!process.argv[i + 1]) throw new Error(`Missing value for ${name}`);
  return path.resolve(process.argv[i + 1]);
};
const buildDir = arg("--build-dir", path.join(root, ".test-results/compact-deck"));
const finalPptx = arg("--output-pptx", path.join(root, "slides/managing_multi_agent_teams_6_slides.pptx"));
const finalPdf = arg("--output-pdf", path.join(root, "pdf/managing_multi_agent_teams_6_slides.pdf"));
const source = path.join(root, "slides/managing_multi_agent_teams_6_slides.md");
await fs.mkdir(buildDir, { recursive: true });
await fs.mkdir(path.dirname(finalPptx), { recursive: true });
await fs.mkdir(path.dirname(finalPdf), { recursive: true });
const moduleLink = path.join(buildDir, "node_modules");
try { await fs.symlink(runtime, moduleLink, "dir"); }
catch (error) { if (error.code !== "EEXIST") throw error; }
const { Presentation, PresentationFile } = await import(pathToFileURL(path.join(runtime, "@oai/artifact-tool/dist/artifact_tool.mjs")).href);
const { finalizePresentation, makeNativeBulletParagraphs, resolvePresentationFont } = await import(pathToFileURL(path.join(skill, "container_tools/artifact_tool_utils.mjs")).href);
const font = resolvePresentationFont({ fontFamily: "Arial" });
const markdown = await fs.readFile(source, "utf8");
const body = markdown.replace(/^---\n[\s\S]*?\n---\n/, "").trim();
const slides = body.split(/\n---\n/).map(block => {
  const layout = block.match(/<!-- layout: (.*?) -->/)?.[1];
  const sources = block.match(/<!-- sources: (.*?) -->/)?.[1].split("; ") ?? [];
  const title = block.match(/^# (.+)$/m)?.[1];
  const subtitle = block.match(/^## (.+)$/m)?.[1];
  const flow = block.match(/```flow\n([\s\S]*?)\n```/)?.[1].split(" → ");
  const oversight = block.match(/```oversight\n([\s\S]*?)\n```/)?.[1].split("\n");
  const code = block.match(/```python\n([\s\S]*?)\n```/)?.[1];
  const bullets = [...block.matchAll(/^- (.+)$/gm)].map(match => match[1]);
  const prose = block.replace(/<!--[\s\S]*?-->/g, "").replace(/```[\s\S]*?```/g, "")
    .split("\n").map(line => line.trim()).filter(line => line && !line.startsWith("#") && !line.startsWith("- "));
  if (!title || !layout || bullets.length > 3) throw new Error("Slide source violates the six-slide content contract.");
  return { layout, sources, title, subtitle, flow, oversight, code, bullets, prose };
});
if (slides.length !== 6) throw new Error(`Expected six slides; found ${slides.length}`);
const palette = { ink: "#1E1E24", paper: "#F8F9FA", blue: "#0066FF" };
const presentation = Presentation.create({ slideSize: { width: 1280, height: 720 } });
function text(slide, value, x, y, w, h, size = 28, options = {}) {
  const shape = slide.shapes.add({ geometry: "textbox", name: options.name ?? value.slice(0, 45),
    position: { left: x, top: y, width: w, height: h }, fill: "none",
    line: { fill: "none", width: 0 } });
  shape.text = value;
  shape.text.style = { typeface: font, fontSize: size, color: options.color ?? palette.ink,
    bold: options.bold ?? false, alignment: options.align ?? "left", verticalAlignment: "top",
    insets: 0, autoFit: "none", wrap: "square" };
  return shape;
}
function bulletList(slide, items, x, y, w, h, size = 28) {
  const shape = text(slide, "", x, y, w, h, size, { name: "Key points" });
  shape.text = makeNativeBulletParagraphs(items, { marginLeftPoints: 18, hangingPoints: 9, spaceAfterPoints: 22 });
  shape.text.style = { typeface: font, fontSize: size, color: palette.ink, insets: 0, autoFit: "none" };
  return shape;
}
function flow(slide, labels, y, nodeWidth, fontSize = 28) {
  const gap = labels.length === 4 ? 42 : 68;
  const total = labels.length * nodeWidth + (labels.length - 1) * gap;
  const left = (1280 - total) / 2;
  const nodes = labels.map((label, index) => {
    const shape = slide.shapes.add({ geometry: "rect", name: label,
      position: { left: left + index * (nodeWidth + gap), top: y, width: nodeWidth, height: 88 },
      fill: palette.paper, line: { fill: palette.blue, width: 1.5 } });
    shape.text = label;
    shape.text.style = { typeface: font, fontSize, bold: true, color: palette.blue,
      alignment: "center", verticalAlignment: "middle", insets: 10, autoFit: "none" };
    return shape;
  });
  for (let i = 0; i < nodes.length - 1; i++) slide.shapes.connect(nodes[i], nodes[i + 1], {
    kind: "straight", fromSide: "right", toSide: "left",
    line: { fill: palette.blue, width: 2 }, tail: { type: "arrow", width: "med", length: "med" },
  });
}
function oversight(slide, lines) {
  const addRole = (label, x, y, w) => {
    const shape = slide.shapes.add({ geometry: "rect", name: label,
      position: { left: x, top: y, width: w, height: 64 },
      fill: palette.paper, line: { fill: palette.blue, width: 1.5 } });
    shape.text = label;
    shape.text.style = { typeface: font, fontSize: 27, bold: true, color: palette.blue,
      alignment: "center", verticalAlignment: "middle", insets: 8, autoFit: "none" };
    return shape;
  };
  const manager = addRole(lines[0], 390, 178, 500);
  const [coderLabel, qaLabel] = lines[1].split(" | ");
  const coder = addRole(coderLabel, 150, 294, 340);
  const qa = addRole(qaLabel, 790, 294, 340);
  for (const target of [coder, qa]) slide.shapes.connect(manager, target, {
    kind: "elbow", fromSide: "bottom", toSide: "top",
    line: { fill: palette.blue, width: 2 }, tail: { type: "arrow", width: "med", length: "med" },
  });
}
for (const [index, data] of slides.entries()) {
  const slide = presentation.slides.add();
  slide.background.fill = palette.paper;
  if (data.layout === "cover") {
    text(slide, data.title, 72, 72, 1136, 84, 56, { bold: true });
    text(slide, data.subtitle, 72, 166, 1136, 64, 46, { bold: true, color: palette.blue });
    text(slide, data.prose[0], 72, 285, 1136, 48, 28);
    flow(slide, data.flow, 390, 236, 28);
    text(slide, data.prose[1], 72, 570, 1136, 56, 26);
  } else {
    const longTitle = data.layout === "contract";
    text(slide, data.title, 72, 56, 1136, longTitle ? 118 : 100, 44, { bold: true });
    if (data.layout === "contract") {
      flow(slide, data.flow, 210, 310, 28);
      text(slide, data.code, 72, 365, 595, 225, 28);
      bulletList(slide, data.bullets, 735, 365, 470, 270, 28);
    } else if (data.layout === "review") {
      oversight(slide, data.oversight);
      bulletList(slide, data.bullets, 72, 414, 1110, 238, 29);
    } else if (data.layout === "logistics") {
      bulletList(slide, data.bullets, 72, 215, 1110, 340, 30);
      text(slide, data.prose[0], 72, 590, 1136, 48, 26, { color: palette.blue });
    } else {
      flow(slide, data.flow, 205, data.flow.length === 4 ? 236 : 310, data.title.includes("Homework") ? 27 : 28);
      bulletList(slide, data.bullets, 72, 365, 1110, 266, 30);
    }
  }
  text(slide, String(index + 1), 1160, 660, 48, 24, 16, { align: "right" });
  slide.speakerNotes.text = "Sources (repository paths relative to slides/):\n" + data.sources.join("\n") +
    (index === 2 ? "\nA2A here means the local typed Development-to-Security handoff; no network A2A transport is exercised." : "") +
    (index === 3 ? "\nThe diagram shows the configured three-role design. The required local fixture validates the patch and fills qa_inbox; the QA task is not run." : "");
}
const candidate = path.join(buildDir, "candidate.pptx");
await (await PresentationFile.exportPptx(presentation)).save(candidate);
for (const [index, slide] of presentation.slides.items.entries()) {
  const stem = `slide-${index + 1}`;
  const png = await presentation.export({ slide, format: "png", scale: 1.5 });
  await fs.writeFile(path.join(buildDir, `${stem}.png`), new Uint8Array(await png.arrayBuffer()));
  const layout = await slide.export({ format: "layout" });
  await fs.writeFile(path.join(buildDir, `${stem}.layout.json`), await layout.text());
}
// Finalize to a fresh private path; reruns can safely refresh only this deck's
// stable outputs. The preserved v16 deck is never read or changed by this tool.
const finalizedDir = await fs.mkdtemp(path.join(buildDir, "final-"));
const validatedPptx = path.join(finalizedDir, path.basename(finalPptx));
const validatedReceipt = path.join(buildDir, `${path.basename(finalizedDir)}.validation.json`);
const receipt = await finalizePresentation({
  workspaceDir: root, candidatePath: candidate, finalPath: validatedPptx,
  pythonExecutable: runtimePython,
  integrityValidatorPath: path.join(skill, "container_tools/inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(skill, "container_tools/inspect_presentation_layout_geometry.py"),
  layoutArgs: ["--expected-slide-size-emu", "12192000,6858000", "--validate-bullet-geometry", "--validate-heading-fit"],
  explicitTotalSlideCount: 6, requiredNativeTableOwnerSlides: [], requiredNativeChartOwnerSlides: [],
  fontPolicy: { basis: "design", families: [font] }, verifyArtifactToolImport: true,
  receiptPath: validatedReceipt,
});
// The supplied Artifact Tool PDF backend lacks a standard-font module in the
// desktop runtime. Convert the finalized editable PPTX with supplied LibreOffice.
// Its headless fontconfig needs an explicit font directory to avoid silently
// substituting Liberation Sans for Arial. Keep the configuration and cache local
// to this build; never modify installed fonts or the bundled runtime.
const soffice = process.env.CODEX_SOFFICE ?? "soffice";
const pdfFontDir = process.env.CODEX_PDF_FONT_DIR ?? "/System/Library/Fonts/Supplemental";
for (const filename of ["Arial.ttf", "Arial Bold.ttf"]) {
  await fs.access(path.join(pdfFontDir, filename)).catch(() => {
    throw new Error(`Arial font missing: ${path.join(pdfFontDir, filename)}; set CODEX_PDF_FONT_DIR.`);
  });
}
const xml = value => value.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
const fontConfigPath = path.join(finalizedDir, "fonts.conf");
await fs.writeFile(fontConfigPath, `<?xml version="1.0"?>\n<!DOCTYPE fontconfig SYSTEM "fonts.dtd">\n<fontconfig><dir>${xml(pdfFontDir)}</dir><cachedir>${xml(path.join(finalizedDir, "font-cache"))}</cachedir></fontconfig>\n`);
const profile = pathToFileURL(path.join(finalizedDir, "lo-profile")).href;
const converted = spawnSync(soffice, ["--headless", `-env:UserInstallation=${profile}`,
  "--convert-to", "pdf", "--outdir", finalizedDir, validatedPptx], {
  encoding: "utf8", timeout: 120000,
  env: { ...process.env, FONTCONFIG_FILE: fontConfigPath, SAL_FONTPATH: pdfFontDir },
});
if (converted.error || converted.status !== 0) throw new Error(`PDF conversion failed: ${converted.error ?? converted.stderr}`);
const validatedPdf = validatedPptx.replace(/\.pptx$/i, ".pdf");
if (!(await fs.stat(validatedPdf)).size) throw new Error("PDF conversion produced an empty file");
const pdfFontCheck = spawnSync(runtimePython, ["-c", `
import json, re, sys
from pypdf import PdfReader
reader = PdfReader(sys.argv[1])
if len(reader.pages) != 6:
    raise ValueError("PDF must contain six pages")
fonts = set()
for page in reader.pages:
    for ref in page["/Resources"]["/Font"].values():
        font = ref.get_object()
        name = re.sub(r"^[A-Z]{6}\\+", "", str(font["/BaseFont"]).lstrip("/"))
        fonts.add(name)
        if not (name.startswith("Arial") or name == "OpenSymbol"):
            raise ValueError(f"Unexpected PDF font substitution: {name}")
        descriptor = font.get("/FontDescriptor")
        descriptor = descriptor.get_object() if descriptor else {}
        if not any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3")):
            raise ValueError(f"PDF font is not embedded: {name}")
if not any(name.startswith("Arial") for name in fonts):
    raise ValueError("PDF contains no embedded Arial text")
print(json.dumps({"pages": 6, "embeddedFonts": sorted(fonts)}))
`, validatedPdf], { encoding: "utf8", timeout: 30000 });
if (pdfFontCheck.error || pdfFontCheck.status !== 0) throw new Error(`PDF font validation failed: ${pdfFontCheck.error ?? pdfFontCheck.stderr}`);
await fs.writeFile(path.join(buildDir, "pdf-font-validation.json"), pdfFontCheck.stdout.trim() + "\n");
await fs.copyFile(validatedPptx, finalPptx);
await fs.copyFile(validatedPdf, finalPdf);
await fs.copyFile(validatedReceipt, path.join(buildDir, "validation.json"));
await fs.writeFile(path.join(buildDir, "source-content.json"), JSON.stringify(slides, null, 2) + "\n");
console.log(JSON.stringify({ source, pptx: finalPptx, pdf: finalPdf, slides: slides.length, receipt }, null, 2));
