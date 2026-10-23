"""Spending gates exercise durable state and concurrent paid-call authorization."""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from datetime import datetime, timezone
from decimal import Decimal
import json
import multiprocessing

import pytest

from cost_tracker import BudgetExceeded, CostTracker, CostTrackerError, LedgerPolicyError, estimated_cost


pytestmark = pytest.mark.unit


def _concurrent_reservation(path: str, sequence: int) -> bool:
    tracker = CostTracker(path, daily_limit="1", run_id=f"worker-{sequence}")
    try:
        tracker.reserve("coder", "explicit-model", "0.30")
    except BudgetExceeded:
        return False
    return True


def test_cost_uses_provider_counts_and_decimal_prices(tmp_path):
    tracker = CostTracker(tmp_path / "ledger.db", daily_limit="1", run_limit="0.20", run_id="build")
    reservation = tracker.reserve("coder", "configured-model", "0.10")
    receipt = tracker.settle(reservation, 1000, 2000, "2", "4", cached_input_tokens=400,
                             provider="example", provider_request_id="request-17")
    assert receipt["estimated_usd"] == "0.010000000"
    assert receipt["usage"]["cached_input_tokens"] == 400
    assert receipt["usage"]["provider_request_id"] == "request-17"
    summary = tracker.summary()
    assert summary["daily_settled_estimate"] == "0.010000000"
    assert summary["pending_maximum"] == "0.000000000"
    assert summary["daily_remaining"] == "0.990000000"
    assert summary["run_remaining"] == "0.190000000"
    assert summary["usage_cost_is_provider_invoice"] is False
    json.dumps(summary)


def test_ledger_is_durable_across_instances_and_fixes_policy(tmp_path):
    path = tmp_path / "ledger.db"
    first = CostTracker(path, "1", run_limit="0.8", run_id="build")
    first.reserve("manager", "configured-model", "0.6")
    second = CostTracker(path, "1.0", run_limit="0.8", run_id="build")
    assert second.summary()["pending_maximum"] == "0.600000000"
    with pytest.raises(BudgetExceeded, match="daily"):
        second.reserve("coder", "configured-model", "0.5")
    with pytest.raises(LedgerPolicyError, match="daily_limit"):
        CostTracker(path, "2", run_id="other")
    wrong_run_policy = CostTracker(path, "1", run_limit="0.9", run_id="build")
    with pytest.raises(LedgerPolicyError, match="run_limit"):
        wrong_run_policy.reserve("coder", "configured-model", "0.01")


def test_run_cap_is_independent_of_other_runs(tmp_path):
    path = tmp_path / "ledger.db"
    first = CostTracker(path, "1", run_limit="0.2", run_id="first")
    first.reserve("manager", "m", "0.2")
    with pytest.raises(BudgetExceeded, match="run"):
        first.reserve("coder", "m", "0.001")
    second = CostTracker(path, "1", run_limit="0.2", run_id="second")
    second.reserve("manager", "m", "0.2")
    assert second.summary()["pending_maximum"] == "0.400000000"
    assert second.summary()["run_pending_maximum"] == "0.200000000"


def test_daily_cap_rejects_before_a_provider_call(tmp_path):
    tracker = CostTracker(tmp_path / "ledger.db", "0.10")
    calls = []
    with pytest.raises(BudgetExceeded):
        tracker.reserve("coder", "m", "0.11")
        calls.append("paid provider call")
    assert calls == []
    assert tracker.events() == []


def test_reservation_and_settlement_are_idempotent(tmp_path):
    tracker = CostTracker(tmp_path / "ledger.db", "1", run_id="build")
    reservation = tracker.reserve("qa", "m", "0.2", reservation_id="stable-request")
    assert tracker.reserve("qa", "m", "0.20", reservation_id=reservation) == reservation
    assert len(tracker.events()) == 1
    with pytest.raises(CostTrackerError, match="different request"):
        tracker.reserve("qa", "m", "0.3", reservation_id=reservation)
    receipt = tracker.settle(reservation, 200, 100, "1", "2")
    assert tracker.settle(reservation, 200, 100, "1", "2") == receipt
    assert len(tracker.events()) == 2
    with pytest.raises(CostTrackerError, match="different usage"):
        tracker.settle(reservation, 200, 200, "1", "2")


def test_uncertain_calls_keep_reservation_until_reconciled(tmp_path):
    tracker = CostTracker(tmp_path / "ledger.db", "0.1", run_id="build")
    reservation = tracker.reserve("coder", "m", "0.1")
    tracker.mark_uncertain(reservation, "Timeout after provider accepted request")
    tracker.mark_uncertain(reservation, "Timeout after provider accepted request")
    assert len(tracker.events()) == 2
    with pytest.raises(BudgetExceeded):
        tracker.reserve("qa", "m", "0.001")
    with pytest.raises(CostTrackerError, match="confirmed_not_charged"):
        tracker.release(reservation)
    assert tracker.summary()["pending_maximum"] == "0.100000000"
    tracker.settle(reservation, 200, 100, "1", "2", provider_request_id="late-receipt")
    assert tracker.summary()["pending_maximum"] == "0.000000000"
    assert tracker.summary()["daily_settled_estimate"] == "0.000400000"


def test_confirmed_no_charge_reconciliation_and_predispatch_cancel(tmp_path):
    tracker = CostTracker(tmp_path / "ledger.db", "1")
    cancelled = tracker.reserve("qa", "m", "0.2")
    tracker.release(cancelled, "Cancelled before dispatch")
    tracker.release(cancelled, "Already cancelled")
    unknown = tracker.reserve("coder", "m", "0.2")
    tracker.mark_uncertain(unknown, "Connection dropped")
    tracker.release(unknown, "Provider support confirmed request was not billed", confirmed_not_charged=True)
    assert tracker.summary()["daily_remaining"] == "1.000000000"
    with pytest.raises(CostTrackerError, match="released"):
        tracker.settle(unknown, 1, 1, "1", "1")


def test_reservation_overrun_is_recorded_and_blocks_new_calls(tmp_path):
    tracker = CostTracker(tmp_path / "ledger.db", "0.1", run_limit="0.1")
    reservation = tracker.reserve("coder", "m", "0.05")
    receipt = tracker.settle(reservation, 100_000, 100_000, "1", "1")
    assert receipt["estimated_usd"] == "0.200000000"
    assert tracker.summary()["daily_over_limit"] is True
    assert tracker.summary()["run_over_limit"] is True
    assert tracker.events()[-1]["details"]["overrun"] is True
    with pytest.raises(BudgetExceeded):
        tracker.reserve("qa", "m", "0.001")
    with pytest.raises(CostTrackerError, match="settled"):
        tracker.release(reservation)


def test_utc_rollover_carries_unresolved_and_dates_actual_settlement(tmp_path):
    now = [datetime(2026, 10, 20, 23, 59, tzinfo=timezone.utc)]
    tracker = CostTracker(tmp_path / "ledger.db", "1", run_id="overnight", clock=lambda: now[0])
    completed = tracker.reserve("manager", "m", "0.3")
    tracker.settle(completed, 300_000, 0, "1", "1")
    pending = tracker.reserve("coder", "m", "0.7")
    tracker.mark_uncertain(pending, "Provider response lost")
    now[0] = datetime(2026, 10, 21, 0, 1, tzinfo=timezone.utc)
    summary = tracker.summary()
    assert summary["daily_settled_estimate"] == "0.000000000"
    assert summary["pending_maximum"] == "0.700000000"
    assert summary["daily_remaining"] == "0.300000000"
    with pytest.raises(BudgetExceeded):
        tracker.reserve("qa", "m", "0.31")
    tracker.settle(pending, 600_000, 0, "1", "1")
    assert tracker.summary()["daily_settled_estimate"] == "0.600000000"
    assert tracker.summary()["run_settled_estimate"] == "0.900000000"


def test_environment_daily_limit_and_utc_clock(tmp_path, monkeypatch):
    monkeypatch.setenv("MAX_DAILY_SPEND", "0.25")
    tracker = CostTracker(tmp_path / "ledger.db", clock=lambda: datetime(2026, 10, 21, 1, tzinfo=timezone.utc))
    assert tracker.summary()["daily_limit"] == "0.250000000"
    tracker.clock = lambda: datetime(2026, 10, 21, 1)
    with pytest.raises(CostTrackerError, match="timezone-aware"):
        tracker.reserve("coder", "m", "0.01")


@pytest.mark.parametrize("invalid", ["-1", "NaN", "Infinity", "-Infinity", 0.1, True, None, "hello", "1e100"])
def test_invalid_request_money_fails_closed(tmp_path, invalid):
    tracker = CostTracker(tmp_path / "ledger.db", "1")
    with pytest.raises(CostTrackerError):
        tracker.reserve("coder", "m", invalid)
    assert tracker.summary()["pending_maximum"] == "0.000000000"


@pytest.mark.parametrize("invalid", [-1, 0.5, True, None, "10", 2**64])
def test_invalid_provider_usage_keeps_reservation(tmp_path, invalid):
    tracker = CostTracker(tmp_path / "ledger.db", "1")
    reservation = tracker.reserve("coder", "m", "0.1")
    with pytest.raises(CostTrackerError):
        tracker.settle(reservation, invalid, 10, "1", "1")
    assert tracker.summary()["pending_maximum"] == "0.100000000"


@pytest.mark.parametrize("invalid", ["-1", "NaN", "Infinity", 0.1, True])
def test_invalid_provider_rates_keep_reservation(tmp_path, invalid):
    tracker = CostTracker(tmp_path / "ledger.db", "1")
    reservation = tracker.reserve("coder", "m", "0.1")
    with pytest.raises(CostTrackerError):
        tracker.settle(reservation, 10, 10, invalid, "1")
    assert tracker.summary()["pending_maximum"] == "0.100000000"


def test_cached_usage_is_subset_and_missing_usage_does_not_free_money(tmp_path):
    tracker = CostTracker(tmp_path / "ledger.db", "1")
    reservation = tracker.reserve("coder", "m", "0.1")
    with pytest.raises(CostTrackerError, match="cannot exceed"):
        tracker.settle(reservation, 1, 1, "1", "1", cached_input_tokens=2)
    assert tracker.summary()["pending_maximum"] == "0.100000000"
    with pytest.raises(CostTrackerError, match="unknown"):
        tracker.settle("missing", 1, 1, "1", "1")


def test_nanodollar_rounding_never_expands_cap_or_understates_usage(tmp_path):
    tracker = CostTracker(tmp_path / "ledger.db", "0.0000000019")
    assert tracker.summary()["daily_limit"] == "0.000000001"
    with pytest.raises(BudgetExceeded):
        tracker.reserve("qa", "m", "0.0000000011")
    assert estimated_cost(1, 0, "0.00000000001", "0") == Decimal("0.000000001")
    assert estimated_cost(1, 0, "0.00100000000000000000000000000000000000000000000000001", "0") == Decimal("0.000001001")


def test_threaded_reservations_share_one_atomic_cap(tmp_path):
    path = tmp_path / "ledger.db"
    CostTracker(path, "1")
    with ThreadPoolExecutor(max_workers=8) as pool:
        admitted = list(pool.map(lambda item: _concurrent_reservation(str(path), item), range(20)))
    assert sum(admitted) == 3
    assert CostTracker(path, "1").summary()["pending_maximum"] == "0.900000000"


def test_processes_share_one_atomic_cap(tmp_path):
    path = tmp_path / "ledger.db"
    CostTracker(path, "1")
    with ProcessPoolExecutor(max_workers=4, mp_context=multiprocessing.get_context("spawn")) as pool:
        admitted = list(pool.map(_concurrent_reservation, [str(path)] * 12, range(12)))
    assert sum(admitted) == 3
    assert CostTracker(path, "1").summary()["pending_maximum"] == "0.900000000"
