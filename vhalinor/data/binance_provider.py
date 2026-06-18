"""Provedor Binance (via `python-binance`)."""
from __future__ import annotations

import os
from typing import Optional

import pandas as pd

from ..utils import logger
from .base import DataProvider, MarketData


_INTERVALS = {
    "1m": "1m", "3m": "3m", "5m": "5m", "15m": "15m", "30m": "30m",
    "1h": "1h", "2h": "2h", "4h": "4h", "6h": "6h", "8h": "8h", "12h": "12h",
    "1d": "1d", "3d": "3d", "1w": "1w", "1M": "1M",
}


class BinanceProvider(DataProvider):
    name = "binance"

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
                 testnet: bool = False) -> None:
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.testnet = testnet

    def fetch(self, symbol: str, period: str = "1y", interval: str = "1d") -> MarketData:
        try:
            from binance.client import Client
        except ImportError as e:
            raise ImportError("python-binance não está instalado. Rode `pip install python-binance`.") from e

        client = Client(self.api_key, self.api_secret, testnet=self.testnet)
        tf = _INTERVALS.get(interval, "1d")

        from datetime import datetime, timedelta
        days = {"d": 1, "mo": 30, "y": 365}.get(period[-1], 365)
        try:
            n = int(period[:-1]) if not period[-1].isdigit() else int(period)
        except ValueError:
            n = 365
        start_str = (datetime.utcnow() - timedelta(days=days * n)).strftime("%d %b %Y")

        logger.info(f"Binance: baixando {symbol} (start={start_str}, interval={tf})")
        klines = client.get_historical_klines(symbol, tf, start_str)
        if not klines:
            raise ValueError(f"Binance sem dados para {symbol}")

        df = pd.DataFrame(klines, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_volume", "trades",
            "taker_buy_base", "taker_buy_quote", "ignore",
        ])
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
        df = df[["open_time", "open", "high", "low", "close", "volume"]].astype(float)
        df = df.set_index("open_time")
        df.columns = ["open", "high", "low", "close", "volume"]
        return MarketData(symbol=symbol, df=df, source=self.name, extra={"testnet": self.testnet})
