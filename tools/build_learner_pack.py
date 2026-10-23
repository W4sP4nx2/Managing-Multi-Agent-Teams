"""Build a core-only learner ZIP without solutions or local environments."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "managing-multi-agent-teams-learner"
FILES = (
    'README.md',
    'ASSIGNMENTS.md',
    'SETUP.md',
    'COURSE_MAP.md',
    'requirements.txt',
    'notebook_manifest.yml',
    'slides/managing_multi_agent_teams_6_slides.pptx',
    'slides/managing_multi_agent_teams_6_slides.md',
    'output/pdf/managing_multi_agent_teams_6_slides.pdf',
    'slides/assets/managing_multi_agent_teams_mindmap.png',
    'slides/assets/un_volunteers_iyv26.png',
    'slides/trinity_adaptive_workflow_access_list.svg',
    'resources/diagrams/lab1-contract-flow.svg',
    'resources/diagrams/lab2-team-audit.svg',
    'resources/diagrams/notebook-preflight-flow.svg',
    'resources/diagrams/notebook-security-flow.svg',
    'resources/diagrams/notebook-capstone-flow.svg',
    'resources/diagrams/notebook-factory-flow.svg',
    'resources/diagrams/notebook-cicd-flow.svg',
    'resources/diagrams/notebook-collaboration-patterns.svg',
    'resources/diagrams/live-software-factory.svg',
    'resources/diagrams/capstone_factory_erd.md',
    'resources/diagrams/capstone_factory_erd.svg',
    'agent_harness.py',
    'cost_tracker.py',
    'orchestrator.py',
    'orchestrator_with_approval.py',
    'index.html',
    'live_simulation_orchestrator.py',
    'software_factory/__init__.py',
    'software_factory/contracts.py',
    'software_factory/workflow.py',
    'software_factory/storage.py',
    'software_factory/local_checks.py',
    'software_factory/simulation_config.json',
    'software_factory/fixtures/index.html',
    'software_factory/fixtures/security_review.json',
    'software_factory/fixtures/ui_review.json',
    'software_factory/fixtures/qa_plan.json',
    'extensions/live_software_factory.md',
    'extensions/software_factory/setup-local-factory.sh',
    'crewai_learning/README.md',
    'crewai_learning/01_Bridge_Sequential_Crew.ipynb',
    'crewai_learning/coding_team.py',
    'crewai_learning/offline.py',
    'crewai_learning/__init__.py',
)
MARKDOWN_LINK = re.compile(r"(?<!!)\[([^\]\n]+)\]\(([^)\s]+)\)")
PACK_NOTE = (
    "> **Course learner pack:** start with SETUP.md, then notebooks 00–06. "
    "The current deck and its slide index are included. Text marked “full repository” "
    "refers to optional or instructor material outside this handout. "
    "Extract the ZIP and keep its folders together.\n\n"
)


def remove_section(text: str, heading: str) -> str:
    """Omit a named section, up to the next heading of the same/higher level."""
    level = len(heading) - len(heading.lstrip("#"))
    return re.sub(r"(?ms)^" + re.escape(heading) + r"\n.*?(?=^#{1," + str(level) + r"} |\Z)", "", text)


def local_target(source: str, target: str) -> str | None:
    parts = urlsplit(target)
    if parts.scheme or parts.netloc or not parts.path:
        return None
    # Resolve relative links without trusting the process working directory.
    return str((ROOT / source).parent.joinpath(unquote(parts.path)).resolve().relative_to(ROOT))


def learner_text(name: str, text: str, included: set[str]) -> str:
    sections = {
        "README.md": ("## What to teach", "## Optional Mock CI/CD Pipeline", "### Teaching and research foundations",
                      "### Instructors and maintainers"),
        "SETUP.md": ("## Optional packages", "## Verification", "## Repository map"),
    }
    for heading in sections.get(name, ()):
        text = remove_section(text, heading)
    # Omit invitations to optional activities, rather than turning them into
    # non-clickable entries in the learner's navigation.
    optional_targets = ("extensions/bonus_live_demo.ipynb", "extensions/11_mock_cicd_pipeline.ipynb",
                        "assignment_09_framework_comparison.md", "_archive/")
    optional_starts = ("The optional [", "After the Capstone, the optional [", "For an executable, ungraded", "Any live-provider",
                       "Optional [extensions]")
    text = "\n\n".join(paragraph for paragraph in text.split("\n\n")
                         if not (paragraph.startswith(optional_starts)
                                 and any(target in paragraph for target in optional_targets))
                         and not paragraph.startswith(("The v13, v14, and v15 files",
                                                       "The previous 26-slide presentation",
                                                       "For leadership, share")))
    text = "\n".join(line for line in text.split("\n")
                     if not (line.startswith("| ")
                             and any(target in line for target in optional_targets)))
    for sentence in (
        r" Optional \[extensions\]\([^)]+\) are available for post-course study\.",
    ):
        text = re.sub(sentence, "", text)
    if name == "README.md":
        text = "\n".join(line for line in text.split("\n")
                         if not (line.startswith("| ") and "_archive/" in line))
        text = re.sub(r"(^# [^\n]+\n\n)", lambda match: match.group(1) + PACK_NOTE, text, count=1)

    def replace_link(match):
        label, target = match.groups()
        local = local_target(name, target)
        if local is not None and local not in included:
            return f"{label} (full repository)"
        return match.group(0)

    return MARKDOWN_LINK.sub(replace_link, text)


def package_files(root: Path) -> dict[str, bytes]:
    manifest = yaml.safe_load((root / "notebook_manifest.yml").read_text(encoding="utf-8"))
    names = set(FILES) | {"notebooks/" + row["file"] for row in manifest["required_sequence"]}
    if len(manifest["required_sequence"]) != 7:
        raise ValueError("Review the learner package when the required sequence changes")
    payload = {}
    for name in sorted(names):
        path = root / name
        if path.is_symlink():
            raise ValueError(f"Refusing symlink in learner pack: {name}")
        if name == "notebook_manifest.yml":
            core = {key: value for key, value in manifest.items()
                    if key not in {"compatibility_demo", "instructor_output_policy"}}
            core["package_tiers"] = {key: value for key, value in core["package_tiers"].items()
                                     if key != "reference_extensions"}
            data = yaml.safe_dump(core, sort_keys=False).encode()
        elif path.suffix == ".md":
            data = learner_text(name, path.read_text(encoding="utf-8"), names).encode()
        elif path.suffix == ".ipynb":
            notebook = json.loads(path.read_text(encoding="utf-8"))
            for cell in notebook["cells"]:
                if cell["cell_type"] == "code":
                    if cell.get("outputs") or cell.get("execution_count") is not None:
                        raise ValueError(f"Clear notebook outputs before packaging: {name}")
                elif cell["cell_type"] == "markdown":
                    cell["source"] = learner_text(name, "".join(cell["source"]), names).splitlines(keepends=True)
            data = (json.dumps(notebook, indent=2, ensure_ascii=False) + "\n").encode()
        else:
            data = path.read_bytes()
        payload[name] = data
    return payload


def build(root: Path = ROOT, output_dir: Path | None = None) -> Path:
    output_dir = output_dir or root / "dist"
    payload = package_files(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{PACKAGE}.zip"
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for name, data in sorted(payload.items()):
            info = ZipInfo(f"{PACKAGE}/{name}", date_time=(2000, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    report = {"archive": output.name, "scope": "offline course with integrated deterministic factory and local CI/CD",
              "file_count": len(payload), "zip_bytes": output.stat().st_size,
              "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
              "files": {name: {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                        for name, data in sorted(payload.items())}}
    (output_dir / "learner-pack-manifest.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    result = build(output_dir=args.output_dir)
    print(f"Learner pack: {result} ({result.stat().st_size:,} bytes)")
