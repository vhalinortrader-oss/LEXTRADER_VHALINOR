"""Camada de persistência SQLite (memória, trades, sinais)."""
from .database import Database, TradeRecord, SignalRecord

__all__ = ["Database", "TradeRecord", "SignalRecord"]
