"""Neurônio de Memória — atualiza pesos via média móvel exponencial e persiste padrões."""
from __future__ import annotations

import json
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np

from ..config import data_dir
from ..utils import logger
from .cerebro import OrdemSimulada
from .estado import EstadoGlobal


class NeuronioMemoria(threading.Thread):
    """Mantém pesos adaptativos no `EstadoGlobal` e persiste episódios em SQLite."""

    def __init__(self, estado: EstadoGlobal, db_path: Optional[str | Path] = None) -> None:
        super().__init__(daemon=True, name="NeuronioMemoria")
        self.estado = estado
        self.db_path = Path(db_path) if db_path else (data_dir() / "cerebro_memoria.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._criar_tabelas()
        self._stop = threading.Event()
        self.janela_sharpe: Dict[str, list[float]] = {}

    def stop(self) -> None:
        self._stop.set()

    def _criar_tabelas(self) -> None:
        cur = self._conn.cursor()
        cur.executescript("""
        CREATE TABLE IF NOT EXISTS ordens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ativo TEXT, sinal INTEGER, tamanho REAL, preco_entrada REAL,
            stop_loss REAL, take_profit REAL, preco_saida REAL,
            lucro REAL, risco REAL, confianca REAL, sinal_origem TEXT,
            aberta_em TEXT, fechada_em TEXT, recompensa REAL
        );
        CREATE TABLE IF NOT EXISTS padroes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ativo TEXT, estado_entrada TEXT, recompensa REAL, criado_em TEXT
        );
        CREATE TABLE IF NOT EXISTS pesos_regras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ativo TEXT, regra TEXT, peso REAL, atualizado_em TEXT
        );
        """)
        self._conn.commit()

    # --- persistência ---
    def _salvar_ordem(self, o: OrdemSimulada, recompensa: float) -> None:
        cur = self._conn.cursor()
        cur.execute("""
        INSERT INTO ordens (ativo, sinal, tamanho, preco_entrada, stop_loss, take_profit,
            preco_saida, lucro, risco, confianca, sinal_origem, aberta_em, fechada_em, recompensa)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (o.ativo, o.sinal, o.tamanho, o.preco_entrada, o.stop_loss, o.take_profit,
              o.preco_saida, o.lucro, o.risco, o.confianca, o.sinal_origem,
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(o.aberta_em)) if o.aberta_em else None,
              time.strftime("%Y-%m-%d %H:%M:%S"), float(recompensa)))
        self._conn.commit()

    def _salvar_padrao(self, ativo: str, estado_entrada: Dict[str, Any], recompensa: float) -> None:
        cur = self._conn.cursor()
        cur.execute("INSERT INTO padroes (ativo, estado_entrada, recompensa, criado_em) VALUES (?,?,?,?)",
                    (ativo, json.dumps(estado_entrada, ensure_ascii=False), float(recompensa),
                     time.strftime("%Y-%m-%d %H:%M:%S")))
        self._conn.commit()

    def _atualizar_peso_regra(self, ativo: str, regra: str, peso: float) -> None:
        cur = self._conn.cursor()
        cur.execute("INSERT INTO pesos_regras (ativo, regra, peso, atualizado_em) VALUES (?,?,?,?)",
                    (ativo, regra, float(peso), time.strftime("%Y-%m-%d %H:%M:%S")))
        self._conn.commit()

    # --- ciclo de atualização ---
    def _atualizar_pesos(self, ativo: str, fonte: str, recompensa: float) -> None:
        chave = f"memoria.{ativo}.peso_{fonte}"
        atual = float(self.estado.get(chave, 1.0) or 1.0)
        novo = atual * 0.9 + recompensa * 0.1
        self.estado.set(chave, float(novo))

    def _atualizar_pesos_regras(self, ativo: str, detalhes: Dict[str, Any], recompensa: float) -> None:
        for regra, info in (detalhes or {}).items():
            chave = f"memoria.{ativo}.peso_regra_{regra}"
            atual = float(self.estado.get(chave, 1.0) or 1.0)
            sinal = float(info.get("sinal", 0)) if isinstance(info, dict) else 0.0
            # só atualiza peso se a regra contribuiu para o sinal final
            if sinal == 0:
                continue
            novo = atual * 0.9 + (recompensa * np.sign(sinal)) * 0.1
            self.estado.set(chave, float(novo))
            self._atualizar_peso_regra(ativo, regra, novo)

    def _atualizar_sharpe(self, ativo: str, retorno: float, fonte: str) -> None:
        chave = f"memoria.{ativo}.retornos_{fonte}"
        hist = list(self.estado.get(chave, []) or [])
        hist.append(float(retorno))
        if len(hist) > 100:
            hist = hist[-100:]
        self.estado.set(chave, hist)
        if len(hist) >= 10:
            arr = np.array(hist)
            mean = float(arr.mean())
            std = float(arr.std() or 1e-9)
            sharpe = mean / std
            self.estado.set(f"memoria.{ativo}.sharpe_{fonte}", sharpe)
            janela = self.janela_sharpe.setdefault(ativo, [])
            janela.append(sharpe)
            if len(janela) > 30:
                janela.pop(0)
            self.estado.set(f"memoria.{ativo}.sharpe_janela", float(np.mean(janela[-10:])) if janela else 0.0)

    # --- loop principal ---
    def run(self) -> None:
        while not self._stop.is_set():
            for ativo in self.estado.get("config.ativos") or []:
                ordem: Optional[OrdemSimulada] = self.estado.get(f"executor.{ativo}.ordem")
                if not ordem or not ordem.fechada:
                    continue
                retorno = (ordem.lucro / ordem.risco) if ordem.risco else 0.0
                self._salvar_ordem(ordem, retorno)
                self._salvar_padrao(ativo, {
                    "preco": ordem.preco_entrada, "sinal": ordem.sinal, "conf": ordem.confianca,
                }, retorno)
                self._atualizar_pesos(ativo, ordem.sinal_origem or "regra+ml", retorno)
                detalhes = self.estado.get(f"estrategista.{ativo}.detalhes") or {}
                self._atualizar_pesos_regras(ativo, detalhes, retorno)
                self._atualizar_sharpe(ativo, retorno, "regra+ml")
                # marca ordem como consumida
                self.estado.set(f"executor.{ativo}.ordem", None)
            self._stop.wait(1.0)
