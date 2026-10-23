"""Durable, fail-closed spending reservations for the live Software Factory.

Money is stored as integer nanodollars. Rates are explicit USD per million
tokens, supplied by the configured provider route; this module has no price list.
Settled amounts are estimates from provider-reported usage, not provider invoices.
The daily cap uses UTC settlement dates and includes *every* unresolved reservation,
including calls started on a previous day. A timeout must remain uncertain until
provider usage or positive evidence of no charge is available.
"""
from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, localcontext
from fractions import Fraction
import json
import os
from pathlib import Path
import sqlite3
from typing import Callable, Iterator
import uuid


NANODOLLARS_PER_DOLLAR = 1_000_000_000
MAX_SQLITE_INTEGER = 2**63 - 1


class CostTrackerError(ValueError):
    """Invalid ledger operation or configuration."""


class BudgetExceeded(CostTrackerError):
    """The requested reservation would exceed a daily or run limit."""


class LedgerPolicyError(CostTrackerError):
    """Another client of the ledger uses a different spending policy."""


def _decimal(value: Decimal | str | int, name: str) -> Decimal:
    if isinstance(value, (bool, float)) or not isinstance(value, (Decimal, str, int)):
        raise CostTrackerError(f"{name} must be a Decimal, decimal string, or integer")
    try:
        parsed = Decimal(value)
    except (InvalidOperation, ValueError):
        raise CostTrackerError(f"{name} must be a finite nonnegative decimal") from None
    if not parsed.is_finite() or parsed < 0:
        raise CostTrackerError(f"{name} must be a finite nonnegative decimal")
    return parsed


def _units(value: Decimal | str | int, name: str, *, cap: bool = False) -> int:
    parsed = _decimal(value, name)
    if parsed > Decimal(MAX_SQLITE_INTEGER).scaleb(-9):
        raise CostTrackerError(f"{name} exceeds the ledger's monetary range")
    numerator, denominator = parsed.as_integer_ratio()
    scaled = numerator * NANODOLLARS_PER_DOLLAR
    # Limits round down, while reservations and usage round up. Neither may
    # understate an obligation or expand the user's configured allowance.
    return scaled // denominator if cap else (scaled + denominator - 1) // denominator


def _usd(units: int) -> str:
    with localcontext() as context:
        context.prec = 80
        return format(Decimal(units) / NANODOLLARS_PER_DOLLAR, ".9f")


def _tokens(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0 or value > MAX_SQLITE_INTEGER:
        raise CostTrackerError(f"{name} must be a nonnegative integer token count")
    return value


def estimated_cost(
    input_tokens: int,
    output_tokens: int,
    input_rate: Decimal | str | int,
    output_rate: Decimal | str | int,
) -> Decimal:
    """Return a conservative USD estimate, rounded upward to a nanodollar.

    Input tokens include any cached input. Charging these at the full input rate
    deliberately avoids assuming a cache discount that the provider may not grant.
    """
    incoming = _tokens(input_tokens, "input_tokens")
    outgoing = _tokens(output_tokens, "output_tokens")
    input_price = _decimal(input_rate, "input_rate")
    output_price = _decimal(output_rate, "output_rate")
    exact_units = (incoming * Fraction(input_price) + outgoing * Fraction(output_price)) * 1000
    rounded_units = (exact_units.numerator + exact_units.denominator - 1) // exact_units.denominator
    if rounded_units > MAX_SQLITE_INTEGER:
        raise CostTrackerError("usage cost exceeds the ledger's monetary range")
    with localcontext() as context:
        context.prec = 80
        return Decimal(rounded_units) / NANODOLLARS_PER_DOLLAR


class CostTracker:
    """Reserve before dispatch, then settle actual usage or retain uncertainty.

    Use the same database for all processes sharing a spending allowance. SQLite
    ``BEGIN IMMEDIATE`` serializes the check and reservation across processes.
    The first constructor fixes the ledger's daily policy; changing its limit
    requires an explicit new ledger or an audited database policy migration.
    A run's first reservation similarly fixes its optional run limit.
    """

    def __init__(
        self,
        path: Path | str,
        daily_limit: Decimal | str | int | None = None,
        run_limit: Decimal | str | int | None = None,
        run_id: str | None = None,
        *,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        configured_daily = daily_limit if daily_limit is not None else os.environ.get("MAX_DAILY_SPEND", "1.00")
        self.daily_limit_units = _units(configured_daily, "daily_limit", cap=True)
        self.run_limit_units = None if run_limit is None else _units(run_limit, "run_limit", cap=True)
        self.run_id = self._identifier(run_id or uuid.uuid4().hex, "run_id")
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        with self._connect() as connection:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS policy (
                    key TEXT PRIMARY KEY, value INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY, limit_units INTEGER
                );
                CREATE TABLE IF NOT EXISTS reservations (
                    reservation_id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    model TEXT NOT NULL,
                    reserved_units INTEGER NOT NULL CHECK(reserved_units >= 0),
                    status TEXT NOT NULL CHECK(status IN ('reserved','uncertain','settled','released')),
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    settled_day TEXT,
                    actual_units INTEGER,
                    receipt TEXT,
                    reason TEXT NOT NULL DEFAULT ''
                );
                CREATE INDEX IF NOT EXISTS reservations_run ON reservations(run_id);
                CREATE TABLE IF NOT EXISTS events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reservation_id TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    details TEXT NOT NULL
                );
            """)
        with self._transaction() as connection:
            connection.execute("INSERT OR IGNORE INTO policy(key,value) VALUES ('daily_limit',?)", (self.daily_limit_units,))
            policy = connection.execute("SELECT value FROM policy WHERE key='daily_limit'").fetchone()[0]
            if policy != self.daily_limit_units:
                raise LedgerPolicyError("daily_limit differs from the policy already recorded in this ledger")

    @staticmethod
    def _identifier(value: str, name: str) -> str:
        if not isinstance(value, str) or not value.strip() or len(value) > 512:
            raise CostTrackerError(f"{name} must be a nonempty string of at most 512 characters")
        return value

    def _now(self) -> tuple[str, str]:
        now = self.clock()
        if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
            raise CostTrackerError("clock must return a timezone-aware datetime")
        utc_now = now.astimezone(timezone.utc)
        return utc_now.isoformat(), utc_now.date().isoformat()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(str(self.path), timeout=30, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA busy_timeout=30000")
        try:
            yield connection
        finally:
            connection.close()

    @contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                yield connection
                connection.commit()
            except BaseException:
                connection.rollback()
                raise

    @staticmethod
    def _event(connection: sqlite3.Connection, reservation_id: str, kind: str, when: str, details: dict) -> None:
        connection.execute(
            "INSERT INTO events(reservation_id,kind,occurred_at,details) VALUES (?,?,?,?)",
            (reservation_id, kind, when, json.dumps(details, sort_keys=True)),
        )

    @staticmethod
    def _row(connection: sqlite3.Connection, reservation_id: str) -> sqlite3.Row:
        row = connection.execute("SELECT * FROM reservations WHERE reservation_id=?", (reservation_id,)).fetchone()
        if row is None:
            raise CostTrackerError("unknown reservation_id")
        return row

    @staticmethod
    def _exposure(connection: sqlite3.Connection, day: str, run_id: str) -> tuple[int, int, int, int]:
        daily_settled = daily_pending = run_settled = run_pending = 0
        for row in connection.execute("SELECT run_id,status,reserved_units,actual_units,settled_day FROM reservations"):
            if row["status"] in ("reserved", "uncertain"):
                daily_pending += row["reserved_units"]
                if row["run_id"] == run_id:
                    run_pending += row["reserved_units"]
            elif row["status"] == "settled":
                if row["settled_day"] == day:
                    daily_settled += row["actual_units"]
                if row["run_id"] == run_id:
                    run_settled += row["actual_units"]
        return daily_settled, daily_pending, run_settled, run_pending

    def reserve(
        self,
        role: str,
        model: str,
        max_cost: Decimal | str | int,
        run_id: str | None = None,
        reservation_id: str | None = None,
    ) -> str:
        """Atomically allocate the full request envelope before a paid call.

        An explicit reservation_id makes retries of *this ledger operation*
        idempotent. It does not authorize a second provider call with the same ID.
        """
        role = self._identifier(role, "role")
        model = self._identifier(model, "model")
        selected_run = self._identifier(run_id or self.run_id, "run_id")
        selected_id = self._identifier(reservation_id or uuid.uuid4().hex, "reservation_id")
        maximum = _units(max_cost, "max_cost")
        when, day = self._now()
        with self._transaction() as connection:
            existing = connection.execute("SELECT * FROM reservations WHERE reservation_id=?", (selected_id,)).fetchone()
            if existing is not None:
                if (existing["run_id"], existing["role"], existing["model"], existing["reserved_units"]) != (selected_run, role, model, maximum):
                    raise CostTrackerError("reservation_id was already used with different request details")
                return selected_id
            connection.execute("INSERT OR IGNORE INTO runs(run_id,limit_units) VALUES (?,?)", (selected_run, self.run_limit_units))
            run_policy = connection.execute("SELECT limit_units FROM runs WHERE run_id=?", (selected_run,)).fetchone()[0]
            if run_policy != self.run_limit_units:
                raise LedgerPolicyError("run_limit differs from this run's recorded policy")
            daily_settled, daily_pending, run_settled, run_pending = self._exposure(connection, day, selected_run)
            if daily_settled + daily_pending + maximum > self.daily_limit_units:
                raise BudgetExceeded("daily spending limit would be exceeded; no provider call is authorized")
            if run_policy is not None and run_settled + run_pending + maximum > run_policy:
                raise BudgetExceeded("run spending limit would be exceeded; no provider call is authorized")
            connection.execute(
                "INSERT INTO reservations(reservation_id,run_id,role,model,reserved_units,status,created_at,updated_at) VALUES (?,?,?,?,?,'reserved',?,?)",
                (selected_id, selected_run, role, model, maximum, when, when),
            )
            self._event(connection, selected_id, "reserved", when, {"maximum_usd": _usd(maximum), "run_id": selected_run})
        return selected_id

    def settle(
        self,
        reservation_id: str,
        input_tokens: int,
        output_tokens: int,
        input_rate: Decimal | str | int,
        output_rate: Decimal | str | int,
        cached_input_tokens: int = 0,
        provider_request_id: str = "",
        provider: str = "",
    ) -> dict:
        """Record actual reported token usage, including any reservation overrun.

        ``input_tokens`` is the total input, with cached tokens a subset. An
        overrun is never hidden or capped to the reservation; future requests
        see the true exposure and are blocked when a cap has been consumed.
        """
        incoming = _tokens(input_tokens, "input_tokens")
        outgoing = _tokens(output_tokens, "output_tokens")
        cached = _tokens(cached_input_tokens, "cached_input_tokens")
        if cached > incoming:
            raise CostTrackerError("cached_input_tokens cannot exceed total input_tokens")
        for value, name in ((provider_request_id, "provider_request_id"), (provider, "provider")):
            if not isinstance(value, str):
                raise CostTrackerError(f"{name} must be a string")
        input_price = _decimal(input_rate, "input_rate")
        output_price = _decimal(output_rate, "output_rate")
        actual = _units(estimated_cost(incoming, outgoing, input_price, output_price), "actual_cost")
        receipt = {
            "input_tokens": incoming, "output_tokens": outgoing, "cached_input_tokens": cached,
            "input_rate_per_million": str(input_price.normalize()), "output_rate_per_million": str(output_price.normalize()),
            "provider_request_id": provider_request_id, "provider": provider,
        }
        encoded_receipt = json.dumps(receipt, sort_keys=True)
        when, day = self._now()
        with self._transaction() as connection:
            row = self._row(connection, reservation_id)
            if row["status"] == "settled":
                if row["receipt"] != encoded_receipt:
                    raise CostTrackerError("reservation already settled with different usage")
                return self._public(row)
            if row["status"] == "released":
                raise CostTrackerError("cannot settle a released reservation")
            connection.execute(
                "UPDATE reservations SET status='settled',actual_units=?,receipt=?,settled_day=?,updated_at=? WHERE reservation_id=?",
                (actual, encoded_receipt, day, when, reservation_id),
            )
            self._event(connection, reservation_id, "settled", when, {
                **receipt, "estimated_usd": _usd(actual), "overrun": actual > row["reserved_units"],
                "usage_cost_is_provider_invoice": False,
            })
            return self._public(self._row(connection, reservation_id))

    def mark_uncertain(self, reservation_id: str, reason: str) -> dict:
        """Hold the maximum after dispatch when actual billing is unknown."""
        self._identifier(reason, "reason")
        when, _ = self._now()
        with self._transaction() as connection:
            row = self._row(connection, reservation_id)
            if row["status"] == "uncertain" and row["reason"] == reason:
                return self._public(row)
            if row["status"] not in ("reserved", "uncertain"):
                raise CostTrackerError("only outstanding reservations can become uncertain")
            connection.execute("UPDATE reservations SET status='uncertain',reason=?,updated_at=? WHERE reservation_id=?", (reason, when, reservation_id))
            self._event(connection, reservation_id, "uncertain", when, {"reason": reason})
            return self._public(self._row(connection, reservation_id))

    def release(self, reservation_id: str, reason: str = "known not charged", *, confirmed_not_charged: bool = False) -> dict:
        """Release a request cancelled before dispatch, or a confirmed no-charge call.

        Uncertain calls require explicit positive reconciliation; a timeout is
        never evidence that the provider did not charge for work.
        """
        self._identifier(reason, "reason")
        when, _ = self._now()
        with self._transaction() as connection:
            row = self._row(connection, reservation_id)
            if row["status"] == "released":
                return self._public(row)
            if row["status"] == "settled":
                raise CostTrackerError("cannot release settled usage")
            if row["status"] == "uncertain" and confirmed_not_charged is not True:
                raise CostTrackerError("uncertain usage requires confirmed_not_charged=True and reconciliation evidence")
            connection.execute("UPDATE reservations SET status='released',reason=?,updated_at=? WHERE reservation_id=?", (reason, when, reservation_id))
            self._event(connection, reservation_id, "released", when, {"reason": reason, "confirmed_not_charged": confirmed_not_charged})
            return self._public(self._row(connection, reservation_id))

    @staticmethod
    def _public(row: sqlite3.Row) -> dict:
        return {
            "reservation_id": row["reservation_id"], "run_id": row["run_id"], "role": row["role"],
            "model": row["model"], "status": row["status"], "maximum_usd": _usd(row["reserved_units"]),
            "estimated_usd": None if row["actual_units"] is None else _usd(row["actual_units"]),
            "created_at": row["created_at"], "updated_at": row["updated_at"], "settled_day": row["settled_day"],
            "usage": None if row["receipt"] is None else json.loads(row["receipt"]), "reason": row["reason"],
        }

    def summary(self, run_id: str | None = None) -> dict:
        selected_run = self._identifier(run_id or self.run_id, "run_id")
        _, day = self._now()
        with self._transaction() as connection:
            daily_settled, daily_pending, run_settled, run_pending = self._exposure(connection, day, selected_run)
            policy_row = connection.execute("SELECT limit_units FROM runs WHERE run_id=?", (selected_run,)).fetchone()
            run_limit = self.run_limit_units if policy_row is None else policy_row[0]
            reservations = [self._public(row) for row in connection.execute("SELECT * FROM reservations WHERE run_id=? ORDER BY created_at,reservation_id", (selected_run,))]
            return {
                "currency": "USD", "utc_day": day, "daily_limit": _usd(self.daily_limit_units),
                "daily_settled_estimate": _usd(daily_settled), "pending_maximum": _usd(daily_pending),
                "daily_remaining": _usd(max(0, self.daily_limit_units - daily_settled - daily_pending)),
                "daily_over_limit": daily_settled + daily_pending > self.daily_limit_units,
                "run_id": selected_run, "run_limit": None if run_limit is None else _usd(run_limit),
                "run_settled_estimate": _usd(run_settled), "run_pending_maximum": _usd(run_pending),
                "run_remaining": None if run_limit is None else _usd(max(0, run_limit - run_settled - run_pending)),
                "run_over_limit": run_limit is not None and run_settled + run_pending > run_limit,
                "usage_cost_is_provider_invoice": False,
                "cache_pricing": "cached input conservatively priced at the full input rate",
                "reservations": reservations,
            }

    def events(self, run_id: str | None = None) -> list[dict]:
        with self._connect() as connection:
            if run_id is None:
                rows = connection.execute("SELECT * FROM events ORDER BY event_id").fetchall()
            else:
                rows = connection.execute("SELECT e.* FROM events e JOIN reservations r USING(reservation_id) WHERE r.run_id=? ORDER BY e.event_id", (run_id,)).fetchall()
            return [{"event_id": row["event_id"], "reservation_id": row["reservation_id"], "kind": row["kind"], "occurred_at": row["occurred_at"], "details": json.loads(row["details"])} for row in rows]
