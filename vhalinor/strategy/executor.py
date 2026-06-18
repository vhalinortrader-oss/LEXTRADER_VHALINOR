"""Executor simulado (paper trading) com ordens, stop e take-profit."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from ..utils import utcnow
from .risk import RiskManager


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    CANCELED = "CANCELED"


@dataclass
class Order:
    symbol: str
    side: OrderSide
    size: float
    entry: float
    stop: float
    take: float
    opened_at: datetime = field(default_factory=utcnow)
    closed_at: Optional[datetime] = None
    status: OrderStatus = OrderStatus.OPEN
    exit_price: Optional[float] = None
    pnl: float = 0.0
    reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol, "side": self.side.value, "size": self.size,
            "entry": self.entry, "stop": self.stop, "take": self.take,
            "opened_at": self.opened_at.isoformat(),
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
            "status": self.status.value,
            "exit_price": self.exit_price, "pnl": self.pnl, "reason": self.reason,
        }


class Executor:
    """Mantém capital, posições abertas e processa ordens a partir de decisões."""

    def __init__(self, initial_capital: float = 10_000.0, risk: Optional[RiskManager] = None) -> None:
        self.initial_capital = float(initial_capital)
        self.capital = float(initial_capital)
        self.risk = risk or RiskManager()
        self.open: Dict[str, Order] = {}
        self.closed: List[Order] = []

    @property
    def equity(self) -> float:
        return self.capital + sum(o.entry * o.size for o in self.open.values())

    def open_trade(self, symbol: str, side: OrderSide, price: float, size: Optional[float] = None) -> Optional[Order]:
        if side == OrderSide.SELL and symbol in self.open:
            return None  # encerra via close_trade
        if not self.risk.allow_new_trade(len(self.open)):
            return None
        if size is None:
            size = self.risk.position_size(self.capital, price)
        if size <= 0:
            return None

        if side == OrderSide.BUY:
            cost = price * size
            if cost > self.capital:
                size = self.capital / price
            if size <= 0:
                return None
            self.capital -= price * size
            stop = self.risk.stop_loss(price)
            take = self.risk.take_profit(price)
            order = Order(symbol, side, size, price, stop, take)
            self.open[symbol] = order
            return order
        return None

    def close_trade(self, symbol: str, price: float, reason: str = "") -> Optional[Order]:
        order = self.open.pop(symbol, None)
        if order is None:
            return None
        pnl = (price - order.entry) * order.size
        self.capital += price * order.size
        order.status = OrderStatus.CLOSED
        order.exit_price = price
        order.pnl = pnl
        order.closed_at = utcnow()
        order.reason = reason
        self.closed.append(order)
        return order

    def update(self, price_by_symbol: Dict[str, float]) -> List[Order]:
        """Verifica stops/takes e fecha o que precisar. Retorna ordens fechadas neste tick."""
        closed_now: List[Order] = []
        for sym, price in list(price_by_symbol.items()):
            o = self.open.get(sym)
            if not o:
                continue
            if price <= o.stop:
                closed_now.append(self.close_trade(sym, price, reason="stop_loss"))
            elif price >= o.take:
                closed_now.append(self.close_trade(sym, price, reason="take_profit"))
        return [o for o in closed_now if o is not None]

    def stats(self) -> Dict[str, Any]:
        if not self.closed:
            return {"trades": 0, "winrate": 0.0, "pnl": 0.0, "capital": self.capital}
        wins = sum(1 for o in self.closed if o.pnl > 0)
        total = len(self.closed)
        pnl = sum(o.pnl for o in self.closed)
        return {
            "trades": total,
            "winrate": wins / total if total else 0.0,
            "pnl": pnl,
            "capital": self.capital,
            "open": len(self.open),
        }
