"""Provedor Yahoo Finance via `yfinance`."""
from __future__ import annotations

from typing import Optional

import pandas as pd

from ..utils import logger
from .base import DataProvider, MarketData


class YahooProvider(DataProvider):
    name = "yahoo"

    def __init__(self, proxy: Optional[str] = None) -> None:
        self.proxy = proxy

    def fetch(self, symbol: str, period: str = "1y", interval: str = "1d") -> MarketData:
        try:
            import yfinance as yf
        except ImportError as e:
            raise ImportError("yfinance não está instalado. Rode `pip install yfinance`.") from e

        logger.info(f"Yahoo: baixando {symbol} (period={period}, interval={interval})")
        kwargs = {"period": period, "interval": interval, "progress": False, "auto_adjust": True}
        if self.proxy:
            kwargs["proxy"] = self.proxy
        df = yf.download(symbol, **kwargs)
        if df is None or df.empty:
            raise ValueError(f"Sem dados de Yahoo para {symbol}")

        # yfinance devolve MultiIndex quando uma chamada inclui um único ticker novo; normaliza
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c[0].lower() for c in df.columns]
        else:
            df.columns = [str(c).lower() for c in df.columns]

        # garantir colunas essenciais
        rename = {"adj close": "adj_close"}
        df = df.rename(columns=rename)
        keep = [c for c in ["open", "high", "low", "close", "volume"] if c in df.columns]
        df = df[keep].dropna()
        if df.empty:
            raise ValueError(f"Dados vazios para {symbol}")
        df.index = pd.to_datetime(df.index)
        return MarketData(symbol=symbol, df=df, source=self.name)
