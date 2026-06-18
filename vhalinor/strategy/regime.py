"""Detector de regime de mercado (tendência / lateralização)."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

import numpy as np
import pandas as pd


class MarketRegime(str, Enum):
    BULL = "bull"      # tendência de alta
    BEAR = "bear"      # tendência de baixa
    SIDEWAYS = "sideways"
    VOLATILE = "volatile"


class MarketRegimeDetector:
    """Classifica o regime atual com base em SMA, ADX e volatilidade."""

    def __init__(self, adx_trend: float = 20.0, adx_strong: float = 25.0, vol_threshold: float = 0.04) -> None:
        self.adx_trend = adx_trend
        self.adx_strong = adx_strong
        self.vol_threshold = vol_threshold

    def detect(self, df: pd.DataFrame) -> Tuple[MarketRegime, dict]:
        if df is None or df.empty:
            return MarketRegime.SIDEWAYS, {}

        info = {}
        adx = float(df.get("ADX_14", pd.Series([np.nan])).iloc[-1]) if "ADX_14" in df.columns else np.nan
        sma20 = float(df.get("SMA_20", pd.Series([np.nan])).iloc[-1]) if "SMA_20" in df.columns else np.nan
        sma50 = float(df.get("SMA_50", pd.Series([np.nan])).iloc[-1]) if "SMA_50" in df.columns else np.nan
        close = float(df["close"].iloc[-1])
        vol = float(df.get("vol_20", pd.Series([np.nan])).iloc[-1]) if "vol_20" in df.columns else np.nan

        info.update({"adx": adx, "sma20": sma20, "sma50": sma50, "close": close, "vol": vol})

        if not np.isnan(vol) and vol > self.vol_threshold:
            return MarketRegime.VOLATILE, info

        if np.isnan(adx) or adx < self.adx_trend:
            return MarketRegime.SIDEWAYS, info

        if not np.isnan(sma20) and not np.isnan(sma50) and close > sma20 > sma50:
            return MarketRegime.BULL, info
        if not np.isnan(sma20) and not np.isnan(sma50) and close < sma20 < sma50:
            return MarketRegime.BEAR, info
        return MarketRegime.SIDEWAYS, info
