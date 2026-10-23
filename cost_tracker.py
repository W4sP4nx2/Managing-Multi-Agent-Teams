"""Durable simulated stage costs: no provider calls, invoices, or actual charges.

The orchestrator records a stage only after its approval and execution. This
ledger enforces a simulated run budget atomically; it does not enforce provider
or daily spending controls because this course never makes paid API calls.
"""
from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
import sqlite3
from typing import Iterator
import uuid


class CostTrackerError(ValueError):
    """A simulated ledger value or operation is invalid."""


class BudgetExceeded(CostTrackerError):
    """A completed stage cannot fit inside the simulated run budget."""


def _cents(value: Decimal | str | int, name: str) -> int:
    if isinstance(value, (float, bool)) or not isinstance(value, (Decimal, str, int)):
        raise CostTrackerError(f"{name} must be an exact decimal string or Decimal")
    try:
        parsed = Decimal(value)
    except InvalidOperation:
        raise CostTrackerError(f"{name} must be finite and nonnegative") from None
    if not parsed.is_finite() or parsed < 0 or parsed > Decimal("92233720368547758.07"):
        raise CostTrackerError(f"{name} must be finite, nonnegative, and inside the ledger's range")
    numerator, denominator = parsed.as_integer_ratio()
    cents, remainder = divmod(numerator * 100, denominator)
    if remainder:
        raise CostTrackerError(f"{name} must have no fractional cents")
    return cents


def _usd(cents: int) -> str:
    whole, fraction = divmod(cents, 100)
    return f"{whole}.{fraction:02d}"


def _text(value: str, name: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 200:
        raise CostTrackerError(f"{name} must be a nonempty string of at most 200 characters")
    return value


class CostTracker:
    """Record only simulated work that has actually run under human approval.

    The same path and run_id reopen the same history. Each stage has one stable
    idempotency key, preventing a retry from inventing additional simulated cost.
    With path=None the ledger is isolated and in memory.
    """

    def __init__(self, path: Path | str | None = None, simulated_budget: Decimal | str | int = "0.50", run_id: str | None = None) -> None:
        self.run_id = _text(run_id or uuid.uuid4().hex, "run_id")
        self._budget_cents = _cents(simulated_budget, "simulated_budget")
        self.path = None if path is None else Path(path)
        if self.path is not None:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self._memory = sqlite3.connect(":memory:", isolation_level=None, check_same_thread=False) if path is None else None
        with self._connection() as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS simulated_cost_runs (
                    run_id TEXT PRIMARY KEY,
                    budget_cents INTEGER NOT NULL CHECK(budget_cents >= 0)
                );
                CREATE TABLE IF NOT EXISTS simulated_cost_events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    amount_cents INTEGER NOT NULL CHECK(amount_cents >= 0),
                    idempotency_key TEXT NOT NULL,
                    recorded_at TEXT NOT NULL,
                    UNIQUE(run_id, idempotency_key)
                );
            """)
        with self._transaction() as connection:
            connection.execute("INSERT OR IGNORE INTO simulated_cost_runs(run_id,budget_cents) VALUES (?,?)", (self.run_id, self._budget_cents))
            actual_budget = connection.execute("SELECT budget_cents FROM simulated_cost_runs WHERE run_id=?", (self.run_id,)).fetchone()[0]
            if actual_budget != self._budget_cents:
                raise CostTrackerError("simulated_budget differs from this run's recorded budget")

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        connection = self._memory or sqlite3.connect(str(self.path), timeout=30, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA busy_timeout=30000")
        try:
            yield connection
        finally:
            if self._memory is None:
                connection.close()

    @contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                yield connection
                connection.commit()
            except BaseException:
                connection.rollback()
                raise

    @staticmethod
    def _receipt(row: sqlite3.Row) -> dict:
        return {"event_id": row["event_id"], "run_id": row["run_id"], "stage": row["stage"],
                "simulated_amount": _usd(row["amount_cents"]), "actual_cost": "0.00",
                "idempotency_key": row["idempotency_key"], "recorded_at": row["recorded_at"]}

    def can_record(self, amount: Decimal | str | int) -> bool:
        """Allow the orchestrator to stop before executing an unaffordable stage.

        ``record`` repeats this check inside a write transaction. A successful
        preflight is advisory when another process uses the same run concurrently.
        """
        cents = _cents(amount, "amount")
        with self._connection() as connection:
            spent = sum(row[0] for row in connection.execute("SELECT amount_cents FROM simulated_cost_events WHERE run_id=?", (self.run_id,)))
            return spent + cents <= self._budget_cents

    def record(self, stage: str, amount: Decimal | str | int, idempotency_key: str | None = None) -> dict:
        """Record approved, executed work; denials and skipped stages cost zero."""
        stage = _text(stage, "stage")
        key = _text(idempotency_key or stage, "idempotency_key")
        cents = _cents(amount, "amount")
        with self._transaction() as connection:
            row = connection.execute("SELECT * FROM simulated_cost_events WHERE run_id=? AND idempotency_key=?", (self.run_id, key)).fetchone()
            if row is not None:
                if row["stage"] != stage or row["amount_cents"] != cents:
                    raise CostTrackerError("idempotency_key already recorded with different stage details")
                return self._receipt(row)
            spent = sum(row[0] for row in connection.execute("SELECT amount_cents FROM simulated_cost_events WHERE run_id=?", (self.run_id,)))
            if spent + cents > self._budget_cents:
                raise BudgetExceeded("stage exceeds the simulated run budget; actual API cost remains $0.00")
            cursor = connection.execute(
                "INSERT INTO simulated_cost_events(run_id,stage,amount_cents,idempotency_key,recorded_at) VALUES (?,?,?,?,?)",
                (self.run_id, stage, cents, key, datetime.now(timezone.utc).isoformat()),
            )
            return self._receipt(connection.execute("SELECT * FROM simulated_cost_events WHERE event_id=?", (cursor.lastrowid,)).fetchone())

    @property
    def total_simulated_cost(self) -> Decimal:
        return Decimal(self.summary()["simulated_total"])

    def summary(self) -> dict:
        with self._transaction() as connection:
            rows = connection.execute("SELECT * FROM simulated_cost_events WHERE run_id=? ORDER BY event_id", (self.run_id,)).fetchall()
            total = sum(row["amount_cents"] for row in rows)
            return {"run_id": self.run_id, "currency": "USD", "mode": "deterministic_simulation",
                    "simulated_budget": _usd(self._budget_cents), "simulated_total": _usd(total),
                    "simulated_remaining": _usd(self._budget_cents - total), "actual_cost": "0.00",
                    "provider_calls": 0, "daily_provider_controls_active": False,
                    "events": [self._receipt(row) for row in rows]}

    def close(self) -> None:
        if self._memory is not None:
            self._memory.close()

