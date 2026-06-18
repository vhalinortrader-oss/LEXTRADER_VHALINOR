"""Orquestrador end-to-end: dados -> indicadores -> cérebro -> executor -> aprendizado."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from .brain.brain import Brain, BrainDecision
from .config import load_config
from .data.base import MarketData
from .data.binance_provider import BinanceProvider
from .data.ccxt_provider import CCXTProvider
from .data.yahoo_provider import YahooProvider
from .indicators.technical import FEATURE_COLUMNS, compute_indicators
from .learning import LearningLoop
from .models.base import BaseModel
from .models.ensemble import Ensemble
from .models.lstm import LSTM_AVAILABLE, LSTMModel
from .models.random_forest import RandomForestModel
from .storage.database import Database, SignalRecord, TradeRecord
from .strategy.executor import Executor, OrderSide
from .strategy.regime import MarketRegime, MarketRegimeDetector
from .strategy.risk import RiskManager, RiskProfile
from .utils import logger, setup_logger, utcnow


def _make_provider(source: str, **kwargs) -> Any:
    source = (source or "yahoo").lower()
    if source == "ccxt":
        return CCXTProvider(exchange_id=kwargs.get("exchange", "binance"))
    if source == "binance":
        return BinanceProvider(testnet=bool(kwargs.get("testnet", False)))
    return YahooProvider()


@dataclass
class Orchestrator:
    config_path: Optional[str] = None
    initial_capital: float = 10_000.0
    risk_profile: str = "moderado"
    source: str = "yahoo"
    use_lstm: bool = False

    def __post_init__(self) -> None:
        setup_logger()
        self.config: Dict[str, Any] = load_config(self.config_path)
        self.risk = RiskManager(
            profile=self.config.get("risk_profile", self.risk_profile),
            overrides=self.config.get("risk"),
        )
        self.provider = _make_provider(self.config.get("source", self.source))
        self.regime_detector = MarketRegimeDetector()
        self.brain = Brain(self.config, use_ml=True)

        models: List[BaseModel] = [RandomForestModel(
            n_estimators=int(self.config["models"]["random_forest"].get("n_estimators", 200)),
            max_depth=int(self.config["models"]["random_forest"].get("max_depth", 8)),
        )]
        if self.use_lstm and self.config["models"]["lstm"].get("enabled") and LSTM_AVAILABLE:
            models.append(LSTMModel(
                sequence_length=int(self.config["models"]["lstm"].get("sequence_length", 60)),
                epochs=int(self.config["models"]["lstm"].get("epochs", 20)),
            ))

        self.feature_cols: List[str] = list(FEATURE_COLUMNS)
        self.ensemble = Ensemble(models)
        self.learning = LearningLoop(
            ensemble=self.ensemble,
            base_models=models,
            feature_cols=self.feature_cols,
            retrain_every=int(self.config["learning"].get("retrain_every_n_signals", 50)),
            min_samples=int(self.config["learning"].get("min_samples_to_train", 200)),
        )
        self.executor = Executor(initial_capital=self.initial_capital, risk=self.risk)
        self.db = Database()

    def _load_market(self, symbol: str, period: str, interval: str) -> MarketData:
        try:
            return self.provider.fetch(symbol, period=period, interval=interval)
        except Exception as exc:
            logger.warning(f"Falha ao buscar {symbol} via {self.provider.name}: {exc}")
            raise

    def _enrich(self, md: MarketData) -> pd.DataFrame:
        df = compute_indicators(md.df, self.config.get("indicators"))
        df.attrs["symbol"] = md.symbol
        return df

    def step(self, symbol: str, period: str = "1y", interval: str = "1d") -> BrainDecision:
        """Executa UM ciclo: coletar -> enriquecer -> pensar -> agir -> aprender."""
        md = self._load_market(symbol, period, interval)
        df = self._enrich(md)
        df = df.dropna(subset=[c for c in self.feature_cols if c in df.columns])
        if df.empty:
            raise RuntimeError(f"Sem dados válidos para {symbol}")

        regime, regime_info = self.regime_detector.detect(df)
        ml_pred = self.ensemble.predict(df, self.feature_cols)
        ml_payload = ml_pred.to_dict() if ml_pred else None
        if ml_payload:
            ml_payload["prob_up"] = ml_pred.prob_up
            ml_payload["expected_return"] = ml_pred.expected_return

        context = {
            "symbol": symbol,
            "df": df,
            "regime": regime,
            "regime_info": regime_info,
            "ml_prediction": ml_payload,
            "sentiment": 0.0,  # sem feed de notícias ativo
        }
        decision = self.brain.think(context)
        self._act(decision, price=md.last_price(), df=df)
        self._persist(decision, regime=regime, regime_info=regime_info)
        return decision

    def _act(self, decision: BrainDecision, price: float, df: pd.DataFrame) -> None:
        if decision.action == "BUY" and not self.executor.open.get(decision.symbol):
            order = self.executor.open_trade(decision.symbol, OrderSide.BUY, price=price)
            if order:
                logger.info(f"[executor] abriu {order.side.value} {order.symbol} @ {order.entry:.2f} "
                            f"size={order.size:.6f} stop={order.stop:.2f} take={order.take:.2f}")
        # fechamento depende de stop/take; o dashboard pode disparar manual
        closed = self.executor.update({decision.symbol: price})
        for c in closed:
            self._log_closed_trade(c)

    def _log_closed_trade(self, order) -> None:
        rec = TradeRecord(
            symbol=order.symbol, side=order.side.value, size=order.size,
            entry=order.entry, exit_price=order.exit_price or 0.0, pnl=order.pnl,
            opened_at=order.opened_at.isoformat(),
            closed_at=(order.closed_at or utcnow()).isoformat(),
            reason=order.reason,
        )
        self.db.log_trade(rec)

    def _persist(self, decision: BrainDecision, regime, regime_info) -> None:
        rec = SignalRecord(
            symbol=decision.symbol, action=decision.action,
            score=decision.score, confidence=decision.confidence,
            rationale=decision.rationale, created_at=utcnow().isoformat(),
            extra={"regime": regime.value, "regime_info": regime_info,
                   "signals": [s.to_dict() for s in decision.signals]},
        )
        self.db.log_signal(rec)
        ml_pred = decision.context.get("ml_prediction") or {}
        per_model = (ml_pred.get("extra") or {}).get("per_model") if hasattr(ml_pred, "to_dict") is False else None
        if not per_model and ml_pred:
            per_model = ml_pred.get("per_model", {})

    def close(self, symbol: str, price: Optional[float] = None, reason: str = "manual") -> None:
        if price is None:
            try:
                md = self.provider.fetch(symbol, period="5d", interval="1d")
                price = md.last_price()
            except Exception:
                price = 0.0
        order = self.executor.close_trade(symbol, price=price, reason=reason)
        if order:
            self._log_closed_trade(order)
