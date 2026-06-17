import requests
import pandas as pd
import numpy as np
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import threading
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio
import aiohttp
from abc import ABC, abstractmethod
import json
import feedparser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

# Configuração avançada de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('omega_trading_advanced.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('OmegaTradingAdvanced')

class APIClient:
    """Cliente HTTP otimizado com cache e retry"""
    
    def __init__(self, base_url: str = None, timeout: int = 30, max_retries: int = 3):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = None
        self._cache = {}
        self.cache_ttl = timedelta(minutes=5)
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get(self, url: str, params: Dict = None, use_cache: bool = True) -> Dict:
        """Requisição GET otimizada com cache e retry automático"""
        cache_key = f"{url}_{hash(frozenset(params.items())) if params else ''}"
        
        if use_cache and cache_key in self._cache:
            cached_data, timestamp = self._cache[cache_key]
            if datetime.now() - timestamp < self.cache_ttl:
                logger.debug(f"Retornando dados do cache para: {url}")
                return cached_data
        
        for attempt in range(self.max_retries):
            try:
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if use_cache:
                            self._cache[cache_key] = (data, datetime.now())
                        
                        return data
                    else:
                        logger.warning(f"Status {response.status} para {url}, tentativa {attempt + 1}")
            except Exception as e:
                logger.error(f"Erro na tentativa {attempt + 1}: {e}")
                if attempt == self.max_retries - 1:
                    raise
        
        raise Exception(f"Falha após {self.max_retries} tentativas para: {url}")

class ColetorDadosMercado:
    """Coletor otimizado de dados de mercado"""
    
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys
        self.coletores = {
            'alpha_vantage': AlphaVantageColetor(api_keys.get('alpha_vantage')),
            'news': NewsColetor(),
            'binance': BinanceColetor(api_keys.get('binance'))
        }
    
    async def coletar_dados_acao(self, symbol: str, fonte: str = 'alpha_vantage') -> Dict:
        """Coleta dados de ação de forma assíncrona"""
        if fonte not in self.coletores:
            raise ValueError(f"Fonte não suportada: {fonte}")
        
        return await self.coletores[fonte].coletar_dados(symbol)
    
    async def coletar_multiplas_acoes(self, symbols: List[str]) -> Dict[str, Dict]:
        """Coleta dados de múltiplas ações em paralelo"""
        tasks = []
        for symbol in symbols:
            task = self.coletar_dados_acao(symbol)
            tasks.append(task)
        
        resultados = await asyncio.gather(*tasks, return_exceptions=True)
        
        dados = {}
        for symbol, resultado in zip(symbols, resultados):
            if isinstance(resultado, Exception):
                logger.error(f"Erro ao coletar {symbol}: {resultado}")
            else:
                dados[symbol] = resultado
        
        return dados

class AlphaVantageColetor:
    """Coletor específico para Alpha Vantage"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
    
    async def coletar_dados(self, symbol: str) -> Dict:
        """Coleta dados do Alpha Vantage"""
        params = {
            'function': 'TIME_SERIES_DAILY_ADJUSTED',
            'symbol': symbol,
            'apikey': self.api_key,
            'outputsize': 'compact'
        }
        
        async with APIClient() as client:
            return await client.get(self.base_url, params=params)

class NewsColetor:
    """Coletor otimizado de notícias financeiras"""
    
    def __init__(self):
        self.feeds = [
            'https://rss.cnn.com/rss/money_news_international.rss',
            'https://feeds.reuters.com/reuters/businessNews',
            'https://www.bloomberg.com/feeds/podcasts/etf_report.xml'
        ]
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    
    async def coletar_noticias(self, limit: int = 50) -> List[Dict]:
        """Coleta notícias de múltiplos feeds"""
        todas_noticias = []
        
        for feed_url in self.feeds:
            try:
                noticias = await self._parse_feed(feed_url)
                todas_noticias.extend(noticias)
            except Exception as e:
                logger.error(f"Erro ao processar feed {feed_url}: {e}")
        
        return todas_noticias[:limit]
    
    async def _parse_feed(self, feed_url: str) -> List[Dict]:
        """Processa um feed RSS individual"""
        loop = asyncio.get_event_loop()
        
        def parse():
            feed = feedparser.parse(feed_url)
            noticias = []
            
            for entry in feed.entries[:20]:  # Limitar por feed
                noticia = {
                    'titulo': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'resumo': entry.get('summary', ''),
                    'data': entry.get('published', ''),
                    'fonte': feed_url,
                    'imagem': self._extrair_imagem(entry)
                }
                noticias.append(noticia)
            
            return noticias
        
        return await loop.run_in_executor(None, parse)
    
    def _extrair_imagem(self, entry) -> str:
        """Extrai URL da imagem da notícia"""
        if 'media_thumbnail' in entry:
            return entry.media_thumbnail[0]['url']
        elif 'links' in entry:
            for link in entry.links:
                if link.get('type', '').startswith('image/'):
                    return link.href
        return ''

class AnalisadorTecnicoAvancado:
    """Análise técnica com múltiplos indicadores"""
    
    @staticmethod
    def calcular_media_movel(dados: Dict, periodo: int = 20, coluna: str = '4. close') -> pd.Series:
        """Calcula média móvel simples"""
        try:
            df = pd.DataFrame(dados['Time Series (Daily)']).T
            df = df.apply(pd.to_numeric, errors='coerce')
            
            if coluna not in df.columns:
                coluna = df.columns[0]  # Usar primeira coluna disponível
            
            df['SMA'] = df[coluna].rolling(window=periodo).mean()
            return df['SMA']
        except Exception as e:
            logger.error(f"Erro ao calcular SMA: {e}")
            return pd.Series()
    
    @staticmethod
    def calcular_rsi(dados: Dict, periodo: int = 14) -> pd.Series:
        """Calcula RSI (Relative Strength Index)"""
        try:
            df = pd.DataFrame(dados['Time Series (Daily)']).T
            df = df.apply(pd.to_numeric, errors='coerce')
            
            # Usar adjusted close ou close
            price_col = '5. adjusted close' if '5. adjusted close' in df.columns else '4. close'
            prices = df[price_col]
            
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi
        except Exception as e:
            logger.error(f"Erro ao calcular RSI: {e}")
            return pd.Series()
    
    @staticmethod
    def calcular_macd(dados: Dict) -> pd.DataFrame:
        """Calcula MACD"""
        try:
            df = pd.DataFrame(dados['Time Series (Daily)']).T
            df = df.apply(pd.to_numeric, errors='coerce')
            
            price_col = '5. adjusted close' if '5. adjusted close' in df.columns else '4. close'
            prices = df[price_col]
            
            ema_12 = prices.ewm(span=12, adjust=False).mean()
            ema_26 = prices.ewm(span=26, adjust=False).mean()
            
            df['MACD'] = ema_12 - ema_26
            df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
            
            return df[['MACD', 'MACD_Signal', 'MACD_Histogram']]
        except Exception as e:
            logger.error(f"Erro ao calcular MACD: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def calcular_bb(dados: Dict, periodo: int = 20, desvios: int = 2) -> pd.DataFrame:
        """Calcula Bollinger Bands"""
        try:
            df = pd.DataFrame(dados['Time Series (Daily)']).T
            df = df.apply(pd.to_numeric, errors='coerce')
            
            price_col = '5. adjusted close' if '5. adjusted close' in df.columns else '4. close'
            prices = df[price_col]
            
            sma = prices.rolling(window=periodo).mean()
            std = prices.rolling(window=periodo).std()
            
            df['BB_Upper'] = sma + (std * desvios)
            df['BB_Lower'] = sma - (std * desvios)
            df['BB_Middle'] = sma
            
            return df[['BB_Upper', 'BB_Middle', 'BB_Lower']]
        except Exception as e:
            logger.error(f"Erro ao calcular Bollinger Bands: {e}")
            return pd.DataFrame()

class MLNewsAnalyzer:
    """Analisador de notícias com machine learning"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.model = None
        self.is_trained = False
    
    def preparar_dados(self, noticias: List[Dict]) -> tuple:
        """Prepara dados para treinamento"""
        textos = [noticia['resumo'] for noticia in noticias if noticia.get('resumo')]
        
        if not textos:
            return None, None
        
        X = self.vectorizer.fit_transform(textos)
        return X, textos
    
    def treinar_modelo(self, X, y, test_size: float = 0.2):
        """Treina o modelo de rede neural"""
        if X is None or len(y) == 0:
            logger.warning("Dados insuficientes para treinamento")
            return
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        self.model = MLPClassifier(
            hidden_layer_sizes=(100, 50),
            max_iter=500,
            alpha=1e-4,
            solver='adam',
            verbose=False,
            random_state=42,
            learning_rate_init=0.001
        )
        
        self.model.fit(X_train, y_train)
        
        # Avaliar modelo
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        logger.info(f"Acurácia do modelo: {accuracy:.2f}")
        self.is_trained = True
    
    def prever_sentimento(self, noticias: List[Dict]) -> List[float]:
        """Prevê sentimento das notícias"""
        if not self.is_trained or not self.model:
            logger.warning("Modelo não treinado")
            return [0.5] * len(noticias)  # Retorno neutro
        
        textos = [noticia['resumo'] for noticia in noticias if noticia.get('resumo')]
        
        if not textos:
            return [0.5] * len(noticias)
        
        X = self.vectorizer.transform(textos)
        probabilidades = self.model.predict_proba(X)
        
        # Retornar probabilidade da classe positiva
        return probabilidades[:, 1] if probabilidades.shape[1] > 1 else probabilidades.flatten()

class GerenciadorRisco:
    """Gerenciamento avançado de risco"""
    
    def __init__(self, capital_total: float, risco_por_trade: float = 0.02):
        self.capital_total = capital_total
        self.risco_por_trade = risco_por_trade
        self.historico_trades = []
    
    def calcular_tamanho_posicao(self, preco_entrada: float, preco_stop: float) -> float:
        """Calcula tamanho da posição baseado no risco"""
        risco_por_unidade = abs(preco_entrada - preco_stop)
        
        if risco_por_unidade == 0:
            return 0
        
        risco_maximo = self.capital_total * self.risco_por_trade
        tamanho_posicao = risco_maximo / risco_por_unidade
        
        return min(tamanho_posicao, self.capital_total * 0.1)  # Limitar a 10% do capital
    
    def atualizar_historico(self, trade: Dict):
        """Atualiza histórico de trades"""
        self.historico_trades.append({
            **trade,
            'timestamp': datetime.now()
        })
        
        # Manter apenas últimos 1000 trades
        if len(self.historico_trades) > 1000:
            self.historico_trades.pop(0)
    
    def calcular_metricas_risco(self) -> Dict:
        """Calcula métricas de risco"""
        if not self.historico_trades:
            return {}
        
        df = pd.DataFrame(self.historico_trades)
        
        retornos = df['resultado'] / self.capital_total
        drawdown = self._calcular_max_drawdown(retornos)
        
        return {
            'sharpe_ratio': self._calcular_sharpe_ratio(retornos),
            'max_drawdown': drawdown,
            'win_rate': len(df[df['resultado'] > 0]) / len(df),
            'expectancy': df['resultado'].mean(),
            'volatilidade': retornos.std()
        }
    
    def _calcular_max_drawdown(self, retornos: pd.Series) -> float:
        """Calcula máximo drawdown"""
        cumulative = (1 + retornos).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return drawdown.min()
    
    def _calcular_sharpe_ratio(self, retornos: pd.Series) -> float:
        """Calcula Sharpe Ratio"""
        if len(retornos) < 2 or retornos.std() == 0:
            return 0
        return (retornos.mean() * 252) / (retornos.std() * np.sqrt(252))

class ExecutorTrade:
    """Executor otimizado de trades"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.gerenciador_risco = GerenciadorRisco(
            capital_total=config.get('capital_total', 10000),
            risco_por_trade=config.get('risco_por_trade', 0.02)
        )
    
    async def executar_trade(self, acao: str, quantidade: float, tipo: str, preco: float = None) -> Dict:
        """Executa um trade de forma otimizada"""
        try:
            # Simular execução (substituir por API real)
            logger.info(f"Executando {tipo} de {quantidade} ações de {acao}")
            
            trade_id = f"TRADE_{int(time.time())}_{acao}"
            
            resultado = {
                'id': trade_id,
                'acao': acao,
                'quantidade': quantidade,
                'tipo': tipo,
                'preco': preco or self._obter_preco_atual(acao),
                'timestamp': datetime.now(),
                'status': 'executado'
            }
            
            # Registrar no gerenciador de risco
            self.gerenciador_risco.atualizar_historico(resultado)
            
            return resultado
            
        except Exception as e:
            logger.error(f"Erro ao executar trade: {e}")
            return {
                'status': 'erro',
                'erro': str(e)
            }
    
    def _obter_preco_atual(self, acao: str) -> float:
        """Obtém preço atual (simulado)"""
        # Em produção, buscar de API real
        return np.random.uniform(100, 500)

class SistemaNotificacao:
    """Sistema avançado de notificações"""
    
    def __init__(self, config_email: Dict = None):
        self.config_email = config_email or {}
        self.historico_notificacoes = []
    
    async def enviar_notificacao_email(self, destinatario: str, assunto: str, corpo: str) -> bool:
        """Envia notificação por email de forma assíncrona"""
        if not self.config_email:
            logger.warning("Configuração de email não definida")
            return False
        
        try:
            loop = asyncio.get_event_loop()
            
            def enviar_email():
                msg = MIMEMultipart()
                msg['From'] = self.config_email['remetente']
                msg['To'] = destinatario
                msg['Subject'] = assunto
                msg.attach(MIMEText(corpo, 'plain'))
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(self.config_email['remetente'], self.config_email['senha'])
                server.send_message(msg)
                server.quit()
                return True
            
            success = await loop.run_in_executor(None, enviar_email)
            
            if success:
                logger.info(f"Notificação enviada para {destinatario}")
                self._registrar_notificacao('email', assunto, success)
            
            return success
            
        except Exception as e:
            logger.error(f"Erro ao enviar email: {e}")
            self._registrar_notificacao('email', assunto, False, str(e))
            return False
    
    async def enviar_notificacao_webhook(self, webhook_url: str, dados: Dict) -> bool:
        """Envia notificação via webhook"""
        try:
            async with APIClient() as client:
                async with client.session.post(webhook_url, json=dados) as response:
                    success = response.status == 200
                    self._registrar_notificacao('webhook', webhook_url, success)
                    return success
        except Exception as e:
            logger.error(f"Erro ao enviar webhook: {e}")
            self._registrar_notificacao('webhook', webhook_url, False, str(e))
            return False
    
    def _registrar_notificacao(self, tipo: str, destino: str, sucesso: bool, erro: str = None):
        """Registra notificação no histórico"""
        self.historico_notificacoes.append({
            'tipo': tipo,
            'destino': destino,
            'sucesso': sucesso,
            'erro': erro,
            'timestamp': datetime.now()
        })

class OmegaTradingSystem:
    """Sistema principal de trading Omega"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.coletor_dados = ColetorDadosMercado(config.get('api_keys', {}))
        self.analisador_tecnico = AnalisadorTecnicoAvancado()
        self.analisador_noticias = MLNewsAnalyzer()
        self.executor_trade = ExecutorTrade(config)
        self.sistema_notificacao = SistemaNotificacao(config.get('email_config'))
        
        self.ativo = False
        self.historico_decisoes = []
        
        # Configurações
        self.symbols = config.get('symbols', ['AAPL', 'GOOGL', 'MSFT'])
        self.intervalo_analise = config.get('intervalo_analise', 60)  # segundos
    
    async def iniciar_sistema(self):
        """Inicia o sistema de trading"""
        logger.info("Iniciando Sistema Omega Trading...")
        self.ativo = True
        
        # Treinar modelo de notícias se necessário
        await self._treinar_modelo_noticias()
        
        # Iniciar loop principal
        while self.ativo:
            try:
                await self._ciclo_operacional()
                await asyncio.sleep(self.intervalo_analise)
            except Exception as e:
                logger.error(f"Erro no ciclo operacional: {e}")
                await asyncio.sleep(30)  # Esperar antes de retry
    
    async def parar_sistema(self):
        """Para o sistema de trading"""
        logger.info("Parando Sistema Omega Trading...")
        self.ativo = False
    
    async def _ciclo_operacional(self):
        """Executa um ciclo completo de operações"""
        inicio_ciclo = datetime.now()
        logger.info("Iniciando ciclo operacional...")
        
        try:
            # 1. Coletar dados de mercado
            dados_mercado = await self.coletor_dados.coletar_multiplas_acoes(self.symbols)
            
            # 2. Coletar notícias
            noticias = await self.coletor_dados.coletores['news'].coletar_noticias()
            
            # 3. Analisar dados técnicos
            analises_tecnicas = {}
            for symbol, dados in dados_mercado.items():
                if dados and 'Time Series (Daily)' in dados:
                    analises_tecnicas[symbol] = {
                        'sma_20': self.analisador_tecnico.calcular_media_movel(dados, 20),
                        'rsi': self.analisador_tecnico.calcular_rsi(dados),
                        'macd': self.analisador_tecnico.calcular_macd(dados)
                    }
            
            # 4. Analisar sentimento das notícias
            sentimentos = self.analisador_noticias.prever_sentimento(noticias)
            
            # 5. Tomar decisões de trading
            decisoes = await self._tomar_decisoes(dados_mercado, analises_tecnicas, sentimentos, noticias)
            
            # 6. Executar trades
            trades_executados = []
            for decisao in decisoes:
                if decisao['acao'] == 'comprar':
                    trade = await self.executor_trade.executar_trade(
                        decisao['symbol'],
                        decisao['quantidade'],
                        'compra',
                        decisao['preco']
                    )
                    trades_executados.append(trade)
            
            # 7. Registrar e notificar
            await self._processar_resultados_ciclo(decises, trades_executados, noticias)
            
            tempo_ciclo = (datetime.now() - inicio_ciclo).total_seconds()
            logger.info(f"Ciclo operacional concluído em {tempo_ciclo:.2f} segundos")
            
        except Exception as e:
            logger.error(f"Erro no ciclo operacional: {e}")
            raise
    
    async def _treinar_modelo_noticias(self):
        """Treina o modelo de análise de notícias"""
        try:
            # Coletar notícias para treinamento
            noticias = await self.coletor_dados.coletores['news'].coletar_noticias(limit=100)
            
            if len(noticias) < 20:
                logger.warning("Notícias insuficientes para treinamento")
                return
            
            # Gerar labels fictícios para demonstração
            # Em produção, usar dados históricos reais com sentimentos conhecidos
            X, textos = self.analisador_noticias.preparar_dados(noticias)
            
            if X is not None:
                y = np.random.randint(0, 2, len(textos))  # Labels binários fictícios
                self.analisador_noticias.treinar_modelo(X, y)
                logger.info("Modelo de notícias treinado com sucesso")
        
        except Exception as e:
            logger.error(f"Erro ao treinar modelo de notícias: {e}")
    
    async def _tomar_decisoes(self, dados_mercado: Dict, analises_tecnicas: Dict, 
                            sentimentos: List, noticias: List) -> List[Dict]:
        """Toma decisões de trading baseadas em múltiplos fatores"""
        decisoes = []
        
        for symbol, dados in dados_mercado.items():
            if not dados or 'Time Series (Daily)' not in dados:
                continue
            
            try:
                # Obter preço atual
                time_series = dados['Time Series (Daily)']
                ultima_data = sorted(time_series.keys())[-1]
                preco_atual = float(time_series[ultima_data]['4. close'])
                
                # Análise técnica
                analise = analises_tecnicas.get(symbol, {})
                sma_20 = analise.get('sma_20', pd.Series())
                rsi = analise.get('rsi', pd.Series())
                
                # Média de sentimentos das notícias relevantes
                sentimento_medio = np.mean(sentimentos) if sentimentos else 0.5
                
                # Lógica de decisão avançada
                if not sma_20.empty and not rsi.empty:
                    sma_recente = sma_20.iloc[-1] if not sma_20.empty else preco_atual
                    rsi_recente = rsi.iloc[-1] if not rsi.empty else 50
                    
                    # Critérios múltiplos para decisão
                    condicao_compra = (
                        preco_atual > sma_recente and  # Preço acima da média
                        rsi_recente < 70 and           # Não sobrecomprado
                        sentimento_medio > 0.6         # Sentimento positivo
                    )
                    
                    condicao_venda = (
                        preco_atual < sma_recente and  # Preço abaixo da média
                        rsi_recente > 30 and           # Não sobrevendido
                        sentimento_medio < 0.4         # Sentimento negativo
                    )
                    
                    if condicao_compra:
                        quantidade = self.executor_trade.gerenciador_risco.calcular_tamanho_posicao(
                            preco_atual, preco_atual * 0.95  # Stop de 5%
                        )
                        
                        decisoes.append({
                            'symbol': symbol,
                            'acao': 'comprar',
                            'quantidade': quantidade,
                            'preco': preco_atual,
                            'motivo': f'Preço acima SMA, RSI: {rsi_recente:.1f}, Sentimento: {sentimento_medio:.2f}'
                        })
                    
                    elif condicao_venda:
                        # Lógica para venda (implementar conforme necessidade)
                        pass
            
            except Exception as e:
                logger.error(f"Erro ao analisar {symbol}: {e}")
        
        return decisoes
    
    async def _processar_resultados_ciclo(self, decisoes: List, trades: List, noticias: List):
        """Processa resultados do ciclo e envia notificações"""
        # Registrar decisões
        for decisao in decisoes:
            self.historico_decisoes.append({
                **decisao,
                'timestamp': datetime.now()
            })
        
        # Enviar notificações se houver trades
        if trades and self.sistema_notificacao.config_email:
            for trade in trades:
                if trade['status'] == 'executado':
                    assunto = f"Trade Executado - {trade['acao']}"
                    corpo = f"""
                    Trade executado com sucesso:
                    - Ação: {trade['acao']}
                    - Quantidade: {trade['quantidade']}
                    - Preço: ${trade['preco']:.2f}
                    - ID: {trade['id']}
                    """
                    
                    await self.sistema_notificacao.enviar_notificacao_email(
                        self.config['email_config']['destinatario'],
                        assunto,
                        corpo
                    )
        
        # Log de resumo
        logger.info(f"Ciclo processado - Decisões: {len(decisoes)}, Trades: {len(trades)}")

# Exemplo de uso otimizado
async def main():
    """Função principal otimizada"""
    
    config = {
        'api_keys': {
            'alpha_vantage': 'SUA_CHAVE_ALPHA_VANTAGE',
            'binance': 'SUA_CHAVE_BINANCE'
        },
        'email_config': {
            'remetente': 'seu_email@gmail.com',
            'senha': 'sua_senha_app',
            'destinatario': 'destinatario@gmail.com'
        },
        'symbols': ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'],
        'capital_total': 10000,
        'risco_por_trade': 0.02,
        'intervalo_analise': 300  # 5 minutos
    }
    
    sistema = Lextrader-iag(config)
    
    try:
        # Executar por 30 minutos para demonstração
        await asyncio.wait_for(sistema.iniciar_sistema(), timeout=1800)
    except asyncio.TimeoutError:
        logger.info("Execução concluída (timeout)")
    except KeyboardInterrupt:
        logger.info("Sistema interrompido pelo usuário")
    finally:
        await sistema.parar_sistema()

if __name__ == "__main__":
    # Executar sistema
    asyncio.run(main())