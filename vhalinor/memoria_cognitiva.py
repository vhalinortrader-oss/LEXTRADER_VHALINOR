"""🧠 Memória Cognitiva — episódica, semântica e de trabalho com recuperação por similaridade."""
from __future__ import annotations

import json
import math
import sqlite3
import time
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Deque, Dict, List, Optional, Tuple

from .config import data_dir


@dataclass
class Episodio:
    """Um evento vivido pelo sistema: (contexto, ação, recompensa)."""
    contexto: Dict[str, Any]
    acao: str
    recompensa: float
    ts: float = field(default_factory=time.time)
    rotulos: List[str] = field(default_factory=list)


class MemoriaCognitiva:
    """Memória em três camadas: trabalho, episódica (SQLite) e semântica (vetores)."""

    def __init__(self, db_path: Optional[str | Path] = None) -> None:
        self.db_path = Path(db_path) if db_path else (
            data_dir() / "memoria_cognitiva.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(
            str(self.db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init()
        self.trabalho: Deque[Dict[str, Any]] = deque(maxlen=50)
        # (vetor, rótulo)
        self.semantica: List[Tuple[Dict[str, float], str]] = []

    def _init(self) -> None:
        cur = self._conn.cursor()
        cur.executescript("""
        CREATE TABLE IF NOT EXISTS episodica (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts REAL,
            contexto TEXT,
            acao TEXT,
            recompensa REAL,
            rotulos TEXT
        );
        CREATE TABLE IF NOT EXISTS semantica (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rotulo TEXT,
            vetor TEXT
        );
        """)
        self._conn.commit()

    # ----- trabalho -----
    def trabalhar(self, item: Dict[str, Any]) -> None:
        self.trabalho.append({"ts": time.time(), **item})

    # ----- episódica -----
    def registrar_episodio(self, ep: Episodio) -> int:
        cur = self._conn.cursor()
        cur.execute("INSERT INTO episodica (ts, contexto, acao, recompensa, rotulos) VALUES (?,?,?,?,?)",
                    (ep.ts, json.dumps(ep.contexto, ensure_ascii=False), ep.acao, float(ep.recompensa),
                     json.dumps(ep.rotulos, ensure_ascii=False)))
        self._conn.commit()
        return cur.lastrowid

    def ultimos_episodios(self, n: int = 20, rotulo: Optional[str] = None) -> List[Dict[str, Any]]:
        cur = self._conn.cursor()
        if rotulo:
            cur.execute("SELECT * FROM episodica WHERE rotulos LIKE ? ORDER BY id DESC LIMIT ?",
                        (f"%{rotulo}%", int(n)))
        else:
            cur.execute(
                "SELECT * FROM episodica ORDER BY id DESC LIMIT ?", (int(n),))
        return [dict(r) for r in cur.fetchall()]

    # ----- semântica (similaridade cosseno) -----
    def aprender_padrao(self, rotulo: str, vetor: Dict[str, float]) -> None:
        if not vetor:
            return
        self.semantica.append((dict(vetor), rotulo))
        cur = self._conn.cursor()
        cur.execute("INSERT INTO semantica (rotulo, vetor) VALUES (?, ?)",
                    (rotulo, json.dumps(vetor, ensure_ascii=False)))
        self._conn.commit()

    @staticmethod
    def _norma(v: Dict[str, float]) -> float:
        return math.sqrt(sum(x * x for x in v.values())) or 1.0

    def reconhecer(self, vetor: Dict[str, float], top: int = 3) -> List[Tuple[str, float]]:
        if not vetor or not self.semantica:
            return []
        n1 = self._norma(vetor)
        resultados: List[Tuple[str, float]] = []
        for v, rotulo in self.semantica:
            chaves = set(v.keys()) & set(vetor.keys())
            dot = sum(v[k] * vetor[k] for k in chaves)
            sim = dot / (n1 * self._norma(v) or 1.0)
            resultados.append((rotulo, float(sim)))
        resultados.sort(key=lambda x: x[1], reverse=True)
        return resultados[:top]

    def esquecer_antigos(self, manter: int = 5000) -> int:
        cur = self._conn.cursor()
        cur.execute("SELECT COUNT(*) AS c FROM episodica")
        total = int(cur.fetchone()["c"])
        if total <= manter:
            return 0
        apagar = total - manter
        cur.execute(
            "DELETE FROM episodica WHERE id IN (SELECT id FROM episodica ORDER BY id ASC LIMIT ?)", (apagar,))
        self._conn.commit()
        return apagar
