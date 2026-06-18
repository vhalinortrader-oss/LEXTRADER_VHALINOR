"""Persistência SQLite — memória, sinais e trades."""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..config import data_dir


@dataclass
class TradeRecord:
    symbol: str
    side: str
    size: float
    entry: float
    exit_price: float
    pnl: float
    opened_at: str
    closed_at: str
    reason: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SignalRecord:
    symbol: str
    action: str
    score: float
    confidence: float
    rationale: str
    created_at: str
    extra: Dict[str, Any] = field(default_factory=dict)


class Database:
    def __init__(self, db_path: Optional[str | Path] = None) -> None:
        if db_path is None:
            db_path = data_dir() / "lextrader.db"
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self._conn.cursor()
        cur.executescript("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            action TEXT NOT NULL,
            score REAL,
            confidence REAL,
            rationale TEXT,
            created_at TEXT,
            extra TEXT
        );
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            side TEXT NOT NULL,
            size REAL,
            entry REAL,
            exit_price REAL,
            pnl REAL,
            opened_at TEXT,
            closed_at TEXT,
            reason TEXT,
            extra TEXT
        );
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL,
            key TEXT,
            value TEXT,
            created_at TEXT
        );
        CREATE TABLE IF NOT EXISTS model_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            metric TEXT,
            value REAL,
            created_at TEXT
        );
        """)
        self._conn.commit()

    # --- sinais ---
    def log_signal(self, rec: SignalRecord) -> int:
        cur = self._conn.cursor()
        cur.execute(
            "INSERT INTO signals (symbol, action, score, confidence, rationale, created_at, extra) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (rec.symbol, rec.action, rec.score, rec.confidence, rec.rationale,
             rec.created_at, json.dumps(rec.extra, ensure_ascii=False)),
        )
        self._conn.commit()
        return cur.lastrowid

    def recent_signals(self, limit: int = 100) -> List[Dict[str, Any]]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM signals ORDER BY id DESC LIMIT ?", (int(limit),))
        return [dict(r) for r in cur.fetchall()]

    # --- trades ---
    def log_trade(self, rec: TradeRecord) -> int:
        cur = self._conn.cursor()
        cur.execute(
            "INSERT INTO trades (symbol, side, size, entry, exit_price, pnl, opened_at, closed_at, reason, extra) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (rec.symbol, rec.side, rec.size, rec.entry, rec.exit_price, rec.pnl,
             rec.opened_at, rec.closed_at, rec.reason, json.dumps(rec.extra, ensure_ascii=False)),
        )
        self._conn.commit()
        return cur.lastrowid

    def closed_trades(self, limit: int = 200) -> List[Dict[str, Any]]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM trades WHERE exit_price IS NOT NULL ORDER BY id DESC LIMIT ?", (int(limit),))
        return [dict(r) for r in cur.fetchall()]

    # --- memória ---
    def remember(self, kind: str, key: str, value: Any) -> int:
        cur = self._conn.cursor()
        cur.execute(
            "INSERT INTO memory (kind, key, value, created_at) VALUES (?, ?, ?, datetime('now'))",
            (kind, key, json.dumps(value, ensure_ascii=False)),
        )
        self._conn.commit()
        return cur.lastrowid

    def recall(self, kind: str, key: str) -> Optional[Any]:
        cur = self._conn.cursor()
        cur.execute("SELECT value FROM memory WHERE kind = ? AND key = ? ORDER BY id DESC LIMIT 1", (kind, key))
        row = cur.fetchone()
        if not row:
            return None
        try:
            return json.loads(row["value"])
        except Exception:
            return row["value"]

    # --- métricas ---
    def log_metric(self, model: str, metric: str, value: float) -> None:
        cur = self._conn.cursor()
        cur.execute(
            "INSERT INTO model_metrics (model, metric, value, created_at) VALUES (?, ?, ?, datetime('now'))",
            (model, metric, float(value)),
        )
        self._conn.commit()

    def close(self) -> None:
        try:
            self._conn.close()
        except Exception:
            pass
