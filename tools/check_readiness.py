"""Local/CI gate for the deterministic course distribution (Python 3.12)."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]


def pinned_requirements(path: Path) -> dict[str, str]:
    pins = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line.startswith("-r "):
            pins.update(pinned_requirements(path.parent / line[3:].strip()))
        elif "==" in line:
            name, version = line.split("==", 1)
            pins[name.strip()] = version.strip()
    return pins


def environment_check(root: Path) -> dict:
    packages = {}
    for name, expected in pinned_requirements(root / "requirements/maintenance.txt").items():
        try:
            installed = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            installed = None
        packages[name] = {"expected": expected, "installed": installed}
    valid = sys.version_info[:2] == (3, 12) and all(
        item["expected"] == item["installed"] for item in packages.values())
    return {"passed": valid, "python": platform.python_version(),
            "platform": platform.platform(), "packages": packages}


def source_fingerprint(root: Path) -> dict:
    patterns = ["src/*.py", "tests/*.py", "tools/**/*.py", "tools/*.mjs", "*.py", "software_factory/**/*.py",
                "software_factory/**/*.json", "software_factory/**/*.html",
                "notebooks/*.ipynb", "extensions/*.ipynb", "extensions/*.md", "extensions/**/*.sh", "_archive/**/*.ipynb",
                "crewai_learning/*.py", "crewai_learning/*.ipynb", "crewai_learning/*.md", "index.html",
                "requirements.txt", "requirements/*.txt", ".github/workflows/*.yml",
                "*.md", "assignments/*.md", "resources/**/*.md", "resources/diagrams/*.svg", "slides/*.md",
                "slides/*.pptx", "slides/*.svg", "slides/assets/*", "leadership/*.md",
                "output/pdf/managing_multi_agent_teams_6_slides.pdf",
                "output/pdf/executive_brief_governed_multi_agent_training.pdf"]
    paths = {path for pattern in patterns for path in root.glob(pattern)}
    paths.update(root / name for name in (
        "pytest.ini", "notebook_manifest.yml", "tools/check_readiness.py",
        "assignments/starter_code/ex5_capstone_starter.py",
        "instructor/solutions/core_notebook_solution_guide.md"))
    inputs = {str(path.relative_to(root)).replace("\\", "/"):
              hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(paths) if path.is_file()}
    digest = hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()
    return {"sha256": digest, "files": inputs}


def run_command(command: list[str], root: Path, log: Path, timeout: int) -> dict:
    started = time.monotonic()
    try:
        result = subprocess.run(command, cwd=root, text=True, encoding="utf-8", errors="replace",
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        code, output = result.returncode, result.stdout
    except subprocess.TimeoutExpired as exc:
        code = 124
        partial = exc.stdout or b""
        output = partial.decode("utf-8", errors="replace") if isinstance(partial, bytes) else partial
        output += f"\nReadiness command exceeded {timeout} seconds.\n"
    except OSError as exc:
        code, output = 127, str(exc)
    log.write_text(output, encoding="utf-8")
    print(output, end="", flush=True)
    return {"returncode": code, "seconds": round(time.monotonic() - started, 3),
            "log": str(log)}


def junit_counts(path: Path) -> dict:
    cases = list(ElementTree.parse(path).getroot().iter("testcase"))
    return {"tests": len(cases),
            **{name: sum(case.find(tag) is not None for case in cases)
               for name, tag in (("failures", "failure"), ("errors", "error"), ("skipped", "skipped"))}}


def check_readiness(root: Path, report_dir: Path, stage: str = "all") -> dict:
    report_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
    run_dir = report_dir / run_id
    run_dir.mkdir()
    report = {"scope": "deterministic workshop distribution", "run_id": run_id,
              "requested_stage": stage, "status": "failed", "environment": environment_check(root),
              "sources": source_fingerprint(root), "checks": {}}
    try:
        if not report["environment"]["passed"]:
            report["reason"] = "Use Python 3.12 and install requirements/maintenance.txt with its exact pins."
            return report
        dependency = run_command([sys.executable, "-m", "pip", "check"], root,
                                 run_dir / "dependencies.log", 120)
        report["checks"]["dependencies"] = dependency
        if dependency["returncode"]:
            report["reason"] = "Dependency compatibility check failed."
            return report
        stages = ("unit", "integration") if stage == "all" else (stage,)
        for name in stages:
            junit = run_dir / f"{name}.xml"
            command = [sys.executable, "-m", "pytest", "tests", "-m", name, "-q",
                       f"--junitxml={junit}", f"--notebook-artifacts={run_dir / 'notebooks'}"]
            result = run_command(command, root, run_dir / f"{name}.log", 600)
            report["checks"][name] = result
            try:
                result["counts"] = junit_counts(junit)
            except (OSError, ElementTree.ParseError) as exc:
                result["report_error"] = str(exc)
                report["reason"] = f"{name} produced no usable JUnit report."
                return report
            counts = result["counts"]
            if result["returncode"] or not counts["tests"] or any(
                    counts[key] for key in ("failures", "errors", "skipped")):
                report["reason"] = f"{name} must pass with collected tests and no skips."
                return report
        if report["sources"] != source_fingerprint(root):
            report["reason"] = "Verification inputs changed during execution; rerun the gate."
            return report
        report["status"] = "passed"
        return report
    finally:
        serialized = json.dumps(report, indent=2) + "\n"
        (run_dir / "summary.json").write_text(serialized, encoding="utf-8")
        (report_dir / "summary.json").write_text(serialized, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("unit", "integration", "all"), default="all")
    parser.add_argument("--report-dir", type=Path, default=ROOT / ".test-results/readiness")
    args = parser.parse_args(argv)
    report = check_readiness(ROOT, args.report_dir.resolve(), args.stage)
    print(f"Readiness ({args.stage}): {report['status']}")
    if "reason" in report:
        print(report["reason"])
    print(f"Report: {args.report_dir.resolve() / 'summary.json'}")
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
