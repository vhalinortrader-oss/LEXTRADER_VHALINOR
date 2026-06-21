"""
LEXTRADER — Motor de IA Real
RandomForest + Ensemble de regras técnicas + gestão de risco real.
"""
import json
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Tuple, Dict, Any

try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    SK_AVAILABLE = True
except ImportError:
    SK_AVAILABLE = False

from ..data.market_data import fetch_ohlcv, compute_indicators
from ..db.database import save_signal, save_trade, get_stats, save_snapshot, get_config

MODEL_DIR = Path(__file__).parent.parent / "models"
MODEL_DIR.mkdir(exist_ok=True)

# ─── Feature engineering ─────────────────────────────────────────────────────

FEATURES = [
    "rsi", "macd", "macd_signal", "macd_hist",
    "bb_upper", "bb_lower", "bb_mid", "bb_position",
    "sma20", "sma50", "ema9", "ema21",
    "atr", "stoch_k", "stoch_d",
    "volume_ratio", "return_1d", "return_5d",
]


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    close = df["Close"]
    df["bb_position"] = (close - df["bb_lower"]) / (df["bb_upper"] - df["bb_lower"] + 1e-9)

    # Label: retorno futuro de 5 dias
    df["future_return"] = close.shift(-5) / close - 1
    df["label"] = 0  # HOLD
    df.loc[df["future_return"] > 0.02, "label"] = 1   # BUY
    df.loc[df["future_return"] < -0.02, "label"] = -1  # SELL

    return df.dropna(subset=FEATURES + ["label"])


# ─── Modelo ML ───────────────────────────────────────────────────────────────

class TradingModel:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.model_path = MODEL_DIR / f"{symbol.replace('.', '_')}_rf.pkl"
        self.scaler_path = MODEL_DIR / f"{symbol.replace('.', '_')}_scaler.pkl"
        self.rf = None
        self.scaler = None
        self.is_trained = False
        self._load()

    def _load(self):
        if self.model_path.exists() and self.scaler_path.exists():
            try:
                with open(self.model_path, "rb") as f:
                    self.rf = pickle.load(f)
                with open(self.scaler_path, "rb") as f:
                    self.scaler = pickle.load(f)
                self.is_trained = True
            except Exception:
                pass

    def train(self, df: pd.DataFrame) -> Dict:
        if not SK_AVAILABLE:
            return {"error": "scikit-learn não disponível"}

        df = build_features(df)
        if len(df) < 100:
            return {"error": "Dados insuficientes para treino"}

        X = df[FEATURES].values
        y = df["label"].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.scaler = StandardScaler()
        X_train_s = self.scaler.fit_transform(X_train)
        X_test_s = self.scaler.transform(X_test)

        self.rf = RandomForestClassifier(
            n_estimators=200, max_depth=8,
            min_samples_leaf=5, n_jobs=-1,
            random_state=42, class_weight="balanced"
        )
        self.rf.fit(X_train_s, y_train)
        self.is_trained = True

        # Salva modelo
        with open(self.model_path, "wb") as f:
            pickle.dump(self.rf, f)
        with open(self.scaler_path, "wb") as f:
            pickle.dump(self.scaler, f)

        preds = self.rf.predict(X_test_s)
        metrics = {
            "accuracy": round(accuracy_score(y_test, preds), 4),
            "n_samples": len(df),
            "trained_at": datetime.now().isoformat(),
        }
        return metrics

    def predict_proba(self, features: np.ndarray) -> Dict:
        if not self.is_trained or self.rf is None:
            return {"buy": 0.33, "sell": 0.33, "hold": 0.34, "source": "uniform_fallback"}

        x = self.scaler.transform(features.reshape(1, -1))
        proba = self.rf.predict_proba(x)[0]
        classes = self.rf.classes_

        result = {"buy": 0.0, "sell": 0.0, "hold": 0.0, "source": "random_forest"}
        for cls, p in zip(classes, proba):
            if cls == 1:
                result["buy"] = float(p)
            elif cls == -1:
                result["sell"] = float(p)
            else:
                result["hold"] = float(p)
        return result


# ─── Sinais baseados em regras ───────────────────────────────────────────────

def rule_based_signal(ind: Dict) -> Tuple[str, float, list]:
    """Análise técnica clássica — retorna (decisão, confiança, razões)."""
    buy_score = 0.0
    sell_score = 0.0
    reasons = []

    rsi_val = ind.get("rsi", 50)
    if rsi_val < 30:
        buy_score += 0.25
        reasons.append(f"RSI sobrevendido ({rsi_val:.1f})")
    elif rsi_val > 70:
        sell_score += 0.25
        reasons.append(f"RSI sobrecomprado ({rsi_val:.1f})")

    macd_hist = ind.get("macd_hist", 0)
    if macd_hist > 0:
        buy_score += 0.20
        reasons.append("MACD histograma positivo (momentum bullish)")
    elif macd_hist < 0:
        sell_score += 0.20
        reasons.append("MACD histograma negativo (momentum bearish)")

    bb_pos = ind.get("bb_position", 0.5)
    if bb_pos < 0.2:
        buy_score += 0.20
        reasons.append(f"Preço próximo banda inferior Bollinger ({bb_pos:.1%})")
    elif bb_pos > 0.8:
        sell_score += 0.20
        reasons.append(f"Preço próximo banda superior Bollinger ({bb_pos:.1%})")

    ema9 = ind.get("ema9", 0)
    ema21 = ind.get("ema21", 0)
    if ema9 > ema21:
        buy_score += 0.15
        reasons.append("Cruzamento EMA9 > EMA21 (tendência alta)")
    elif ema9 < ema21:
        sell_score += 0.15
        reasons.append("Cruzamento EMA9 < EMA21 (tendência baixa)")

    stoch_k = ind.get("stoch_k", 50)
    if stoch_k < 20:
        buy_score += 0.10
        reasons.append(f"Estocástico sobrevendido ({stoch_k:.1f})")
    elif stoch_k > 80:
        sell_score += 0.10
        reasons.append(f"Estocástico sobrecomprado ({stoch_k:.1f})")

    vol_ratio = ind.get("volume_ratio", 1.0)
    if vol_ratio > 1.5:
        if buy_score > sell_score:
            buy_score += 0.10
            reasons.append(f"Volume acima da média ({vol_ratio:.1f}x) confirma compra")
        else:
            sell_score += 0.10
            reasons.append(f"Volume acima da média ({vol_ratio:.1f}x) confirma venda")

    total = buy_score + sell_score
    if total == 0:
        return "HOLD", 0.5, ["Sem sinal claro — mercado lateral"]

    if buy_score > sell_score:
        confidence = min(buy_score / (total) * 1.2, 0.95)
        return "BUY", round(confidence, 4), reasons
    elif sell_score > buy_score:
        confidence = min(sell_score / (total) * 1.2, 0.95)
        return "SELL", round(confidence, 4), reasons
    else:
        return "HOLD", 0.50, reasons


# ─── Motor principal ─────────────────────────────────────────────────────────

class LEXTRADEREngine:
    def __init__(self):
        self.models: Dict[str, TradingModel] = {}
        self.capital = float(get_config("initial_capital", "100000.0"))
        self.cash = self.capital
        self.positions: Dict[str, Dict] = {}

    def get_model(self, symbol: str) -> TradingModel:
        if symbol not in self.models:
            self.models[symbol] = TradingModel(symbol)
        return self.models[symbol]

    def train_symbol(self, symbol: str) -> Dict:
        df = fetch_ohlcv(symbol, period="2y")
        df = compute_indicators(df)
        model = self.get_model(symbol)
        return model.train(df)

    def analyze(self, symbol: str, data: Dict) -> Dict:
        """Análise completa: ML + regras técnicas + gestão de risco."""
        ind = data["indicators"]
        price = data["price"]

        # 1. Sinal por regras técnicas
        rule_decision, rule_conf, reasons = rule_based_signal(ind)

        # 2. Predição ML (se modelo treinado)
        model = self.get_model(symbol)
        features = np.array([ind.get(f, 0) for f in FEATURES])
        ml_proba = model.predict_proba(features)

        # 3. Ensemble: média ponderada regras (40%) + ML (60%)
        buy_th = float(get_config("buy_threshold", "0.60"))
        sell_th = float(get_config("sell_threshold", "0.40"))

        ml_buy = ml_proba.get("buy", 0.33)
        ml_sell = ml_proba.get("sell", 0.33)

        rule_buy = rule_conf if rule_decision == "BUY" else 0.0
        rule_sell = rule_conf if rule_decision == "SELL" else 0.0

        ensemble_buy = 0.6 * ml_buy + 0.4 * rule_buy
        ensemble_sell = 0.6 * ml_sell + 0.4 * rule_sell

        if ensemble_buy >= buy_th:
            final_decision = "BUY"
            confidence = ensemble_buy
        elif ensemble_sell >= (1 - sell_th):
            final_decision = "SELL"
            confidence = ensemble_sell
        else:
            final_decision = "HOLD"
            confidence = max(ensemble_buy, ensemble_sell)

        # 4. Gestão de risco
        max_pos = float(get_config("max_position_pct", "0.10"))
        sl_pct = float(get_config("stop_loss_pct", "0.05"))
        tp_pct = float(get_config("take_profit_pct", "0.10"))
        position_size = self.cash * max_pos / price
        stop_loss = price * (1 - sl_pct)
        take_profit = price * (1 + tp_pct)

        reasoning = " | ".join(reasons[:3]) if reasons else "Análise de indicadores técnicos"

        # 5. Salva sinal no banco de dados
        sig_id = save_signal(
            symbol=symbol,
            decision=final_decision,
            confidence=confidence,
            price=price,
            indicators=ind,
            reasoning=reasoning,
            model=f"Ensemble({'RF+Rules' if model.is_trained else 'Rules Only'})"
        )

        # 6. Executa trade simulado (paper trading)
        trade_id = None
        if final_decision in ("BUY", "SELL") and confidence >= 0.55:
            if final_decision == "BUY" and self.cash >= price * position_size * 0.1:
                direction = "LONG"
                qty = min(position_size, self.cash * 0.1 / price)
                cost = qty * price
                self.cash -= cost
                self.positions[symbol] = {"qty": qty, "entry": price, "direction": direction}
                trade_id = save_trade(symbol, direction, price, qty, stop_loss, take_profit, sig_id)

        return {
            "symbol": symbol,
            "decision": final_decision,
            "confidence": round(confidence, 4),
            "price": price,
            "indicators": ind,
            "reasoning": reasoning,
            "reasons": reasons,
            "ml_proba": ml_proba,
            "ensemble": {"buy": round(ensemble_buy, 4), "sell": round(ensemble_sell, 4)},
            "risk": {
                "stop_loss": round(stop_loss, 4),
                "take_profit": round(take_profit, 4),
                "position_size": round(position_size, 2),
            },
            "signal_id": sig_id,
            "trade_id": trade_id,
            "timestamp": datetime.now().isoformat(),
        }

    def portfolio_summary(self) -> Dict:
        stats = get_stats()
        return {
            "cash": round(self.cash, 2),
            "capital": round(self.capital, 2),
            "open_positions": len(self.positions),
            "positions": self.positions,
            **stats,
        }


# Instância global
engine = LEXTRADEREngine()
