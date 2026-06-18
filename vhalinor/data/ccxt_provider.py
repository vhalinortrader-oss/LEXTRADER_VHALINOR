"""Provedor CCXT (qualquer exchange pública)."""
from __future__ import annotations

from typing import Optional

import pandas as pd

from ..utils import logger
from .base import DataProvider, MarketData


class CCXTProvider(DataProvider):
    name = "ccxt"

    def __init__(self, exchange_id: str = "binance") -> None:
        self.exchange_id = exchange_id

    def _interval_to_ccxt(self, interval: str) -> str:
        return {
            "1m": "1m", "5m": "5m", "15m": "15m", "1h": "1h", "4h": "4h",
            "1d": "1d", "1w": "1w", "1M": "1M",
        }.get(interval, "1d")

    def _period_to_ms(self, period: str) -> int:
        # "1y" / "6mo" / "30d"
        units = {"d": 86_400_000, "mo": 30 * 86_400_000, "y": 365 * 86_400_000}
        digits = ""
        unit = "y"
        for ch in period:
            if ch.isdigit():
                digits += ch
            else:
                unit = ch + ("o" if ch == "m" else "")
                break
        n = int(digits or 365)
        return n * units.get(unit, units["y"])

    def fetch(self, symbol: str, period: str = "1y", interval: str = "1d") -> MarketData:
        try:
            import ccxt
        except ImportError as e:
            raise ImportError("ccxt não está instalado. Rode `pip install ccxt`.") from e

        logger.info(f"CCXT[{self.exchange_id}]: baixando {symbol} (period={period}, interval={interval})")
        ex_class = getattr(ccxt, self.exchange_id)
        ex = ex_class({"enableRateLimit": True})
        tf = self._interval_to_ccxt(interval)
        limit = 1000  # máx por chamada
        since = None
        all_ohlcv = []
        if period and period != "max":
            from datetime import datetime, timedelta
            days = {"d": 1, "mo": 30, "y": 365}.get(period[-1], 365)
            try:
                n = int(period[:-1]) if not period[-1].isdigit() else int(period)
            except ValueError:
                n = 365
            start = int((datetime.utcnow() - timedelta(days=days * n)).timestamp() * 1000)
            since = start
        cursor = since
        while True:
            ohlcv = ex.fetch_ohlcv(symbol, timeframe=tf, since=cursor, limit=limit)
            if not ohlcv:
                break
            all_ohlcv += ohlcv
            cursor = ohlcv[-1][0] + 1
            if len(ohlcv) < limit:
                break
            if since and cursor > int(__import__("time").time() * 1000):
                break

        if not all_ohlcv:
            raise ValueError(f"CCXT sem dados para {symbol}")

        df = pd.DataFrame(all_ohlcv, columns=["ts", "open", "high", "low", "close", "volume"])
        df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
        df = df.set_index("ts").astype(float)
        return MarketData(symbol=symbol, df=df, source=self.name, extra={"exchange": self.exchange_id})
