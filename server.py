"""
LEXTRADER — API FastAPI Real
Endpoints para análise, dados de mercado, trades e portfólio.
"""
import json
import sys
from datetime import datetime
from typing import List, Optional

try:
    from fastapi import FastAPI, HTTPException, BackgroundTasks
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    FASTAPI_OK = True
except ImportError:
    FASTAPI_OK = False

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import (
    get_recent_signals, get_open_trades, get_closed_trades,
    get_equity_history, get_stats, get_config, set_config, init_db
)

init_db()

# Import com fallback para quando rodar sem dependências de ML
try:
    from data.market_data import get_full_data, get_multi_symbol_data
    DATA_OK = True
except ImportError:
    DATA_OK = False

try:
    from ml.engine import engine
    ML_OK = True
except ImportError:
    ML_OK = False

app = FastAPI(
    title="LEXTRADER VHALINOR API",
    description="Sistema de IA para trading algorítmico — B3 & Mercados Globais",
    version="5.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Health ──────────────────────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "version": "5.0.0",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "database": True,
            "market_data": DATA_OK,
            "ml_engine": ML_OK,
        }
    }


# ─── Mercado ─────────────────────────────────────────────────────────────────

@app.get("/api/market/{symbol}")
def get_market_data(symbol: str):
    """Busca cotação e indicadores técnicos reais do ativo."""
    if not DATA_OK:
        raise HTTPException(503, "yfinance não instalado")
    try:
        data = get_full_data(symbol)
        return data
    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/api/market")
def get_all_market_data():
    """Busca dados de todos os símbolos configurados."""
    if not DATA_OK:
        raise HTTPException(503, "yfinance não instalado")
    symbols_json = get_config("symbols", '["PETR4.SA","VALE3.SA","ITUB4.SA"]')
    symbols = json.loads(symbols_json)
    return get_multi_symbol_data(symbols)


# ─── Análise e Sinais ─────────────────────────────────────────────────────────

@app.post("/api/analyze/{symbol}")
def analyze_symbol(symbol: str):
    """Roda análise IA completa (ML + regras técnicas) para um ativo."""
    if not ML_OK or not DATA_OK:
        raise HTTPException(503, "Motor de ML ou dados não disponíveis")
    try:
        data = get_full_data(symbol)
        result = engine.analyze(symbol, data)
        return result
    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/api/signals")
def get_signals(limit: int = 20):
    """Retorna sinais recentes do banco de dados."""
    return get_recent_signals(limit)


# ─── Treino ──────────────────────────────────────────────────────────────────

@app.post("/api/train/{symbol}")
def train_model(symbol: str, background_tasks: BackgroundTasks):
    """Treina o modelo RandomForest com dados históricos reais."""
    if not ML_OK or not DATA_OK:
        raise HTTPException(503, "Motor de ML não disponível")

    def _train():
        metrics = engine.train_symbol(symbol)
        from db.database import get_conn
        conn = get_conn()
        conn.execute("""
            INSERT INTO model_metrics (model_name, symbol, accuracy, n_samples, trained_at)
            VALUES (?, ?, ?, ?, ?)
        """, ("RandomForest", symbol, metrics.get("accuracy"), metrics.get("n_samples"), datetime.now().isoformat()))
        conn.commit()
        conn.close()

    background_tasks.add_task(_train)
    return {"status": "training_started", "symbol": symbol}


# ─── Trades & Portfólio ───────────────────────────────────────────────────────

@app.get("/api/trades/open")
def open_trades():
    return get_open_trades()


@app.get("/api/trades/history")
def trade_history(limit: int = 50):
    return get_closed_trades(limit)


@app.get("/api/portfolio")
def portfolio():
    if ML_OK:
        return engine.portfolio_summary()
    # Fallback: dados do banco de dados apenas
    stats = get_stats()
    capital = float(get_config("initial_capital", "100000"))
    return {
        "cash": capital,
        "capital": capital,
        "open_positions": 0,
        **stats,
    }


@app.get("/api/portfolio/equity")
def equity_history():
    return get_equity_history(100)


# ─── Configurações ───────────────────────────────────────────────────────────

@app.get("/api/config")
def get_all_config():
    keys = [
        "initial_capital", "max_position_pct", "stop_loss_pct",
        "take_profit_pct", "buy_threshold", "sell_threshold",
        "risk_profile", "symbols"
    ]
    return {k: get_config(k) for k in keys}


class ConfigUpdate(BaseModel):
    key: str
    value: str


@app.post("/api/config")
def update_config(payload: ConfigUpdate):
    set_config(payload.key, payload.value)
    return {"status": "ok", "key": payload.key, "value": payload.value}


# ─── Stats gerais ─────────────────────────────────────────────────────────────

@app.get("/api/stats")
def system_stats():
    stats = get_stats()
    capital = float(get_config("initial_capital", "100000"))
    return {
        **stats,
        "capital": capital,
        "return_pct": round(stats["total_pnl"] / capital * 100, 2) if capital > 0 else 0,
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
