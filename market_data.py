"""
LEXTRADER — Dados de mercado REAIS via yfinance
Busca cotações, calcula indicadores técnicos reais.
"""
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

try:
    import yfinance as yf
    YF_AVAILABLE = True
except ImportError:
    YF_AVAILABLE = False

# ─── Indicadores técnicos ────────────────────────────────────────────────────

def rsi(series: pd.Series, period=14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / (loss + 1e-9)
    return 100 - (100 / (1 + rs))


def macd(series: pd.Series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def bollinger_bands(series: pd.Series, period=20, std=2):
    sma = series.rolling(period).mean()
    std_dev = series.rolling(period).std()
    upper = sma + std * std_dev
    lower = sma - std * std_dev
    return upper, sma, lower


def atr(df: pd.DataFrame, period=14) -> pd.Series:
    high = df["High"]
    low = df["Low"]
    close = df["Close"]
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)
    return tr.rolling(period).mean()


def stochastic(df: pd.DataFrame, k=14, d=3):
    low_min = df["Low"].rolling(k).min()
    high_max = df["High"].rolling(k).max()
    k_pct = 100 * (df["Close"] - low_min) / (high_max - low_min + 1e-9)
    d_pct = k_pct.rolling(d).mean()
    return k_pct, d_pct


# ─── Fetch de dados ──────────────────────────────────────────────────────────

def fetch_ohlcv(symbol: str, period="6mo", interval="1d") -> pd.DataFrame:
    """Busca dados OHLCV reais do Yahoo Finance."""
    if not YF_AVAILABLE:
        raise RuntimeError("yfinance não instalado. Execute: pip install yfinance")

    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)
    if df.empty:
        raise ValueError(f"Sem dados para {symbol}")
    df.index = pd.to_datetime(df.index)
    return df


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula todos os indicadores técnicos sobre o DataFrame."""
    close = df["Close"]

    df["rsi"] = rsi(close)
    df["macd"], df["macd_signal"], df["macd_hist"] = macd(close)
    df["bb_upper"], df["bb_mid"], df["bb_lower"] = bollinger_bands(close)
    df["sma20"] = close.rolling(20).mean()
    df["sma50"] = close.rolling(50).mean()
    df["ema9"] = close.ewm(span=9, adjust=False).mean()
    df["ema21"] = close.ewm(span=21, adjust=False).mean()
    df["atr"] = atr(df)
    df["stoch_k"], df["stoch_d"] = stochastic(df)
    df["volume_sma"] = df["Volume"].rolling(20).mean()
    df["volume_ratio"] = df["Volume"] / (df["volume_sma"] + 1e-9)

    # Retornos
    df["return_1d"] = close.pct_change(1)
    df["return_5d"] = close.pct_change(5)

    return df.dropna()


def get_full_data(symbol: str) -> dict:
    """Retorna dados completos + indicadores + preço atual para um ativo."""
    df = fetch_ohlcv(symbol, period="1y")
    df = compute_indicators(df)

    last = df.iloc[-1]
    close = df["Close"]

    # Tendência
    trend = "ALTA" if last["ema9"] > last["ema21"] else "BAIXA"
    bb_pos = (last["Close"] - last["bb_lower"]) / (last["bb_upper"] - last["bb_lower"] + 1e-9)

    return {
        "symbol": symbol,
        "price": round(float(last["Close"]), 4),
        "change_1d": round(float(last["return_1d"]) * 100, 2),
        "volume": int(last["Volume"]),
        "indicators": {
            "rsi": round(float(last["rsi"]), 2),
            "macd": round(float(last["macd"]), 4),
            "macd_signal": round(float(last["macd_signal"]), 4),
            "macd_hist": round(float(last["macd_hist"]), 4),
            "bb_upper": round(float(last["bb_upper"]), 4),
            "bb_lower": round(float(last["bb_lower"]), 4),
            "bb_mid": round(float(last["bb_mid"]), 4),
            "bb_position": round(float(bb_pos), 3),
            "sma20": round(float(last["sma20"]), 4),
            "sma50": round(float(last["sma50"]), 4),
            "ema9": round(float(last["ema9"]), 4),
            "ema21": round(float(last["ema21"]), 4),
            "atr": round(float(last["atr"]), 4),
            "stoch_k": round(float(last["stoch_k"]), 2),
            "stoch_d": round(float(last["stoch_d"]), 2),
            "volume_ratio": round(float(last["volume_ratio"]), 2),
        },
        "trend": trend,
        "df_tail": df.tail(60).reset_index().to_dict(orient="records"),
    }


def get_multi_symbol_data(symbols: list) -> list:
    """Busca dados para múltiplos símbolos em paralelo."""
    results = []
    for sym in symbols:
        try:
            data = get_full_data(sym)
            results.append(data)
        except Exception as e:
            results.append({"symbol": sym, "error": str(e)})
    return results
