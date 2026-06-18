"""Entry-point CLI: modos `core`, `train`, `trade`, `backtest`, `dashboard`."""
from __future__ import annotations

import argparse
import json
import sys
from typing import List

from .config import load_config
from .data.yahoo_provider import YahooProvider
from .indicators.technical import compute_indicators
from .models.random_forest import RandomForestModel
from .utils import logger, setup_logger, timeit
from .orchestrator import Orchestrator


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="lextrader", description="LEXTRADER-IAG 5.0")
    sub = p.add_subparsers(dest="mode", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--config", type=str, default=None)
    common.add_argument("--symbol", type=str, default=None)
    common.add_argument("--period", type=str, default="1y")
    common.add_argument("--interval", type=str, default="1d")
    common.add_argument("--capital", type=float, default=10_000.0)
    common.add_argument("--risk", type=str, default="moderado")

    sub.add_parser("core", parents=[common], help="roda um ciclo: dados -> cérebro -> decisão")
    sub.add_parser("train", parents=[common], help="treina modelos com o histórico")
    sub.add_parser("trade", parents=[common], help="paper trading contínuo por N ciclos")
    sub.add_parser("backtest", parents=[common], help="backtest simples no histórico")
    sub.add_parser("dashboard", parents=[common], help="abre o painel Tkinter")

    for s in ("train", "trade", "backtest"):
        getattr(sub.choices[s], "add_argument")("--symbol", type=str, default=None)
    p_trade = sub.choices["trade"]
    p_trade.add_argument("--cycles", type=int, default=3)
    p_trade.add_argument("--sleep", type=float, default=0.0)

    return p.parse_args(argv)


def _run_core(args) -> int:
    cfg = load_config(args.config)
    sym = args.symbol or cfg.get("symbols", ["BTC-USD"])[0]
    orch = Orchestrator(
        config_path=args.config,
        initial_capital=args.capital,
        risk_profile=args.risk,
        source=cfg.get("source", "yahoo"),
    )
    decision = orch.step(sym, period=args.period, interval=args.interval)
    out = {
        "symbol": decision.symbol,
        "action": decision.action,
        "score": decision.score,
        "confidence": decision.confidence,
        "rationale": decision.rationale,
        "signals": [s.to_dict() for s in decision.signals],
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


def _run_train(args) -> int:
    cfg = load_config(args.config)
    sym = args.symbol or cfg.get("symbols", ["BTC-USD"])[0]
    provider = YahooProvider()
    md = provider.fetch(sym, period=args.period, interval=args.interval)
    df = compute_indicators(md.df, cfg.get("indicators")).dropna()
    from .indicators.technical import FEATURE_COLUMNS
    model = RandomForestModel(
        n_estimators=int(cfg["models"]["random_forest"].get("n_estimators", 200)),
        max_depth=int(cfg["models"]["random_forest"].get("max_depth", 8)),
    )
    model.fit(df, FEATURE_COLUMNS)
    out = provider.name
    pred = model.predict(df, FEATURE_COLUMNS)
    print(json.dumps({
        "trained_on": sym, "samples": int(len(df)),
        "prob_up": pred.prob_up, "expected_return": pred.expected_return,
        "source": out,
    }, indent=2, ensure_ascii=False))
    return 0


def _run_backtest(args) -> int:
    cfg = load_config(args.config)
    sym = args.symbol or cfg.get("symbols", ["BTC-USD"])[0]
    orch = Orchestrator(
        config_path=args.config,
        initial_capital=args.capital,
        risk_profile=args.risk,
        source=cfg.get("source", "yahoo"),
    )
    provider = YahooProvider()
    md = provider.fetch(sym, period=args.period, interval=args.interval)
    df = compute_indicators(md.df, cfg.get("indicators")).dropna()
    if len(df) < 60:
        print("Histórico insuficiente para backtest.")
        return 1
    equity = args.capital
    wins = 0
    total = 0
    buy_price = None
    for i in range(60, len(df)):
        window = df.iloc[:i]
        last = window.iloc[-1]
        ml_pred = orch.ensemble.predict(window, orch.feature_cols)
        ml_payload = ml_pred.to_dict() if ml_pred else None
        if ml_payload:
            ml_payload["prob_up"] = ml_pred.prob_up
            ml_payload["expected_return"] = ml_pred.expected_return
        decision = orch.brain.think({
            "symbol": sym, "df": window,
            "ml_prediction": ml_payload, "sentiment": 0.0,
        })
        price = float(last["close"])
        if decision.action == "BUY" and buy_price is None:
            buy_price = price
        elif decision.action == "SELL" and buy_price is not None:
            ret = (price - buy_price) / buy_price
            equity *= (1 + ret)
            total += 1
            if ret > 0:
                wins += 1
            buy_price = None
    if buy_price is not None:
        ret = (float(df["close"].iloc[-1]) - buy_price) / buy_price
        equity *= (1 + ret)
        total += 1
        if ret > 0:
            wins += 1
    print(json.dumps({
        "symbol": sym, "samples": int(len(df)),
        "trades": total, "winrate": (wins / total) if total else 0.0,
        "final_equity": equity, "return_pct": (equity / args.capital - 1) * 100,
    }, indent=2, ensure_ascii=False))
    return 0


def _run_trade(args) -> int:
    import time
    cfg = load_config(args.config)
    sym = args.symbol or cfg.get("symbols", ["BTC-USD"])[0]
    orch = Orchestrator(
        config_path=args.config,
        initial_capital=args.capital,
        risk_profile=args.risk,
        source=cfg.get("source", "yahoo"),
    )
    for i in range(int(args.cycles)):
        decision = orch.step(sym, period=args.period, interval=args.interval)
        print(f"[{i+1}/{args.cycles}] {decision.action} score={decision.score:+.2f} conf={decision.confidence:.2f}")
        if args.sleep and i + 1 < args.cycles:
            time.sleep(float(args.sleep))
    print(json.dumps(orch.executor.stats(), indent=2, ensure_ascii=False))
    return 0


def _run_dashboard(args) -> int:
    from .dashboard.app import run_dashboard
    cfg = load_config(args.config)
    sym = args.symbol or cfg.get("symbols", ["BTC-USD"])[0]
    orch = Orchestrator(
        config_path=args.config,
        initial_capital=args.capital,
        risk_profile=args.risk,
        source=cfg.get("source", "yahoo"),
    )
    run_dashboard(orchestrator=orch, symbol=sym, interval_ms=5000)
    return 0


def main(argv: List[str] | None = None) -> int:
    setup_logger()
    args = _parse_args(argv)
    mode = (args.mode or "core").lower()
    try:
        if mode == "core":
            return _run_core(args)
        if mode == "train":
            return _run_train(args)
        if mode == "trade":
            return _run_trade(args)
        if mode == "backtest":
            return _run_backtest(args)
        if mode == "dashboard":
            return _run_dashboard(args)
    except KeyboardInterrupt:
        logger.warning("interrompido pelo usuário")
        return 130
    except Exception as exc:  # pragma: no cover
        logger.exception(f"falha: {exc}")
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
