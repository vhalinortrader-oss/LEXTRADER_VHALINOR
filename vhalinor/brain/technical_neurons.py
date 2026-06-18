"""Neurônios especializados (técnica, momentum, risco, tendência, ML, sentimento)."""
from __future__ import annotations

from typing import Any, Dict

import numpy as np
import pandas as pd

from .neuron import Neuron, NeuronSignal


def _last(series: pd.Series, default: float = 0.0) -> float:
    try:
        v = float(series.iloc[-1])
        return v if np.isfinite(v) else default
    except Exception:
        return default


class RSINeuron(Neuron):
    name = "RSI"
    weight = 1.0

    def process(self, context: Dict[str, Any]) -> NeuronSignal:
        df = context.get("df")
        if df is None or "RSI_14" not in df.columns:
            return NeuronSignal(self.name, 0.0, 0.1, weight=self.weight)
        rsi = _last(df["RSI_14"])
        if rsi < 30:
            score, conf = 0.7, 0.7
        elif rsi > 70:
            score, conf = -0.7, 0.7
        else:
            score, conf = (50.0 - rsi) / 50.0, 0.3
        return NeuronSignal(self.name, float(np.clip(score, -1, 1)), float(np.clip(conf, 0, 1)),
                            {"rsi": rsi}, weight=self.weight)


class MACDNeuron(Neuron):
    name = "MACD"
    weight = 1.0

    def process(self, context: Dict[str, Any]) -> NeuronSignal:
        df = context.get("df")
        if df is None or "MACD_12_26_9" not in df.columns or "MACDs_12_26_9" not in df.columns:
            return NeuronSignal(self.name, 0.0, 0.1, weight=self.weight)
        macd = _last(df["MACD_12_26_9"])
        sig = _last(df["MACDs_12_26_9"])
        diff = macd - sig
        score = float(np.clip(diff * 10, -1, 1))  # normalização grosseira
        conf = float(min(0.8, abs(diff) * 5 + 0.1))
        return NeuronSignal(self.name, score, conf,
                            {"macd": macd, "signal": sig, "diff": diff}, weight=self.weight)


class BollingerNeuron(Neuron):
    name = "Bollinger"
    weight = 0.8

    def process(self, context: Dict[str, Any]) -> NeuronSignal:
        df = context.get("df")
        if df is None or "BBL_20_2.0" not in df.columns or "BBU_20_2.0" not in df.columns:
            return NeuronSignal(self.name, 0.0, 0.1, weight=self.weight)
        close = _last(df["close"])
        low = _last(df["BBL_20_2.0"])
        up = _last(df["BBU_20_2.0"])
        if up == low:
            return NeuronSignal(self.name, 0.0, 0.1, weight=self.weight)
        position = (close - low) / (up - low)  # 0 = na banda inferior, 1 = na superior
        score = float(np.clip(0.5 - position, -1, 1) * 2)  # compra na baixa, venda na alta
        conf = 0.4 + 0.4 * (1 - abs(0.5 - position) * 2)  # mais confiante nos extremos
        return NeuronSignal(self.name, float(np.clip(score, -1, 1)), float(np.clip(conf, 0, 1)),
                            {"position": position, "close": close}, weight=self.weight)


class TrendNeuron(Neuron):
    """Detecta tendência com cruzamento de médias."""
    name = "Trend"
    weight = 1.0

    def process(self, context: Dict[str, Any]) -> NeuronSignal:
        df = context.get("df")
        if df is None or "SMA_20" not in df.columns or "SMA_50" not in df.columns:
            return NeuronSignal(self.name, 0.0, 0.1, weight=self.weight)
        sma20 = _last(df["SMA_20"])
        sma50 = _last(df["SMA_50"])
        close = _last(df["close"])
        if sma50 == 0:
            return NeuronSignal(self.name, 0.0, 0.1, weight=self.weight)
        gap = (sma20 - sma50) / sma50
        above = close > sma20
        score = float(np.clip(gap * 20, -1, 1))
        if above:
            score = abs(score) * 0.5 + 0.3
        else:
            score = -abs(score) * 0.5 - 0.3
        conf = float(min(0.8, abs(gap) * 8 + 0.2))
        return NeuronSignal(self.name, float(np.clip(score, -1, 1)), float(np.clip(conf, 0, 1)),
                            {"sma20": sma20, "sma50": sma50, "close": close}, weight=self.weight)


class VolatilityNeuron(Neuron):
    name = "Volatility"
    weight = 0.5

    def process(self, context: Dict[str, Any]) -> NeuronSignal:
        df = context.get("df")
        if df is None or "ATRr_14" not in df.columns:
            return NeuronSignal(self.name, 0.0, 0.1, weight=self.weight)
        atr = _last(df["ATRr_14"])
        close = _last(df["close"])
        rel = atr / close if close else 0
        # alta volatilidade → mais cautela (sinal neutro, baixa confiança)
        if rel > 0.05:
            return NeuronSignal(self.name, 0.0, 0.2,
                                {"atr": atr, "rel": rel}, weight=self.weight)
        score = 0.0
        return NeuronSignal(self.name, score, 0.5, {"atr": atr, "rel": rel}, weight=self.weight)


class VolumeNeuron(Neuron):
    name = "Volume"
    weight = 0.6

    def process(self, context: Dict[str, Any]) -> NeuronSignal:
        df = context.get("df")
        if df is None or "volume" not in df.columns or len(df) < 20:
            return NeuronSignal(self.name, 0.0, 0.1, weight=self.weight)
        vol = df["volume"].astype(float)
        avg = vol.rolling(20).mean().iloc[-1]
        cur = float(vol.iloc[-1])
        if avg is None or np.isnan(avg) or avg == 0:
            return NeuronSignal(self.name, 0.0, 0.1, weight=self.weight)
        ratio = cur / float(avg)
        # volume acima da média com preço subindo → confirma alta
        change = _last(df["close"]) - _last(df["close"].shift(1)) if "close" in df else 0
        score = 0.4 if (ratio > 1.2 and change > 0) else (-0.4 if (ratio > 1.2 and change < 0) else 0)
        conf = float(min(0.7, abs(ratio - 1) * 0.5 + 0.1))
        return NeuronSignal(self.name, score, conf, {"ratio": ratio}, weight=self.weight)


class MLNeuron(Neuron):
    """Integra a previsão do modelo supervisionado (Random Forest / LSTM)."""
    name = "ML"
    weight = 1.4

    def process(self, context: Dict[str, Any]) -> NeuronSignal:
        ml = context.get("ml_prediction")
        if not ml:
            return NeuronSignal(self.name, 0.0, 0.1, weight=self.weight)
        prob_up = float(ml.get("prob_up", 0.5))
        score = float(np.clip((prob_up - 0.5) * 2, -1, 1))
        conf = float(abs(prob_up - 0.5) * 2)
        return NeuronSignal(self.name, score, conf, ml, weight=self.weight)


class SentimentNeuron(Neuron):
    name = "Sentiment"
    weight = 0.3

    def process(self, context: Dict[str, Any]) -> NeuronSignal:
        sent = context.get("sentiment")
        if sent is None:
            return NeuronSignal(self.name, 0.0, 0.1, weight=self.weight)
        # sent em [-1, 1]
        score = float(np.clip(sent, -1, 1))
        conf = 0.4
        return NeuronSignal(self.name, score, conf, {"sentiment": sent}, weight=self.weight)
