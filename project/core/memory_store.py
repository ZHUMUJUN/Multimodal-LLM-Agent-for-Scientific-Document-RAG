import json
import os
import sqlite3
import threading
import uuid
from datetime import datetime, timezone
from typing import Any


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json_dumps(value: Any) -> str:
    return json.dumps(value or {}, ensure_ascii=False, sort_keys=True, default=str)


class MemoryStore:
    """SQLite-backed run trace and lightweight memory store for the agent harness."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        db_dir = os.path.dirname(os.path.abspath(db_path))
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        with self._lock:
            self._conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    session_id TEXT,
                    collection TEXT,
                    message TEXT,
                    active_skill TEXT,
                    model TEXT,
                    retrieval_mode TEXT,
                    resolved_retrieval_mode TEXT,
                    status TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    ended_at TEXT,
                    answer TEXT,
                    summary_json TEXT NOT NULL DEFAULT '{}'
                );

                CREATE TABLE IF NOT EXISTS run_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    event TEXT NOT NULL,
                    node TEXT,
                    tool_name TEXT,
                    payload_json TEXT NOT NULL DEFAULT '{}',
                    FOREIGN KEY(run_id) REFERENCES runs(run_id)
                );

                CREATE INDEX IF NOT EXISTS idx_run_events_run_id ON run_events(run_id, id);
                CREATE INDEX IF NOT EXISTS idx_run_events_event ON run_events(event);

                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scope TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    kind TEXT NOT NULL DEFAULT 'semantic',
                    importance REAL NOT NULL DEFAULT 0.5,
                    expires_at TEXT,
                    access_count INTEGER NOT NULL DEFAULT 0,
                    last_accessed_at TEXT,
                    source_run_id TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(scope, key)
                );

                CREATE INDEX IF NOT EXISTS idx_memories_scope ON memories(scope);
                CREATE INDEX IF NOT EXISTS idx_memories_kind ON memories(kind);

                CREATE TABLE IF NOT EXISTS tool_approvals (
                    approval_id TEXT PRIMARY KEY,
                    run_id TEXT,
                    tool_name TEXT NOT NULL,
                    risk TEXT NOT NULL,
                    args_json TEXT NOT NULL DEFAULT '{}',
                    reason TEXT,
                    status TEXT NOT NULL DEFAULT 'pending',
                    requested_at TEXT NOT NULL,
                    resolved_at TEXT,
                    resolved_by TEXT,
                    resolution_note TEXT
                );

                CREATE INDEX IF NOT EXISTS idx_tool_approvals_run_id ON tool_approvals(run_id);
                CREATE INDEX IF NOT EXISTS idx_tool_approvals_status ON tool_approvals(status);
                """
            )
            self._ensure_column("memories", "importance", "REAL NOT NULL DEFAULT 0.5")
            self._ensure_column("memories", "expires_at", "TEXT")
            self._ensure_column("memories", "access_count", "INTEGER NOT NULL DEFAULT 0")
            self._ensure_column("memories", "last_accessed_at", "TEXT")
            self._conn.commit()

    def _ensure_column(self, table: str, column: str, ddl: str) -> None:
        columns = {
            row["name"]
            for row in self._conn.execute(f"PRAGMA table_info({table})").fetchall()
        }
        if column not in columns:
            self._conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}")

    def close(self) -> None:
        with self._lock:
            self._conn.close()

    def start_run(
        self,
        *,
        session_id: str,
        collection: str,
        message: str,
        active_skill: str | None = None,
        model: str | None = None,
        retrieval_mode: str | None = None,
        resolved_retrieval_mode: str | None = None,
    ) -> str:
        run_id = str(uuid.uuid4())
        with self._lock:
            self._conn.execute(
                """
                INSERT INTO runs (
                    run_id, session_id, collection, message, active_skill, model,
                    retrieval_mode, resolved_retrieval_mode, status, started_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    session_id,
                    collection,
                    message,
                    active_skill,
                    model,
                    retrieval_mode,
                    resolved_retrieval_mode,
                    "running",
                    _utc_now(),
                ),
            )
            self._conn.commit()
        return run_id

    def update_run(self, run_id: str, **fields: Any) -> None:
        allowed = {
            "active_skill",
            "model",
            "retrieval_mode",
            "resolved_retrieval_mode",
            "status",
            "answer",
            "summary_json",
            "ended_at",
        }
        updates = {key: value for key, value in fields.items() if key in allowed}
        if not updates:
            return
        assignments = ", ".join(f"{key} = ?" for key in updates)
        values = list(updates.values()) + [run_id]
        with self._lock:
            self._conn.execute(f"UPDATE runs SET {assignments} WHERE run_id = ?", values)
            self._conn.commit()

    def finish_run(
        self,
        run_id: str,
        *,
        status: str,
        answer: str = "",
        summary: dict | None = None,
        **fields: Any,
    ) -> None:
        payload = {
            "status": status,
            "ended_at": _utc_now(),
            "answer": answer,
            "summary_json": _json_dumps(summary),
            **fields,
        }
        self.update_run(run_id, **payload)

    def record_event(
        self,
        run_id: str,
        event: str,
        *,
        node: str | None = None,
        tool_name: str | None = None,
        payload: dict | None = None,
        **payload_fields: Any,
    ) -> None:
        event_payload = dict(payload or {})
        event_payload.update(payload_fields)
        node = node or event_payload.get("node")
        tool_name = tool_name or event_payload.get("tool_name") or event_payload.get("tool")
        with self._lock:
            self._conn.execute(
                """
                INSERT INTO run_events (run_id, timestamp, event, node, tool_name, payload_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (run_id, _utc_now(), event, node, tool_name, _json_dumps(event_payload)),
            )
            self._conn.commit()

    def record_logged_event(self, run_id: str, event: str, fields: dict) -> None:
        self.record_event(run_id, event, payload=fields)

    def write_memory(
        self,
        *,
        scope: str,
        key: str,
        value: str,
        kind: str = "semantic",
        importance: float = 0.5,
        ttl_seconds: int | None = None,
        expires_at: str | None = None,
        source_run_id: str | None = None,
    ) -> int:
        now = _utc_now()
        if ttl_seconds is not None:
            expires_at = datetime.fromtimestamp(datetime.now(timezone.utc).timestamp() + ttl_seconds, timezone.utc).isoformat()
        importance = max(0.0, min(1.0, float(importance)))
        with self._lock:
            self._conn.execute(
                """
                INSERT INTO memories (
                    scope, key, value, kind, importance, expires_at, source_run_id, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(scope, key) DO UPDATE SET
                    value = excluded.value,
                    kind = excluded.kind,
                    importance = excluded.importance,
                    expires_at = excluded.expires_at,
                    source_run_id = excluded.source_run_id,
                    updated_at = excluded.updated_at
                """,
                (scope, key, value, kind, importance, expires_at, source_run_id, now, now),
            )
            row = self._conn.execute(
                "SELECT id FROM memories WHERE scope = ? AND key = ?",
                (scope, key),
            ).fetchone()
            self._conn.commit()
        return int(row["id"])

    def search_memories(self, query: str, *, scope: str | None = None, limit: int = 10) -> list[dict]:
        pattern = f"%{query.strip()}%" if query.strip() else "%"
        now = _utc_now()
        params: list[Any] = [pattern, pattern, now]
        where = "(key LIKE ? OR value LIKE ?) AND (expires_at IS NULL OR expires_at > ?)"
        if scope:
            where += " AND scope = ?"
            params.append(scope)
        params.append(limit)
        with self._lock:
            rows = self._conn.execute(
                f"""
                SELECT id, scope, key, value, kind, source_run_id, created_at, updated_at
                    , importance, expires_at, access_count, last_accessed_at
                FROM memories
                WHERE {where}
                ORDER BY importance DESC, updated_at DESC
                LIMIT ?
                """,
                params,
            ).fetchall()
            ids = [int(row["id"]) for row in rows]
            if ids:
                placeholders = ",".join("?" for _ in ids)
                self._conn.execute(
                    f"""
                    UPDATE memories
                    SET access_count = access_count + 1, last_accessed_at = ?
                    WHERE id IN ({placeholders})
                    """,
                    [now, *ids],
                )
                self._conn.commit()
        return [dict(row) for row in rows]

    def prune_memories(self, *, max_importance: float | None = None, expired_only: bool = True) -> int:
        clauses = []
        params: list[Any] = []
        if expired_only:
            clauses.append("expires_at IS NOT NULL AND expires_at <= ?")
            params.append(_utc_now())
        if max_importance is not None:
            clauses.append("importance <= ?")
            params.append(max_importance)
        if not clauses:
            return 0
        where = " OR ".join(f"({clause})" for clause in clauses)
        with self._lock:
            cursor = self._conn.execute(f"DELETE FROM memories WHERE {where}", params)
            self._conn.commit()
        return int(cursor.rowcount or 0)

    def delete_memory(self, memory_id: int) -> bool:
        with self._lock:
            cursor = self._conn.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            self._conn.commit()
        return bool(cursor.rowcount)

    def get_run(self, run_id: str) -> dict | None:
        with self._lock:
            row = self._conn.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
        if not row:
            return None
        result = dict(row)
        result["summary"] = json.loads(result.pop("summary_json") or "{}")
        return result

    def get_run_events(self, run_id: str) -> list[dict]:
        with self._lock:
            rows = self._conn.execute(
                """
                SELECT id, run_id, timestamp, event, node, tool_name, payload_json
                FROM run_events
                WHERE run_id = ?
                ORDER BY id ASC
                """,
                (run_id,),
            ).fetchall()

        events = []
        for row in rows:
            item = dict(row)
            item["payload"] = json.loads(item.pop("payload_json") or "{}")
            events.append(item)
        return events

    def list_recent_runs(self, limit: int = 20) -> list[dict]:
        with self._lock:
            rows = self._conn.execute(
                """
                SELECT run_id, session_id, collection, active_skill, model, status, started_at, ended_at
                FROM runs
                ORDER BY started_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def export_run(self, run_id: str) -> dict:
        run = self.get_run(run_id)
        if run is None:
            raise KeyError(f"Unknown run_id: {run_id}")
        return {"run": run, "events": self.get_run_events(run_id)}

    def create_tool_approval(
        self,
        *,
        approval_id: str,
        run_id: str | None,
        tool_name: str,
        risk: str,
        args: dict,
        reason: str,
    ) -> dict:
        now = _utc_now()
        with self._lock:
            self._conn.execute(
                """
                INSERT INTO tool_approvals (
                    approval_id, run_id, tool_name, risk, args_json, reason, status, requested_at
                )
                VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)
                ON CONFLICT(approval_id) DO NOTHING
                """,
                (approval_id, run_id, tool_name, risk, _json_dumps(args), reason, now),
            )
            self._conn.commit()
        approval = self.get_tool_approval(approval_id)
        return approval or {
            "approval_id": approval_id,
            "run_id": run_id,
            "tool_name": tool_name,
            "risk": risk,
            "args": args,
            "reason": reason,
            "status": "pending",
            "requested_at": now,
        }

    def get_tool_approval(self, approval_id: str) -> dict | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM tool_approvals WHERE approval_id = ?",
                (approval_id,),
            ).fetchone()
        if not row:
            return None
        item = dict(row)
        item["args"] = json.loads(item.pop("args_json") or "{}")
        return item

    def list_tool_approvals(
        self,
        *,
        status: str | None = None,
        run_id: str | None = None,
        limit: int = 50,
    ) -> list[dict]:
        clauses = []
        params: list[Any] = []
        if status:
            clauses.append("status = ?")
            params.append(status)
        if run_id:
            clauses.append("run_id = ?")
            params.append(run_id)
        where = "WHERE " + " AND ".join(clauses) if clauses else ""
        params.append(limit)
        with self._lock:
            rows = self._conn.execute(
                f"""
                SELECT * FROM tool_approvals
                {where}
                ORDER BY requested_at DESC
                LIMIT ?
                """,
                params,
            ).fetchall()
        approvals = []
        for row in rows:
            item = dict(row)
            item["args"] = json.loads(item.pop("args_json") or "{}")
            approvals.append(item)
        return approvals

    def resolve_tool_approval(
        self,
        approval_id: str,
        *,
        status: str,
        resolved_by: str = "user",
        note: str = "",
    ) -> dict | None:
        if status not in {"approved", "rejected"}:
            raise ValueError("status must be approved or rejected")
        with self._lock:
            self._conn.execute(
                """
                UPDATE tool_approvals
                SET status = ?, resolved_at = ?, resolved_by = ?, resolution_note = ?
                WHERE approval_id = ?
                """,
                (status, _utc_now(), resolved_by, note, approval_id),
            )
            self._conn.commit()
        return self.get_tool_approval(approval_id)

    def is_tool_approved(self, approval_id: str) -> bool:
        approval = self.get_tool_approval(approval_id)
        return bool(approval and approval.get("status") == "approved")
