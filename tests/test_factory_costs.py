"""Simulated totals reflect completed stages, including partial and denied runs."""
from concurrent.futures import ProcessPoolExecutor
from decimal import Decimal
import json
import multiprocessing

import pytest

from cost_tracker import BudgetExceeded, CostTracker, CostTrackerError

pytestmark = pytest.mark.unit

STAGES = [("manager", "0.05"), ("coder", "0.15"), ("security", "0.10"),
          ("ui_ux", "0.10"), ("qa", "0.05"), ("publish", "0.05")]


def _record_concurrently(path, number):
    tracker = CostTracker(path, "0.50", "shared")
    try:
        tracker.record(f"stage-{number}", "0.15")
        return True
    except BudgetExceeded:
        return False


def test_complete_execution_total_is_derived_from_stage_events(tmp_path):
    tracker = CostTracker(tmp_path / "ledger.db", run_id="build")
    for stage, cost in STAGES:
        tracker.record(stage, cost)
    summary = tracker.summary()
    assert summary["simulated_total"] == "0.50"
    assert summary["simulated_remaining"] == "0.00"
    assert summary["actual_cost"] == "0.00"
    assert summary["provider_calls"] == 0
    assert summary["daily_provider_controls_active"] is False
    assert tracker.total_simulated_cost == Decimal("0.50")
    assert len(summary["events"]) == 6
    json.dumps(summary)


@pytest.mark.parametrize("executed_count,expected", [(0, "0.00"), (1, "0.05"), (2, "0.20"), (3, "0.30"), (4, "0.40"), (5, "0.45")])
def test_denial_and_early_stop_never_charge_skipped_stages(executed_count, expected):
    tracker = CostTracker()
    for stage, cost in STAGES[:executed_count]:
        tracker.record(stage, cost)
    assert tracker.summary()["simulated_total"] == expected
    assert tracker.summary()["actual_cost"] == "0.00"


def test_budget_preflight_and_atomic_gate(tmp_path):
    tracker = CostTracker(tmp_path / "ledger.db", simulated_budget="0.19")
    tracker.record("manager", "0.05")
    assert tracker.can_record("0.14")
    assert not tracker.can_record("0.15")
    with pytest.raises(BudgetExceeded, match="simulated"):
        tracker.record("coder", "0.15")
    assert tracker.summary()["simulated_total"] == "0.05"
    assert len(tracker.summary()["events"]) == 1


def test_reopen_preserves_totals_and_cannot_silently_change_budget(tmp_path):
    path = tmp_path / "ledger.db"
    first = CostTracker(path, run_id="build")
    first.record("manager", "0.05")
    assert CostTracker(path, run_id="build").summary()["simulated_total"] == "0.05"
    assert CostTracker(path, run_id="other").summary()["simulated_total"] == "0.00"
    with pytest.raises(CostTrackerError, match="recorded budget"):
        CostTracker(path, simulated_budget="1.00", run_id="build")


def test_record_is_idempotent_and_rejects_conflicting_retries():
    tracker = CostTracker()
    receipt = tracker.record("coder", "0.15", "coder-attempt-1")
    assert tracker.record("coder", Decimal("0.1500"), "coder-attempt-1") == receipt
    assert tracker.summary()["simulated_total"] == "0.15"
    with pytest.raises(CostTrackerError, match="different stage"):
        tracker.record("qa", "0.15", "coder-attempt-1")
    with pytest.raises(CostTrackerError, match="different stage"):
        tracker.record("coder", "0.10", "coder-attempt-1")


@pytest.mark.parametrize("invalid", [-1, "NaN", "Infinity", "-Infinity", True, 0.1, "0.001", "wrong", None, "1e100"])
def test_invalid_values_fail_closed(invalid):
    tracker = CostTracker()
    with pytest.raises(CostTrackerError):
        tracker.record("coder", invalid)
    assert tracker.summary()["simulated_total"] == "0.00"


def test_separate_processes_cannot_overrun_shared_simulated_budget(tmp_path):
    path = str(tmp_path / "ledger.db")
    CostTracker(path, run_id="shared")
    with ProcessPoolExecutor(max_workers=4, mp_context=multiprocessing.get_context("spawn")) as pool:
        accepted = list(pool.map(_record_concurrently, [path] * 12, range(12)))
    assert sum(accepted) == 3
    assert CostTracker(path, run_id="shared").summary()["simulated_total"] == "0.45"
