"""SQLite evidence for the deterministic factory's real local operations."""
from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS factory_runs (
 run_id TEXT PRIMARY KEY, mode TEXT NOT NULL, request_sha256 TEXT NOT NULL,
 status TEXT NOT NULL, branch TEXT, created_at TEXT NOT NULL, config_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS artifacts (
 artifact_id TEXT PRIMARY KEY, run_id TEXT NOT NULL REFERENCES factory_runs(run_id),
 sha256 TEXT NOT NULL, source_commit TEXT, path TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS stage_approvals (
 approval_id INTEGER PRIMARY KEY AUTOINCREMENT,
 run_id TEXT NOT NULL REFERENCES factory_runs(run_id), stage TEXT NOT NULL,
 subject_sha256 TEXT NOT NULL, approved INTEGER NOT NULL CHECK(approved IN (0,1)),
 actor TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS reviews (
 review_id INTEGER PRIMARY KEY AUTOINCREMENT,
 run_id TEXT NOT NULL REFERENCES factory_runs(run_id),
 artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id), role TEXT NOT NULL,
 approved INTEGER NOT NULL CHECK(approved IN (0,1)), issues_json TEXT NOT NULL,
 summary TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS qa_cases (
 case_id INTEGER PRIMARY KEY AUTOINCREMENT,
 run_id TEXT NOT NULL REFERENCES factory_runs(run_id),
 artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
 name TEXT NOT NULL, selector TEXT NOT NULL, assertion TEXT NOT NULL,
 expected TEXT NOT NULL, passed INTEGER NOT NULL CHECK(passed IN (0,1)), observed TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS deployments (
 deployment_id INTEGER PRIMARY KEY AUTOINCREMENT,
 run_id TEXT NOT NULL REFERENCES factory_runs(run_id),
 artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
 approval_id INTEGER NOT NULL REFERENCES stage_approvals(approval_id),
 target_path TEXT NOT NULL, sha256 TEXT NOT NULL, commit_sha TEXT NOT NULL,
 status TEXT NOT NULL CHECK(status IN ('PREPARED','PUBLISHED')), created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS factory_events (
 event_id INTEGER PRIMARY KEY AUTOINCREMENT,
 run_id TEXT NOT NULL REFERENCES factory_runs(run_id),
 stage TEXT NOT NULL, payload_json TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TRIGGER IF NOT EXISTS publication_requires_matching_approval
BEFORE INSERT ON deployments
WHEN NOT EXISTS (
 SELECT 1 FROM stage_approvals AS approval
 JOIN artifacts AS artifact ON artifact.artifact_id=NEW.artifact_id
 WHERE approval.approval_id=NEW.approval_id AND approval.run_id=NEW.run_id
   AND approval.approved=1 AND approval.stage='publish'
   AND approval.subject_sha256=NEW.sha256 AND artifact.run_id=NEW.run_id
   AND artifact.sha256=NEW.sha256 AND artifact.source_commit=NEW.commit_sha
)
BEGIN SELECT RAISE(ABORT, 'Publication requires matching approval, artifact hash and commit'); END;
"""


class EvidenceStore:
    def __init__(self, path: Path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as database:
            database.executescript(SCHEMA)

    @contextmanager
    def connection(self):
        database = sqlite3.connect(self.path, timeout=30)
        database.row_factory = sqlite3.Row
        database.execute("PRAGMA foreign_keys=ON")
        try:
            with database:
                yield database
        finally:
            database.close()

    def add(self, table: str, **values):
        # Table/column identifiers come exclusively from trusted orchestration.
        allowed = {
            "factory_runs", "artifacts", "stage_approvals", "reviews", "qa_cases",
            "deployments", "factory_events",
        }
        if table not in allowed:
            raise ValueError("Unknown evidence table")
        with self.connection() as database:
            columns = {row[1] for row in database.execute(f"PRAGMA table_info({table})")}
            if not values or not set(values) <= columns:
                raise ValueError("Unknown evidence column")
            cursor = database.execute(
                f"INSERT INTO {table} ({','.join(values)}) VALUES ({','.join('?' for _ in values)})",
                tuple(values.values()),
            )
            return cursor.lastrowid

    def event(self, run_id: str, stage: str, data: dict):
        return self.add("factory_events", run_id=run_id, stage=stage,
                        payload_json=json.dumps(data, sort_keys=True), created_at=timestamp())

    def status(self, run_id: str, status: str, branch: str | None = None):
        with self.connection() as database:
            database.execute("UPDATE factory_runs SET status=?,branch=COALESCE(?,branch) WHERE run_id=?",
                             (status, branch, run_id))

    def rows(self, table: str, run_id: str) -> list[dict]:
        if table not in {"factory_runs", "artifacts", "stage_approvals", "reviews", "qa_cases", "deployments", "factory_events"}:
            raise ValueError("Unknown evidence table")
        with self.connection() as database:
            return [dict(row) for row in database.execute(f"SELECT * FROM {table} WHERE run_id=?", (run_id,))]
