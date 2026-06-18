"""Aprendizado contínuo: monitora acertos, dispara re-treino e atualiza ensemble."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from .config import models_dir
from .models.base import BaseModel
from .models.ensemble import Ensemble
from .utils import logger


@dataclass
class FeedbackEvent:
    symbol: str
    action: str          # BUY / SELL
    per_model: Dict[str, float]   # nome -> prob_up previsto
    actual_return: float          # retorno realizado após a decisão


class LearningLoop:
    """Mantém o ensemble calibrado e dispara re-treino quando necessário."""

    def __init__(self, ensemble: Ensemble, base_models: List[BaseModel],
                 feature_cols: List[str], retrain_every: int = 50,
                 min_samples: int = 200) -> None:
        self.ensemble = ensemble
        self.base_models = base_models
        self.feature_cols = list(feature_cols)
        self.retrain_every = int(retrain_every)
        self.min_samples = int(min_samples)
        self.signals_since_train = 0
        self.last_metrics: Dict[str, float] = {}

    def feedback(self, event: FeedbackEvent) -> None:
        """Informa ao ensemble qual modelo acertou / errou o sinal."""
        for name, prob in (event.per_model or {}).items():
            predicted_up = prob > 0.5
            actual_up = event.actual_return > 0
            self.ensemble.update(name, predicted_up == actual_up)
        self.signals_since_train += 1
        logger.debug(f"[learning] feedback registrado, sinais desde último treino={self.signals_since_train}")

    def should_retrain(self) -> bool:
        return self.signals_since_train >= self.retrain_every

    def retrain(self, df: pd.DataFrame) -> Dict[str, float]:
        """Re-treina todos os modelos base. Retorna métricas simples."""
        n = len(df)
        if n < self.min_samples:
            logger.info(f"[learning] ainda sem dados suficientes ({n}<{self.min_samples}).")
            return {}
        metrics: Dict[str, float] = {}
        for m in self.base_models:
            try:
                m.fit(df, self.feature_cols)
                metrics[m.name] = float(getattr(m, "n_estimators", 0))  # proxy
                path = models_dir() / f"{m.name.lower()}_{df.attrs.get('symbol', 'asset')}.joblib"
                try:
                    m.save(path)
                except Exception as exc:  # LSTM pode não ter persistência sem torch
                    logger.debug(f"[learning] não foi possível salvar {m.name}: {exc}")
            except Exception as exc:  # pragma: no cover
                logger.warning(f"[learning] falha ao treinar {m.name}: {exc}")
        self.signals_since_train = 0
        self.last_metrics = metrics
        return metrics
