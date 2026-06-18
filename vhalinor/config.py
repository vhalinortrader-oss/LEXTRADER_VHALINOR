"""Carregamento de configuração do LEXTRADER-IAG."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import json

import yaml
from dotenv import load_dotenv


def project_root() -> Path:
    """Retorna a raiz do projeto (pasta que contém `lextrader/`)."""
    return Path(__file__).resolve().parent.parent


def data_dir() -> Path:
    p = project_root() / "data"
    p.mkdir(parents=True, exist_ok=True)
    return p


def models_dir() -> Path:
    p = project_root() / "models"
    p.mkdir(parents=True, exist_ok=True)
    return p


def logs_dir() -> Path:
    p = project_root() / "logs"
    p.mkdir(parents=True, exist_ok=True)
    return p


DEFAULT_CONFIG: Dict[str, Any] = {
    "symbols": ["BTC-USD", "ETH-USD"],
    "timeframe": "1d",
    "lookback_days": 365,
    "source": "yahoo",  # yahoo | ccxt
    "risk_profile": "moderado",  # conservador | moderado | agressivo
    "indicators": ["rsi", "macd", "bbands", "sma", "ema", "atr", "stoch"],
    "models": {
        "random_forest": {"enabled": True, "n_estimators": 200, "max_depth": 8},
        "lstm": {"enabled": False, "sequence_length": 60, "epochs": 20},
    },
    "decision": {
        "buy_threshold": 0.6,
        "sell_threshold": 0.4,
        "min_confidence": 0.55,
    },
    "risk": {
        "max_position_pct": 0.10,  # fração do capital por trade
        "stop_loss_pct": 0.05,
        "take_profit_pct": 0.10,
        "max_open_trades": 3,
    },
    "database": "lextrader.db",
    "learning": {
        "retrain_every_n_signals": 50,
        "min_samples_to_train": 200,
    },
}


def load_config(path: str | os.PathLike | None = None) -> Dict[str, Any]:
    """Carrega config.yaml e mescla com DEFAULT_CONFIG (defaults têm prioridade mais baixa)."""
    load_dotenv(project_root() / ".env")
    cfg: Dict[str, Any] = json.loads(json.dumps(DEFAULT_CONFIG))  # deep copy simples

    if path is None:
        path = project_root() / "lextrader" / "config.yaml"

    p = Path(path)
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            user_cfg = yaml.safe_load(f) or {}
        _deep_merge(cfg, user_cfg)
    return cfg


def _deep_merge(base: Dict[str, Any], extra: Dict[str, Any]) -> Dict[str, Any]:
    for k, v in (extra or {}).items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v
    return base
