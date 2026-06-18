"""Regras determinísticas usadas pelo `NeuronioEstrategista`."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np
import pandas as pd


@dataclass
class RegraBase:
    nome: str = "Base"
    peso: float = 1.0

    def avaliar(self, df: pd.DataFrame) -> Tuple[int, float]:
        """Retorna (sinal, confiança) — sinal em {-1, 0, 1}."""
        raise NotImplementedError


class RegraCruzamentoMM(RegraBase):
    """Detecta cruzamento de SMA rápida (20) sobre SMA lenta (50)."""

    nome = "cruzamento_sma"

    def avaliar(self, df: pd.DataFrame) -> Tuple[int, float]:
        if df is None or len(df) < 3 or "SMA_20" not in df.columns or "SMA_50" not in df.columns:
            return 0, 0.0
        s20 = df["SMA_20"].astype(float)
        s50 = df["SMA_50"].astype(float)
        prev_diff = s20.iloc[-2] - s50.iloc[-2]
        cur_diff = s20.iloc[-1] - s50.iloc[-1]
        if prev_diff <= 0 < cur_diff:
            return 1, 0.7
        if prev_diff >= 0 > cur_diff:
            return -1, 0.7
        if cur_diff > 0:
            return 1, 0.3
        if cur_diff < 0:
            return -1, 0.3
        return 0, 0.0


class RegraRSIMACD(RegraBase):
    """Combina RSI sobrevendido/sobrecomprado com cruzamento de MACD."""

    nome = "rsi_macd"

    def avaliar(self, df: pd.DataFrame) -> Tuple[int, float]:
        if df is None or len(df) < 3:
            return 0, 0.0
        rsi = df.get("RSI_14")
        macd = df.get("MACD_12_26_9")
        sig = df.get("MACDs_12_26_9")
        if rsi is None or macd is None or sig is None:
            return 0, 0.0
        rsi_v = float(rsi.iloc[-1])
        macd_v = float(macd.iloc[-1])
        sig_v = float(sig.iloc[-1])
        macd_prev = float(macd.iloc[-2]) if len(macd) >= 2 else macd_v
        sig_prev = float(sig.iloc[-2]) if len(sig) >= 2 else sig_v
        macd_cross_up = macd_prev <= sig_prev and macd_v > sig_v
        macd_cross_dn = macd_prev >= sig_prev and macd_v < sig_v

        if rsi_v < 30 and (macd_cross_up or macd_v > sig_v):
            return 1, 0.75
        if rsi_v > 70 and (macd_cross_dn or macd_v < sig_v):
            return -1, 0.75
        if 40 < rsi_v < 60 and macd_v > sig_v:
            return 1, 0.4
        if 40 < rsi_v < 60 and macd_v < sig_v:
            return -1, 0.4
        return 0, 0.0


class RegraBollingerReversao(RegraBase):
    """Sinal de reversão quando o preço toca a banda inferior/superior."""

    nome = "bollinger_reversao"

    def avaliar(self, df: pd.DataFrame) -> Tuple[int, float]:
        if df is None or len(df) < 2:
            return 0, 0.0
        low = df.get("BBL_20_2.0")
        up = df.get("BBU_20_2.0")
        close = df.get("close")
        if low is None or up is None or close is None:
            return 0, 0.0
        c = float(close.iloc[-1])
        l = float(low.iloc[-1])
        u = float(up.iloc[-1])
        if u == l:
            return 0, 0.0
        if c <= l:
            return 1, 0.6
        if c >= u:
            return -1, 0.6
        # distância normalizada
        pos = (c - l) / (u - l)
        if pos < 0.2:
            return 1, 0.3
        if pos > 0.8:
            return -1, 0.3
        return 0, 0.0


def agregar_votos(votos) -> Tuple[float, float]:
    """Combina (sinal, peso) ponderado por peso dinâmico do EstadoGlobal."""
    if not votos:
        return 0.0, 0.0
    num = sum(s * w for s, w in votos)
    den = sum(abs(w) for _, w in votos) or 1.0
    sinal = float(np.clip(num / den, -1, 1))
    confianca = float(min(1.0, sum(abs(s) * w for s, w in votos) / den))
    return sinal, confianca
