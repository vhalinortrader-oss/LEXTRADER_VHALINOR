"""Gestão de risco com perfil adaptativo (conservador / moderado / agressivo)."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict


class RiskProfile(str, Enum):
    CONSERVADOR = "conservador"
    MODERADO = "moderado"
    AGRESSIVO = "agressivo"


_RISK_PARAMS: Dict[RiskProfile, Dict[str, float]] = {
    RiskProfile.CONSERVADOR: {
        "max_position_pct": 0.05, "stop_loss_pct": 0.03, "take_profit_pct": 0.06,
        "max_open_trades": 2, "max_daily_loss_pct": 0.02, "min_confidence": 0.65,
    },
    RiskProfile.MODERADO: {
        "max_position_pct": 0.10, "stop_loss_pct": 0.05, "take_profit_pct": 0.10,
        "max_open_trades": 3, "max_daily_loss_pct": 0.05, "min_confidence": 0.55,
    },
    RiskProfile.AGRESSIVO: {
        "max_position_pct": 0.20, "stop_loss_pct": 0.08, "take_profit_pct": 0.20,
        "max_open_trades": 5, "max_daily_loss_pct": 0.10, "min_confidence": 0.45,
    },
}


@dataclass
class RiskManager:
    profile: RiskProfile = RiskProfile.MODERADO
    overrides: Dict[str, Any] = None

    def __post_init__(self):
        if isinstance(self.profile, str):
            self.profile = RiskProfile(self.profile.lower())
        base = dict(_RISK_PARAMS[self.profile])
        if self.overrides:
            base.update(self.overrides)
        self.params = base

    def position_size(self, capital: float, price: float) -> float:
        if price <= 0:
            return 0.0
        size_pct = self.params["max_position_pct"]
        return (capital * size_pct) / price

    def stop_loss(self, entry: float) -> float:
        return entry * (1 - self.params["stop_loss_pct"])

    def take_profit(self, entry: float) -> float:
        return entry * (1 + self.params["take_profit_pct"])

    def allow_new_trade(self, open_trades: int) -> bool:
        return open_trades < self.params["max_open_trades"]

    def passes_confidence(self, confidence: float) -> bool:
        return confidence >= self.params["min_confidence"]
