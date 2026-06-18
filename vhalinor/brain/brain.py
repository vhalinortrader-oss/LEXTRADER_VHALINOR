"""Cérebro central — agrega sinais dos neurônios em uma decisão final."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np

from ..utils import logger
from .neuron import Neuron, NeuronSignal
from .technical_neurons import (
    RSINeuron, MACDNeuron, BollingerNeuron, TrendNeuron,
    VolatilityNeuron, VolumeNeuron, MLNeuron, SentimentNeuron,
)


@dataclass
class BrainDecision:
    symbol: str
    action: str          # "BUY" | "SELL" | "HOLD"
    score: float         # [-1, 1] — soma ponderada dos sinais
    confidence: float    # [0, 1]
    signals: List[NeuronSignal] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    rationale: str = ""


class Brain:
    """Cérebro central que orquestra os neurônios especializados."""

    def __init__(self, config: Optional[Dict[str, Any]] = None, use_ml: bool = True) -> None:
        self.config = config or {}
        self.use_ml = use_ml
        self.neurons: List[Neuron] = [
            RSINeuron(),
            MACDNeuron(),
            BollingerNeuron(),
            TrendNeuron(),
            VolatilityNeuron(),
            VolumeNeuron(),
        ]
        if use_ml:
            self.neurons.append(MLNeuron())
        self.neurons.append(SentimentNeuron())

        dec = self.config.get("decision", {}) or {}
        self.buy_threshold = float(dec.get("buy_threshold", 0.6))
        self.sell_threshold = float(dec.get("sell_threshold", 0.4))
        self.min_confidence = float(dec.get("min_confidence", 0.55))

    def think(self, context: Dict[str, Any]) -> BrainDecision:
        """Processa o contexto de mercado e retorna a decisão agregada."""
        signals: List[NeuronSignal] = []
        for n in self.neurons:
            try:
                sig = n.process(context)
                sig.weight = n.weight
            except Exception as exc:  # pragma: no cover
                logger.warning(f"Neuron {n.name} falhou: {exc}")
                sig = NeuronSignal(n.name, 0.0, 0.0, {"error": str(exc)}, weight=n.weight)
            signals.append(sig)
            n.last_signal = sig

        total_w = sum(max(s.weight, 0.0) * max(s.confidence, 0.05) for s in signals)
        if total_w <= 0:
            score, confidence = 0.0, 0.0
        else:
            score = sum(s.weight * s.score * s.confidence for s in signals) / total_w
            confidence = sum(s.weight * s.confidence for s in signals) / sum(s.weight for s in signals)

        score = float(np.clip(score, -1, 1))
        confidence = float(np.clip(confidence, 0, 1))

        if confidence < self.min_confidence:
            action = "HOLD"
        elif score >= self.buy_threshold:
            action = "BUY"
        elif score <= self.sell_threshold:
            action = "SELL"
        else:
            action = "HOLD"

        rationale = self._explain(signals, score, confidence, action)
        return BrainDecision(
            symbol=context.get("symbol", "?"),
            action=action,
            score=score,
            confidence=confidence,
            signals=signals,
            context=context,
            rationale=rationale,
        )

    def _explain(self, signals: List[NeuronSignal], score: float, confidence: float, action: str) -> str:
        ordered = sorted(signals, key=lambda s: abs(s.score) * s.confidence, reverse=True)[:3]
        parts = [f"{s.name}={s.score:+.2f}@{s.confidence:.2f}" for s in ordered]
        return f"{action} (score={score:+.2f}, conf={confidence:.2f}) | top: " + ", ".join(parts)
