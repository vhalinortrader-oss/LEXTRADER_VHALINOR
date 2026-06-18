"""Neurônio de Aprendizado — dispara re-treino e otimização por gatilho de Sharpe."""
from __future__ import annotations

import threading
import time
from typing import Any, Dict

from ..utils import logger
from .estado import EstadoGlobal
from .memoria import NeuronioMemoria


class NeuronioAprendizado(threading.Thread):
    def __init__(self, estado: EstadoGlobal, preditivo, estrategista,
                 intervalo_seg: int = 3600, sharpe_limiar: float = 0.5) -> None:
        super().__init__(daemon=True, name="NeuronioAprendizado")
        self.estado = estado
        self.preditivo = preditivo
        self.estrategista = estrategista
        self.intervalo_seg = int(intervalo_seg)
        self.sharpe_limiar = float(sharpe_limiar)
        self._stop = threading.Event()

    def stop(self) -> None:
        self._stop.set()

    def run(self) -> None:
        while not self._stop.is_set():
            for ativo in self.estado.get("config.ativos") or []:
                sharpe = float(self.estado.get(f"memoria.{ativo}.sharpe_janela", 0.0) or 0.0)
                n_amostras = int(self.estado.get(f"memoria.{ativo}.n_amostras", 0) or 0)
                if sharpe < self.sharpe_limiar and n_amostras >= 100:
                    try:
                        df = self.estado.get(f"analitico.{ativo}.features")
                        if df is not None and len(df) >= 200:
                            logger.info(f"[aprendizado] re-treinando modelos para {ativo} (sharpe={sharpe:.2f})")
                            self.preditivo.treinar(ativo, df)
                            self.estrategista.otimizar_pesos(ativo)
                    except Exception as exc:  # pragma: no cover
                        logger.warning(f"[aprendizado] {ativo}: {exc}")
            self._stop.wait(self.intervalo_seg)
