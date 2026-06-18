"""Interfaces base para provedores de dados de mercado."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import pandas as pd


@dataclass
class MarketData:
    symbol: str
    df: pd.DataFrame            # OHLCV com colunas: open, high, low, close, volume
    source: str
    extra: Dict[str, Any] = field(default_factory=dict)

    def last_price(self) -> float:
        return float(self.df["close"].iloc[-1])


class DataProvider(ABC):
    """Provedor genérico de dados OHLCV."""

    name: str = "base"

    @abstractmethod
    def fetch(self, symbol: str, period: str = "1y", interval: str = "1d") -> MarketData:
        ...
