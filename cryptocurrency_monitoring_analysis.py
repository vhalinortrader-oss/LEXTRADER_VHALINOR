#!/usr/bin/env python3
"""
Sistema de monitoramento e análise de criptomoedas.
Requer: ccxt, pandas, matplotlib, numpy, scikit-learn (opcional)
"""

import time
import threading
from datetime import datetime
from typing import List, Optional

import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sklearn.preprocessing import MinMaxScaler  # ou implementação manual


class DataPoint:
    """Representa um ponto de dados (data e preço de fechamento)."""
    def __init__(self, date: datetime, close: float):
        self.date = date
        self.close = close

    def __repr__(self):
        return f"DataPoint(date={self.date}, close={self.close})"


class CryptocurrencyMonitoringAnalysis:
    """
    Classe principal para monitoramento e análise de criptomoedas.
    """

    def __init__(self, api_key: str, api_secret: str, symbol: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.symbol = symbol
        self.interval = '1m'          # intervalo dos candles
        self.lookback = 60            # número de velas a buscar
        self.scaler = MinMaxScaler(feature_range=(0, 1))

        # Inicializa a exchange (usando Binance como exemplo)
        self.exchange = ccxt.binance({
            'apiKey': self.api_key,
            'secret': self.api_secret,
            'enableRateLimit': True,
        })
        # Para dados públicos, não precisa de autenticação, mas mantemos

        # Dados atuais (serão atualizados a cada iteração)
        self.data: List[DataPoint] = []
        self.df: Optional[pd.DataFrame] = None

        # Configuração do gráfico interativo
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.line = None
        self.ani = None

    def fetch_market_data(self) -> List[DataPoint]:
        """
        Obtém os dados de mercado da exchange (candles) e retorna
        uma lista de DataPoints.
        """
        try:
            # Busca as últimas 'lookback' velas com intervalo 'interval'
            candles = self.exchange.fetch_ohlcv(
                self.symbol,
                timeframe=self.interval,
                limit=self.lookback
            )
            data_points = []
            for candle in candles:
                # candle: [timestamp, open, high, low, close, volume]
                timestamp = datetime.fromtimestamp(candle[0] / 1000.0)
                close = candle[4]
                data_points.append(DataPoint(timestamp, close))
            return data_points
        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
            return []

    def preprocess_data(self, data: List[DataPoint]) -> np.ndarray:
        """
        Pré-processa os dados: converte para array numpy e aplica
        normalização (opcional).
        """
        if not data:
            return np.array([])
        prices = np.array([dp.close for dp in data]).reshape(-1, 1)
        # Aplica MinMaxScaler
        scaled = self.scaler.fit_transform(prices)
        return scaled.flatten()

    def calculate_technical_indicators(self, data: List[DataPoint]) -> pd.DataFrame:
        """
        Calcula indicadores técnicos (exemplo: SMA 5 e SMA 20).
        Retorna um DataFrame com os indicadores.
        """
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame({
            'timestamp': [dp.date for dp in data],
            'close': [dp.close for dp in data]
        })
        # Média móvel simples de 5 e 20 períodos
        df['sma_5'] = df['close'].rolling(window=5).mean()
        df['sma_20'] = df['close'].rolling(window=20).mean()
        # Opcional: RSI, MACD, etc. (pode usar bibliotecas como `ta`)
        return df

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Gera sinais de compra/venda com base nos indicadores.
        Exemplo: cruzamento de médias móveis.
        """
        if df.empty:
            return df

        # Sinal de compra quando SMA_5 cruza acima de SMA_20
        df['signal'] = 0
        df.loc[df['sma_5'] > df['sma_20'], 'signal'] = 1
        df.loc[df['sma_5'] < df['sma_20'], 'signal'] = -1
        # Detecta mudanças
        df['position'] = df['signal'].diff()
        return df

    def plot_data(self, df: pd.DataFrame, signals: pd.DataFrame):
        """
        Atualiza o gráfico com os dados e os sinais.
        """
        if df.empty:
            return

        # Limpa o eixo
        self.ax.clear()

        # Plota o preço de fechamento
        self.ax.plot(df['timestamp'], df['close'], label='Close Price', color='blue')

        # Plota as médias móveis
        self.ax.plot(df['timestamp'], df['sma_5'], label='SMA 5', color='orange', linestyle='--')
        self.ax.plot(df['timestamp'], df['sma_20'], label='SMA 20', color='green', linestyle='--')

        # Plota sinais de compra/venda
        buy_signals = signals[signals['position'] == 1]
        sell_signals = signals[signals['position'] == -1]
        if not buy_signals.empty:
            self.ax.scatter(buy_signals['timestamp'], buy_signals['close'],
                            marker='^', color='green', s=100, label='Buy Signal')
        if not sell_signals.empty:
            self.ax.scatter(sell_signals['timestamp'], sell_signals['close'],
                            marker='v', color='red', s=100, label='Sell Signal')

        self.ax.set_title(f'Cryptocurrency Price and Technical Indicators ({self.symbol})')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Price')
        self.ax.legend()
        self.ax.grid(True)

        # Formata o eixo x para exibir datas
        self.fig.autofmt_xdate()
        plt.tight_layout()

    def update(self, frame):
        """Função chamada a cada iteração do animation."""
        try:
            # Busca novos dados
            new_data = self.fetch_market_data()
            if not new_data:
                return

            self.data = new_data

            # Calcula indicadores
            df = self.calculate_technical_indicators(self.data)
            if df.empty:
                return

            # Gera sinais
            signals = self.generate_signals(df)

            # Atualiza o gráfico
            self.plot_data(df, signals)

        except Exception as e:
            print(f"Erro na atualização: {e}")

    def run(self):
        """
        Inicia o monitoramento contínuo (atualização a cada 60 segundos).
        """
        print(f"Iniciando monitoramento para {self.symbol}...")
        # Configura o animation do matplotlib para atualizar a cada 60 segundos
        self.ani = FuncAnimation(
            self.fig, self.update, interval=60000,  # 60000 ms = 60 segundos
            cache_frame_data=False
        )
        plt.show()

    def run_blocking(self):
        """
        Versão alternativa usando loop com sleep (sem animation).
        """
        print(f"Iniciando monitoramento (loop) para {self.symbol}...")
        try:
            while True:
                self.update(None)  # frame é ignorado
                plt.draw()
                plt.pause(0.001)   # permite que o gráfico seja renderizado
                time.sleep(60)     # aguarda 60 segundos
        except KeyboardInterrupt:
            print("Monitoramento interrompido.")


def main():
    # Substitua pelas suas credenciais (se necessário para dados privados)
    api_key = "your_api_key"
    api_secret = "your_api_secret"
    symbol = "BTC/USDT"  # ou "BTCUSDT" dependendo da exchange

    monitoring = CryptocurrencyMonitoringAnalysis(api_key, api_secret, symbol)

    # Escolha um dos modos de execução:
    # monitoring.run()           # com FuncAnimation (recomendado)
    monitoring.run_blocking()    # com loop tradicional


if __name__ == "__main__":
    main()