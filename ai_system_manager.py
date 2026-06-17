"""
Sistema Avançado de IA para Previsão Financeira
===============================================
Sistema de aprendizado profundo para análise e previsão de mercados financeiros
com múltiplas arquiteturas de modelos, processamento paralelo e monitoramento avançado.

Autor: Sistema de IA Financeira Avançada
Versão: 4.2.0
Data: 2024
Licença: MIT
"""

import os
import sys
import logging
import warnings
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Callable, Union
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from functools import wraps, lru_cache
import hashlib
import pickle
import json
import time
import gc
import traceback
import threading
import queue
import asyncio
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from contextlib import contextmanager, asynccontextmanager
import weakref
import copy
import inspect
import random
from statistics import mean, median, stdev
import secrets

# Data Science & ML
import numpy as np
import pandas as pd
from scipy import stats, signal, optimize
from scipy.stats import norm, skew, kurtosis
import sklearn
from sklearn.preprocessing import (
    MinMaxScaler, StandardScaler, RobustScaler,
    PowerTransformer, QuantileTransformer, FunctionTransformer
)
from sklearn.model_selection import (
    train_test_split, TimeSeriesSplit, GridSearchCV, RandomizedSearchCV
)
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    mean_absolute_percentage_error, explained_variance_score,
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
from sklearn.ensemble import (
    RandomForestRegressor, GradientBoostingRegressor,
    VotingRegressor, StackingRegressor
)
from sklearn.decomposition import PCA, FastICA, TruncatedSVD
from sklearn.cluster import KMeans, DBSCAN
from sklearn.feature_selection import (
    SelectKBest, RFE, SelectFromModel, mutual_info_regression
)
from sklearn.covariance import EllipticEnvelope

# Deep Learning
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model, Input
from tensorflow.keras.models import Sequential, load_model, clone_model
from tensorflow.keras.layers import (
    LSTM, GRU, Bidirectional, Conv1D, Conv2D, MaxPooling1D, MaxPooling2D,
    Dense, Dropout, BatchNormalization, LayerNormalization,
    Flatten, Reshape, Concatenate, Multiply, Add,
    Attention, MultiHeadAttention, LayerNormalization,
    TimeDistributed, SpatialDropout1D, GaussianNoise,
    Lambda, Activation, LeakyReLU, PReLU, ELU
)
from tensorflow.keras.optimizers import (
    Adam, SGD, RMSprop, Nadam, Adagrad, Adadelta, Adamax
)
from tensorflow.keras.optimizers.schedules import (
    ExponentialDecay, PiecewiseConstantDecay,
    CosineDecay, CosineDecayRestarts
)
from tensorflow.keras.regularizers import l1, l2, l1_l2
from tensorflow.keras.constraints import max_norm, unit_norm
from tensorflow.keras.callbacks import (
    EarlyStopping, ReduceLROnPlateau, ModelCheckpoint,
    TensorBoard, CSVLogger, TerminateOnNaN,
    LearningRateScheduler, LambdaCallback, RemoteMonitor
)
from tensorflow.keras.metrics import (
    MeanSquaredError, MeanAbsoluteError, RootMeanSquaredError,
    AUC, Precision, Recall
)
from tensorflow.keras.losses import (
    MeanSquaredError, MeanAbsoluteError, Huber, LogCosh
)
from tensorflow.keras.utils import plot_model
import tensorflow_probability as tfp
import tensorflow_addons as tfa
from tensorflow_addons.optimizers import (
    CyclicalLearningRate, RectifiedAdam, Lookahead
)
from tensorflow_addons.losses import TripletSemiHardLoss
from tensorflow_addons.metrics import (
    F1Score, MatthewsCorrelationCoefficient, CohenKappa
)

# Data Acquisition
import yfinance as yf
import pandas_datareader.data as web
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import aiohttp
import asyncio_throttle
from bs4 import BeautifulSoup

# System & Performance
import psutil
import GPUtil
import pynvml
import multiprocessing
from multiprocessing import Pool, Manager, cpu_count
import signal
import zmq
import redis
import msgpack
import orjson
import dill
import joblib
from joblib import Parallel, delayed, Memory
import numba
from numba import jit, prange, vectorize
import cython

# Visualization (optional imports)
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    from mplfinance.original_flavor import candlestick_ohlc
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    import bokeh.plotting as bp
    from bokeh.models import ColumnDataSource, HoverTool
    from bokeh.layouts import gridplot
    HAVE_VIS = True
except ImportError:
    HAVE_VIS = False
    logging.warning("Bibliotecas de visualização não encontradas")

# Database
try:
    import sqlalchemy as sa
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker, declarative_base
    from sqlalchemy.pool import QueuePool
    import pymongo
    from pymongo import MongoClient
    import influxdb
    from influxdb import InfluxDBClient
    HAVE_DB = True
except ImportError:
    HAVE_DB = False

# Crypto & Blockchain
try:
    import ccxt
    from web3 import Web3
    HAVE_CRYPTO = True
except ImportError:
    HAVE_CRYPTO = False

# ============================================================================
# CONFIGURAÇÃO AVANÇADA
# ============================================================================

# Suprimir warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Configurar TensorFlow para performance
tf.config.optimizer.set_jit(True)  # Ativar XLA
tf.config.threading.set_intra_op_parallelism_threads(0)  # Auto-otimizar
tf.config.threading.set_inter_op_parallelism_threads(0)  # Auto-otimizar

# Configuração avançada de logging
def setup_advanced_logging(log_level=logging.INFO, log_to_file=True, log_to_console=True):
    """Configura sistema de logging avançado com múltiplos handlers"""
    
    # Criar logger principal
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Limpar handlers existentes
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Formato estruturado
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - '
        '%(filename)s:%(lineno)d - %(funcName)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler com rotação
    if log_to_file:
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / f'ai_system_{datetime.now().strftime("%Y%m%d")}.log',
            maxBytes=10485760,  # 10MB
            backupCount=10,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)
    
    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(log_level)
        logger.addHandler(console_handler)
    
    # Syslog handler (opcional)
    try:
        syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
        syslog_handler.setFormatter(formatter)
        logger.addHandler(syslog_handler)
    except:
        pass
    
    # JSON handler para logs estruturados
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_record = {
                'timestamp': self.formatTime(record),
                'level': record.levelname,
                'logger': record.name,
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno,
                'message': record.getMessage(),
                'exception': record.exc_info
            }
            return json.dumps(log_record)
    
    json_handler = logging.FileHandler(log_dir / 'structured_logs.jsonl')
    json_handler.setFormatter(JSONFormatter())
    logger.addHandler(json_handler)
    
    # Capture warnings
    logging.captureWarnings(True)
    
    return logger

# Inicializar logging
logger = setup_advanced_logging(logging.INFO)

# ============================================================================
# ENUMS E ESTRUTURAS DE DADOS
# ============================================================================

class ModelType(Enum):
    """Tipos de modelos disponíveis"""
    LSTM_BASIC = "lstm_basic"
    LSTM_ADVANCED = "lstm_advanced"
    CNN_LSTM = "cnn_lstm"
    TRANSFORMER = "transformer"
    ATTENTION_LSTM = "attention_lstm"
    WAVENET = "wavenet"
    ENSEMBLE = "ensemble"
    AUTOENCODER = "autoencoder"
    BIDIRECTIONAL_LSTM = "bidirectional_lstm"
    GRU = "gru"
    TCN = "tcn"  # Temporal Convolutional Network
    NEURALODE = "neural_ode"  # Neural Ordinary Differential Equations

class DataSource(Enum):
    """Fontes de dados disponíveis"""
    YFINANCE = "yfinance"
    ALPHA_VANTAGE = "alpha_vantage"
    TIINGO = "tiingo"
    IEX_CLOUD = "iex_cloud"
    QUANDL = "quandl"
    CRYPTO = "crypto_exchange"
    CUSTOM_API = "custom_api"
    DATABASE = "database"

class TradingSignal(Enum):
    """Sinais de trading gerados"""
    STRONG_BUY = 2
    BUY = 1
    NEUTRAL = 0
    SELL = -1
    STRONG_SELL = -2

class MarketCondition(Enum):
    """Condições de mercado"""
    BULLISH = "bullish"
    BEARISH = "bearish"
    SIDEWAYS = "sideways"
    VOLATILE = "volatile"
    TRENDING = "trending"
    RANGING = "ranging"

@dataclass
class TrainingConfig:
    """Configuração completa de treinamento"""
    epochs: int = 200
    batch_size: int = 64
    validation_split: float = 0.15
    test_split: float = 0.15
    early_stopping_patience: int = 20
    learning_rate: float = 0.001
    sequence_length: int = 60
    lookback_window: int = 30
    shuffle: bool = True
    use_class_weights: bool = True
    augmentation: bool = True
    curriculum_learning: bool = False
    gradient_accumulation_steps: int = 1
    mixed_precision: bool = True
    distributed_training: bool = False
    
    # Otimizador
    optimizer: str = "adam"
    optimizer_params: Dict = field(default_factory=lambda: {
        "beta_1": 0.9,
        "beta_2": 0.999,
        "epsilon": 1e-7,
        "amsgrad": False
    })
    
    # Schedule de learning rate
    lr_schedule: str = "exponential_decay"
    lr_params: Dict = field(default_factory=lambda: {
        "decay_rate": 0.96,
        "decay_steps": 1000,
        "staircase": True
    })
    
    # Regularização
    regularization: Dict = field(default_factory=lambda: {
        "l1": 0.001,
        "l2": 0.01,
        "dropout_rate": 0.3,
        "recurrent_dropout": 0.2
    })
    
    def to_dict(self):
        return asdict(self)

@dataclass
class ModelPerformance:
    """Métricas de performance detalhadas do modelo"""
    symbol: str
    mse: float
    rmse: float
    mae: float
    mape: float
    r2: float
    directional_accuracy: float
    sharpe_ratio: float
    max_drawdown: float
    profit_factor: float
    win_rate: float
    avg_win_loss_ratio: float
    confidence_score: float
    last_updated: datetime
    training_time: float
    inference_time: float
    model_size_mb: float
    calibration_error: float = 0.0
    uncertainty_score: float = 0.0
    
    def get_summary(self) -> Dict:
        return {
            'symbol': self.symbol,
            'accuracy': self.directional_accuracy,
            'sharpe': self.sharpe_ratio,
            'max_dd': self.max_drawdown,
            'confidence': self.confidence_score,
            'timestamp': self.last_updated.isoformat()
        }

@dataclass
class PredictionResult:
    """Resultado detalhado de previsão"""
    symbol: str
    predictions: np.ndarray
    confidence_intervals: Tuple[np.ndarray, np.ndarray]
    point_predictions: np.ndarray
    probabilities: Optional[np.ndarray] = None
    signals: Optional[List[TradingSignal]] = None
    uncertainty: Optional[np.ndarray] = None
    feature_importance: Optional[Dict[str, float]] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame({
            'prediction': self.point_predictions,
            'lower_bound': self.confidence_intervals[0],
            'upper_bound': self.confidence_intervals[1],
            'confidence': self.confidence_intervals[1] - self.confidence_intervals[0]
        })
        
        if self.uncertainty is not None:
            df['uncertainty'] = self.uncertainty
        
        if self.signals is not None:
            df['signal'] = [s.value for s in self.signals]
        
        return df

@dataclass
class PortfolioRecommendation:
    """Recomendação de portfolio baseada em previsões"""
    symbol: str
    action: str  # BUY, SELL, HOLD
    target_price: float
    stop_loss: float
    take_profit: float
    position_size: float
    risk_reward_ratio: float
    confidence: float
    time_horizon: str
    reasoning: List[str]
    alternatives: List[Dict]

# ============================================================================
# DECORADORES E UTILITÁRIOS
# ============================================================================

def retry_with_backoff(max_retries=3, base_delay=1.0, max_delay=30.0, 
                      exponential_base=2.0, jitter=True):
    """Decorador para retry com backoff exponencial e jitter"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Todas as {max_retries} tentativas falharam: {e}")
                        raise
                    
                    # Calcular delay com jitter
                    if jitter:
                        delay *= exponential_base * (0.5 + random.random())
                    else:
                        delay *= exponential_base
                    
                    delay = min(delay, max_delay)
                    
                    logger.warning(f"Tentativa {attempt + 1} falhou para {func.__name__}: {e}. "
                                  f"Retrying in {delay:.2f}s...")
                    await asyncio.sleep(delay)
            
            raise RuntimeError(f"Falha após {max_retries} tentativas")
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Todas as {max_retries} tentativas falharam: {e}")
                        raise
                    
                    if jitter:
                        delay *= exponential_base * (0.5 + random.random())
                    else:
                        delay *= exponential_base
                    
                    delay = min(delay, max_delay)
                    
                    logger.warning(f"Tentativa {attempt + 1} falhou para {func.__name__}: {e}. "
                                  f"Retrying in {delay:.2f}s...")
                    time.sleep(delay)
            
            raise RuntimeError(f"Falha após {max_retries} tentativas")
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

def benchmark(n_iterations=100, warmup=10):
    """Decorador para benchmark de performance com warmup"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Warmup
            for _ in range(warmup):
                func(*args, **kwargs)
            
            # Benchmark
            times = []
            results = []
            
            for i in range(n_iterations):
                start_time = time.perf_counter_ns()
                result = func(*args, **kwargs)
                end_time = time.perf_counter_ns()
                
                times.append((end_time - start_time) / 1e9)  # Converter para segundos
                results.append(result)
                
                if i % 10 == 0:
                    logger.debug(f"Benchmark iteration {i}: {times[-1]:.6f}s")
            
            stats = {
                'function': func.__name__,
                'min': min(times),
                'max': max(times),
                'mean': mean(times),
                'median': median(times),
                'std': stdev(times) if len(times) > 1 else 0,
                'p95': np.percentile(times, 95),
                'p99': np.percentile(times, 99),
                'iterations': n_iterations
            }
            
            logger.info(f"Benchmark results for {func.__name__}: {stats}")
            return results[-1] if results else None
        
        return wrapper
    return decorator

def cache_results(ttl_seconds=3600, max_size=1000):
    """Decorador para cache de resultados com TTL"""
    cache = {}
    cache_timestamps = {}
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Criar chave de cache
            cache_key = hashlib.md5(
                f"{func.__module__}.{func.__name__}:{args}:{kwargs}".encode()
            ).hexdigest()
            
            current_time = time.time()
            
            # Verificar cache válido
            if cache_key in cache:
                timestamp = cache_timestamps[cache_key]
                if current_time - timestamp < ttl_seconds:
                    logger.debug(f"Cache hit for {func.__name__}")
                    return cache[cache_key]
            
            # Limpar cache se necessário
            if len(cache) >= max_size:
                oldest_key = min(cache_timestamps.keys(), key=lambda k: cache_timestamps[k])
                del cache[oldest_key]
                del cache_timestamps[oldest_key]
            
            # Executar função
            result = func(*args, **kwargs)
            
            # Armazenar em cache
            cache[cache_key] = result
            cache_timestamps[cache_key] = current_time
            
            return result
        
        return wrapper
    return decorator

@contextmanager
def resource_monitor(resource_type='memory', threshold=0.8):
    """Monitora uso de recursos durante execução"""
    monitor = SystemMonitor()
    
    if resource_type == 'memory':
        start_usage = psutil.virtual_memory().percent / 100
    elif resource_type == 'cpu':
        start_usage = psutil.cpu_percent() / 100
    elif resource_type == 'gpu':
        gpus = GPUtil.getGPUs()
        start_usage = gpus[0].memoryUtil if gpus else 0
    else:
        start_usage = 0
    
    try:
        yield
    finally:
        if resource_type == 'memory':
            end_usage = psutil.virtual_memory().percent / 100
        elif resource_type == 'cpu':
            end_usage = psutil.cpu_percent() / 100
        elif resource_type == 'gpu':
            gpus = GPUtil.getGPUs()
            end_usage = gpus[0].memoryUtil if gpus else 0
        
        usage_change = end_usage - start_usage
        
        if usage_change > threshold:
            logger.warning(f"Alto uso de {resource_type}: {usage_change:.2%}")

# ============================================================================
# PROCESSAMENTO AVANÇADO DE DADOS
# ============================================================================

class AdvancedDataPreprocessor:
    """Pré-processador avançado de dados financeiros com múltiplas técnicas"""
    
    def __init__(self):
        self.scalers = {}
        self.feature_encoders = {}
        self.feature_columns = [
            'Open', 'High', 'Low', 'Close', 'Volume',
            'Returns', 'Volatility', 'Volume_MA'
        ]
        self.cache = {}
        
    def create_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cria indicadores técnicos avançados"""
        data = df.copy()
        
        # Preços
        data['Returns'] = data['Close'].pct_change()
        data['Log_Returns'] = np.log(data['Close'] / data['Close'].shift(1))
        data['Price_Change'] = data['Close'].diff()
        
        # Médias Móveis
        for period in [5, 10, 20, 50, 100, 200]:
            data[f'SMA_{period}'] = data['Close'].rolling(window=period).mean()
            data[f'EMA_{period}'] = data['Close'].ewm(span=period, adjust=False).mean()
            data[f'WMA_{period}'] = data['Close'].rolling(window=period).apply(
                lambda x: np.dot(x, np.arange(1, period + 1)) / np.sum(np.arange(1, period + 1)),
                raw=True
            )
        
        # Bandas de Bollinger
        data['BB_Middle'] = data['SMA_20']
        bb_std = data['Close'].rolling(window=20).std()
        data['BB_Upper'] = data['BB_Middle'] + (2 * bb_std)
        data['BB_Lower'] = data['BB_Middle'] - (2 * bb_std)
        data['BB_Width'] = (data['BB_Upper'] - data['BB_Lower']) / data['BB_Middle']
        data['BB_Position'] = (data['Close'] - data['BB_Lower']) / (data['BB_Upper'] - data['BB_Lower'])
        
        # MACD
        data['MACD'] = data['EMA_12'] - data['EMA_26']
        data['MACD_Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
        data['MACD_Histogram'] = data['MACD'] - data['MACD_Signal']
        
        # RSI
        data['RSI'] = self.calculate_rsi(data['Close'], period=14)
        data['RSI_MA'] = data['RSI'].rolling(window=9).mean()
        
        # Estocástico
        data['Stochastic'] = self.calculate_stochastic(data, period=14)
        data['Stochastic_Signal'] = data['Stochastic'].rolling(window=3).mean()
        
        # ATR
        data['ATR'] = self.calculate_atr(data, period=14)
        
        # Volume Indicators
        data['Volume_MA'] = data['Volume'].rolling(window=20).mean()
        data['Volume_Ratio'] = data['Volume'] / data['Volume_MA']
        data['OBV'] = self.calculate_obv(data)
        data['Volume_Price_Trend'] = self.calculate_vpt(data)
        
        # Indicadores de Momentum
        data['ROC'] = data['Close'].pct_change(periods=10) * 100
        data['Williams_%R'] = self.calculate_williams_r(data)
        data['CCI'] = self.calculate_cci(data)
        
        # Indicadores de Tendência
        data['ADX'] = self.calculate_adx(data)
        data['Parabolic_SAR'] = self.calculate_parabolic_sar(data)
        
        # Indicadores de Volatilidade
        data['Volatility'] = data['Returns'].rolling(window=20).std() * np.sqrt(252)
        data['Historical_VaR'] = self.calculate_var(data['Returns'])
        data['Expected_Shortfall'] = self.calculate_expected_shortfall(data['Returns'])
        
        # Indicadores de Ciclo
        data['Hilbert_Transform'] = self.calculate_hilbert_transform(data['Close'])
        
        # Features de padrões de candles
        data = self.add_candle_patterns(data)
        
        # Features de Fourier
        data = self.add_fourier_features(data, 'Close', n_components=5)
        
        # Features de wavelet
        data = self.add_wavelet_features(data, 'Close')
        
        # Remover NaN values
        data = data.replace([np.inf, -np.inf], np.nan).dropna()
        
        # Adicionar timestamp features
        data = self.add_temporal_features(data)
        
        logger.info(f"Criados {len(data.columns)} indicadores técnicos")
        
        return data
    
    def calculate_atr(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calcula Average True Range"""
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        return true_range.rolling(window=period).mean()
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calcula Relative Strength Index com suavização Wilder"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def calculate_stochastic(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calcula Stochastic Oscillator"""
        lowest_low = df['Low'].rolling(window=period).min()
        highest_high = df['High'].rolling(window=period).max()
        
        return 100 * ((df['Close'] - lowest_low) / (highest_high - lowest_low))
    
    def calculate_obv(self, df: pd.DataFrame) -> pd.Series:
        """Calcula On-Balance Volume"""
        obv = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()
        return obv
    
    def calculate_vpt(self, df: pd.DataFrame) -> pd.Series:
        """Calcula Volume Price Trend"""
        vpt = df['Volume'] * ((df['Close'] - df['Close'].shift(1)) / df['Close'].shift(1))
        return vpt.cumsum()
    
    def calculate_williams_r(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calcula Williams %R"""
        highest_high = df['High'].rolling(window=period).max()
        lowest_low = df['Low'].rolling(window=period).min()
        
        return -100 * ((highest_high - df['Close']) / (highest_high - lowest_low))
    
    def calculate_cci(self, df: pd.DataFrame, period: int = 20) -> pd.Series:
        """Calcula Commodity Channel Index"""
        typical_price = (df['High'] + df['Low'] + df['Close']) / 3
        sma = typical_price.rolling(window=period).mean()
        mean_deviation = typical_price.rolling(window=period).apply(
            lambda x: np.mean(np.abs(x - x.mean()))
        )
        
        return (typical_price - sma) / (0.015 * mean_deviation)
    
    def calculate_adx(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calcula Average Directional Index"""
        # True Range
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        
        # Directional Movement
        up_move = df['High'].diff()
        down_move = -df['Low'].diff()
        
        pos_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
        neg_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
        
        # Suavizado
        pos_dm_smooth = pd.Series(pos_dm).rolling(window=period).sum()
        neg_dm_smooth = pd.Series(neg_dm).rolling(window=period).sum()
        tr_smooth = tr.rolling(window=period).sum()
        
        # Directional Indicators
        pos_di = 100 * (pos_dm_smooth / tr_smooth)
        neg_di = 100 * (neg_dm_smooth / tr_smooth)
        
        # DX e ADX
        dx = 100 * np.abs(pos_di - neg_di) / (pos_di + neg_di)
        adx = dx.rolling(window=period).mean()
        
        return adx
    
    def calculate_parabolic_sar(self, df: pd.DataFrame, 
                               acceleration: float = 0.02,
                               maximum: float = 0.2) -> pd.Series:
        """Calcula Parabolic SAR"""
        high = df['High'].values
        low = df['Low'].values
        close = df['Close'].values
        
        psar = np.zeros(len(df))
        trend = np.zeros(len(df))
        ep = np.zeros(len(df))
        af = np.zeros(len(df))
        
        # Inicialização
        psar[0] = close[0]
        trend[0] = 1
        ep[0] = high[0]
        af[0] = acceleration
        
        for i in range(1, len(df)):
            # SAR reverso
            if trend[i-1] == 1:
                psar[i] = psar[i-1] + af[i-1] * (ep[i-1] - psar[i-1])
                if low[i] < psar[i]:
                    trend[i] = -1
                    psar[i] = ep[i-1]
                    ep[i] = low[i]
                    af[i] = acceleration
                else:
                    trend[i] = 1
                    if high[i] > ep[i-1]:
                        ep[i] = high[i]
                        af[i] = min(af[i-1] + acceleration, maximum)
                    else:
                        ep[i] = ep[i-1]
                        af[i] = af[i-1]
            else:
                psar[i] = psar[i-1] - af[i-1] * (psar[i-1] - ep[i-1])
                if high[i] > psar[i]:
                    trend[i] = 1
                    psar[i] = ep[i-1]
                    ep[i] = high[i]
                    af[i] = acceleration
                else:
                    trend[i] = -1
                    if low[i] < ep[i-1]:
                        ep[i] = low[i]
                        af[i] = min(af[i-1] + acceleration, maximum)
                    else:
                        ep[i] = ep[i-1]
                        af[i] = af[i-1]
        
        return pd.Series(psar, index=df.index)
    
    def calculate_var(self, returns: pd.Series, confidence: float = 0.95) -> pd.Series:
        """Calcula Value at Risk histórico"""
        return returns.rolling(window=252).quantile(1 - confidence)
    
    def calculate_expected_shortfall(self, returns: pd.Series, 
                                    confidence: float = 0.95) -> pd.Series:
        """Calcula Expected Shortfall (CVaR)"""
        def es_calc(x):
            var = x.quantile(1 - confidence)
            return x[x <= var].mean()
        
        return returns.rolling(window=252).apply(es_calc)
    
    def calculate_hilbert_transform(self, series: pd.Series) -> pd.Series:
        """Aplica transformada de Hilbert para análise de fase"""
        analytic_signal = signal.hilbert(series.values)
        return pd.Series(np.angle(analytic_signal), index=series.index)
    
    def add_candle_patterns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adiciona padrões de candles japoneses"""
        data = df.copy()
        
        # Corpo do candle
        body = np.abs(data['Close'] - data['Open'])
        candle_range = data['High'] - data['Low']
        
        # Padrões básicos
        data['Is_Doji'] = (body / candle_range) < 0.1
        data['Is_Marubozu'] = (body / candle_range) > 0.9
        data['Is_Hammer'] = ((data['High'] - data['Low']) > 3 * body) & \
                           ((data['Close'] - data['Low']) / (data['High'] - data['Low']) > 0.6)
        
        # Engulfing patterns
        data['Bullish_Engulfing'] = (data['Open'] < data['Close'].shift(1)) & \
                                   (data['Close'] > data['Open'].shift(1)) & \
                                   (data['Open'] < data['Close'].shift(1)) & \
                                   (data['Close'] > data['Open'].shift(1))
        
        data['Bearish_Engulfing'] = (data['Open'] > data['Close'].shift(1)) & \
                                   (data['Close'] < data['Open'].shift(1)) & \
                                   (data['Open'] > data['Close'].shift(1)) & \
                                   (data['Close'] < data['Open'].shift(1))
        
        return data
    
    def add_fourier_features(self, df: pd.DataFrame, column: str, 
                            n_components: int = 5) -> pd.DataFrame:
        """Adiciona features de transformada de Fourier"""
        data = df.copy()
        series = data[column].values
        
        # Aplicar FFT
        fft_values = np.fft.fft(series)
        frequencies = np.fft.fftfreq(len(series))
        
        # Manter componentes principais
        magnitudes = np.abs(fft_values)
        indices = np.argsort(magnitudes)[-n_components:]
        
        for i, idx in enumerate(indices):
            data[f'Fourier_{i}_Freq'] = frequencies[idx]
            data[f'Fourier_{i}_Mag'] = magnitudes[idx]
            data[f'Fourier_{i}_Phase'] = np.angle(fft_values[idx])
        
        return data
    
    def add_wavelet_features(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Adiciona features de wavelet transform"""
        data = df.copy()
        series = data[column].values
        
        try:
            import pywt
            # Aplicar wavelet transform
            coeffs = pywt.wavedec(series, 'db4', level=4)
            
            for i, coeff in enumerate(coeffs):
                # Reconstruir cada nível
                reconstructed = pywt.waverec([coeffs[j] if j == i else None for j in range(len(coeffs))], 
                                           'db4')
                # Garantir mesmo tamanho
                if len(reconstructed) > len(series):
                    reconstructed = reconstructed[:len(series)]
                elif len(reconstructed) < len(series):
                    reconstructed = np.pad(reconstructed, (0, len(series) - len(reconstructed)))
                
                data[f'Wavelet_Level_{i}'] = reconstructed
            
        except ImportError:
            logger.warning("PyWavelets não instalado. Pulando features de wavelet.")
        
        return data
    
    def add_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adiciona features temporais"""
        data = df.copy()
        
        # Features baseadas no índice temporal
        if isinstance(data.index, pd.DatetimeIndex):
            data['Day_of_Week'] = data.index.dayofweek
            data['Day_of_Month'] = data.index.day
            data['Week_of_Year'] = data.index.isocalendar().week
            data['Month'] = data.index.month
            data['Quarter'] = data.index.quarter
            data['Year'] = data.index.year
            
            # Features cíclicas
            data['Day_sin'] = np.sin(2 * np.pi * data['Day_of_Week'] / 7)
            data['Day_cos'] = np.cos(2 * np.pi * data['Day_of_Week'] / 7)
            data['Month_sin'] = np.sin(2 * np.pi * data['Month'] / 12)
            data['Month_cos'] = np.cos(2 * np.pi * data['Month'] / 12)
        
        return data
    
    def prepare_sequences(self, data: np.ndarray, sequence_length: int, 
                         prediction_horizon: int = 1) -> Tuple[np.ndarray, np.ndarray]:
        """Prepara sequências para treinamento com múltiplos horizontes"""
        X, y = [], []
        
        for i in range(sequence_length, len(data) - prediction_horizon + 1):
            X.append(data[i-sequence_length:i])
            # Prever múltiplos passos à frente
            y.append(data[i:i+prediction_horizon, 0])  # Assume que Close é a primeira coluna
            
        return np.array(X), np.array(y)
    
    def create_multivariate_sequences(self, data: np.ndarray, sequence_length: int,
                                     target_col_idx: int = 0,
                                     prediction_horizon: int = 1) -> Tuple[np.ndarray, np.ndarray]:
        """Cria sequências multivariadas"""
        X, y = [], []
        
        for i in range(sequence_length, len(data) - prediction_horizon + 1):
            X.append(data[i-sequence_length:i])
            y.append(data[i:i+prediction_horizon, target_col_idx])
        
        return np.array(X), np.array(y)
    
    def normalize_data(self, data: np.ndarray, symbol: str, 
                      scaler_type: str = 'robust') -> Tuple[np.ndarray, Any]:
        """Normaliza dados usando diferentes estratégias"""
        
        cache_key = f"{symbol}_{scaler_type}_{data.shape}_{data.mean():.6f}"
        
        if cache_key in self.cache:
            logger.debug(f"Cache hit para normalização: {symbol}")
            return self.cache[cache_key]
        
        if scaler_type == 'minmax':
            scaler = MinMaxScaler(feature_range=(-1, 1))
        elif scaler_type == 'standard':
            scaler = StandardScaler()
        elif scaler_type == 'robust':
            scaler = RobustScaler(quantile_range=(5, 95))
        elif scaler_type == 'power':
            scaler = PowerTransformer(method='yeo-johnson')
        elif scaler_type == 'quantile':
            scaler = QuantileTransformer(output_distribution='normal')
        else:
            scaler = RobustScaler()
        
        scaled_data = scaler.fit_transform(data)
        
        self.scalers[symbol] = scaler
        self.cache[cache_key] = (scaled_data, scaler)
        
        # Limpar cache se muito grande
        if len(self.cache) > 1000:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        return scaled_data, scaler
    
    def detect_anomalies(self, data: pd.DataFrame, contamination: float = 0.1) -> pd.DataFrame:
        """Detecta anomalias nos dados"""
        # Isolation Forest
        from sklearn.ensemble import IsolationForest
        from sklearn.svm import OneClassSVM
        
        features = data.select_dtypes(include=[np.number]).columns
        
        # Usar múltiplos detectores
        detectors = {
            'isolation_forest': IsolationForest(
                contamination=contamination,
                random_state=42,
                n_estimators=100
            ),
            'elliptic_envelope': EllipticEnvelope(
                contamination=contamination,
                random_state=42
            )
        }
        
        anomaly_scores = pd.DataFrame(index=data.index)
        
        for name, detector in detectors.items():
            try:
                detector.fit(data[features])
                anomaly_scores[f'{name}_score'] = detector.decision_function(data[features])
                anomaly_scores[f'{name}_anomaly'] = detector.predict(data[features]) == -1
            except Exception as e:
                logger.warning(f"Erro no detector {name}: {e}")
        
        # Votação por consenso
        anomaly_cols = [col for col in anomaly_scores.columns if col.endswith('_anomaly')]
        if anomaly_cols:
            anomaly_scores['consensus_anomaly'] = anomaly_scores[anomaly_cols].mean(axis=1) > 0.5
        
        return anomaly_scores

# ============================================================================
# FÁBRICA DE MODELOS AVANÇADA
# ============================================================================

class AdvancedModelFactory:
    """Fábrica avançada para criação de modelos de deep learning"""
    
    @staticmethod
    def create_model(model_type: ModelType, 
                    sequence_length: int, 
                    n_features: int,
                    n_outputs: int = 1,
                    config: Optional[Dict] = None) -> tf.keras.Model:
        """Cria modelo baseado no tipo especificado com configuração avançada"""
        
        config = config or {}
        
        model_creators = {
            ModelType.LSTM_BASIC: AdvancedModelFactory._create_lstm_basic,
            ModelType.LSTM_ADVANCED: AdvancedModelFactory._create_lstm_advanced,
            ModelType.CNN_LSTM: AdvancedModelFactory._create_cnn_lstm,
            ModelType.TRANSFORMER: AdvancedModelFactory._create_transformer,
            ModelType.ATTENTION_LSTM: AdvancedModelFactory._create_attention_lstm,
            ModelType.WAVENET: AdvancedModelFactory._create_wavenet,
            ModelType.ENSEMBLE: AdvancedModelFactory._create_ensemble_model,
            ModelType.AUTOENCODER: AdvancedModelFactory._create_autoencoder,
            ModelType.BIDIRECTIONAL_LSTM: AdvancedModelFactory._create_bidirectional_lstm,
            ModelType.GRU: AdvancedModelFactory._create_gru,
            ModelType.TCN: AdvancedModelFactory._create_tcn,
            ModelType.NEURALODE: AdvancedModelFactory._create_neural_ode
        }
        
        creator = model_creators.get(model_type, AdvancedModelFactory._create_lstm_advanced)
        
        try:
            model = creator(sequence_length, n_features, n_outputs, config)
            logger.info(f"Modelo {model_type.value} criado com sucesso")
            return model
        except Exception as e:
            logger.error(f"Erro ao criar modelo {model_type}: {e}")
            # Fallback para modelo básico
            return AdvancedModelFactory._create_lstm_basic(sequence_length, n_features, n_outputs, config)
    
    @staticmethod
    def _create_lstm_basic(sequence_length: int, n_features: int, 
                          n_outputs: int, config: Dict) -> tf.keras.Model:
        """Cria modelo LSTM básico"""
        
        reg = config.get('regularization', {})
        
        model = Sequential([
            LSTM(50, return_sequences=True, 
                 input_shape=(sequence_length, n_features),
                 kernel_regularizer=l2(reg.get('l2', 0.01)),
                 recurrent_regularizer=l2(reg.get('l2', 0.01))),
            Dropout(reg.get('dropout_rate', 0.2)),
            LSTM(50, return_sequences=False),
            Dropout(reg.get('dropout_rate', 0.2)),
            Dense(25, activation='relu'),
            Dense(n_outputs)
        ])
        
        return model
    
    @staticmethod
    def _create_lstm_advanced(sequence_length: int, n_features: int, 
                             n_outputs: int, config: Dict) -> tf.keras.Model:
        """Cria modelo LSTM avançado com múltiplas camadas e regularização"""
        
        reg = config.get('regularization', {})
        lstm_units = config.get('lstm_units', [128, 64, 32])
        
        model = Sequential()
        model.add(Input(shape=(sequence_length, n_features)))
        
        # Primeira camada LSTM
        model.add(LSTM(
            lstm_units[0], 
            return_sequences=True,
            kernel_regularizer=l2(reg.get('l2', 0.01)),
            recurrent_regularizer=l2(reg.get('l2', 0.01)),
            kernel_initializer='he_normal'
        ))
        model.add(BatchNormalization())
        model.add(Dropout(reg.get('dropout_rate', 0.3)))
        
        # Segunda camada LSTM
        if len(lstm_units) > 1:
            model.add(LSTM(
                lstm_units[1],
                return_sequences=True,
                kernel_regularizer=l2(reg.get('l2', 0.01)),
                recurrent_regularizer=l2(reg.get('l2', 0.01))
            ))
            model.add(BatchNormalization())
            model.add(Dropout(reg.get('dropout_rate', 0.3)))
        
        # Terceira camada LSTM
        if len(lstm_units) > 2:
            model.add(LSTM(
                lstm_units[2],
                return_sequences=False,
                kernel_regularizer=l2(reg.get('l2', 0.01))
            ))
            model.add(BatchNormalization())
            model.add(Dropout(reg.get('dropout_rate', 0.2)))
        
        # Camadas densas
        dense_units = config.get('dense_units', [64, 32])
        
        for units in dense_units:
            model.add(Dense(
                units,
                activation='relu',
                kernel_regularizer=l2(reg.get('l2', 0.01))
            ))
            model.add(BatchNormalization())
            model.add(Dropout(reg.get('dropout_rate', 0.2)))
        
        # Camada de saída
        model.add(Dense(n_outputs))
        
        # Adicionar ativação customizada se necessário
        if config.get('output_activation'):
            model.add(Activation(config['output_activation']))
        
        return model
    
    @staticmethod
    def _create_cnn_lstm(sequence_length: int, n_features: int, 
                        n_outputs: int, config: Dict) -> tf.keras.Model:
        """Cria modelo CNN-LSTM híbrido"""
        
        model = Sequential([
            # Camadas CNN para extração de features
            Conv1D(filters=64, kernel_size=3, activation='relu',
                   input_shape=(sequence_length, n_features),
                   padding='same'),
            BatchNormalization(),
            MaxPooling1D(pool_size=2),
            
            Conv1D(filters=32, kernel_size=3, activation='relu',
                   padding='same'),
            BatchNormalization(),
            MaxPooling1D(pool_size=2),
            
            # Camadas LSTM para sequências
            LSTM(50, return_sequences=True),
            Dropout(0.3),
            LSTM(25, return_sequences=False),
            Dropout(0.2),
            
            # Camadas densas
            Dense(50, activation='relu'),
            BatchNormalization(),
            Dropout(0.2),
            
            Dense(25, activation='relu'),
            Dense(n_outputs)
        ])
        
        return model
    
    @staticmethod
    def _create_transformer(sequence_length: int, n_features: int,
                           n_outputs: int, config: Dict) -> tf.keras.Model:
        """Cria modelo baseado em Transformer"""
        
        # Hiperparâmetros do transformer
        num_heads = config.get('num_heads', 4)
        key_dim = config.get('key_dim', 32)
        ff_dim = config.get('ff_dim', 128)
        num_layers = config.get('num_layers', 2)
        
        inputs = Input(shape=(sequence_length, n_features))
        
        # Posicional Encoding
        positions = tf.range(start=0, limit=sequence_length, delta=1)
        position_embedding = layers.Embedding(
            input_dim=sequence_length, output_dim=n_features
        )(positions)
        
        x = inputs + position_embedding
        
        # Camadas Transformer
        for _ in range(num_layers):
            # Attention
            attn_output = MultiHeadAttention(
                num_heads=num_heads,
                key_dim=key_dim
            )(x, x)
            
            # Residual connection & normalization
            x = LayerNormalization(epsilon=1e-6)(x + attn_output)
            
            # Feed Forward
            ff_output = layers.Dense(ff_dim, activation='relu')(x)
            ff_output = layers.Dense(n_features)(ff_output)
            
            # Residual connection & normalization
            x = LayerNormalization(epsilon=1e-6)(x + ff_output)
        
        # Global Average Pooling
        x = layers.GlobalAveragePooling1D()(x)
        
        # Camadas de saída
        x = layers.Dense(64, activation='relu')(x)
        x = layers.Dropout(0.2)(x)
        x = layers.Dense(32, activation='relu')(x)
        outputs = layers.Dense(n_outputs)(x)
        
        return Model(inputs=inputs, outputs=outputs)
    
    @staticmethod
    def _create_attention_lstm(sequence_length: int, n_features: int,
                              n_outputs: int, config: Dict) -> tf.keras.Model:
        """Cria modelo LSTM com mecanismo de atenção"""
        
        inputs = Input(shape=(sequence_length, n_features))
        
        # Camada LSTM
        lstm_out = LSTM(64, return_sequences=True)(inputs)
        
        # Mecanismo de atenção
        attention = layers.Dense(1, activation='tanh')(lstm_out)
        attention = layers.Flatten()(attention)
        attention = layers.Activation('softmax')(attention)
        attention = layers.RepeatVector(64)(attention)
        attention = layers.Permute([2, 1])(attention)
        
        # Aplicar atenção
        sent_representation = layers.multiply([lstm_out, attention])
        sent_representation = layers.Lambda(lambda x: tf.keras.backend.sum(x, axis=1))(sent_representation)
        
        # Camadas densas
        x = layers.Dense(50, activation='relu')(sent_representation)
        x = layers.Dropout(0.3)(x)
        x = layers.Dense(25, activation='relu')(x)
        outputs = layers.Dense(n_outputs)(x)
        
        return Model(inputs=inputs, outputs=outputs)
    
    @staticmethod
    def _create_wavenet(sequence_length: int, n_features: int,
                       n_outputs: int, config: Dict) -> tf.keras.Model:
        """Cria modelo WaveNet para séries temporais"""
        
        num_filters = config.get('num_filters', 32)
        num_blocks = config.get('num_blocks', 3)
        num_layers = config.get('num_layers', 6)
        dilation_rates = [2**i for i in range(num_layers)] * num_blocks
        
        inputs = Input(shape=(sequence_length, n_features))
        x = inputs
        
        # Camadas convolucionais dilatadas
        skip_connections = []
        
        for dilation_rate in dilation_rates:
            # Causal convolution
            x_conv = layers.Conv1D(
                filters=num_filters,
                kernel_size=2,
                padding='causal',
                dilation_rate=dilation_rate,
                activation='tanh'
            )(x)
            
            # Gate
            x_gate = layers.Conv1D(
                filters=num_filters,
                kernel_size=2,
                padding='causal',
                dilation_rate=dilation_rate,
                activation='sigmoid'
            )(x)
            
            # Multiply gate
            x = layers.multiply([x_conv, x_gate])
            
            # Residual and skip connections
            x_res = layers.Conv1D(filters=num_filters, kernel_size=1)(x)
            x_skip = layers.Conv1D(filters=num_filters, kernel_size=1)(x)
            
            inputs_res = layers.Conv1D(filters=num_filters, kernel_size=1)(inputs)
            x = layers.add([x_res, inputs_res])
            skip_connections.append(x_skip)
        
        # Soma das skip connections
        x = layers.add(skip_connections)
        x = layers.Activation('relu')(x)
        
        # Camadas finais
        x = layers.Conv1D(filters=num_filters, kernel_size=1, activation='relu')(x)
        x = layers.GlobalAveragePooling1D()(x)
        x = layers.Dense(50, activation='relu')(x)
        outputs = layers.Dense(n_outputs)(x)
        
        return Model(inputs=inputs, outputs=outputs)
    
    @staticmethod
    def _create_ensemble_model(sequence_length: int, n_features: int,
                              n_outputs: int, config: Dict) -> tf.keras.Model:
        """Cria modelo ensemble de múltiplas arquiteturas"""
        
        inputs = Input(shape=(sequence_length, n_features))
        
        # Submodelos
        # 1. LSTM
        lstm_branch = LSTM(32, return_sequences=True)(inputs)
        lstm_branch = LSTM(16, return_sequences=False)(lstm_branch)
        
        # 2. CNN
        cnn_branch = Conv1D(32, kernel_size=3, activation='relu')(inputs)
        cnn_branch = MaxPooling1D(pool_size=2)(cnn_branch)
        cnn_branch = Conv1D(16, kernel_size=3, activation='relu')(cnn_branch)
        cnn_branch = GlobalAveragePooling1D()(cnn_branch)
        
        # 3. Transformer
        transformer_branch = MultiHeadAttention(num_heads=2, key_dim=8)(inputs, inputs)
        transformer_branch = GlobalAveragePooling1D()(transformer_branch)
        
        # Concatenar todas as branches
        concatenated = layers.Concatenate()([lstm_branch, cnn_branch, transformer_branch])
        
        # Camadas densas
        x = Dense(64, activation='relu')(concatenated)
        x = Dropout(0.3)(x)
        x = Dense(32, activation='relu')(x)
        outputs = Dense(n_outputs)(x)
        
        return Model(inputs=inputs, outputs=outputs)
    
    @staticmethod
    def _create_autoencoder(sequence_length: int, n_features: int,
                           n_outputs: int, config: Dict) -> tf.keras.Model:
        """Cria autoencoder para aprendizado de representação"""
        
        # Encoder
        encoder_inputs = Input(shape=(sequence_length, n_features))
        x = LSTM(64, return_sequences=True)(encoder_inputs)
        x = LSTM(32, return_sequences=False)(x)
        encoded = Dense(16, name='encoded')(x)
        
        # Decoder
        x = RepeatVector(sequence_length)(encoded)
        x = LSTM(32, return_sequences=True)(x)
        x = LSTM(64, return_sequences=True)(x)
        decoder_outputs = TimeDistributed(Dense(n_features))(x)
        
        # Autoencoder completo
        autoencoder = Model(encoder_inputs, decoder_outputs)
        
        # Encoder standalone
        encoder = Model(encoder_inputs, encoded)
        
        # Decoder standalone
        encoded_input = Input(shape=(16,))
        x = RepeatVector(sequence_length)(encoded_input)
        x = LSTM(32, return_sequences=True)(x)
        x = LSTM(64, return_sequences=True)(x)
        x = TimeDistributed(Dense(n_features))(x)
        decoder = Model(encoded_input, x)
        
        # Para previsão, adicionar camadas de regressão
        regression_input = Input(shape=(16,))
        x = Dense(32, activation='relu')(regression_input)
        x = Dropout(0.2)(x)
        x = Dense(16, activation='relu')(x)
        regression_output = Dense(n_outputs)(x)
        
        regression_model = Model(regression_input, regression_output)
        
        # Modelo completo: encoder + regressor
        prediction_output = regression_model(encoder(encoder_inputs))
        full_model = Model(encoder_inputs, [decoder_outputs, prediction_output])
        
        return full_model
    
    @staticmethod
    def _create_bidirectional_lstm(sequence_length: int, n_features: int,
                                  n_outputs: int, config: Dict) -> tf.keras.Model:
        """Cria modelo Bidirectional LSTM"""
        
        model = Sequential([
            Bidirectional(LSTM(64, return_sequences=True),
                         input_shape=(sequence_length, n_features)),
            Dropout(0.3),
            Bidirectional(LSTM(32, return_sequences=False)),
            Dropout(0.2),
            Dense(50, activation='relu'),
            Dense(25, activation='relu'),
            Dense(n_outputs)
        ])
        
        return model
    
    @staticmethod
    def _create_gru(sequence_length: int, n_features: int,
                   n_outputs: int, config: Dict) -> tf.keras.Model:
        """Cria modelo GRU"""
        
        model = Sequential([
            GRU(64, return_sequences=True, 
                input_shape=(sequence_length, n_features)),
            Dropout(0.3),
            GRU(32, return_sequences=False),
            Dropout(0.2),
            Dense(50, activation='relu'),
            Dense(25, activation='relu'),
            Dense(n_outputs)
        ])
        
        return model
    
    @staticmethod
    def _create_tcn(sequence_length: int, n_features: int,
                   n_outputs: int, config: Dict) -> tf.keras.Model:
        """Cria Temporal Convolutional Network"""
        try:
            from tcn import TCN
            
            inputs = Input(shape=(sequence_length, n_features))
            
            x = TCN(
                nb_filters=64,
                kernel_size=3,
                nb_stacks=2,
                dilations=[1, 2, 4, 8],
                padding='causal',
                use_skip_connections=True,
                dropout_rate=0.1,
                return_sequences=False
            )(inputs)
            
            x = Dense(32, activation='relu')(x)
            x = Dropout(0.2)(x)
            outputs = Dense(n_outputs)(x)
            
            return Model(inputs=inputs, outputs=outputs)
        except ImportError:
            logger.warning("TCN não instalado. Usando CNN-LSTM como fallback.")
            return AdvancedModelFactory._create_cnn_lstm(sequence_length, n_features, n_outputs, config)
    
    @staticmethod
    def _create_neural_ode(sequence_length: int, n_features: int,
                          n_outputs: int, config: Dict) -> tf.keras.Model:
        """Cria Neural ODE (Ordinary Differential Equations)"""
        try:
            import torch
            import torchdiffeq
            
            # Esta é uma implementação simplificada
            # Em produção, use bibliotecas especializadas como torchdiffeq
            
            logger.warning("Neural ODE é experimental. Usando LSTM avançado como fallback.")
            return AdvancedModelFactory._create_lstm_advanced(sequence_length, n_features, n_outputs, config)
        except ImportError:
            logger.warning("PyTorch/torchdiffeq não instalado. Usando LSTM avançado.")
            return AdvancedModelFactory._create_lstm_advanced(sequence_length, n_features, n_outputs, config)

# ============================================================================
# OTIMIZADOR DE HIPERPARÂMETROS
# ============================================================================

class HyperparameterOptimizer:
    """Otimizador avançado de hiperparâmetros"""
    
    def __init__(self, optimizer_type='bayesian', n_iter=100, cv_folds=5):
        self.optimizer_type = optimizer_type
        self.n_iter = n_iter
        self.cv_folds = cv_folds
        self.best_params = {}
        self.history = []
        
    def optimize(self, model_fn, param_space, X, y, 
                 scoring='neg_mean_squared_error', n_jobs=-1):
        """Otimiza hiperparâmetros usando diferentes estratégias"""
        
        if self.optimizer_type == 'grid':
            return self._grid_search(model_fn, param_space, X, y, scoring, n_jobs)
        elif self.optimizer_type == 'random':
            return self._random_search(model_fn, param_space, X, y, scoring, n_jobs)
        elif self.optimizer_type == 'bayesian':
            return self._bayesian_optimization(model_fn, param_space, X, y, scoring)
        elif self.optimizer_type == 'evolutionary':
            return self._evolutionary_optimization(model_fn, param_space, X, y, scoring)
        else:
            return self._random_search(model_fn, param_space, X, y, scoring, n_jobs)
    
    def _grid_search(self, model_fn, param_space, X, y, scoring, n_jobs):
        """Busca em grade tradicional"""
        
        cv = TimeSeriesSplit(n_splits=self.cv_folds)
        
        grid_search = GridSearchCV(
            estimator=model_fn(),
            param_grid=param_space,
            cv=cv,
            scoring=scoring,
            n_jobs=n_jobs,
            verbose=1
        )
        
        grid_search.fit(X, y)
        self.best_params = grid_search.best_params_
        self.history = grid_search.cv_results_['mean_test_score']
        
        return grid_search.best_estimator_, grid_search.best_score_
    
    def _random_search(self, model_fn, param_space, X, y, scoring, n_jobs):
        """Busca aleatória"""
        
        cv = TimeSeriesSplit(n_splits=self.cv_folds)
        
        random_search = RandomizedSearchCV(
            estimator=model_fn(),
            param_distributions=param_space,
            n_iter=self.n_iter,
            cv=cv,
            scoring=scoring,
            n_jobs=n_jobs,
            random_state=42,
            verbose=1
        )
        
        random_search.fit(X, y)
        self.best_params = random_search.best_params_
        self.history = random_search.cv_results_['mean_test_score']
        
        return random_search.best_estimator_, random_search.best_score_
    
    def _bayesian_optimization(self, model_fn, param_space, X, y, scoring):
        """Otimização bayesiana com Gaussian Process"""
        try:
            from skopt import BayesSearchCV
            from skopt.space import Real, Categorical, Integer
            
            cv = TimeSeriesSplit(n_splits=self.cv_folds)
            
            # Converter param_space para formato skopt
            skopt_space = {}
            for param, values in param_space.items():
                if isinstance(values[0], (int, np.integer)):
                    skopt_space[param] = Integer(min(values), max(values))
                elif isinstance(values[0], (float, np.floating)):
                    skopt_space[param] = Real(min(values), max(values), prior='uniform')
                else:
                    skopt_space[param] = Categorical(values)
            
            bayes_search = BayesSearchCV(
                estimator=model_fn(),
                search_spaces=skopt_space,
                n_iter=self.n_iter,
                cv=cv,
                scoring=scoring,
                random_state=42,
                verbose=1
            )
            
            bayes_search.fit(X, y)
            self.best_params = bayes_search.best_params_
            self.history = [bayes_search.cv_results_['mean_test_score'][i] 
                          for i in bayes_search.cv_results_['rank_test_score'].argsort()]
            
            return bayes_search.best_estimator_, bayes_search.best_score_
        
        except ImportError:
            logger.warning("scikit-optimize não instalado. Usando Random Search.")
            return self._random_search(model_fn, param_space, X, y, scoring, n_jobs=-1)
    
    def _evolutionary_optimization(self, model_fn, param_space, X, y, scoring):
        """Otimização evolucionária"""
        try:
            from evolutionary_search import EvolutionaryAlgorithmSearchCV
            
            cv = TimeSeriesSplit(n_splits=self.cv_folds)
            
            evolutionary_search = EvolutionaryAlgorithmSearchCV(
                estimator=model_fn(),
                params=param_space,
                scoring=scoring,
                cv=cv,
                verbose=1,
                population_size=50,
                gene_mutation_prob=0.10,
                gene_crossover_prob=0.5,
                tournament_size=3,
                generations_number=10,
                n_jobs=-1
            )
            
            evolutionary_search.fit(X, y)
            self.best_params = evolutionary_search.best_params_
            self.history = evolutionary_search.cv_results_['mean_test_score']
            
            return evolutionary_search.best_estimator_, evolutionary_search.best_score_
        
        except ImportError:
            logger.warning("evolutionary-search não instalado. Usando Random Search.")
            return self._random_search(model_fn, param_space, X, y, scoring, n_jobs=-1)

# ============================================================================
# SISTEMA DE MONITORAMENTO AVANÇADO
# ============================================================================

class AdvancedResourceMonitor:
    """Monitor avançado de recursos do sistema"""
    
    def __init__(self, alert_thresholds=None):
        self.alert_thresholds = alert_thresholds or {
            'cpu_percent': 85.0,
            'memory_percent': 80.0,
            'gpu_memory_percent': 85.0,
            'disk_percent': 90.0,
            'temperature': 85.0,
            'queue_size': 1000
        }
        
        self.monitoring = False
        self.metrics_history = defaultdict(lambda: deque(maxlen=1000))
        self.alerts = deque(maxlen=100)
        self.alert_handlers = []
        
    def start_monitoring(self, interval=60):
        """Inicia monitoramento contínuo"""
        self.monitoring = True
        monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,),
            daemon=True,
            name="ResourceMonitor"
        )
        monitor_thread.start()
        logger.info("Monitoramento de recursos iniciado")
    
    def stop_monitoring(self):
        """Para o monitoramento"""
        self.monitoring = False
    
    def _monitoring_loop(self, interval):
        """Loop principal de monitoramento"""
        while self.monitoring:
            try:
                metrics = self._collect_all_metrics()
                self._store_metrics(metrics)
                self._check_thresholds(metrics)
                self._trigger_alert_handlers()
                
                time.sleep(interval)
                
            except Exception as e:
                logger.error(f"Erro no loop de monitoramento: {e}")
                time.sleep(interval * 2)  # Backoff em caso de erro
    
    def _collect_all_metrics(self) -> Dict:
        """Coleta todas as métricas do sistema"""
        
        metrics = {
            'timestamp': datetime.now(),
            'cpu': {},
            'memory': {},
            'disk': {},
            'network': {},
            'gpu': {},
            'process': {},
            'system': {}
        }
        
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        metrics['cpu']['percent_per_core'] = cpu_percent
        metrics['cpu']['percent_total'] = np.mean(cpu_percent)
        metrics['cpu']['frequency'] = psutil.cpu_freq().current if psutil.cpu_freq() else None
        metrics['cpu']['load_avg'] = psutil.getloadavg()
        
        # Memória
        memory = psutil.virtual_memory()
        metrics['memory']['total_gb'] = memory.total / (1024**3)
        metrics['memory']['available_gb'] = memory.available / (1024**3)
        metrics['memory']['used_percent'] = memory.percent
        metrics['memory']['used_gb'] = memory.used / (1024**3)
        
        # Swap
        swap = psutil.swap_memory()
        metrics['memory']['swap_total_gb'] = swap.total / (1024**3)
        metrics['memory']['swap_used_percent'] = swap.percent
        
        # Disco
        disk = psutil.disk_usage('/')
        metrics['disk']['total_gb'] = disk.total / (1024**3)
        metrics['disk']['used_percent'] = disk.percent
        metrics['disk']['used_gb'] = disk.used / (1024**3)
        
        # IO
        disk_io = psutil.disk_io_counters()
        if disk_io:
            metrics['disk']['read_mb'] = disk_io.read_bytes / (1024**2)
            metrics['disk']['write_mb'] = disk_io.write_bytes / (1024**2)
            metrics['disk']['read_count'] = disk_io.read_count
            metrics['disk']['write_count'] = disk_io.write_count
        
        # Rede
        net_io = psutil.net_io_counters()
        metrics['network']['bytes_sent_mb'] = net_io.bytes_sent / (1024**2)
        metrics['network']['bytes_recv_mb'] = net_io.bytes_recv / (1024**2)
        metrics['network']['packets_sent'] = net_io.packets_sent
        metrics['network']['packets_recv'] = net_io.packets_recv
        
        # GPU (se disponível)
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                metrics['gpu']['count'] = len(gpus)
                for i, gpu in enumerate(gpus):
                    metrics['gpu'][f'gpu_{i}'] = {
                        'name': gpu.name,
                        'memory_total_mb': gpu.memoryTotal,
                        'memory_used_mb': gpu.memoryUsed,
                        'memory_free_mb': gpu.memoryFree,
                        'memory_percent': gpu.memoryUtil * 100,
                        'temperature': gpu.temperature,
                        'load_percent': gpu.load * 100
                    }
        except ImportError:
            pass
        
        # Processo atual
        process = psutil.Process()
        metrics['process']['pid'] = process.pid
        metrics['process']['memory_percent'] = process.memory_percent()
        metrics['process']['memory_rss_mb'] = process.memory_info().rss / (1024**2)
        metrics['process']['cpu_percent'] = process.cpu_percent(interval=0.1)
        metrics['process']['threads'] = process.num_threads()
        metrics['process']['open_files'] = len(process.open_files())
        
        # Sistema
        metrics['system']['boot_time'] = datetime.fromtimestamp(psutil.boot_time())
        metrics['system']['users'] = len(psutil.users())
        
        # TensorFlow
        metrics['tensorflow'] = {
            'devices': tf.config.list_physical_devices(),
            'memory_growth': tf.config.list_physical_devices('GPU')[0].memory_growth 
            if tf.config.list_physical_devices('GPU') else None
        }
        
        return metrics
    
    def _store_metrics(self, metrics):
        """Armazena métricas no histórico"""
        for category, values in metrics.items():
            if category != 'timestamp':
                if isinstance(values, dict):
                    for key, value in values.items():
                        metric_name = f"{category}_{key}"
                        self.metrics_history[metric_name].append({
                            'timestamp': metrics['timestamp'],
                            'value': value
                        })
                else:
                    self.metrics_history[category].append({
                        'timestamp': metrics['timestamp'],
                        'value': values
                    })
    
    def _check_thresholds(self, metrics):
        """Verifica se alguma métrica excedeu os thresholds"""
        
        alerts = []
        
        # Verificar CPU
        if metrics['cpu']['percent_total'] > self.alert_thresholds['cpu_percent']:
            alerts.append({
                'type': 'cpu',
                'level': 'warning',
                'message': f"CPU usage high: {metrics['cpu']['percent_total']:.1f}%",
                'value': metrics['cpu']['percent_total'],
                'threshold': self.alert_thresholds['cpu_percent']
            })
        
        # Verificar Memória
        if metrics['memory']['used_percent'] > self.alert_thresholds['memory_percent']:
            alerts.append({
                'type': 'memory',
                'level': 'warning',
                'message': f"Memory usage high: {metrics['memory']['used_percent']:.1f}%",
                'value': metrics['memory']['used_percent'],
                'threshold': self.alert_thresholds['memory_percent']
            })
        
        # Verificar GPU
        if 'gpu' in metrics and metrics['gpu'].get('count', 0) > 0:
            for gpu_key in metrics['gpu']:
                if gpu_key.startswith('gpu_'):
                    gpu_data = metrics['gpu'][gpu_key]
                    if gpu_data['memory_percent'] > self.alert_thresholds['gpu_memory_percent']:
                        alerts.append({
                            'type': 'gpu',
                            'level': 'warning',
                            'message': f"GPU {gpu_key} memory high: {gpu_data['memory_percent']:.1f}%",
                            'value': gpu_data['memory_percent'],
                            'threshold': self.alert_thresholds['gpu_memory_percent']
                        })
        
        # Registrar alertas
        for alert in alerts:
            self.alerts.append({
                **alert,
                'timestamp': metrics['timestamp']
            })
            logger.warning(f"ALERT: {alert['message']}")
    
    def register_alert_handler(self, handler):
        """Registra handler para alertas"""
        self.alert_handlers.append(handler)
    
    def _trigger_alert_handlers(self):
        """Dispara handlers de alerta"""
        for alert in list(self.alerts):
            for handler in self.alert_handlers:
                try:
                    handler(alert)
                except Exception as e:
                    logger.error(f"Erro no handler de alerta: {e}")
    
    def get_metrics_report(self, last_n=100) -> Dict:
        """Gera relatório das métricas"""
        report = {
            'summary': {},
            'trends': {},
            'alerts': list(self.alerts)[-10:],
            'timestamp': datetime.now()
        }
        
        # Calcular médias recentes
        for metric_name, history in self.metrics_history.items():
            if history:
                recent_values = [h['value'] for h in list(history)[-last_n:]]
                if all(isinstance(v, (int, float)) for v in recent_values):
                    report['summary'][metric_name] = {
                        'current': recent_values[-1] if recent_values else None,
                        'average': np.mean(recent_values) if recent_values else None,
                        'max': np.max(recent_values) if recent_values else None,
                        'min': np.min(recent_values) if recent_values else None,
                        'trend': self._calculate_trend(recent_values)
                    }
        
        return report
    
    def _calculate_trend(self, values, window=10):
        """Calcula tendência dos valores"""
        if len(values) < window:
            return 0
        
        recent = values[-window:]
        x = np.arange(len(recent))
        slope, _ = np.polyfit(x, recent, 1)
        
        return slope

# ============================================================================
# GERENCIADOR DE DADOS AVANÇADO
# ============================================================================

class AdvancedDataManager:
    """Gerenciador avançado de dados com cache, persistência e otimização"""
    
    def __init__(self, cache_dir='data_cache', use_redis=False):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        self.use_redis = use_redis
        self.redis_client = None
        
        if use_redis:
            try:
                import redis
                self.redis_client = redis.Redis(
                    host='localhost',
                    port=6379,
                    db=0,
                    decode_responses=False
                )
                logger.info("Redis conectado para cache")
            except Exception as e:
                logger.warning(f"Não foi possível conectar ao Redis: {e}")
                self.use_redis = False
        
        # Cache em memória
        self.memory_cache = {}
        self.cache_stats = {'hits': 0, 'misses': 0, 'size': 0}
        
        # Configuração de persistência
        self.persistence_config = {
            'format': 'parquet',  # parquet, feather, hdf5, pickle
            'compression': 'snappy',
            'chunk_size': 10000
        }
        
    def fetch_stock_data(self, symbol: str, 
                        start_date: Optional[datetime] = None,
                        end_date: Optional[datetime] = None,
                        interval: str = '1d',
                        source: DataSource = DataSource.YFINANCE,
                        **kwargs) -> Optional[pd.DataFrame]:
        """Busca dados de ações de múltiplas fontes com cache"""
        
        cache_key = self._generate_cache_key(symbol, start_date, end_date, interval, source)
        
        # Verificar cache
        cached_data = self._get_from_cache(cache_key)
        if cached_data is not None:
            logger.debug(f"Cache hit para {symbol}")
            return cached_data
        
        logger.info(f"Buscando dados para {symbol} de {source.value}")
        
        try:
            if source == DataSource.YFINANCE:
                data = self._fetch_from_yfinance(symbol, start_date, end_date, interval, **kwargs)
            elif source == DataSource.ALPHA_VANTAGE:
                data = self._fetch_from_alphavantage(symbol, interval, **kwargs)
            elif source == DataSource.CRYPTO and HAVE_CRYPTO:
                data = self._fetch_crypto_data(symbol, interval, **kwargs)
            else:
                raise ValueError(f"Fonte de dados não suportada: {source}")
            
            if data is not None and not data.empty:
                # Processar dados
                data = self._post_process_data(data, symbol, interval)
                
                # Armazenar em cache
                self._store_in_cache(cache_key, data)
                
                logger.info(f"Dados obtidos para {symbol}: {len(data)} registros")
                return data
            else:
                logger.warning(f"Nenhum dado obtido para {symbol}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao buscar dados para {symbol}: {e}")
            return None
    
    def _fetch_from_yfinance(self, symbol, start_date, end_date, interval, **kwargs):
        """Busca dados do Yahoo Finance"""
        
        max_retries = kwargs.get('max_retries', 3)
        retry_delay = kwargs.get('retry_delay', 1)
        
        for attempt in range(max_retries):
            try:
                ticker = yf.Ticker(symbol)
                
                # Definir datas padrão
                if not end_date:
                    end_date = datetime.now()
                if not start_date:
                    start_date = end_date - timedelta(days=365 * 2)  # 2 anos
                
                # Baixar dados
                data = ticker.history(
                    start=start_date,
                    end=end_date,
                    interval=interval,
                    auto_adjust=True,
                    prepost=kwargs.get('prepost', False),
                    actions=kwargs.get('actions', True)
                )
                
                if data.empty:
                    # Tentar período diferente
                    data = ticker.history(period="max", interval=interval)
                
                return data
                
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Tentativa {attempt + 1} falhou para {symbol}: {e}")
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    logger.error(f"Falha ao buscar dados para {symbol}: {e}")
                    return None
    
    def _fetch_from_alphavantage(self, symbol, interval, **kwargs):
        """Busca dados do Alpha Vantage"""
        api_key = kwargs.get('api_key')
        if not api_key:
            logger.error("Chave da API Alpha Vantage não fornecida")
            return None
        
        try:
            import requests
            
            # Mapear intervalos
            interval_map = {
                '1d': 'TIME_SERIES_DAILY',
                '1wk': 'TIME_SERIES_WEEKLY',
                '1mo': 'TIME_SERIES_MONTHLY'
            }
            
            function = interval_map.get(interval, 'TIME_SERIES_DAILY')
            
            url = f"https://www.alphavantage.co/query"
            params = {
                'function': function,
                'symbol': symbol,
                'apikey': api_key,
                'outputsize': 'full',
                'datatype': 'json'
            }
            
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            # Processar resposta
            time_series_key = list(data.keys())[1]  # A chave dos dados varia
            time_series = data[time_series_key]
            
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.astype(float)
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            
            return df.sort_index()
            
        except Exception as e:
            logger.error(f"Erro ao buscar dados do Alpha Vantage: {e}")
            return None
    
    def _fetch_crypto_data(self, symbol, interval, **kwargs):
        """Busca dados de criptomoedas"""
        try:
            exchange_id = kwargs.get('exchange', 'binance')
            exchange_class = getattr(ccxt, exchange_id)
            exchange = exchange_class({
                'enableRateLimit': True,
                'timeout': 30000
            })
            
            # Converter intervalos
            interval_map = {
                '1d': '1d',
                '1h': '1h',
                '15m': '15m',
                '5m': '5m',
                '1m': '1m'
            }
            
            timeframe = interval_map.get(interval, '1d')
            
            # Baixar OHLCV
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
            
            # Converter para DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            logger.error(f"Erro ao buscar dados de criptomoeda: {e}")
            return None
    
    def _post_process_data(self, data: pd.DataFrame, symbol: str, interval: str) -> pd.DataFrame:
        """Processamento pós-busca de dados"""
        
        # Garantir que temos todas as colunas necessárias
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_columns:
            if col not in data.columns:
                logger.warning(f"Coluna {col} não encontrada nos dados de {symbol}")
        
        # Remover duplicatas
        data = data[~data.index.duplicated(keep='first')]
        
        # Preencher valores ausentes
        data = data.ffill().bfill()
        
        # Adicionar metadados
        data.attrs['symbol'] = symbol
        data.attrs['interval'] = interval
        data.attrs['last_updated'] = datetime.now()
        data.attrs['data_points'] = len(data)
        
        return data
    
    def _generate_cache_key(self, symbol, start_date, end_date, interval, source):
        """Gera chave única para cache"""
        key_parts = [
            symbol,
            start_date.isoformat() if start_date else 'none',
            end_date.isoformat() if end_date else 'none',
            interval,
            source.value
        ]
        return hashlib.md5('_'.join(str(p) for p in key_parts).encode()).hexdigest()
    
    def _get_from_cache(self, cache_key):
        """Obtém dados do cache"""
        self.cache_stats['misses'] += 1
        
        # Primeiro, verificar cache em memória
        if cache_key in self.memory_cache:
            self.cache_stats['hits'] += 1
            self.cache_stats['misses'] -= 1
            return self.memory_cache[cache_key]
        
        # Em seguida, verificar Redis
        if self.use_redis and self.redis_client:
            try:
                cached = self.redis_client.get(cache_key)
                if cached:
                    data = pickle.loads(cached)
                    self.memory_cache[cache_key] = data  # Cache em memória também
                    self.cache_stats['hits'] += 1
                    self.cache_stats['misses'] -= 1
                    return data
            except Exception as e:
                logger.warning(f"Erro ao acessar cache Redis: {e}")
        
        # Finalmente, verificar arquivo
        cache_file = self.cache_dir / f"{cache_key}.{self.persistence_config['format']}"
        if cache_file.exists():
            try:
                if self.persistence_config['format'] == 'parquet':
                    data = pd.read_parquet(cache_file)
                elif self.persistence_config['format'] == 'feather':
                    data = pd.read_feather(cache_file)
                elif self.persistence_config['format'] == 'hdf5':
                    data = pd.read_hdf(cache_file, key='data')
                else:
                    data = pd.read_pickle(cache_file)
                
                self.memory_cache[cache_key] = data
                self.cache_stats['hits'] += 1
                self.cache_stats['misses'] -= 1
                return data
            except Exception as e:
                logger.warning(f"Erro ao ler cache de arquivo: {e}")
        
        return None
    
    def _store_in_cache(self, cache_key, data):
        """Armazena dados no cache"""
        
        # Cache em memória
        self.memory_cache[cache_key] = data
        self.cache_stats['size'] = len(self.memory_cache)
        
        # Limitar tamanho do cache em memória
        if len(self.memory_cache) > 100:
            # Remover item mais antigo
            oldest_key = next(iter(self.memory_cache))
            del self.memory_cache[oldest_key]
        
        # Cache Redis
        if self.use_redis and self.redis_client:
            try:
                serialized = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
                self.redis_client.setex(cache_key, 86400, serialized)  # TTL de 24 horas
            except Exception as e:
                logger.warning(f"Erro ao armazenar no Redis: {e}")
        
        # Cache em arquivo
        try:
            cache_file = self.cache_dir / f"{cache_key}.{self.persistence_config['format']}"
            
            if self.persistence_config['format'] == 'parquet':
                data.to_parquet(cache_file, compression=self.persistence_config['compression'])
            elif self.persistence_config['format'] == 'feather':
                data.to_feather(cache_file, compression=self.persistence_config['compression'])
            elif self.persistence_config['format'] == 'hdf5':
                data.to_hdf(cache_file, key='data', mode='w', complevel=9)
            else:
                data.to_pickle(cache_file)
                
        except Exception as e:
            logger.warning(f"Erro ao armazenar cache em arquivo: {e}")
    
    def get_cache_stats(self):
        """Retorna estatísticas do cache"""
        hit_rate = (self.cache_stats['hits'] / 
                   max(self.cache_stats['hits'] + self.cache_stats['misses'], 1))
        
        return {
            **self.cache_stats,
            'hit_rate': hit_rate,
            'memory_cache_size': len(self.memory_cache),
            'disk_cache_size': len(list(self.cache_dir.glob('*'))),
            'timestamp': datetime.now()
        }

# ============================================================================
# SISTEMA DE IA AVANÇADO
# ============================================================================

class AdvancedAISystem:
    """Sistema avançado de IA para previsão financeira"""
    
    VERSION = "4.2.0"
    
    def __init__(self, config: Optional[Dict] = None):
        
        # Configuração
        self.config = self._merge_configs(config or {})
        
        # Estado do sistema
        self.system_state = 'initializing'
        self.start_time = datetime.now()
        self.operation_mode = 'production'  # production, backtest, research
        
        # Componentes principais
        self.data_manager = AdvancedDataManager(
            cache_dir=self.config['system']['cache_dir'],
            use_redis=self.config['system'].get('use_redis', False)
        )
        
        self.data_preprocessor = AdvancedDataPreprocessor()
        self.resource_monitor = AdvancedResourceMonitor(
            alert_thresholds=self.config['monitoring']['alert_thresholds']
        )
        
        # Modelos e dados
        self.models: Dict[str, Dict] = {}
        self.performance_tracker = PerformanceTracker()
        self.prediction_cache = {}
        
        # Filas e processamento
        self.data_queue = queue.PriorityQueue(maxsize=10000)
        self.training_queue = queue.PriorityQueue(maxsize=1000)
        self.prediction_queue = queue.PriorityQueue(maxsize=10000)
        self.result_queue = queue.Queue(maxsize=10000)
        
        # Thread pools
        self.thread_pool = ThreadPoolExecutor(
            max_workers=self.config['system']['max_workers'],
            thread_name_prefix="AIWorker"
        )
        
        self.process_pool = ProcessPoolExecutor(
            max_workers=max(1, multiprocessing.cpu_count() // 2)
        )
        
        # Workers
        self.workers = []
        self.is_running = False
        
        # Inicialização
        self._initialize_system()
        
        logger.info(f"Sistema de IA Avançado v{self.VERSION} inicializado")
    
    def _merge_configs(self, user_config: Dict) -> Dict:
        """Mescla configuração do usuário com padrão"""
        
        default_config = {
            'system': {
                'name': 'Advanced AI Trading System',
                'version': self.VERSION,
                'mode': 'production',
                'cache_dir': 'ai_cache',
                'model_dir': 'models',
                'data_dir': 'data',
                'log_dir': 'logs',
                'max_workers': 10,
                'max_models': 100,
                'use_gpu': True,
                'mixed_precision': True,
                'enable_distributed': False,
                'enable_telemetry': True
            },
            'data': {
                'default_source': DataSource.YFINANCE,
                'default_interval': '1d',
                'default_period': '2y',
                'feature_columns': [
                    'Open', 'High', 'Low', 'Close', 'Volume',
                    'Returns', 'Volatility', 'SMA_20', 'EMA_12',
                    'RSI', 'MACD', 'BB_Width', 'ATR'
                ],
                'sequence_length': 60,
                'prediction_horizon': 10,
                'test_size': 0.15,
                'validation_size': 0.15,
                'shuffle': False,  # Não embaralhar séries temporais
                'scaler_type': 'robust',
                'augmentation': True,
                'anomaly_detection': True
            },
            'model': {
                'default_type': ModelType.LSTM_ADVANCED,
                'hyperparameter_optimization': True,
                'optimizer': 'adam',
                'loss': 'huber',
                'metrics': ['mse', 'mae', 'mape'],
                'regularization': {
                    'l1': 0.001,
                    'l2': 0.01,
                    'dropout_rate': 0.3,
                    'recurrent_dropout': 0.2
                },
                'callbacks': {
                    'early_stopping': True,
                    'reduce_lr': True,
                    'model_checkpoint': True,
                    'tensorboard': True
                },
                'ensemble_method': 'stacking',
                'uncertainty_estimation': True
            },
            'training': {
                'epochs': 200,
                'batch_size': 64,
                'learning_rate': 0.001,
                'validation_split': 0.15,
                'early_stopping_patience': 20,
                'reduce_lr_patience': 10,
                'min_delta': 0.001,
                'warmup_epochs': 10,
                'gradient_accumulation_steps': 1,
                'max_gradient_norm': 1.0,
                'label_smoothing': 0.1,
                'class_weights': True
            },
            'prediction': {
                'confidence_level': 0.95,
                'n_future': 30,
                'enable_monte_carlo': True,
                'mc_dropout_samples': 100,
                'enable_ensemble': True,
                'ensemble_size': 5,
                'risk_adjustment': True,
                'signal_generation': True
            },
            'monitoring': {
                'enable': True,
                'interval_seconds': 60,
                'alert_thresholds': {
                    'cpu_percent': 85,
                    'memory_percent': 80,
                    'gpu_memory_percent': 85,
                    'queue_size': 1000,
                    'model_accuracy': 0.6,
                    'data_freshness_hours': 24
                },
                'metrics_retention_days': 30,
                'enable_alerting': True,
                'alert_channels': ['log', 'email']
            },
            'risk': {
                'max_position_size': 0.1,  # 10% do portfolio
                'max_daily_loss': 0.02,    # 2% por dia
                'stop_loss_pct': 0.05,     # 5% stop loss
                'take_profit_pct': 0.1,    # 10% take profit
                'var_confidence': 0.95,
                'enable_hedging': True,
                'max_leverage': 3.0
            },
            'backtest': {
                'initial_capital': 100000,
                'commission': 0.001,  # 0.1%
                'slippage': 0.0005,   # 0.05%
                'enable_shorting': True,
                'max_hold_period': 30,
                'benchmark': 'SPY'
            }
        }
        
        # Merge recursivo
        def deep_merge(base, override):
            for key, value in override.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    base[key] = deep_merge(base[key], value)
                else:
                    base[key] = value
            return base
        
        return deep_merge(default_config, user_config)
    
    def _initialize_system(self):
        """Inicialização completa do sistema"""
        try:
            logger.info("Inicializando sistema de IA...")
            
            # 1. Criar diretórios
            self._create_directories()
            
            # 2. Configurar TensorFlow
            self._configure_tensorflow()
            
            # 3. Iniciar monitoramento
            if self.config['monitoring']['enable']:
                self.resource_monitor.start_monitoring(
                    interval=self.config['monitoring']['interval_seconds']
                )
                self.resource_monitor.register_alert_handler(self._handle_system_alert)
            
            # 4. Carregar modelos existentes
            self._load_existing_models()
            
            # 5. Iniciar workers
            self._start_workers()
            
            # 6. Warmup do sistema
            self._warmup_system()
            
            self.system_state = 'ready'
            logger.info("✅ Sistema de IA inicializado com sucesso")
            
        except Exception as e:
            self.system_state = 'error'
            logger.error(f"❌ Erro na inicialização do sistema: {e}")
            traceback.print_exc()
            raise
    
    def _create_directories(self):
        """Cria todos os diretórios necessários"""
        directories = [
            self.config['system']['model_dir'],
            self.config['system']['data_dir'],
            self.config['system']['log_dir'],
            self.config['system']['cache_dir'],
            'backtests',
            'reports',
            'exports',
            'checkpoints'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.debug(f"Diretório criado/verificado: {directory}")
    
    def _configure_tensorflow(self):
        """Configura TensorFlow para performance"""
        
        # Habilitar mixed precision
        if self.config['system']['mixed_precision']:
            from tensorflow.keras import mixed_precision
            policy = mixed_precision.Policy('mixed_float16')
            mixed_precision.set_global_policy(policy)
            logger.info("Mixed precision habilitado")
        
        # Configurar GPU
        gpus = tf.config.list_physical_devices('GPU')
        if gpus and self.config['system']['use_gpu']:
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                logger.info(f"{len(gpus)} GPU(s) configurada(s)")
            except RuntimeError as e:
                logger.warning(f"Erro ao configurar GPU: {e}")
        else:
            logger.info("Usando CPU")
        
        # Otimizações de performance
        tf.config.optimizer.set_jit(True)
        tf.config.threading.set_intra_op_parallelism_threads(0)
        tf.config.threading.set_inter_op_parallelism_threads(0)
        
        # Desabilitar warnings do TensorFlow
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    def _load_existing_models(self):
        """Carrega modelos treinados existentes"""
        model_dir = Path(self.config['system']['model_dir'])
        
        if not model_dir.exists():
            return
        
        model_files = list(model_dir.glob('*.h5'))
        logger.info(f"Encontrados {len(model_files)} modelos para carregar")
        
        loaded_count = 0
        
        for model_file in model_files:
            try:
                symbol = model_file.stem.split('_')[0]  # Extrair símbolo do nome do arquivo
                
                model = load_model(model_file, compile=False)
                
                # Carregar metadados do modelo
                metadata_file = model_dir / f"{model_file.stem}_metadata.json"
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                else:
                    metadata = {}
                
                # Carregar scaler
                scaler_file = model_dir / f"{model_file.stem}_scaler.pkl"
                scaler = None
                if scaler_file.exists():
                    with open(scaler_file, 'rb') as f:
                        scaler = pickle.load(f)
                
                # Carregar performance
                perf_file = model_dir / f"{model_file.stem}_performance.json"
                performance = None
                if perf_file.exists():
                    with open(perf_file, 'r') as f:
                        performance = json.load(f)
                
                self.models[symbol] = {
                    'model': model,
                    'scaler': scaler,
                    'metadata': metadata,
                    'performance': performance,
                    'last_updated': datetime.fromtimestamp(model_file.stat().st_mtime),
                    'file_path': model_file
                }
                
                loaded_count += 1
                logger.debug(f"Modelo carregado: {symbol}")
                
            except Exception as e:
                logger.error(f"Erro ao carregar modelo {model_file}: {e}")
        
        logger.info(f"✅ {loaded_count} modelos carregados com sucesso")
    
    def _start_workers(self):
        """Inicia todos os workers do sistema"""
        
        worker_configs = [
            {
                'name': 'DataFetcher',
                'target': self._data_fetcher_worker,
                'daemon': True
            },
            {
                'name': 'TrainingWorker',
                'target': self._training_worker,
                'daemon': True
            },
            {
                'name': 'PredictionWorker',
                'target': self._prediction_worker,
                'daemon': True
            },
            {
                'name': 'MonitoringWorker',
                'target': self._monitoring_worker,
                'daemon': True
            },
            {
                'name': 'ResultsProcessor',
                'target': self._results_processor_worker,
                'daemon': True
            }
        ]
        
        self.is_running = True
        
        for config in worker_configs:
            worker = threading.Thread(
                target=config['target'],
                daemon=config['daemon'],
                name=config['name']
            )
            worker.start()
            self.workers.append(worker)
            
            logger.debug(f"Worker iniciado: {config['name']}")
    
    def _warmup_system(self):
        """Executa warmup do sistema para otimização"""
        logger.info("Executando warmup do sistema...")
        
        warmup_tasks = []
        
        # Warmup de modelos carregados
        for symbol, model_info in list(self.models.items())[:5]:  # Limitar a 5 modelos
            if model_info['model']:
                warmup_tasks.append(
                    self.thread_pool.submit(self._warmup_model, symbol)
                )
        
        # Aguardar warmup
        concurrent.futures.wait(warmup_tasks, timeout=30)
        
        logger.info("Warmup do sistema concluído")
    
    def _warmup_model(self, symbol):
        """Executa warmup de um modelo específico"""
        try:
            model_info = self.models.get(symbol)
            if not model_info or not model_info['model']:
                return
            
            # Criar dados dummy para warmup
            dummy_input = np.random.randn(
                1, 
                self.config['data']['sequence_length'],
                len(self.config['data']['feature_columns'])
            ).astype(np.float32)
            
            # Executar previsão dummy
            _ = model_info['model'].predict(dummy_input, verbose=0)
            
            logger.debug(f"Warmup concluído para modelo: {symbol}")
            
        except Exception as e:
            logger.warning(f"Erro no warmup do modelo {symbol}: {e}")
    
    def train_model(self, symbol: str, 
                   data: Optional[pd.DataFrame] = None,
                   model_type: Optional[ModelType] = None,
                   hyperparameter_opt: bool = True) -> bool:
        """Treina ou retreina um modelo para um símbolo"""
        
        try:
            logger.info(f"Iniciando treinamento para {symbol}")
            
            # Verificar se devemos remover modelos antigos
            if len(self.models) >= self.config['system']['max_models']:
                self._evict_oldest_model()
            
            # Obter dados se não fornecidos
            if data is None:
                data = self.data_manager.fetch_stock_data(
                    symbol=symbol,
                    interval=self.config['data']['default_interval'],
                    source=self.config['data']['default_source']
                )
            
            if data is None or data.empty:
                logger.error(f"Dados insuficientes para treinar {symbol}")
                return False
            
            # Adicionar indicadores técnicos
            data = self.data_preprocessor.create_technical_indicators(data)
            
            # Selecionar colunas de features
            feature_cols = [col for col in self.config['data']['feature_columns'] 
                          if col in data.columns]
            
            if not feature_cols:
                logger.error(f"Nenhuma feature disponível para {symbol}")
                return False
            
            feature_data = data[feature_cols].values
            
            # Normalizar dados
            scaled_data, scaler = self.data_preprocessor.normalize_data(
                feature_data,
                symbol,
                scaler_type=self.config['data']['scaler_type']
            )
            
            # Preparar sequências
            sequence_length = self.config['data']['sequence_length']
            prediction_horizon = self.config['data']['prediction_horizon']
            
            X, y = self.data_preprocessor.prepare_sequences(
                scaled_data,
                sequence_length,
                prediction_horizon
            )
            
            if len(X) < sequence_length * 2:
                logger.error(f"Dados insuficientes para sequências: {len(X)} amostras")
                return False
            
            # Dividir em treino/validação/teste
            test_size = self.config['data']['test_size']
            val_size = self.config['data']['validation_size']
            
            total_size = len(X)
            test_split = int(total_size * (1 - test_size))
            val_split = int(test_split * (1 - val_size))
            
            X_train, y_train = X[:val_split], y[:val_split]
            X_val, y_val = X[val_split:test_split], y[val_split:test_split]
            X_test, y_test = X[test_split:], y[test_split:]
            
            logger.debug(f"Divisão: Treino={len(X_train)}, Val={len(X_val)}, Teste={len(X_test)}")
            
            # Selecionar tipo de modelo
            model_type = model_type or self.config['model']['default_type']
            
            # Otimização de hiperparâmetros
            best_model = None
            if hyperparameter_opt and self.config['model']['hyperparameter_optimization']:
                best_model = self._optimize_hyperparameters(
                    model_type, X_train, y_train, X_val, y_val
                )
            
            # Criar modelo se não otimizado
            if best_model is None:
                best_model = AdvancedModelFactory.create_model(
                    model_type=model_type,
                    sequence_length=sequence_length,
                    n_features=len(feature_cols),
                    n_outputs=prediction_horizon,
                    config=self.config['model']
                )
            
            # Compilar modelo
            optimizer = self._create_optimizer()
            loss = self._create_loss_function()
            metrics = self._create_metrics()
            
            best_model.compile(
                optimizer=optimizer,
                loss=loss,
                metrics=metrics
            )
            
            # Callbacks
            callbacks = self._create_callbacks(symbol)
            
            # Treinar modelo
            start_time = time.time()
            
            history = best_model.fit(
                X_train, y_train,
                epochs=self.config['training']['epochs'],
                batch_size=self.config['training']['batch_size'],
                validation_data=(X_val, y_val),
                callbacks=callbacks,
                verbose=1,
                shuffle=self.config['data']['shuffle']
            )
            
            training_time = time.time() - start_time
            
            # Avaliar no conjunto de teste
            test_results = best_model.evaluate(X_test, y_test, verbose=0)
            
            # Fazer previsões de teste
            y_pred = best_model.predict(X_test, verbose=0)
            
            # Calcular métricas de performance
            performance = self._calculate_performance_metrics(
                symbol, y_test, y_pred, history, training_time
            )
            
            # Salvar modelo
            self._save_model(symbol, best_model, scaler, performance, {
                'model_type': model_type.value,
                'feature_columns': feature_cols,
                'sequence_length': sequence_length,
                'prediction_horizon': prediction_horizon,
                'training_time': training_time,
                'test_results': dict(zip(best_model.metrics_names, test_results))
            })
            
            # Atualizar cache de modelos
            self.models[symbol] = {
                'model': best_model,
                'scaler': scaler,
                'metadata': {
                    'model_type': model_type.value,
                    'feature_columns': feature_cols,
                    'sequence_length': sequence_length,
                    'last_trained': datetime.now()
                },
                'performance': performance,
                'last_updated': datetime.now(),
                'training_time': training_time
            }
            
            logger.info(f"✅ Modelo treinado para {symbol} em {training_time:.2f}s")
            logger.info(f"   Performance: MSE={performance.mse:.6f}, "
                       f"Accuracy={performance.directional_accuracy:.2%}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro no treinamento do modelo {symbol}: {e}")
            traceback.print_exc()
            return False
    
    def predict(self, symbol: str, 
               data: Optional[pd.DataFrame] = None,
               n_future: Optional[int] = None,
               include_uncertainty: bool = True) -> Optional[PredictionResult]:
        """Faz previsões para um símbolo"""
        
        cache_key = f"{symbol}_{n_future}_{include_uncertainty}"
        
        # Verificar cache
        if cache_key in self.prediction_cache:
            cached_result = self.prediction_cache[cache_key]
            cache_age = (datetime.now() - cached_result.timestamp).total_seconds()
            
            if cache_age < 300:  # Cache válido por 5 minutos
                logger.debug(f"Cache hit para previsão de {symbol}")
                return cached_result
        
        try:
            logger.info(f"Gerando previsões para {symbol}")
            
            # Verificar se modelo existe
            if symbol not in self.models:
                logger.warning(f"Modelo não encontrado para {symbol}. Treinando...")
                success = self.train_model(symbol)
                if not success:
                    logger.error(f"Falha ao treinar modelo para {symbol}")
                    return None
            
            model_info = self.models[symbol]
            model = model_info['model']
            scaler = model_info['scaler']
            
            if scaler is None:
                logger.error(f"Scaler não encontrado para {symbol}")
                return None
            
            # Obter dados recentes
            if data is None:
                data = self.data_manager.fetch_stock_data(
                    symbol=symbol,
                    interval=self.config['data']['default_interval'],
                    source=self.config['data']['default_source']
                )
            
            if data is None or data.empty:
                logger.error(f"Dados insuficientes para previsão de {symbol}")
                return None
            
            # Adicionar indicadores técnicos
            data = self.data_preprocessor.create_technical_indicators(data)
            
            # Selecionar colunas de features
            feature_cols = model_info['metadata'].get('feature_columns', 
                                                     self.config['data']['feature_columns'])
            feature_cols = [col for col in feature_cols if col in data.columns]
            
            feature_data = data[feature_cols].values
            
            # Normalizar
            scaled_data = scaler.transform(feature_data)
            
            # Preparar sequência de entrada
            sequence_length = model_info['metadata'].get('sequence_length', 
                                                        self.config['data']['sequence_length'])
            n_future = n_future or self.config['prediction']['n_future']
            
            last_sequence = scaled_data[-sequence_length:]
            
            # Métodos de previsão
            if self.config['prediction']['enable_monte_carlo']:
                predictions, uncertainties = self._monte_carlo_predict(
                    model, last_sequence, n_future,
                    n_samples=self.config['prediction']['mc_dropout_samples']
                )
            else:
                predictions = self._recursive_predict(model, last_sequence, n_future)
                uncertainties = np.zeros_like(predictions)
            
            # Inverter scaling
            predictions_original = self._inverse_scale_predictions(
                predictions, scaler, feature_cols
            )
            
            # Calcular intervalos de confiança
            confidence_level = self.config['prediction']['confidence_level']
            ci_lower, ci_upper = self._calculate_confidence_intervals(
                predictions_original, uncertainties, confidence_level
            )
            
            # Gerar sinais de trading
            signals = None
            if self.config['prediction']['signal_generation']:
                signals = self._generate_trading_signals(
                    predictions_original, ci_lower, ci_upper
                )
            
            # Calcular importância de features (se suportado)
            feature_importance = None
            try:
                feature_importance = self._calculate_feature_importance(
                    model, last_sequence, feature_cols
                )
            except:
                pass
            
            # Criar resultado
            result = PredictionResult(
                symbol=symbol,
                predictions=predictions,
                confidence_intervals=(ci_lower, ci_upper),
                point_predictions=predictions_original,
                uncertainty=uncertainties if include_uncertainty else None,
                signals=signals,
                feature_importance=feature_importance,
                timestamp=datetime.now(),
                metadata={
                    'model_type': model_info['metadata'].get('model_type', 'unknown'),
                    'sequence_length': sequence_length,
                    'n_future': n_future,
                    'confidence_level': confidence_level,
                    'mc_dropout': self.config['prediction']['enable_monte_carlo']
                }
            )
            
            # Armazenar em cache
            self.prediction_cache[cache_key] = result
            
            # Limpar cache antigo
            if len(self.prediction_cache) > 100:
                oldest_key = next(iter(self.prediction_cache))
                del self.prediction_cache[oldest_key]
            
            logger.info(f"✅ Previsões geradas para {symbol}: "
                       f"{predictions_original[-1]:.2f} ± {uncertainties[-1]:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro na previsão para {symbol}: {e}")
            traceback.print_exc()
            return None
    
    def _monte_carlo_predict(self, model, last_sequence, n_future, n_samples=100):
        """Previsão com Monte Carlo Dropout para estimativa de incerteza"""
        
        predictions = []
        all_samples = []
        
        current_sequence = last_sequence.copy()
        
        for step in range(n_future):
            step_predictions = []
            
            for _ in range(n_samples):
                # Adicionar dropout ativo
                input_seq = current_sequence.reshape(1, *current_sequence.shape)
                pred = model(input_seq, training=True).numpy()[0, 0]
                step_predictions.append(pred)
            
            step_predictions = np.array(step_predictions)
            step_mean = np.mean(step_predictions)
            step_std = np.std(step_predictions)
            
            predictions.append(step_mean)
            all_samples.append(step_predictions)
            
            # Atualizar sequência para próximo passo
            new_row = np.zeros(last_sequence.shape[1])
            new_row[0] = step_mean
            current_sequence = np.vstack([current_sequence[1:], new_row])
        
        predictions = np.array(predictions)
        uncertainties = np.array([np.std(samples) for samples in all_samples])
        
        return predictions, uncertainties
    
    def _recursive_predict(self, model, last_sequence, n_future):
        """Previsão recursiva padrão"""
        
        predictions = []
        current_sequence = last_sequence.copy()
        
        for _ in range(n_future):
            input_seq = current_sequence.reshape(1, *current_sequence.shape)
            pred = model.predict(input_seq, verbose=0)[0, 0]
            
            predictions.append(pred)
            
            # Atualizar sequência
            new_row = np.zeros(last_sequence.shape[1])
            new_row[0] = pred
            current_sequence = np.vstack([current_sequence[1:], new_row])
        
        return np.array(predictions)
    
    def _inverse_scale_predictions(self, predictions, scaler, feature_cols):
        """Inverte o scaling das previsões"""
        
        # Criar array dummy com mesma forma que os dados originais
        n_features = len(feature_cols)
        dummy_array = np.zeros((len(predictions), n_features))
        dummy_array[:, 0] = predictions  # Assume que Close é a primeira coluna
        
        # Inverter scaling
        predictions_original = scaler.inverse_transform(dummy_array)[:, 0]
        
        return predictions_original
    
    def _calculate_confidence_intervals(self, predictions, uncertainties, confidence_level):
        """Calcula intervalos de confiança"""
        
        # Z-score para o nível de confiança
        if confidence_level == 0.95:
            z_score = 1.96
        elif confidence_level == 0.99:
            z_score = 2.576
        else:
            z_score = norm.ppf((1 + confidence_level) / 2)
        
        ci_lower = predictions - z_score * uncertainties
        ci_upper = predictions + z_score * uncertainties
        
        return ci_lower, ci_upper
    
    def _generate_trading_signals(self, predictions, ci_lower, ci_upper):
        """Gera sinais de trading baseados nas previsões"""
        
        signals = []
        current_price = predictions[0]  # Preço atual
        
        for i, pred in enumerate(predictions):
            ci_width = ci_upper[i] - ci_lower[i]
            confidence = 1.0 / (1.0 + ci_width / pred)
            
            if pred > current_price * 1.05:  # Alta de 5%
                signal = TradingSignal.STRONG_BUY if confidence > 0.8 else TradingSignal.BUY
            elif pred > current_price * 1.02:  # Alta de 2%
                signal = TradingSignal.BUY
            elif pred < current_price * 0.95:  # Queda de 5%
                signal = TradingSignal.STRONG_SELL if confidence > 0.8 else TradingSignal.SELL
            elif pred < current_price * 0.98:  # Queda de 2%
                signal = TradingSignal.SELL
            else:
                signal = TradingSignal.NEUTRAL
            
            signals.append(signal)
        
        return signals
    
    def _calculate_feature_importance(self, model, input_sequence, feature_names):
        """Calcula importância de features usando permutation importance"""
        
        try:
            from sklearn.inspection import permutation_importance
            
            # Preparar dados
            X = input_sequence.reshape(1, *input_sequence.shape)
            
            # Função de scoring
            def scoring_fn(estimator, X, y):
                pred = estimator.predict(X, verbose=0)
                return -mean_squared_error(y, pred)
            
            # Calcular permutation importance
            result = permutation_importance(
                model, X, np.zeros(1),  # y dummy
                scoring=scoring_fn,
                n_repeats=10,
                random_state=42,
                n_jobs=-1
            )
            
            importance_scores = result.importances_mean
            
            # Mapear para nomes de features
            feature_importance = {}
            for i, (score, name) in enumerate(zip(importance_scores, feature_names)):
                if i < len(feature_names):
                    feature_importance[name] = float(score)
            
            return feature_importance
            
        except Exception as e:
            logger.warning(f"Erro ao calcular feature importance: {e}")
            return None
    
    def _optimize_hyperparameters(self, model_type, X_train, y_train, X_val, y_val):
        """Otimiza hiperparâmetros do modelo"""
        
        logger.info("Otimizando hiperparâmetros...")
        
        try:
            # Definir espaço de busca
            param_space = {
                'lstm_units': [[64, 32], [128, 64], [256, 128]],
                'dropout_rate': [0.2, 0.3, 0.4],
                'learning_rate': [0.001, 0.0005, 0.0001],
                'batch_size': [32, 64, 128]
            }
            
            # Criar otimizador
            optimizer = HyperparameterOptimizer(
                optimizer_type='bayesian',
                n_iter=20,
                cv_folds=3
            )
            
            # Função para criar modelo
            def model_creator():
                sequence_length = X_train.shape[1]
                n_features = X_train.shape[2]
                n_outputs = y_train.shape[1] if len(y_train.shape) > 1 else 1
                
                return AdvancedModelFactory.create_model(
                    model_type=model_type,
                    sequence_length=sequence_length,
                    n_features=n_features,
                    n_outputs=n_outputs,
                    config=self.config['model']
                )
            
            # Executar otimização
            best_model, best_score = optimizer.optimize(
                model_creator,
                param_space,
                np.vstack([X_train, X_val]),
                np.vstack([y_train, y_val]),
                scoring='neg_mean_squared_error'
            )
            
            logger.info(f"Otimização concluída. Melhor score: {-best_score:.6f}")
            
            return best_model
            
        except Exception as e:
            logger.warning(f"Erro na otimização de hiperparâmetros: {e}")
            return None
    
    def _create_optimizer(self):
        """Cria otimizador baseado na configuração"""
        
        optimizer_name = self.config['model']['optimizer']
        learning_rate = self.config['training']['learning_rate']
        
        if optimizer_name == 'adam':
            return Adam(
                learning_rate=learning_rate,
                beta_1=0.9,
                beta_2=0.999,
                epsilon=1e-7,
                amsgrad=False
            )
        elif optimizer_name == 'rmsprop':
            return RMSprop(
                learning_rate=learning_rate,
                rho=0.9,
                momentum=0.0,
                epsilon=1e-7,
                centered=False
            )
        elif optimizer_name == 'sgd':
            return SGD(
                learning_rate=learning_rate,
                momentum=0.9,
                nesterov=True
            )
        elif optimizer_name == 'nadam':
            return Nadam(
                learning_rate=learning_rate,
                beta_1=0.9,
                beta_2=0.999,
                epsilon=1e-7
            )
        else:
            return Adam(learning_rate=learning_rate)
    
    def _create_loss_function(self):
        """Cria função de loss baseada na configuração"""
        
        loss_name = self.config['model']['loss']
        
        if loss_name == 'mse':
            return MeanSquaredError()
        elif loss_name == 'mae':
            return MeanAbsoluteError()
        elif loss_name == 'huber':
            return Huber(delta=1.0)
        elif loss_name == 'logcosh':
            return LogCosh()
        else:
            return MeanSquaredError()
    
    def _create_metrics(self):
        """Cria lista de métricas"""
        
        metrics = []
        for metric_name in self.config['model']['metrics']:
            if metric_name == 'mse':
                metrics.append(MeanSquaredError(name='mse'))
            elif metric_name == 'mae':
                metrics.append(MeanAbsoluteError(name='mae'))
            elif metric_name == 'mape':
                metrics.append(tf.keras.metrics.MeanAbsolutePercentageError(name='mape'))
            elif metric_name == 'rmse':
                metrics.append(RootMeanSquaredError(name='rmse'))
        
        return metrics
    
    def _create_callbacks(self, symbol):
        """Cria callbacks para treinamento"""
        
        callbacks = []
        cb_config = self.config['model']['callbacks']
        
        if cb_config['early_stopping']:
            callbacks.append(
                EarlyStopping(
                    monitor='val_loss',
                    patience=self.config['training']['early_stopping_patience'],
                    restore_best_weights=True,
                    min_delta=self.config['training']['min_delta'],
                    verbose=1
                )
            )
        
        if cb_config['reduce_lr']:
            callbacks.append(
                ReduceLROnPlateau(
                    monitor='val_loss',
                    factor=0.5,
                    patience=self.config['training']['reduce_lr_patience'],
                    min_lr=1e-7,
                    verbose=1
                )
            )
        
        if cb_config['model_checkpoint']:
            callbacks.append(
                ModelCheckpoint(
                    filepath=f"{self.config['system']['model_dir']}/{symbol}_best.h5",
                    monitor='val_loss',
                    save_best_only=True,
                    save_weights_only=False,
                    verbose=1
                )
            )
        
        if cb_config['tensorboard']:
            log_dir = f"{self.config['system']['log_dir']}/tensorboard/{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            callbacks.append(
                TensorBoard(
                    log_dir=log_dir,
                    histogram_freq=1,
                    write_graph=True,
                    write_images=True,
                    update_freq='epoch'
                )
            )
        
        # CSV Logger
        callbacks.append(
            CSVLogger(
                f"{self.config['system']['log_dir']}/training_{symbol}.csv",
                append=True
            )
        )
        
        # TerminateOnNaN
        callbacks.append(TerminateOnNaN())
        
        return callbacks
    
    def _calculate_performance_metrics(self, symbol, y_true, y_pred, history, training_time):
        """Calcula métricas de performance detalhadas"""
        
        # Métricas básicas
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        mape = mean_absolute_percentage_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        
        # Acurácia direcional
        true_direction = np.diff(y_true.flatten()) > 0
        pred_direction = np.diff(y_pred.flatten()) > 0
        directional_accuracy = np.mean(true_direction == pred_direction) if len(true_direction) > 0 else 0
        
        # Métricas de trading
        returns = np.diff(y_true.flatten()) / y_true.flatten()[:-1]
        predicted_returns = np.diff(y_pred.flatten()) / y_pred.flatten()[:-1]
        
        sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
        max_drawdown = self._calculate_max_drawdown(y_true.flatten())
        
        # Calcular métricas de trading simuladas
        profit_factor, win_rate, avg_win_loss = self._simulate_trading_metrics(
            y_true.flatten(), y_pred.flatten()
        )
        
        # Confidence score
        confidence_score = 1.0 / (1.0 + np.std(y_pred - y_true) / np.std(y_true))
        
        # Tempo de inferência estimado
        inference_time = training_time / len(y_true) if len(y_true) > 0 else 0
        
        # Tamanho do modelo (estimado)
        model_size = 0  # Será calculado ao salvar
        
        return ModelPerformance(
            symbol=symbol,
            mse=mse,
            rmse=rmse,
            mae=mae,
            mape=mape,
            r2=r2,
            directional_accuracy=directional_accuracy,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            profit_factor=profit_factor,
            win_rate=win_rate,
            avg_win_loss_ratio=avg_win_loss,
            confidence_score=confidence_score,
            last_updated=datetime.now(),
            training_time=training_time,
            inference_time=inference_time,
            model_size_mb=model_size
        )
    
    def _calculate_max_drawdown(self, prices):
        """Calcula maximum drawdown"""
        peak = prices[0]
        max_dd = 0
        
        for price in prices:
            if price > peak:
                peak = price
            dd = (peak - price) / peak
            if dd > max_dd:
                max_dd = dd
        
        return max_dd
    
    def _simulate_trading_metrics(self, true_prices, pred_prices):
        """Simula trading simples para calcular métricas"""
        
        if len(true_prices) < 2:
            return 1.0, 0.5, 1.0
        
        positions = []
        profits = []
        
        for i in range(1, len(true_prices)):
            # Sinal de compra se previsão de alta
            if pred_prices[i] > true_prices[i-1]:
                # "Compra" no início, "venda" no final
                profit = true_prices[i] - true_prices[i-1]
                positions.append(profit)
        
        if not positions:
            return 1.0, 0.5, 1.0
        
        profits = np.array(positions)
        wins = profits[profits > 0]
        losses = profits[profits < 0]
        
        total_wins = np.sum(wins) if len(wins) > 0 else 0
        total_losses = np.abs(np.sum(losses)) if len(losses) > 0 else 0
        
        profit_factor = total_wins / total_losses if total_losses > 0 else float('inf')
        win_rate = len(wins) / len(positions) if len(positions) > 0 else 0
        avg_win = np.mean(wins) if len(wins) > 0 else 0
        avg_loss = np.mean(np.abs(losses)) if len(losses) > 0 else 0
        avg_win_loss = avg_win / avg_loss if avg_loss > 0 else 0
        
        return float(profit_factor), float(win_rate), float(avg_win_loss)
    
    def _save_model(self, symbol, model, scaler, performance, metadata):
        """Salva modelo e seus componentes"""
        
        model_dir = Path(self.config['system']['model_dir'])
        
        # Salvar modelo
        model_path = model_dir / f"{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.h5"
        model.save(model_path)
        
        # Salvar scaler
        scaler_path = model_dir / f"{symbol}_scaler.pkl"
        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler, f)
        
        # Salvar metadados
        metadata_path = model_dir / f"{symbol}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
        
        # Salvar performance
        performance_dict = asdict(performance)
        performance_dict['last_updated'] = performance_dict['last_updated'].isoformat()
        
        perf_path = model_dir / f"{symbol}_performance.json"
        with open(perf_path, 'w') as f:
            json.dump(performance_dict, f, indent=2)
        
        # Salvar arquitetura do modelo
        try:
            plot_path = model_dir / f"{symbol}_architecture.png"
            plot_model(model, to_file=str(plot_path), show_shapes=True, show_layer_names=True)
        except:
            pass
        
        logger.debug(f"Modelo salvo: {model_path}")
    
    def _evict_oldest_model(self):
        """Remove o modelo mais antigo"""
        if not self.models:
            return
        
        oldest_symbol = min(self.models.keys(), 
                          key=lambda x: self.models[x]['last_updated'])
        
        # Remover arquivos
        model_dir = Path(self.config['system']['model_dir'])
        for file in model_dir.glob(f"{oldest_symbol}*"):
            try:
                file.unlink()
            except:
                pass
        
        # Remover do cache
        del self.models[oldest_symbol]
        
        logger.info(f"Modelo removido: {oldest_symbol}")
    
    def _handle_system_alert(self, alert):
        """Handler para alertas do sistema"""
        
        logger.warning(f"ALERTA DO SISTEMA: {alert}")
        
        # Tomar ações baseadas no tipo de alerta
        if alert['type'] == 'memory' and alert['level'] == 'warning':
            self._cleanup_memory()
        elif alert['type'] == 'cpu' and alert['value'] > 90:
            self._reduce_processing_load()
    
    def _cleanup_memory(self):
        """Limpa memória quando necessário"""
        gc.collect()
        tf.keras.backend.clear_session()
        
        # Limpar cache de previsões
        if len(self.prediction_cache) > 50:
            self.prediction_cache.clear()
        
        logger.info("Memória limpa")
    
    def _reduce_processing_load(self):
        """Reduz carga de processamento"""
        # Reduzir workers ativos
        current_workers = self.thread_pool._max_workers
        if current_workers > 2:
            new_workers = max(2, current_workers // 2)
            self.thread_pool._max_workers = new_workers
            logger.info(f"Workers reduzidos para {new_workers}")
    
    # ============================================================================
    # WORKERS
    # ============================================================================
    
    def _data_fetcher_worker(self):
        """Worker para busca periódica de dados"""
        
        logger.info("DataFetcher worker iniciado")
        
        # Lista de símbolos para monitorar
        symbols_to_monitor = [
            'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA',
            'SPY', 'QQQ', 'DIA', 'IWM', 'GLD'
        ]
        
        while self.is_running:
            try:
                # Buscar dados para cada símbolo
                for symbol in symbols_to_monitor:
                    try:
                        data = self.data_manager.fetch_stock_data(
                            symbol=symbol,
                            interval='1d',
                            source=DataSource.YFINANCE
                        )
                        
                        if data is not None and not data.empty:
                            # Adicionar à fila de processamento
                            self.data_queue.put({
                                'symbol': symbol,
                                'data': data,
                                'timestamp': datetime.now(),
                                'priority': 1
                            })
                            
                            logger.debug(f"Dados buscados para {symbol}")
                    
                    except Exception as e:
                        logger.error(f"Erro ao buscar dados para {symbol}: {e}")
                
                # Aguardar antes da próxima iteração
                time.sleep(3600)  # 1 hora
                
            except Exception as e:
                logger.error(f"Erro no DataFetcher worker: {e}")
                time.sleep(300)  # 5 minutos em caso de erro
    
    def _training_worker(self):
        """Worker para processar treinamentos na fila"""
        
        logger.info("Training worker iniciado")
        
        while self.is_running:
            try:
                # Pegar tarefa da fila
                task = self.training_queue.get(timeout=5)
                
                symbol = task['symbol']
                data = task['data']
                priority = task.get('priority', 5)
                
                logger.info(f"Processando treinamento para {symbol} (priority: {priority})")
                
                # Executar treinamento
                success = self.train_model(symbol, data)
                
                if success:
                    logger.info(f"Treinamento concluído para {symbol}")
                    
                    # Adicionar resultado à fila
                    self.result_queue.put({
                        'type': 'training',
                        'symbol': symbol,
                        'success': True,
                        'timestamp': datetime.now()
                    })
                else:
                    logger.error(f"Treinamento falhou para {symbol}")
                    
                    self.result_queue.put({
                        'type': 'training',
                        'symbol': symbol,
                        'success': False,
                        'timestamp': datetime.now()
                    })
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Erro no training worker: {e}")
            finally:
                if 'task' in locals():
                    self.training_queue.task_done()
    
    def _prediction_worker(self):
        """Worker para processar previsões na fila"""
        
        logger.info("Prediction worker iniciado")
        
        while self.is_running:
            try:
                # Pegar tarefa da fila
                task = self.prediction_queue.get(timeout=1)
                
                symbol = task['symbol']
                data = task.get('data')
                n_future = task.get('n_future', self.config['prediction']['n_future'])
                
                logger.debug(f"Processando previsão para {symbol}")
                
                # Executar previsão
                result = self.predict(symbol, data, n_future)
                
                if result:
                    # Adicionar resultado à fila
                    self.result_queue.put({
                        'type': 'prediction',
                        'symbol': symbol,
                        'result': result,
                        'timestamp': datetime.now()
                    })
                    
                    logger.debug(f"Previsão concluída para {symbol}")
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Erro no prediction worker: {e}")
            finally:
                if 'task' in locals():
                    self.prediction_queue.task_done()
    
    def _monitoring_worker(self):
        """Worker para monitoramento contínuo"""
        
        logger.info("Monitoring worker iniciado")
        
        while self.is_running:
            try:
                # Verificar performance dos modelos
                for symbol, model_info in list(self.models.items()):
                    performance = model_info.get('performance')
                    
                    if performance:
                        # Verificar se precisa retreinar
                        if (performance.directional_accuracy < 
                            self.config['monitoring']['alert_thresholds']['model_accuracy']):
                            
                            logger.info(f"Agendando retreinamento para {symbol} "
                                       f"(accuracy: {performance.directional_accuracy:.2%})")
                            
                            # Agendar retreinamento
                            self.training_queue.put({
                                'symbol': symbol,
                                'priority': 2,  # Prioridade alta
                                'timestamp': datetime.now()
                            })
                
                # Verificar freshness dos dados
                current_time = datetime.now()
                for symbol, model_info in list(self.models.items()):
                    last_updated = model_info.get('last_updated')
                    
                    if last_updated:
                        hours_since_update = (current_time - last_updated).total_seconds() / 3600
                        
                        if hours_since_update > self.config['monitoring']['alert_thresholds']['data_freshness_hours']:
                            logger.info(f"Dados antigos para {symbol} "
                                       f"({hours_since_update:.1f} horas)")
                
                # Aguardar antes da próxima verificação
                time.sleep(300)  # 5 minutos
                
            except Exception as e:
                logger.error(f"Erro no monitoring worker: {e}")
                time.sleep(60)
    
    def _results_processor_worker(self):
        """Worker para processar resultados"""
        
        logger.info("Results processor worker iniciado")
        
        while self.is_running:
            try:
                # Pegar resultado da fila
                result = self.result_queue.get(timeout=5)
                
                result_type = result['type']
                symbol = result['symbol']
                
                if result_type == 'prediction':
                    prediction_result = result['result']
                    
                    # Aqui você pode:
                    # 1. Armazenar em banco de dados
                    # 2. Enviar para API
                    # 3. Gerar alertas
                    # 4. Atualizar dashboard
                    
                    logger.debug(f"Resultado de previsão processado para {symbol}")
                    
                elif result_type == 'training':
                    success = result['success']
                    
                    if success:
                        # Atualizar métricas do sistema
                        logger.info(f"Treinamento bem-sucedido para {symbol}")
                    else:
                        logger.warning(f"Treinamento falhou para {symbol}")
                
                # Processar outras tarefas...
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Erro no results processor: {e}")
            finally:
                if 'result' in locals():
                    self.result_queue.task_done()
    
    # ============================================================================
    # API PÚBLICA
    # ============================================================================
    
    def get_system_status(self) -> Dict[str, Any]:
        """Retorna status completo do sistema"""
        
        # Métricas de recursos
        resource_metrics = self.resource_monitor.get_metrics_report() if hasattr(self, 'resource_monitor') else {}
        
        # Cache stats
        cache_stats = self.data_manager.get_cache_stats() if hasattr(self, 'data_manager') else {}
        
        # Model stats
        model_stats = {
            'total_models': len(self.models),
            'recently_trained': [
                symbol for symbol, info in self.models.items()
                if (datetime.now() - info['last_updated']).days < 7
            ],
            'best_performing': sorted(
                [(symbol, info.get('performance', {}).get('directional_accuracy', 0)) 
                 for symbol, info in self.models.items() 
                 if info.get('performance')],
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }
        
        # Queue stats
        queue_stats = {
            'data_queue': self.data_queue.qsize(),
            'training_queue': self.training_queue.qsize(),
            'prediction_queue': self.prediction_queue.qsize(),
            'result_queue': self.result_queue.qsize()
        }
        
        # Worker stats
        worker_stats = {
            'active_threads': threading.active_count(),
            'thread_pool_workers': self.thread_pool._max_workers if hasattr(self.thread_pool, '_max_workers') else 0,
            'process_pool_workers': self.process_pool._max_workers if hasattr(self.process_pool, '_max_workers') else 0
        }
        
        # System info
        system_info = {
            'system_state': self.system_state,
            'version': self.VERSION,
            'uptime': str(datetime.now() - self.start_time),
            'operation_mode': self.operation_mode,
            'python_version': sys.version,
            'tensorflow_version': tf.__version__,
            'platform': sys.platform
        }
        
        return {
            'system': system_info,
            'resources': resource_metrics,
            'models': model_stats,
            'queues': queue_stats,
            'workers': worker_stats,
            'cache': cache_stats,
            'timestamp': datetime.now().isoformat()
        }
    
    def schedule_training(self, symbol: str, data: Optional[pd.DataFrame] = None, 
                         priority: int = 5) -> bool:
        """Agenda treinamento para um símbolo"""
        
        try:
            self.training_queue.put({
                'symbol': symbol,
                'data': data,
                'priority': priority,
                'timestamp': datetime.now()
            })
            
            logger.info(f"Treinamento agendado para {symbol} (priority: {priority})")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao agendar treinamento para {symbol}: {e}")
            return False
    
    def schedule_prediction(self, symbol: str, data: Optional[pd.DataFrame] = None,
                           n_future: Optional[int] = None) -> bool:
        """Agenda previsão para um símbolo"""
        
        try:
            self.prediction_queue.put({
                'symbol': symbol,
                'data': data,
                'n_future': n_future or self.config['prediction']['n_future'],
                'timestamp': datetime.now()
            })
            
            logger.info(f"Previsão agendada para {symbol}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao agendar previsão para {symbol}: {e}")
            return False
    
    def get_model_info(self, symbol: str) -> Optional[Dict]:
        """Retorna informações detalhadas sobre um modelo"""
        
        if symbol not in self.models:
            return None
        
        model_info = self.models[symbol]
        
        return {
            'symbol': symbol,
            'model_type': model_info['metadata'].get('model_type', 'unknown'),
            'last_updated': model_info['last_updated'].isoformat(),
            'performance': asdict(model_info['performance']) if model_info.get('performance') else None,
            'metadata': model_info['metadata'],
            'training_time': model_info.get('training_time', 0),
            'feature_columns': model_info['metadata'].get('feature_columns', [])
        }
    
    def shutdown(self):
        """Desliga o sistema de forma controlada"""
        
        logger.info("Desligando sistema de IA...")
        
        self.is_running = False
        
        # Parar workers
        self.thread_pool.shutdown(wait=True)
        self.process_pool.shutdown(wait=True)
        
        # Parar monitoramento
        if hasattr(self, 'resource_monitor'):
            self.resource_monitor.stop_monitoring()
        
        # Salvar estado
        self._save_system_state()
        
        # Limpar recursos
        self._cleanup_memory()
        
        self.system_state = 'shutdown'
        logger.info("Sistema de IA desligado")

# ============================================================================
# BACKTESTING AVANÇADO
# ============================================================================

class AdvancedBacktester:
    """Sistema avançado de backtesting"""
    
    def __init__(self, ai_system: AdvancedAISystem):
        self.ai_system = ai_system
        self.results = {}
        self.metrics_history = []
        
    def run_backtest(self, symbol: str, 
                    start_date: datetime,
                    end_date: datetime,
                    initial_capital: float = 100000,
                    commission: float = 0.001,
                    slippage: float = 0.0005) -> Dict:
        """Executa backtest completo"""
        
        logger.info(f"Iniciando backtest para {symbol}")
        
        try:
            # Buscar dados históricos
            data = self.ai_system.data_manager.fetch_stock_data(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                interval='1d'
            )
            
            if data is None or data.empty:
                logger.error(f"Dados insuficientes para backtest de {symbol}")
                return {}
            
            # Preparar dados
            data = self.ai_system.data_preprocessor.create_technical_indicators(data)
            
            # Executar backtest
            results = self._execute_walk_forward(
                data, symbol, initial_capital, commission, slippage
            )
            
            # Calcular métricas
            metrics = self._calculate_backtest_metrics(results)
            
            # Armazenar resultados
            self.results[symbol] = {
                'data': results,
                'metrics': metrics,
                'timestamp': datetime.now()
            }
            
            self.metrics_history.append({
                'symbol': symbol,
                'metrics': metrics,
                'timestamp': datetime.now()
            })
            
            logger.info(f"Backtest concluído para {symbol}")
            logger.info(f"  Return: {metrics['total_return']:.2%}")
            logger.info(f"  Sharpe: {metrics['sharpe_ratio']:.2f}")
            logger.info(f"  Max DD: {metrics['max_drawdown']:.2%}")
            
            return results
            
        except Exception as e:
            logger.error(f"Erro no backtest de {symbol}: {e}")
            return {}
    
    def _execute_walk_forward(self, data, symbol, initial_capital, commission, slippage):
        """Executa walk-forward backtesting"""
        
        # Parâmetros do walk-forward
        train_size = 252  # 1 ano de treinamento
        test_size = 63    # 3 meses de teste
        step_size = 21    # 1 mês de step
        
        results = []
        capital = initial_capital
        position = 0
        trades = []
        
        dates = data.index
        n_periods = len(dates)
        
        for start_idx in range(0, n_periods - train_size - test_size, step_size):
            # Definir janelas
            train_end = start_idx + train_size
            test_end = train_end + test_size
            
            if test_end >= n_periods:
                break
            
            train_data = data.iloc[start_idx:train_end]
            test_data = data.iloc[train_end:test_end]
            
            # Treinar modelo na janela de treino
            logger.info(f"Treinando modelo para janela {start_idx}-{train_end}")
            self.ai_system.train_model(symbol, train_data)
            
            # Testar na janela de teste
            window_results = self._test_on_window(
                test_data, symbol, capital, position, commission, slippage
            )
            
            results.extend(window_results)
            
            # Atualizar capital e posição
            if window_results:
                last_result = window_results[-1]
                capital = last_result['capital']
                position = last_result['position']
        
        return results
    
    def _test_on_window(self, test_data, symbol, initial_capital, initial_position, 
                       commission, slippage):
        """Testa estratégia em uma janela"""
        
        results = []
        capital = initial_capital
        position = initial_position
        trades = []
        
        for i in range(len(test_data) - 1):
            current_date = test_data.index[i]
            next_date = test_data.index[i + 1]
            
            # Dados até o momento atual
            history_data = test_data.iloc[:i+1]
            
            # Fazer previsão
            prediction = self.ai_system.predict(symbol, history_data, n_future=1)
            
            if prediction is None:
                continue
            
            # Gerar sinal
            signal = self._generate_signal_from_prediction(prediction, test_data.iloc[i])
            
            # Executar trade
            trade_result = self._execute_trade(
                symbol, current_date, next_date, signal,
                test_data.iloc[i], test_data.iloc[i+1],
                capital, position, commission, slippage
            )
            
            # Atualizar estado
            capital = trade_result['capital_after']
            position = trade_result['position_after']
            
            if trade_result['trade_executed']:
                trades.append(trade_result)
            
            # Registrar resultado do dia
            results.append({
                'date': current_date,
                'capital': capital,
                'position': position,
                'price': test_data.iloc[i]['Close'],
                'signal': signal.value if signal else 0,
                'trade_executed': trade_result['trade_executed'],
                'trade_pnl': trade_result.get('pnl', 0)
            })
        
        return results
    
    def _generate_signal_from_prediction(self, prediction, current_data):
        """Gera sinal de trading baseado na previsão"""
        
        if not prediction.signals:
            return None
        
        signal = prediction.signals[0]
        current_price = current_data['Close']
        predicted_price = prediction.point_predictions[0]
        
        # Ajustar sinal baseado em confiança
        confidence = 1.0 - (prediction.confidence_intervals[1][0] - 
                          prediction.confidence_intervals[0][0]) / current_price
        
        if confidence < 0.6:
            # Baixa confiança, ficar neutro
            return TradingSignal.NEUTRAL
        
        return signal
    
    def _execute_trade(self, symbol, entry_date, exit_date, signal, 
                      entry_data, exit_data, capital, position, 
                      commission, slippage):
        """Executa um trade"""
        
        entry_price = entry_data['Close']
        exit_price = exit_data['Close']
        
        # Aplicar slippage
        if signal in [TradingSignal.BUY, TradingSignal.STRONG_BUY]:
            entry_price *= (1 + slippage)
            exit_price *= (1 - slippage)
        elif signal in [TradingSignal.SELL, TradingSignal.STRONG_SELL]:
            entry_price *= (1 - slippage)
            exit_price *= (1 + slippage)
        
        trade_result = {
            'symbol': symbol,
            'entry_date': entry_date,
            'exit_date': exit_date,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'signal': signal,
            'trade_executed': False,
            'capital_before': capital,
            'position_before': position,
            'capital_after': capital,
            'position_after': position
        }
        
        if signal is None:
            return trade_result
        
        # Lógica de trading
        if signal in [TradingSignal.BUY, TradingSignal.STRONG_BUY] and position <= 0:
            # Comprar
            trade_size = capital * 0.1  # 10% do capital
            shares = trade_size / entry_price
            cost = shares * entry_price * (1 + commission)
            
            if cost <= capital:
                capital -= cost
                position += shares
                trade_result['trade_executed'] = True
                trade_result['action'] = 'BUY'
                trade_result['shares'] = shares
                trade_result['cost'] = cost
        
        elif signal in [TradingSignal.SELL, TradingSignal.STRONG_SELL] and position > 0:
            # Vender
            proceeds = position * exit_price * (1 - commission)
            capital += proceeds
            pnl = proceeds - (position * entry_price)
            
            trade_result['trade_executed'] = True
            trade_result['action'] = 'SELL'
            trade_result['shares'] = position
            trade_result['proceeds'] = proceeds
            trade_result['pnl'] = pnl
            
            position = 0
        
        trade_result['capital_after'] = capital
        trade_result['position_after'] = position
        
        return trade_result
    
    def _calculate_backtest_metrics(self, results):
        """Calcula métricas de performance do backtest"""
        
        if not results:
            return {}
        
        # Extrair séries
        dates = [r['date'] for r in results]
        capital = [r['capital'] for r in results]
        returns = np.diff(capital) / capital[:-1]
        
        # Métricas básicas
        total_return = (capital[-1] - capital[0]) / capital[0]
        annual_return = (1 + total_return) ** (252 / len(results)) - 1
        
        # Volatilidade
        volatility = np.std(returns) * np.sqrt(252)
        
        # Sharpe Ratio
        risk_free_rate = 0.02  # 2% anual
        sharpe_ratio = (annual_return - risk_free_rate) / volatility if volatility > 0 else 0
        
        # Maximum Drawdown
        peak = capital[0]
        max_dd = 0
        
        for value in capital:
            if value > peak:
                peak = value
            dd = (peak - value) / peak
            if dd > max_dd:
                max_dd = dd
        
        # Calmar Ratio
        calmar_ratio = annual_return / max_dd if max_dd > 0 else 0
        
        # Sortino Ratio (usa apenas downside deviation)
        downside_returns = [r for r in returns if r < 0]
        downside_dev = np.std(downside_returns) * np.sqrt(252) if downside_returns else 0
        sortino_ratio = (annual_return - risk_free_rate) / downside_dev if downside_dev > 0 else 0
        
        # Estatísticas de trades
        trades = [r for r in results if r['trade_executed']]
        winning_trades = [t for t in trades if t.get('pnl', 0) > 0]
        losing_trades = [t for t in trades if t.get('pnl', 0) < 0]
        
        win_rate = len(winning_trades) / len(trades) if trades else 0
        avg_win = np.mean([t.get('pnl', 0) for t in winning_trades]) if winning_trades else 0
        avg_loss = np.mean([t.get('pnl', 0) for t in losing_trades]) if losing_trades else 0
        profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
        
        # Value at Risk (VaR)
        var_95 = np.percentile(returns, 5) if len(returns) > 0 else 0
        var_99 = np.percentile(returns, 1) if len(returns) > 0 else 0
        
        # Expected Shortfall (CVaR)
        cvar_95 = np.mean([r for r in returns if r <= var_95]) if any(r <= var_95 for r in returns) else 0
        
        return {
            'total_return': float(total_return),
            'annual_return': float(annual_return),
            'volatility': float(volatility),
            'sharpe_ratio': float(sharpe_ratio),
            'sortino_ratio': float(sortino_ratio),
            'calmar_ratio': float(calmar_ratio),
            'max_drawdown': float(max_dd),
            'win_rate': float(win_rate),
            'profit_factor': float(profit_factor),
            'avg_win': float(avg_win),
            'avg_loss': float(avg_loss),
            'total_trades': len(trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'var_95': float(var_95),
            'var_99': float(var_99),
            'cvar_95': float(cvar_95)
        }

# ============================================================================
# EXEMPLO DE USO COMPLETO
# ============================================================================

async def comprehensive_example():
    """Exemplo completo do sistema em operação"""
    
    logger.info("Iniciando exemplo completo do Sistema de IA Avançado")
    
    try:
        # 1. Inicializar sistema
        print("=" * 80)
        print("INICIALIZANDO SISTEMA DE IA AVANÇADO")
        print("=" * 80)
        
        config = {
            'system': {
                'name': 'My Advanced Trading AI',
                'max_workers': 8,
                'use_gpu': True,
                'mixed_precision': True
            },
            'model': {
                'default_type': ModelType.LSTM_ADVANCED,
                'hyperparameter_optimization': True,
                'uncertainty_estimation': True
            },
            'prediction': {
                'enable_monte_carlo': True,
                'mc_dropout_samples': 50,
                'signal_generation': True
            }
        }
        
        ai_system = AdvancedAISystem(config)
        
        # Aguardar inicialização
        time.sleep(2)
        
        # 2. Verificar status do sistema
        print("\n" + "=" * 80)
        print("STATUS DO SISTEMA")
        print("=" * 80)
        
        status = ai_system.get_system_status()
        print(f"Estado: {status['system']['system_state']}")
        print(f"Modelos carregados: {status['models']['total_models']}")
        print(f"Uso de CPU: {status['resources']['summary']['cpu_percent_total']['current']:.1f}%")
        print(f"Uso de Memória: {status['resources']['summary']['memory_used_percent']['current']:.1f}%")
        
        # 3. Treinar modelo para AAPL
        print("\n" + "=" * 80)
        print("TREINANDO MODELO PARA AAPL")
        print("=" * 80)
        
        success = ai_system.train_model('AAPL')
        
        if success:
            print("✅ Modelo treinado com sucesso!")
            
            # 4. Fazer previsões
            print("\n" + "=" * 80)
            print("FAZENDO PREVISÕES PARA AAPL")
            print("=" * 80)
            
            prediction = ai_system.predict('AAPL', n_future=10)
            
            if prediction:
                print(f"Previsões para os próximos 10 dias:")
                for i, (point, lower, upper) in enumerate(zip(
                    prediction.point_predictions,
                    prediction.confidence_intervals[0],
                    prediction.confidence_intervals[1]
                )):
                    print(f"  Dia {i+1}: {point:.2f} ({lower:.2f} - {upper:.2f})")
                
                if prediction.signals:
                    print(f"\nSinais de trading:")
                    for i, signal in enumerate(prediction.signals[:5]):
                        print(f"  Dia {i+1}: {signal.name}")
        
        # 5. Executar backtest
        print("\n" + "=" * 80)
        print("EXECUTANDO BACKTEST PARA AAPL")
        print("=" * 80)
        
        backtester = AdvancedBacktester(ai_system)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * 2)  # 2 anos
        
        backtest_results = backtester.run_backtest(
            symbol='AAPL',
            start_date=start_date,
            end_date=end_date,
            initial_capital=100000,
            commission=0.001,
            slippage=0.0005
        )
        
        if backtest_results:
            metrics = backtester._calculate_backtest_metrics(backtest_results)
            print(f"Resultados do Backtest:")
            print(f"  Retorno Total: {metrics['total_return']:.2%}")
            print(f"  Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
            print(f"  Max Drawdown: {metrics['max_drawdown']:.2%}")
            print(f"  Win Rate: {metrics['win_rate']:.2%}")
        
        # 6. Monitorar sistema em tempo real
        print("\n" + "=" * 80)
        print("MONITORAMENTO EM TEMPO REAL (60 segundos)")
        print("=" * 80)
        
        for i in range(12):  # 60 segundos com atualização a cada 5s
            status = ai_system.get_system_status()
            
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] "
                  f"Modelos: {status['models']['total_models']} | "
                  f"CPU: {status['resources']['summary']['cpu_percent_total']['current']:.1f}% | "
                  f"Mem: {status['resources']['summary']['memory_used_percent']['current']:.1f}% | "
                  f"Fila Previsões: {status['queues']['prediction_queue']}")
            
            time.sleep(5)
        
        # 7. Agendar tarefas
        print("\n" + "=" * 80)
        print("AGENDANDO TAREFAS ADICIONAIS")
        print("=" * 80)
        
        # Agendar treinamento para outros símbolos
        symbols_to_train = ['GOOGL', 'MSFT', 'AMZN', 'TSLA']
        
        for symbol in symbols_to_train:
            ai_system.schedule_training(symbol, priority=3)
            print(f"Treinamento agendado para {symbol}")
            time.sleep(1)  # Pequeno delay para não sobrecarregar
        
        # 8. Finalizar
        print("\n" + "=" * 80)
        print("FINALIZANDO SISTEMA")
        print("=" * 80)
        
        ai_system.shutdown()
        
        print("✅ Sistema finalizado com sucesso!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Sistema interrompido pelo usuário")
        if 'ai_system' in locals():
            ai_system.shutdown()
    except Exception as e:
        print(f"\n❌ Erro no exemplo: {e}")
        traceback.print_exc()
        if 'ai_system' in locals():
            ai_system.shutdown()

def main():
    """Função principal"""
    
    # Executar exemplo completo
    asyncio.run(comprehensive_example())

if __name__ == "__main__":
    # Configurar logging
    logger = setup_advanced_logging(logging.INFO)
    
    # Registrar handler para SIGINT (Ctrl+C)
    import signal
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
    
    # Executar
    main()