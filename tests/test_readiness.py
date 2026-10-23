"""The readiness command must fail on broken, empty, or skipped checks."""
from pathlib import Path

import pytest

from tools import check_readiness as gate

pytestmark = pytest.mark.unit


@pytest.fixture
def readiness(monkeypatch, tmp_path):
    monkeypatch.setattr(gate, "environment_check", lambda root: {"passed": True})
    monkeypatch.setattr(gate, "source_fingerprint", lambda root: {"sha256": "fixture"})
    return tmp_path / "reports"


def fake_commands(monkeypatch, xml='<testsuites><testsuite><testcase name="contract"/></testsuite></testsuites>',
                  fail_stage=None):
    calls = []

    def run(command, root, log, timeout):
        name = command[command.index("-m") + 1]
        stage = command[command.index("-m", 3) + 1] if name == "pytest" else "dependencies"
        calls.append(stage)
        if name == "pytest" and xml is not None:
            junit = next(arg.split("=", 1)[1] for arg in command if arg.startswith("--junitxml="))
            Path(junit).write_text(xml, encoding="utf-8")
        return {"returncode": 1 if stage == fail_stage else 0}

    monkeypatch.setattr(gate, "run_command", run)
    return calls


def test_gate_runs_unit_before_integration_and_writes_report(monkeypatch, readiness, repo_root):
    calls = fake_commands(monkeypatch)
    report = gate.check_readiness(repo_root, readiness)
    assert calls == ["dependencies", "unit", "integration"]
    assert report["status"] == "passed"
    assert report["checks"]["integration"]["counts"]["tests"] == 1
    assert (readiness / "summary.json").is_file()


def test_gate_stops_after_a_failing_unit_suite(monkeypatch, readiness, repo_root):
    calls = fake_commands(monkeypatch, fail_stage="unit")
    report = gate.check_readiness(repo_root, readiness)
    assert report["status"] == "failed"
    assert calls == ["dependencies", "unit"]


@pytest.mark.parametrize("xml", [None, "not XML", "<testsuites/>",
    '<testsuites><testcase><skipped/></testcase></testsuites>',
    '<testsuites><testcase><failure/></testcase></testsuites>',
    '<testsuites><testcase><error/></testcase></testsuites>'])
def test_zero_exit_does_not_hide_missing_empty_or_failed_reports(monkeypatch, readiness, repo_root, xml):
    fake_commands(monkeypatch, xml=xml)
    assert gate.check_readiness(repo_root, readiness, "unit")["status"] == "failed"


def test_gate_rejects_environment_drift_before_running_tests(monkeypatch, readiness, repo_root):
    calls = fake_commands(monkeypatch)
    monkeypatch.setattr(gate, "environment_check", lambda root: {"passed": False})
    assert gate.check_readiness(repo_root, readiness)["status"] == "failed"
    assert calls == []


def test_gate_rejects_sources_that_change_during_verification(monkeypatch, readiness, repo_root):
    fake_commands(monkeypatch)
    versions = iter([{"sha256": "before"}, {"sha256": "after"}])
    monkeypatch.setattr(gate, "source_fingerprint", lambda root: next(versions))
    assert gate.check_readiness(repo_root, readiness)["status"] == "failed"


def test_pin_reader_follows_the_required_install_chain(repo_root):
    pins = gate.pinned_requirements(repo_root / "requirements/maintenance.txt")
    assert {"crewai", "pydantic", "pytest", "jupyterlab", "ipykernel", "nbclient", "nbformat", "PyYAML"} <= pins.keys()


@pytest.mark.parametrize("python_version,expected", [((3, 12), True), ((3, 11), False), ((3, 13), False)])
def test_environment_requires_the_workshop_python_version(monkeypatch, repo_root, python_version, expected):
    pins = gate.pinned_requirements(repo_root / "requirements/maintenance.txt")
    monkeypatch.setattr(gate.importlib.metadata, "version", pins.__getitem__)
    monkeypatch.setattr(gate.sys, "version_info", python_version)
    assert gate.environment_check(repo_root)["passed"] is expected


@pytest.mark.parametrize("installed", [None, "0.0.0"])
def test_environment_rejects_missing_or_mismatched_pins(monkeypatch, repo_root, installed):
    pins = gate.pinned_requirements(repo_root / "requirements/maintenance.txt")

    def version(name):
        if name == "crewai":
            if installed is None:
                raise gate.importlib.metadata.PackageNotFoundError(name)
            return installed
        return pins[name]

    monkeypatch.setattr(gate.importlib.metadata, "version", version)
    assert gate.environment_check(repo_root)["passed"] is False


def test_source_fingerprint_changes_when_a_handout_changes(tmp_path):
    notebooks = tmp_path / "notebooks"
    notebooks.mkdir()
    handout = notebooks / "example.ipynb"
    handout.write_text("before", encoding="utf-8")
    before = gate.source_fingerprint(tmp_path)
    handout.write_text("after", encoding="utf-8")
    assert gate.source_fingerprint(tmp_path)["sha256"] != before["sha256"]


def test_main_returns_nonzero_for_failed_readiness(monkeypatch, tmp_path):
    monkeypatch.setattr(gate, "check_readiness", lambda *args: {"status": "failed", "reason": "regression"})
    assert gate.main(["--report-dir", str(tmp_path)]) == 1
