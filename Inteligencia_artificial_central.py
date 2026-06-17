"""
LEXTRADER-IAG 5.0 - Sistema Cerebral Artificial para Mercado Financeiro
=======================================================================
Sistema avançado de rede neural artificial especializado em análises de mercado
financeiro, previsões e aplicações autônomas de trading.

Principais funcionalidades:
- Coleta e processamento de dados financeiros (cotações, indicadores)
- Modelos de previsão (ARIMA, LSTM, Prophet) com integração neural
- Estratégias de trading baseadas em indicadores técnicos e inteligência artificial
- Execução autônoma de trades (simulada ou via API)
- Gestão de risco e otimização de portfólio
- Dashboard interativo com gráficos de candlestick, indicadores e performance
- Sistema de memória para armazenar padrões de mercado e resultados
- Aprendizado contínuo com base em dados históricos e operações realizadas
"""

import os
import sys
import asyncio
import threading
import importlib.util
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable, Tuple, Union
from enum import Enum, auto
import json
import logging
import numpy as np
import pandas as pd
from pathlib import Path
# GUI (Tkinter) pode não existir em alguns ambientes Linux minimalistas.
try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox, filedialog
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    from matplotlib.figure import Figure
    TKINTER_AVAILABLE = True
except Exception:
    TKINTER_AVAILABLE = False

# networkx é usado apenas em partes visuais/expandíveis; não é necessário para rodar o núcleo.
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except Exception:
    NETWORKX_AVAILABLE = False

from collections import deque, defaultdict
import hashlib
import random
import time
import pickle
import csv
import sqlite3
from sqlite3 import Error
import xml.etree.ElementTree as ET
import yaml
import joblib
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Bibliotecas específicas para finanças
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("yfinance não disponível. Instale com: pip install yfinance")

try:
    import pandas_ta as ta
    PANDAS_TA_AVAILABLE = True
except ImportError:
    PANDAS_TA_AVAILABLE = False
    print("pandas_ta não disponível. Instale com: pip install pandas_ta")

# Bibliotecas de ML/AI
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow não disponível. Algumas funcionalidades de previsão serão limitadas.")

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch não disponível. Algumas funcionalidades de previsão serão limitadas.")

try:
    from qiskit import QuantumCircuit, Aer, execute
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    print("Qiskit não disponível. Funcionalidades quânticas limitadas.")

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('lextrader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# ENUMERAÇÕES E CLASSES DE DADOS FINANCEIROS
# ============================================================================

class MarketAssetType(Enum):
    """Tipos de ativos financeiros"""
    STOCK = "stock"
    CRYPTO = "crypto"
    FOREX = "forex"
    COMMODITY = "commodity"
    INDEX = "index"
    ETF = "etf"

class OrderType(Enum):
    """Tipos de ordens de trading"""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

class OrderSide(Enum):
    """Lado da ordem"""
    BUY = "buy"
    SELL = "sell"

class TradeStatus(Enum):
    """Status de uma operação"""
    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

class RiskLevel(Enum):
    """Níveis de risco"""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"

@dataclass
class MarketData:
    """Dados de mercado para um ativo"""
    symbol: str
    asset_type: MarketAssetType
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    adj_close: Optional[float] = None
    indicators: Dict[str, float] = field(default_factory=dict)
    
    def to_dataframe(self) -> pd.DataFrame:
        """Converte para DataFrame pandas"""
        return pd.DataFrame({
            'open': [self.open],
            'high': [self.high],
            'low': [self.low],
            'close': [self.close],
            'volume': [self.volume],
            'adj_close': [self.adj_close if self.adj_close else self.close],
            'timestamp': [self.timestamp]
        })

@dataclass
class TechnicalIndicator:
    """Indicador técnico calculado"""
    name: str
    symbol: str
    value: float
    timestamp: datetime
    parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Trade:
    """Representa uma operação de trading"""
    id: str
    symbol: str
    side: OrderSide
    quantity: float
    price: float
    status: TradeStatus
    entry_time: datetime
    exit_time: Optional[datetime] = None
    entry_price: float = 0.0

    exit_price: Optional[float] = None
    pnl: float = 0.0
    pnl_percent: float = 0.0
    fees: float = 0.0
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    strategy: str = ""

@dataclass
class Portfolio:
    """Portfólio de ativos e posições"""
    cash: float = 100000.0
    positions: Dict[str, float] = field(default_factory=dict)  # symbol -> quantity
    trades: List[Trade] = field(default_factory=list)
    total_pnl: float = 0.0
    total_pnl_percent: float = 0.0
    equity: float = 100000.0

# ============================================================================
# MÓDULO DE COLETA DE DADOS FINANCEIROS
# ============================================================================

class DataCollector:
    """Coleta dados de mercado de diversas fontes"""
    
    def __init__(self):
        self.cache: Dict[str, pd.DataFrame] = {}
        self.symbols: List[str] = []
        
    def fetch_historical(self, symbol: str, period: str = "1y", interval: str = "1d") -> Optional[pd.DataFrame]:
        """Obtém dados históricos via yfinance"""
        if not YFINANCE_AVAILABLE:
            logger.error("yfinance não disponível")
            return None
        
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            if not data.empty:
                self.cache[symbol] = data
                if symbol not in self.symbols:
                    self.symbols.append(symbol)
                return data
        except Exception as e:
            logger.error(f"Erro ao buscar dados para {symbol}: {e}")
        return None
    
    def fetch_realtime(self, symbol: str) -> Optional[MarketData]:
        """Obtém dados em tempo real (último tick)"""
        if not YFINANCE_AVAILABLE:
            return None
        
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")
            if not data.empty:
                last = data.iloc[-1]
                return MarketData(
                    symbol=symbol,
                    asset_type=self._guess_asset_type(symbol),
                    timestamp=datetime.now(),
                    open=last['Open'],
                    high=last['High'],
                    low=last['Low'],
                    close=last['Close'],
                    volume=last['Volume'],
                    adj_close=last['Close']
                )
        except Exception as e:
            logger.error(f"Erro ao buscar dados em tempo real para {symbol}: {e}")
        return None
    
    def _guess_asset_type(self, symbol: str) -> MarketAssetType:
        """Tenta adivinhar o tipo de ativo pelo símbolo"""
        symbol_upper = symbol.upper()
        if symbol_upper.endswith('=X') or symbol_upper in ['EURUSD', 'GBPUSD', 'USDJPY']:
            return MarketAssetType.FOREX
        elif symbol_upper in ['BTC-USD', 'ETH-USD', 'XRP-USD']:
            return MarketAssetType.CRYPTO
        elif symbol_upper in ['GC=F', 'CL=F']:
            return MarketAssetType.COMMODITY
        elif symbol_upper in ['^GSPC', '^DJI', '^IXIC']:
            return MarketAssetType.INDEX
        elif symbol_upper.endswith('.SA') or symbol_upper.endswith('.AX'):
            return MarketAssetType.STOCK
        else:
            return MarketAssetType.STOCK

# ============================================================================
# MÓDULO DE INDICADORES TÉCNICOS
# ============================================================================

class IndicatorCalculator:
    """Calcula indicadores técnicos usando pandas_ta e funções customizadas"""
    
    @staticmethod
    def calculate_rsi(data: pd.DataFrame, period: int = 14) -> pd.Series:
        """RSI - Relative Strength Index"""
        if not PANDAS_TA_AVAILABLE:
            # Implementação simplificada
            delta = data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        return ta.rsi(data['close'], length=period)
    
    @staticmethod
    def calculate_macd(data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """MACD - Moving Average Convergence Divergence"""
        if not PANDAS_TA_AVAILABLE:
            ema_fast = data['close'].ewm(span=fast, adjust=False).mean()
            ema_slow = data['close'].ewm(span=slow, adjust=False).mean()
            macd_line = ema_fast - ema_slow
            signal_line = macd_line.ewm(span=signal, adjust=False).mean()
            histogram = macd_line - signal_line
            return pd.DataFrame({'macd': macd_line, 'signal': signal_line, 'histogram': histogram})
        return ta.macd(data['close'], fast=fast, slow=slow, signal=signal)
    
    @staticmethod
    def calculate_bollinger(data: pd.DataFrame, period: int = 20, std: int = 2) -> pd.DataFrame:
        """Bandas de Bollinger"""
        if not PANDAS_TA_AVAILABLE:
            rolling_mean = data['close'].rolling(window=period).mean()
            rolling_std = data['close'].rolling(window=period).std()
            upper = rolling_mean + (rolling_std * std)
            lower = rolling_mean - (rolling_std * std)
            return pd.DataFrame({'upper': upper, 'middle': rolling_mean, 'lower': lower})
        return ta.bbands(data['close'], length=period, std=std)
    
    @staticmethod
    def calculate_sma(data: pd.DataFrame, period: int) -> pd.Series:
        """Média móvel simples"""
        return data['close'].rolling(window=period).mean()
    
    @staticmethod
    def calculate_ema(data: pd.DataFrame, period: int) -> pd.Series:
        """Média móvel exponencial"""
        return data['close'].ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def calculate_stochastic(data: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> pd.DataFrame:
        """Oscilador Estocástico"""
        if not PANDAS_TA_AVAILABLE:
            high = data['high'].rolling(k_period).max()
            low = data['low'].rolling(k_period).min()
            k = 100 * ((data['close'] - low) / (high - low))
            d = k.rolling(d_period).mean()
            return pd.DataFrame({'k': k, 'd': d})
        return ta.stoch(data['high'], data['low'], data['close'], k_period, d_period)
    
    @staticmethod
    def calculate_atr(data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Average True Range"""
        if not PANDAS_TA_AVAILABLE:
            high_low = data['high'] - data['low']
            high_close = np.abs(data['high'] - data['close'].shift())
            low_close = np.abs(data['low'] - data['close'].shift())
            ranges = pd.concat([high_low, high_close, low_close], axis=1)
            true_range = np.max(ranges, axis=1)
            atr = true_range.rolling(period).mean()
            return atr
        return ta.atr(data['high'], data['low'], data['close'], length=period)

# ============================================================================
# MÓDULO DE PREVISÃO FINANCEIRA
# ============================================================================

class FinancialForecaster:
    """Modelos de previsão para séries temporais financeiras"""
    
    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.scalers = {}
        self.last_training = {}
    
    def train_lstm(self, symbol: str, data: pd.DataFrame, target_col: str = 'close', 
                   sequence_length: int = 60, epochs: int = 20) -> bool:
        """Treina um modelo LSTM com PyTorch ou TensorFlow"""
        if not TORCH_AVAILABLE and not TF_AVAILABLE:
            logger.error("Nenhum framework de deep learning disponível")
            return False
        
        # Prepara dados
        values = data[target_col].values.reshape(-1, 1)
        scaler = StandardScaler()
        scaled = scaler.fit_transform(values)
        
        X, y = [], []
        for i in range(sequence_length, len(scaled)):
            X.append(scaled[i-sequence_length:i, 0])
            y.append(scaled[i, 0])
        
        X, y = np.array(X), np.array(y)
        X = X.reshape(X.shape[0], X.shape[1], 1)
        
        # Divisão treino/teste
        split = int(0.8 * len(X))
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        
        if TORCH_AVAILABLE:
            # Implementação com PyTorch
            import torch
            import torch.nn as nn
            import torch.optim as optim
            
            class LSTMModel(nn.Module):
                def __init__(self, input_size=1, hidden_size=50, num_layers=2):
                    super().__init__()
                    self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
                    self.linear = nn.Linear(hidden_size, 1)
                def forward(self, x):
                    out, _ = self.lstm(x)
                    out = self.linear(out[:, -1, :])
                    return out
            
            model = LSTMModel()
            criterion = nn.MSELoss()
            optimizer = optim.Adam(model.parameters(), lr=0.001)
            
            X_train_t = torch.tensor(X_train, dtype=torch.float32)
            y_train_t = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
            
            for epoch in range(epochs):
                optimizer.zero_grad()
                outputs = model(X_train_t)
                loss = criterion(outputs, y_train_t)
                loss.backward()
                optimizer.step()
            
            self.models[f"{symbol}_lstm"] = (model, scaler)
            self.scalers[symbol] = scaler
            self.last_training[symbol] = datetime.now()
            logger.info(f"✅ Modelo LSTM treinado para {symbol}")
            return True
        
        elif TF_AVAILABLE:
            # Implementação com TensorFlow
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import LSTM, Dense
            
            model = Sequential([
                LSTM(50, return_sequences=True, input_shape=(sequence_length, 1)),
                LSTM(50),
                Dense(1)
            ])
            model.compile(optimizer='adam', loss='mse')
            model.fit(X_train, y_train, epochs=epochs, batch_size=32, verbose=0)
            
            self.models[f"{symbol}_lstm"] = (model, scaler)
            self.scalers[symbol] = scaler
            self.last_training[symbol] = datetime.now()
            logger.info(f"✅ Modelo LSTM (TF) treinado para {symbol}")
            return True
        
        return False
    
    def train_random_forest(self, symbol: str, data: pd.DataFrame, target_col: str = 'close', 
                            n_estimators: int = 100) -> bool:
        """Treina um modelo Random Forest para previsão"""
        try:
            # Criar features: lag features, médias móveis, etc.
            df = data.copy()
            for lag in [1, 2, 3, 5, 10, 20]:
                df[f'lag_{lag}'] = df[target_col].shift(lag)
            df['ma_5'] = df[target_col].rolling(5).mean()
            df['ma_10'] = df[target_col].rolling(10).mean()
            df['return_1'] = df[target_col].pct_change()
            df = df.dropna()
            
            features = [col for col in df.columns if col != target_col]
            X = df[features].values
            y = df[target_col].values
            
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            split = int(0.8 * len(X_scaled))
            X_train, X_test = X_scaled[:split], X_scaled[split:]
            y_train, y_test = y[:split], y[split:]
            
            model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
            model.fit(X_train, y_train)
            
            self.models[f"{symbol}_rf"] = (model, scaler, features)
            self.scalers[symbol] = scaler
            self.last_training[symbol] = datetime.now()
            logger.info(f"✅ Modelo Random Forest treinado para {symbol}")
            return True
        except Exception as e:
            logger.error(f"Erro ao treinar Random Forest para {symbol}: {e}")
            return False
    
    def predict(self, symbol: str, model_type: str = 'lstm', data: Optional[pd.DataFrame] = None) -> Optional[float]:
        """Faz previsão usando o modelo especificado"""
        model_key = f"{symbol}_{model_type}"
        if model_key not in self.models:
            logger.error(f"Modelo {model_key} não encontrado")
            return None
        
        if model_type == 'lstm':
            model, scaler = self.models[model_key]
            if data is None:
                # Usar últimos dados do cache
                # Aqui precisaríamos ter acesso ao DataCollector
                return None
            # Prepara sequência
            values = data['close'].values.reshape(-1, 1)
            scaled = scaler.transform(values)
            if len(scaled) < 60:
                return None
            seq = scaled[-60:].reshape(1, 60, 1)
            
            if TORCH_AVAILABLE:
                import torch
                model.eval()
                with torch.no_grad():
                    pred_scaled = model(torch.tensor(seq, dtype=torch.float32)).numpy()
                pred = scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]
                return pred
            elif TF_AVAILABLE:
                pred_scaled = model.predict(seq)
                pred = scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]
                return pred
        
        elif model_type == 'rf':
            model, scaler, features = self.models[model_key]
            if data is None:
                return None
            # Criar features
            df = data.copy()
            for lag in [1, 2, 3, 5, 10, 20]:
                df[f'lag_{lag}'] = df['close'].shift(lag)
            df['ma_5'] = df['close'].rolling(5).mean()
            df['ma_10'] = df['close'].rolling(10).mean()
            df['return_1'] = df['close'].pct_change()
            df = df.dropna()
            if df.empty:
                return None
            last_row = df.iloc[-1:][features]
            X = scaler.transform(last_row.values)
            pred = model.predict(X)[0]
            return pred
        
        return None
    
    def predict_next_day(self, symbol: str, data: pd.DataFrame) -> Optional[float]:
        """Predição de próximo fechamento usando LSTM ou RF"""
        # Tenta LSTM primeiro, senão RF
        pred = self.predict(symbol, 'lstm', data)
        if pred is None:
            pred = self.predict(symbol, 'rf', data)
        return pred

# ============================================================================
# MÓDULO DE ESTRATÉGIAS DE TRADING
# ============================================================================

class TradingStrategy:
    """Estratégia de trading baseada em indicadores e IA"""
    
    def __init__(self, name: str, indicators: List[str], rules: Dict[str, Any]):
        self.name = name
        self.indicators = indicators
        self.rules = rules
        self.signals: List[Dict] = []
    
    def generate_signal(self, data: pd.DataFrame) -> Optional[str]:
        """Gera sinal de compra/venda baseado na estratégia"""
        # Exemplo: cruzamento de médias
        if 'sma_short' in self.rules and 'sma_long' in self.rules:
            short = IndicatorCalculator.calculate_sma(data, self.rules['sma_short'])
            long = IndicatorCalculator.calculate_sma(data, self.rules['sma_long'])
            if len(short) < 2 or len(long) < 2:
                return None
            if short.iloc[-1] > long.iloc[-1] and short.iloc[-2] <= long.iloc[-2]:
                return 'BUY'
            elif short.iloc[-1] < long.iloc[-1] and short.iloc[-2] >= long.iloc[-2]:
                return 'SELL'
        return None

class StrategyManager:
    """Gerencia múltiplas estratégias e combina sinais"""
    
    def __init__(self):
        self.strategies: Dict[str, TradingStrategy] = {}
    
    def add_strategy(self, strategy: TradingStrategy):
        self.strategies[strategy.name] = strategy
    
    def get_signal(self, symbol: str, data: pd.DataFrame) -> Optional[str]:
        """Combina sinais de todas as estratégias (votação)"""
        votes = {'BUY': 0, 'SELL': 0, 'HOLD': 0}
        for strategy in self.strategies.values():
            signal = strategy.generate_signal(data)
            if signal in votes:
                votes[signal] += 1
            else:
                votes['HOLD'] += 1
        # Decisão por maioria
        max_vote = max(votes, key=votes.get)
        if votes[max_vote] == 0:
            return None
        return max_vote

# ============================================================================
# MÓDULO DE EXECUÇÃO AUTÔNOMA
# ============================================================================

class AutonomousTrader:
    """Executor autônomo de trades com gerenciamento de risco"""
    
    def __init__(self, portfolio: Portfolio, risk_level: RiskLevel = RiskLevel.MODERATE):
        self.portfolio = portfolio
        self.risk_level = risk_level
        self.active_trades: Dict[str, Trade] = {}
        self.trade_history: List[Trade] = []
        self.running = False
        self.task = None
    
    def set_risk_parameters(self):
        """Define parâmetros de risco baseado no nível"""
        if self.risk_level == RiskLevel.CONSERVATIVE:
            self.max_position_size = 0.10  # 10% do capital
            self.stop_loss_percent = 0.02   # 2%
            self.take_profit_percent = 0.05 # 5%
        elif self.risk_level == RiskLevel.MODERATE:
            self.max_position_size = 0.20
            self.stop_loss_percent = 0.05
            self.take_profit_percent = 0.10
        else:  # AGGRESSIVE
            self.max_position_size = 0.30
            self.stop_loss_percent = 0.08
            self.take_profit_percent = 0.15
    
    def calculate_position_size(self, symbol: str, price: float, confidence: float = 1.0) -> float:
        """Calcula o tamanho da posição com base no risco"""
        capital = self.portfolio.equity
        risk_amount = capital * self.max_position_size * confidence
        quantity = risk_amount / price
        # Limitar por liquidez? (simplificado)
        return min(quantity, capital / price)
    
    def execute_trade(self, symbol: str, side: OrderSide, price: float, 
                      confidence: float = 1.0) -> Optional[Trade]:
        """Executa uma ordem de compra/venda"""
        self.set_risk_parameters()
        quantity = self.calculate_position_size(symbol, price, confidence)
        
        if side == OrderSide.BUY:
            cost = quantity * price
            if cost > self.portfolio.cash:
                logger.warning(f"Saldo insuficiente para comprar {symbol}")
                return None
            self.portfolio.cash -= cost
            self.portfolio.positions[symbol] = self.portfolio.positions.get(symbol, 0) + quantity
        
        elif side == OrderSide.SELL:
            if symbol not in self.portfolio.positions or self.portfolio.positions[symbol] < quantity:
                logger.warning(f"Posição insuficiente para vender {symbol}")
                return None
            self.portfolio.positions[symbol] -= quantity
            self.portfolio.cash += quantity * price
            if self.portfolio.positions[symbol] <= 0:
                del self.portfolio.positions[symbol]
        
        trade = Trade(
            id=f"{symbol}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
            status=TradeStatus.OPEN,
            entry_time=datetime.now(),
            entry_price=price,
            stop_loss=price * (1 - self.stop_loss_percent) if side == OrderSide.BUY else price * (1 + self.stop_loss_percent),
            take_profit=price * (1 + self.take_profit_percent) if side == OrderSide.BUY else price * (1 - self.take_profit_percent)
        )
        self.active_trades[trade.id] = trade
        self.portfolio.trades.append(trade)
        logger.info(f"📈 Trade executado: {side.value} {quantity:.4f} {symbol} @ {price:.2f}")
        return trade
    
    def close_trade(self, trade_id: str, current_price: float) -> bool:
        """Fecha uma posição em aberto"""
        if trade_id not in self.active_trades:
            return False
        trade = self.active_trades[trade_id]
        trade.exit_time = datetime.now()
        trade.exit_price = current_price
        trade.pnl = (current_price - trade.entry_price) * trade.quantity if trade.side == OrderSide.BUY else \
                    (trade.entry_price - current_price) * trade.quantity
        trade.pnl_percent = (trade.pnl / (trade.entry_price * trade.quantity)) * 100
        trade.status = TradeStatus.CLOSED
        self.portfolio.total_pnl += trade.pnl
        self.portfolio.equity += trade.pnl
        self.trade_history.append(trade)
        del self.active_trades[trade_id]
        logger.info(f"🔒 Trade fechado: {trade.symbol} PnL: {trade.pnl:.2f} ({trade.pnl_percent:.2f}%)")
        return True
    
    def manage_risk(self, current_prices: Dict[str, float]):
        """Gerencia stop-loss e take-profit para posições abertas"""
        for trade_id, trade in list(self.active_trades.items()):
            price = current_prices.get(trade.symbol)
            if not price:
                continue
            if trade.side == OrderSide.BUY:
                if price <= trade.stop_loss:
                    self.close_trade(trade_id, price)
                elif price >= trade.take_profit:
                    self.close_trade(trade_id, price)
            else:  # SELL
                if price >= trade.stop_loss:
                    self.close_trade(trade_id, price)
                elif price <= trade.take_profit:
                    self.close_trade(trade_id, price)
    
    async def run_loop(self, data_provider: 'DataCollector', strategy_manager: 'StrategyManager'):
        """Loop principal de trading autônomo"""
        self.running = True
        logger.info("🚀 Iniciando loop autônomo de trading...")
        
        while self.running:
            try:
                # Para cada símbolo monitorado
                for symbol in data_provider.symbols:
                    # Obter dados recentes
                    data = data_provider.cache.get(symbol)
                    if data is None or len(data) < 50:
                        continue
                    
                    # Gerar sinal
                    signal = strategy_manager.get_signal(symbol, data)
                    if not signal:
                        continue
                    
                    # Preço atual
                    current_price = data['close'].iloc[-1]
                    
                    # Executar trade
                    if signal == 'BUY':
                        # Verificar se já tem posição
                        if symbol in self.portfolio.positions and self.portfolio.positions[symbol] > 0:
                            continue
                        confidence = 0.8  # poderia vir de um modelo de confiança
                        self.execute_trade(symbol, OrderSide.BUY, current_price, confidence)
                    
                    elif signal == 'SELL':
                        if symbol not in self.portfolio.positions or self.portfolio.positions[symbol] <= 0:
                            continue
                        confidence = 0.8
                        self.execute_trade(symbol, OrderSide.SELL, current_price, confidence)
                
                # Gerenciar risco
                current_prices = {symbol: data['close'].iloc[-1] for symbol, data in data_provider.cache.items() if not data.empty}
                self.manage_risk(current_prices)
                
                # Aguardar próximo ciclo
                await asyncio.sleep(60)  # 1 minuto
                
            except Exception as e:
                logger.error(f"Erro no loop autônomo: {e}")
                await asyncio.sleep(5)
    
    def stop(self):
        """Para o loop autônomo"""
        self.running = False
        if self.task:
            self.task.cancel()
        logger.info("🛑 Loop autônomo parado")

# ============================================================================
# CLASSE DE NEURÔNIO FINANCEIRO (EXTENSÃO DO NEURÔNIO CEREBRAL)
# ============================================================================

class NeuronType(Enum):
    SENSORY = "sensory"
    COGNITIVE = "cognitive"
    MEMORY = "memory"


class AdvancedNeuron:
    """Implementação leve para permitir execução do 'cérebro'.

    Mantém memória de ativações e um contador de disparos.
    """

    def __init__(self, id: str, file_path: str, neuron_type: NeuronType, activation_threshold: float = 0.3, learning_rate: float = 0.1, **kwargs):
        self.id = id
        self.file_path = file_path
        self.neuron_type = neuron_type
        self.activation_threshold = activation_threshold
        self.learning_rate = learning_rate

        self.tags: List[str] = []
        self.current_activation: float = 0.0
        self.activation_history: deque = deque(maxlen=200)
        self.fire_count: int = 0
        self.last_modified: datetime = datetime.now()

    def step(self):
        """Atualiza estado interno com base na ativação atual."""
        # dispara se ultrapassar limiar
        if self.current_activation >= self.activation_threshold:
            self.fire_count += 1


class AdvancedQuantumBrainOrchestrator:
    """Orquestrador mínimo para suportar FinancialBrainOrchestrator."""

    def __init__(self, iag_path: str, quantum_path: str):
        self.iag_path = iag_path
        self.quantum_path = quantum_path
        self.neurons: Dict[str, AdvancedNeuron] = {}
        self.memory: Dict[str, Any] = {}

        # garante diretórios
        Path(self.iag_path).mkdir(parents=True, exist_ok=True)
        Path(self.quantum_path).mkdir(parents=True, exist_ok=True)

    def get_advanced_stats(self) -> Dict[str, Any]:
        return {
            "neurons": len(self.neurons),
            "memory_keys": len(self.memory),
        }


class FinancialNeuron(AdvancedNeuron):

    """Neurônio especializado em dados financeiros"""
    
    def __init__(self, id: str, file_path: str, neuron_type: NeuronType, symbol: Optional[str] = None, **kwargs):
        super().__init__(id, file_path, neuron_type, **kwargs)
        self.symbol = symbol or id
        self.asset_type: Optional[MarketAssetType] = None
        self.indicators: Dict[str, float] = {}
        self.forecast: Optional[float] = None
        self.forecast_confidence: float = 0.0
        self.signal: Optional[str] = None
        self.trade_history: List[Trade] = []
        self.current_position: float = 0.0
        self.pnl_history: List[float] = []
        
        # Adiciona tags financeiras
        if symbol:
            self.tags.append(f"symbol:{symbol}")
        self.tags.append("financial")
    
    def update_market_data(self, market_data: MarketData):
        """Atualiza o neurônio com dados de mercado"""
        self.current_activation = market_data.close / 1000  # Normalização
        self.activation_history.append(self.current_activation)
        if len(self.activation_history) > 100:
            self.activation_history.pop(0)
        
        # Armazena indicadores
        self.indicators['open'] = market_data.open
        self.indicators['high'] = market_data.high
        self.indicators['low'] = market_data.low
        self.indicators['close'] = market_data.close
        self.indicators['volume'] = market_data.volume
        self.asset_type = market_data.asset_type
        self.last_modified = datetime.now()
    
    def set_forecast(self, forecast: float, confidence: float = 0.5):
        """Define previsão de preço"""
        self.forecast = forecast
        self.forecast_confidence = confidence
        # Ativação baseada na previsão
        self.current_activation = max(0.0, min(1.0, forecast / 1000))
    
    def set_signal(self, signal: str):
        """Define sinal de trading"""
        self.signal = signal
        # Ativação mais forte para sinais
        self.fire_count += 1

# ============================================================================
# ORQUESTRADOR FINANCEIRO (EXTENSÃO DO CÉREBRO)
# ============================================================================

class FinancialBrainOrchestrator(AdvancedQuantumBrainOrchestrator):
    """Orquestrador cerebral especializado em finanças"""
    
    def __init__(self, iag_path: str, quantum_path: str):
        super().__init__(iag_path, quantum_path)
        
        # Módulos financeiros
        self.data_collector = DataCollector()
        self.indicator_calc = IndicatorCalculator()
        self.forecaster = FinancialForecaster()
        self.strategy_manager = StrategyManager()
        self.portfolio = Portfolio(cash=100000.0)
        self.trader = AutonomousTrader(self.portfolio, RiskLevel.MODERATE)
        
        # Configurações de mercado
        self.watchlist: List[str] = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'BTC-USD']
        self.interval = "1d"
        self.period = "1y"
        
        # Thread para loop autônomo
        self.autonomous_task = None
        
        # Inicializa neurônios financeiros
        self._initialize_financial_neurons()
        
        # Configura estratégias
        self._setup_strategies()
        
        logger.info("🧠 Orquestrador Financeiro inicializado")
    
    def _initialize_financial_neurons(self):
        """Cria neurônios para cada ativo na watchlist"""
        for symbol in self.watchlist:
            neuron_id = f"fin_{symbol}"
            # Verifica se já existe
            if neuron_id in self.neurons:
                continue
            neuron = FinancialNeuron(
                id=neuron_id,
                file_path=f"/financial/{symbol}",
                neuron_type=NeuronType.SENSORY,
                symbol=symbol,
                activation_threshold=0.3,
                learning_rate=0.1
            )
            self.neurons[neuron_id] = neuron

            
            # Busca dados iniciais
            data = self.data_collector.fetch_historical(symbol, period=self.period, interval=self.interval)
            if data is not None:
                # Atualiza neurônio com último dado
                last_row = data.iloc[-1]
                market_data = MarketData(
                    symbol=symbol,
                    asset_type=self.data_collector._guess_asset_type(symbol),
                    timestamp=datetime.now(),
                    open=last_row['Open'],
                    high=last_row['High'],
                    low=last_row['Low'],
                    close=last_row['Close'],
                    volume=last_row['Volume'],
                    adj_close=last_row['Close']
                )
                neuron.update_market_data(market_data)
                
                # Treina modelos de previsão
                self.forecaster.train_lstm(symbol, data)
                self.forecaster.train_random_forest(symbol, data)
                
                # Faz previsão inicial
                pred = self.forecaster.predict_next_day(symbol, data)
                if pred is not None:
                    neuron.set_forecast(pred, confidence=0.6)
    
    def _setup_strategies(self):
        """Configura estratégias de trading"""
        # Estratégia de cruzamento de médias (Golden Cross)
        strategy1 = TradingStrategy(
            name="GoldenCross",
            indicators=['sma_short', 'sma_long'],
            rules={'sma_short': 50, 'sma_long': 200}
        )
        self.strategy_manager.add_strategy(strategy1)
        
        # Estratégia RSI + MACD
        strategy2 = TradingStrategy(
            name="RSI_MACD",
            indicators=['rsi', 'macd'],
            rules={}
        )
        self.strategy_manager.add_strategy(strategy2)
        
        logger.info(f"✅ {len(self.strategy_manager.strategies)} estratégias configuradas")
    
    async def run_autonomous_trading(self):
        """Inicia o loop autônomo de trading"""
        if self.autonomous_task is None or self.autonomous_task.done():
            self.autonomous_task = asyncio.create_task(
                self.trader.run_loop(self.data_collector, self.strategy_manager)
            )
            logger.info("✅ Trading autônomo iniciado")
        else:
            logger.warning("Trading autônomo já está em execução")
    
    def stop_autonomous_trading(self):
        """Para o trading autônomo"""
        if self.autonomous_task and not self.autonomous_task.done():
            self.trader.stop()
            self.autonomous_task.cancel()
            logger.info("Trading autônomo interrompido")
    
    def update_market_data_all(self):
        """Atualiza dados de mercado para todos os ativos na watchlist"""
        for symbol in self.watchlist:
            data = self.data_collector.fetch_historical(symbol, period=self.period, interval=self.interval)
            if data is not None:
                neuron_id = f"fin_{symbol}"
                if neuron_id in self.neurons:
                    neuron = self.neurons[neuron_id]
                    if isinstance(neuron, FinancialNeuron):
                        last_row = data.iloc[-1]
                        market_data = MarketData(
                            symbol=symbol,
                            asset_type=self.data_collector._guess_asset_type(symbol),
                            timestamp=datetime.now(),
                            open=last_row['Open'],
                            high=last_row['High'],
                            low=last_row['Low'],
                            close=last_row['Close'],
                            volume=last_row['Volume'],
                            adj_close=last_row['Close']
                        )
                        neuron.update_market_data(market_data)
                        
                        # Atualiza previsão
                        pred = self.forecaster.predict_next_day(symbol, data)
                        if pred is not None:
                            neuron.set_forecast(pred, confidence=0.6)
                        
                        # Gera sinal
                        signal = self.strategy_manager.get_signal(symbol, data)
                        if signal:
                            neuron.set_signal(signal)
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Resumo do portfólio atual"""
        return {
            'cash': self.portfolio.cash,
            'equity': self.portfolio.equity,
            'total_pnl': self.portfolio.total_pnl,
            'positions': self.portfolio.positions,
            'open_trades': len(self.trader.active_trades),
            'total_trades': len(self.portfolio.trades),
            'win_rate': self._calculate_win_rate()
        }
    
    def _calculate_win_rate(self) -> float:
        """Calcula taxa de acerto das operações"""
        closed_trades = [t for t in self.portfolio.trades if t.status == TradeStatus.CLOSED]
        if not closed_trades:
            return 0.0
        wins = sum(1 for t in closed_trades if t.pnl > 0)
        return wins / len(closed_trades)
    
    def get_advanced_stats(self) -> Dict[str, Any]:
        """Estatísticas avançadas incluindo dados financeiros"""
        stats = super().get_advanced_stats()
        stats.update({
            'watchlist': self.watchlist,
            'portfolio': self.get_portfolio_summary(),
            'strategies': list(self.strategy_manager.strategies.keys()),
            'trading_active': self.trader.running
        })
        return stats

# ============================================================================
# INTERFACE GRÁFICA AVANÇADA (FINANCEIRA)
# ============================================================================

if not TKINTER_AVAILABLE:
    FinancialDashboard = None
else:
    class FinancialDashboard(tk.Tk):
        """Dashboard gráfico para monitoramento financeiro"""

    
    def __init__(self, orchestrator: FinancialBrainOrchestrator):
        super().__init__()
        self.orchestrator = orchestrator
        self.title("LEXTRADER-IAG 5.0 - Financial Brain")
        self.geometry("1400x900")
        self.configure(bg='#2E2E2E')
        
        # Estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', background='#2E2E2E', foreground='white')
        self.style.configure('TButton', background='#444', foreground='white')
        self.style.configure('TLabelframe', background='#2E2E2E', foreground='white')
        self.style.configure('TLabelframe.Label', background='#2E2E2E', foreground='white')
        
        self.create_widgets()
        self.update_loop()
    
    def create_widgets(self):
        """Cria todos os widgets do dashboard"""
        # Painel principal com abas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba de Visão Geral
        self.tab_overview = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_overview, text="📊 Visão Geral")
        self.create_overview_tab()
        
        # Aba de Gráficos
        self.tab_charts = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_charts, text="📈 Gráficos")
        self.create_charts_tab()
        
        # Aba de Trades
        self.tab_trades = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_trades, text="💹 Trades")
        self.create_trades_tab()
        
        # Aba de Previsões
        self.tab_forecasts = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_forecasts, text="🔮 Previsões")
        self.create_forecasts_tab()
        
        # Aba de Status do Cérebro
        self.tab_brain = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_brain, text="🧠 Cérebro")
        self.create_brain_tab()
    
    def create_overview_tab(self):
        """Visão geral: portfólio, posições, performance"""
        # Frame superior: resumo do portfólio
        frame_top = ttk.LabelFrame(self.tab_overview, text="📊 Portfólio")
        frame_top.pack(fill=tk.X, padx=5, pady=5)
        
        self.lbl_cash = ttk.Label(frame_top, text="Caixa: $0.00")
        self.lbl_cash.pack(side=tk.LEFT, padx=20, pady=5)
        
        self.lbl_equity = ttk.Label(frame_top, text="Patrimônio: $0.00")
        self.lbl_equity.pack(side=tk.LEFT, padx=20, pady=5)
        
        self.lbl_pnl = ttk.Label(frame_top, text="PnL Total: $0.00")
        self.lbl_pnl.pack(side=tk.LEFT, padx=20, pady=5)
        
        self.lbl_winrate = ttk.Label(frame_top, text="Win Rate: 0%")
        self.lbl_winrate.pack(side=tk.LEFT, padx=20, pady=5)
        
        # Frame de posições
        frame_pos = ttk.LabelFrame(self.tab_overview, text="📦 Posições Abertas")
        frame_pos.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.tree_positions = ttk.Treeview(frame_pos, columns=('Ativo', 'Quantidade', 'Preço Médio', 'PnL'), show='headings')
        self.tree_positions.heading('Ativo', text='Ativo')
        self.tree_positions.heading('Quantidade', text='Quantidade')
        self.tree_positions.heading('Preço Médio', text='Preço Médio')
        self.tree_positions.heading('PnL', text='PnL')
        self.tree_positions.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Trades recentes
        frame_trades = ttk.LabelFrame(self.tab_overview, text="📋 Últimos Trades")
        frame_trades.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.tree_recent_trades = ttk.Treeview(frame_trades, columns=('Ativo', 'Lado', 'Qtd', 'Preço', 'PnL'), show='headings')
        self.tree_recent_trades.heading('Ativo', text='Ativo')
        self.tree_recent_trades.heading('Lado', text='Lado')
        self.tree_recent_trades.heading('Qtd', text='Qtd')
        self.tree_recent_trades.heading('Preço', text='Preço')
        self.tree_recent_trades.heading('PnL', text='PnL')
        self.tree_recent_trades.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_charts_tab(self):
        """Aba de gráficos: candlestick, indicadores"""
        # Frame para seleção de ativo
        frame_select = ttk.Frame(self.tab_charts)
        frame_select.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(frame_select, text="Ativo:").pack(side=tk.LEFT, padx=5)
        self.combo_symbol = ttk.Combobox(frame_select, values=self.orchestrator.watchlist)
        self.combo_symbol.pack(side=tk.LEFT, padx=5)
        self.combo_symbol.set(self.orchestrator.watchlist[0] if self.orchestrator.watchlist else 'AAPL')
        
        ttk.Label(frame_select, text="Período:").pack(side=tk.LEFT, padx=5)
        self.combo_period = ttk.Combobox(frame_select, values=['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y'])
        self.combo_period.pack(side=tk.LEFT, padx=5)
        self.combo_period.set('1y')
        
        btn_update = ttk.Button(frame_select, text="Atualizar Gráfico", command=self.update_chart)
        btn_update.pack(side=tk.LEFT, padx=5)
        
        # Frame do gráfico
        self.figure = Figure(figsize=(10, 6), dpi=100, facecolor='#2E2E2E')
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#1E1E1E')
        self.canvas = FigureCanvasTkAgg(self.figure, self.tab_charts)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, self.tab_charts)
        toolbar.update()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_trades_tab(self):
        """Aba de histórico de trades"""
        frame = ttk.LabelFrame(self.tab_trades, text="📋 Histórico de Trades")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.tree_all_trades = ttk.Treeview(frame, columns=('ID', 'Ativo', 'Lado', 'Qtd', 'Entrada', 'Saída', 'PnL', 'Status'), show='headings')
        self.tree_all_trades.heading('ID', text='ID')
        self.tree_all_trades.heading('Ativo', text='Ativo')
        self.tree_all_trades.heading('Lado', text='Lado')
        self.tree_all_trades.heading('Qtd', text='Qtd')
        self.tree_all_trades.heading('Entrada', text='Entrada')
        self.tree_all_trades.heading('Saída', text='Saída')
        self.tree_all_trades.heading('PnL', text='PnL')
        self.tree_all_trades.heading('Status', text='Status')
        self.tree_all_trades.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_forecasts_tab(self):
        """Aba de previsões para os ativos"""
        frame = ttk.LabelFrame(self.tab_forecasts, text="🔮 Previsões")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tabela de previsões
        self.tree_forecasts = ttk.Treeview(frame, columns=('Ativo', 'Preço Atual', 'Previsão', 'Confiança', 'Sinal'), show='headings')
        self.tree_forecasts.heading('Ativo', text='Ativo')
        self.tree_forecasts.heading('Preço Atual', text='Preço Atual')
        self.tree_forecasts.heading('Previsão', text='Previsão')
        self.tree_forecasts.heading('Confiança', text='Confiança')
        self.tree_forecasts.heading('Sinal', text='Sinal')
        self.tree_forecasts.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botão para atualizar previsões
        btn_update_forecast = ttk.Button(frame, text="Atualizar Previsões", command=self.update_forecasts)
        btn_update_forecast.pack(pady=10)
    
    def create_brain_tab(self):
        """Aba de status do cérebro (similar à anterior)"""
        frame = ttk.LabelFrame(self.tab_brain, text="🧠 Status do Cérebro")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.brain_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, bg='#1E1E1E', fg='white')
        self.brain_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def update_loop(self):
        """Loop de atualização da interface"""
        self.update_overview()
        self.update_trades()
        self.update_forecasts()
        self.update_brain()
        self.after(5000, self.update_loop)  # Atualiza a cada 5 segundos
    
    def update_overview(self):
        """Atualiza visão geral"""
        summary = self.orchestrator.get_portfolio_summary()
        self.lbl_cash.config(text=f"Caixa: ${summary['cash']:.2f}")
        self.lbl_equity.config(text=f"Patrimônio: ${summary['equity']:.2f}")
        self.lbl_pnl.config(text=f"PnL Total: ${summary['total_pnl']:.2f}")
        self.lbl_winrate.config(text=f"Win Rate: {summary['win_rate']*100:.1f}%")
        
        # Posições
        for item in self.tree_positions.get_children():
            self.tree_positions.delete(item)
        for symbol, qty in self.orchestrator.portfolio.positions.items():
            if qty > 0:
                # Obter preço atual
                neuron = self.orchestrator.neurons.get(f"fin_{symbol}")
                price = neuron.indicators.get('close', 0) if neuron else 0
                pnl = 0  # calcular...
                self.tree_positions.insert('', tk.END, values=(symbol, f"{qty:.4f}", f"{price:.2f}", f"{pnl:.2f}"))
        
        # Trades recentes
        for item in self.tree_recent_trades.get_children():
            self.tree_recent_trades.delete(item)
        recent = self.orchestrator.portfolio.trades[-10:] if self.orchestrator.portfolio.trades else []
        for trade in reversed(recent):
            pnl_str = f"{trade.pnl:.2f}" if trade.status == TradeStatus.CLOSED else "-"
            self.tree_recent_trades.insert('', tk.END, values=(
                trade.symbol,
                trade.side.value,
                f"{trade.quantity:.4f}",
                f"{trade.price:.2f}",
                pnl_str
            ))
    
    def update_trades(self):
        """Atualiza tabela de todos os trades"""
        for item in self.tree_all_trades.get_children():
            self.tree_all_trades.delete(item)
        for trade in self.orchestrator.portfolio.trades:
            status = trade.status.value
            self.tree_all_trades.insert('', tk.END, values=(
                trade.id,
                trade.symbol,
                trade.side.value,
                f"{trade.quantity:.4f}",
                trade.entry_time.strftime('%Y-%m-%d %H:%M'),
                trade.exit_time.strftime('%Y-%m-%d %H:%M') if trade.exit_time else "-",
                f"{trade.pnl:.2f}" if trade.pnl else "-",
                status
            ))
    
    def update_forecasts(self):
        """Atualiza previsões"""
        for item in self.tree_forecasts.get_children():
            self.tree_forecasts.delete(item)
        for symbol in self.orchestrator.watchlist:
            neuron = self.orchestrator.neurons.get(f"fin_{symbol}")
            if neuron and isinstance(neuron, FinancialNeuron):
                current_price = neuron.indicators.get('close', 0)
                forecast = neuron.forecast if neuron.forecast else 0
                confidence = neuron.forecast_confidence if neuron.forecast_confidence else 0
                signal = neuron.signal if neuron.signal else "-"
                self.tree_forecasts.insert('', tk.END, values=(
                    symbol,
                    f"{current_price:.2f}",
                    f"{forecast:.2f}",
                    f"{confidence*100:.1f}%",
                    signal
                ))
    
    def update_brain(self):
        """Atualiza status do cérebro"""
        stats = self.orchestrator.get_advanced_stats()
        text = json.dumps(stats, indent=2, default=str)
        self.brain_text.delete(1.0, tk.END)
        self.brain_text.insert(tk.END, text)
    
    def update_chart(self):
        """Atualiza gráfico de candlestick"""
        symbol = self.combo_symbol.get()
        period = self.combo_period.get()
        data = self.orchestrator.data_collector.fetch_historical(symbol, period=period)
        if data is None or data.empty:
            return
        
        self.ax.clear()
        # Candlestick simples com matplotlib
        # Adaptado para mostrar linha de preço e volume
        data['date'] = data.index
        self.ax.plot(data['date'], data['Close'], color='cyan', linewidth=1.5, label='Close')
        self.ax.fill_between(data['date'], data['Close'].min(), data['Close'], alpha=0.1, color='cyan')
        self.ax.set_title(f"{symbol} - Preço de Fechamento", color='white')
        self.ax.set_xlabel('Data', color='white')
        self.ax.set_ylabel('Preço', color='white')
        self.ax.tick_params(colors='white')
        self.ax.legend(loc='upper left', facecolor='#2E2E2E', edgecolor='white', labelcolor='white')
        self.ax.grid(True, alpha=0.3)
        
        # Adicionar indicador de previsão se disponível
        neuron = self.orchestrator.neurons.get(f"fin_{symbol}")
        if neuron and neuron.forecast:
            self.ax.axhline(y=neuron.forecast, color='red', linestyle='--', alpha=0.7, label='Previsão')
            self.ax.legend()
        
        self.canvas.draw()

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal para inicializar o sistema"""

    logger.info("🚀 Iniciando LEXTRADER-IAG 5.0...")
    
    # Inicializa orquestrador financeiro
    brain = FinancialBrainOrchestrator(
        iag_path=os.path.join(os.getcwd(), "iag_data"),
        quantum_path=os.path.join(os.getcwd(), "quantum_data")
    )
    
    # Atualiza dados iniciais
    brain.update_market_data_all()
    
    # Inicia loop autônomo em background (se desejar)
    # asyncio.create_task(brain.run_autonomous_trading())
    
    # Inicia interface gráfica
    if FinancialDashboard is None:
        logger.warning("Interface gráfica indisponível (Tkinter não disponível). Rodando somente o núcleo.")
        return
    app = FinancialDashboard(brain)

    
    # Trata fechamento
    def on_closing():
        brain.stop_autonomous_trading()
        app.destroy()
    
    app.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Executa app
    try:
        app.mainloop()
    except KeyboardInterrupt:
        brain.stop_autonomous_trading()
        logger.info("Sistema finalizado pelo usuário")

if __name__ == "__main__":
    # Para Windows, necessário asyncio com event loop
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    main()