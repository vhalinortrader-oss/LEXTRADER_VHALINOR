"""Fachada `CerebroArtificial` — inicializa todos os neurônios baseados em threads."""
from __future__ import annotations

import threading
import time
from typing import Any, Dict, Optional

from ..indicators.technical import FEATURE_COLUMNS
from ..models.ensemble import Ensemble
from ..models.lstm import LSTM_AVAILABLE
from ..models.random_forest import RandomForestModel
from ..utils import logger
from .aprendizado import NeuronioAprendizado
from .cerebro import (NeuronioAnalitico, NeuronioEstrategista, NeuronioExecutor,
                      NeuronioPercepcao, NeuronioPreditivo)
from .estado import EstadoGlobal
from .memoria import NeuronioMemoria


class CerebroArtificial:
    """Instancia todos os neurônios e mantém um loop de coordenação opcional."""

    def __init__(self, config_path: Optional[str] = None, config: Optional[Dict[str, Any]] = None,
                 provider=None, ensemble: Optional[Ensemble] = None) -> None:
        self.estado = EstadoGlobal()
        cfg = config or {}
        self.estado.registrar_config(cfg)
        self.estado.set("config.ativos", cfg.get("ativos", ["BTC-USD"]))
        self.estado.set("config.update_sec", cfg.get("update_sec", 60))
        self.estado.set("config.indicadores", cfg.get("indicadores", None))
        self.estado.set("config.regras", cfg.get("estrategia", {}).get("regras",
                                                                       ["cruzamento_sma", "rsi_macd", "bollinger_reversao"]))

        self.percepcao = NeuronioPercepcao(self.estado, provider=provider)
        self.analitico = NeuronioAnalitico(self.estado)

        if ensemble is None:
            ensemble = Ensemble([
                RandomForestModel(
                    n_estimators=int(cfg.get("modelos", {}).get("rf", {}).get("n_estimadores", 200)),
                    max_depth=int(cfg.get("modelos", {}).get("rf", {}).get("max_depth", 8)),
                ),
            ] + ([LSTM_AVAILABLE] if False else []))  # LSTM adicionado só se habilitado
            if cfg.get("modelos", {}).get("lstm", {}).get("habilitado", False) and LSTM_AVAILABLE:
                from ..models.lstm import LSTMModel
                ensemble.models.append(LSTMModel(
                    sequence_length=int(cfg.get("modelos", {}).get("lstm", {}).get("sequence_length", 60)),
                    epochs=int(cfg.get("modelos", {}).get("lstm", {}).get("epocas", 10)),
                ))

        self.preditivo = NeuronioPreditivo(
            self.estado, cfg.get("modelos", {}), ensemble, FEATURE_COLUMNS,
        )
        self.estrategista = NeuronioEstrategista(self.estado)
        self.executor = NeuronioExecutor(self.estado, cfg.get("risco", {}))
        self.memoria = NeuronioMemoria(self.estado)
        self.aprendizado = NeuronioAprendizado(
            self.estado, self.preditivo, self.estrategista,
            intervalo_seg=int(cfg.get("aprendizado", {}).get("verifica_a_cada_seg", 3600)),
            sharpe_limiar=float(cfg.get("aprendizado", {}).get("sharpe_limiar", 0.5)),
        )

    # ---- ciclo de vida ----
    def iniciar(self) -> None:
        logger.info("[cérebro] iniciando neurônios…")
        for n in (self.percepcao, self.analitico, self.memoria, self.aprendizado):
            n.start()

    def parar(self) -> None:
        logger.info("[cérebro] parando neurônios…")
        for n in (self.percepcao, self.analitico, self.memoria, self.aprendizado):
            try:
                n.stop()
            except Exception:
                pass
        for n in (self.percepcao, self.analitico, self.memoria, self.aprendizado):
            n.join(timeout=2)

    # ---- ciclo de coordenação ----
    def tick(self, ativo: str) -> Dict[str, Any]:
        """Um ciclo de coordenação para UM ativo: previsão → estratégia → execução."""
        self.preditivo.treinar(ativo, self.estado.get(f"analitico.{ativo}.features")) \
            if self.estado.get(f"analitico.{ativo}.features") is not None else None
        pred = self.preditivo.prever(ativo)
        decisao = self.estrategista.decidir(ativo)
        ordem = self.executor.executar(ativo)
        return {"previsao": pred, "decisao": decisao, "ordem": ordem}

    def loop(self, ativos: Optional[list] = None, intervalo_seg: float = 5.0) -> None:
        ativos = ativos or self.estado.get("config.ativos") or []
        try:
            while True:
                for a in ativos:
                    self.tick(a)
                time.sleep(float(intervalo_seg))
        except KeyboardInterrupt:
            self.parar()
