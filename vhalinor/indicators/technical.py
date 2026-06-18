"""Indicadores técnicos via `pandas_ta` + features customizadas."""
from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd

try:
    import pandas_ta as ta
    HAVE_PANDAS_TA = True
except Exception:  # pragma: no cover
    HAVE_PANDAS_TA = False


# Conjunto de features usado pelos modelos preditivos.
FEATURE_COLUMNS: List[str] = [
    "return_1", "return_5", "return_20",
    "vol_10", "vol_20", "vol_60",
    "RSI_14", "MACD_12_26_9", "MACDs_12_26_9", "MACDh_12_26_9",
    "BBL_20_2.0", "BBM_20_2.0", "BBU_20_2.0", "BBB_20_2.0", "BBP_20_2.0",
    "SMA_20", "SMA_50", "EMA_20", "EMA_50",
    "ATRr_14", "STOCHk_14_3_3", "STOCHd_14_3_3",
    "OBV", "MFI_14", "ADX_14",
    "dist_sma20", "dist_sma50", "sma_cross",
]


def _safe_lower(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).lower() for c in df.columns]
    return df


def compute_indicators(df: pd.DataFrame, indicators: list[str] | None = None) -> pd.DataFrame:
    """Aplica o conjunto solicitado (ou o completo) de indicadores `pandas_ta`."""
    if df is None or df.empty:
        return df
    if not HAVE_PANDAS_TA:
        return _fallback_indicators(df)

    df = _safe_lower(df)
    requested = indicators or [
        "rsi", "macd", "bbands", "sma", "ema", "atr", "stoch", "obv", "mfi", "adx",
    ]
    try:
        strat = ta.Strategy(
            name="lextrader",
            description="Conjunto padrão de indicadores do LEXTRADER-IAG",
            ta=[
                {"kind": "rsi", "length": 14},
                {"kind": "macd"},
                {"kind": "bbands", "length": 20},
                {"kind": "sma", "length": 20},
                {"kind": "sma", "length": 50},
                {"kind": "ema", "length": 20},
                {"kind": "ema", "length": 50},
                {"kind": "atr", "length": 14},
                {"kind": "stoch"},
                {"kind": "obv"},
                {"kind": "mfi"},
                {"kind": "adx"},
            ],
        )
        # Executa apenas os que foram pedidos (mantém compat)
        strat.ta = [t for t in strat.ta if t["kind"] in requested]
        df.ta.strategy(strat)
    except Exception as exc:  # pragma: no cover
        # se pandas_ta falhar (MultiIndex, etc), tenta linha a linha
        df = _compute_indicators_line_by_line(df, requested)

    return add_custom_features(df)


def _compute_indicators_line_by_line(df: pd.DataFrame, requested: list[str]) -> pd.DataFrame:
    if "rsi" in requested:
        df["RSI_14"] = ta.rsi(df["close"], length=14)
    if "macd" in requested:
        macd = ta.macd(df["close"])
        if macd is not None and not macd.empty:
            for col in macd.columns:
                df[col] = macd[col]
    if "bbands" in requested:
        bb = ta.bbands(df["close"], length=20)
        if bb is not None and not bb.empty:
            for col in bb.columns:
                df[col] = bb[col]
    if "sma" in requested:
        df["SMA_20"] = ta.sma(df["close"], length=20)
        df["SMA_50"] = ta.sma(df["close"], length=50)
    if "ema" in requested:
        df["EMA_20"] = ta.ema(df["close"], length=20)
        df["EMA_50"] = ta.ema(df["close"], length=50)
    if "atr" in requested:
        df["ATRr_14"] = ta.atr(df["high"], df["low"], df["close"], length=14)
    if "stoch" in requested:
        st = ta.stoch(df["high"], df["low"], df["close"])
        if st is not None and not st.empty:
            for col in st.columns:
                df[col] = st[col]
    if "obv" in requested:
        df["OBV"] = ta.obv(df["close"], df["volume"])
    if "mfi" in requested:
        df["MFI_14"] = ta.mfi(df["high"], df["low"], df["close"], df["volume"])
    if "adx" in requested:
        adx = ta.adx(df["high"], df["low"], df["close"])
        if adx is not None and not adx.empty:
            for col in adx.columns:
                df[col] = adx[col]
    return df


def _fallback_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Implementação mínima caso pandas_ta não esteja disponível."""
    df = _safe_lower(df)
    delta = df["close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    df["RSI_14"] = 100 - 100 / (1 + rs)
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD_12_26_9"] = ema12 - ema26
    df["MACDs_12_26_9"] = df["MACD_12_26_9"].ewm(span=9, adjust=False).mean()
    df["MACDh_12_26_9"] = df["MACD_12_26_9"] - df["MACDs_12_26_9"]
    df["SMA_20"] = df["close"].rolling(20).mean()
    df["SMA_50"] = df["close"].rolling(50).mean()
    df["EMA_20"] = df["close"].ewm(span=20, adjust=False).mean()
    df["EMA_50"] = df["close"].ewm(span=50, adjust=False).mean()
    return add_custom_features(df)


def add_custom_features(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona retornos, volatilidades e features derivadas usadas pelos neurônios e ML."""
    df = df.copy()
    for n in (1, 5, 20):
        df[f"return_{n}"] = df["close"].pct_change(n)

    for n in (10, 20, 60):
        df[f"vol_{n}"] = df["close"].pct_change().rolling(n).std()

    if "SMA_20" in df.columns:
        df["dist_sma20"] = df["close"] / df["SMA_20"] - 1
    if "SMA_50" in df.columns:
        df["dist_sma50"] = df["close"] / df["SMA_50"] - 1
    if "SMA_20" in df.columns and "SMA_50" in df.columns:
        df["sma_cross"] = (df["SMA_20"] > df["SMA_50"]).astype(int) - (df["SMA_20"] < df["SMA_50"]).astype(int)

    df = df.replace([np.inf, -np.inf], np.nan)
    return df
