import importlib
import logging
import time
from typing import Any, Dict, List, Optional, Tuple, Union
from functools import lru_cache
from decimal import Decimal, ROUND_DOWN

try:
    ccxt = importlib.import_module('ccxt')
    HAS_CCXT = True
except ImportError:
    ccxt = None
    HAS_CCXT = False

try:
    from ..config import keys
except ImportError:
    keys = None

# Configuração de logging
logger = logging.getLogger(__name__)

class ExchangeServiceError(Exception):
    """Exceção personalizada para erros do serviço de exchange"""
    pass

class OrderError(Exception):
    """Exceção personalizada para erros de ordens"""
    pass

class ExchangeService:
    """Serviço para operações com exchange"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._exchange = None
            self._initialized = True
    
    @property
    def exchange(self):
        """Getter para a instância da exchange com lazy loading"""
        if self._exchange is None:
            self._initialize_exchange()
        return self._exchange
    
    def _initialize_exchange(self) -> None:
        """Inicializa a conexão com a exchange"""
        if not HAS_CCXT:
            raise ExchangeServiceError("Biblioteca ccxt não instalada")
        
        api_key = getattr(keys, 'BINANCE_API_KEY', '') if keys else ''
        api_secret = getattr(keys, 'BINANCE_API_SECRET', '') if keys else ''
        
        if not api_key or not api_secret:
            logger.warning("Chaves API não encontradas, usando modo sandbox")
        
        try:
            self._exchange = ccxt.binance({
                'apiKey': api_key,
                'secret': api_secret,
                'enableRateLimit': True,
                'sandbox': not (api_key and api_secret),  # Modo sandbox se não houver chaves
                'options': {
                    'defaultType': 'spot',
                    'adjustForTimeDifference': True,
                }
            })
            
            # Carrega mercados uma vez
            self._exchange.load_markets()
            logger.info("Exchange Binance inicializada com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar exchange: {e}")
            raise ExchangeServiceError(f"Falha na inicialização da exchange: {e}")

# Instância global do serviço
_exchange_service = ExchangeService()

def get_exchange() -> Any:
    """Retorna a instância da exchange"""
    return _exchange_service.exchange

# =============================================================================
# FUNÇÕES DE MARKET DATA
# =============================================================================

def pegar_ohlcv(
    symbol: str = "BTC/USDT", 
    timeframe: str = "15m", 
    limit: int = 100
) -> List[List[float]]:
    """
    Busca dados OHLCV (Open, High, Low, Close, Volume)
    
    Args:
        symbol: Par de trading (ex: "BTC/USDT")
        timeframe: Timeframe dos candles (ex: "15m", "1h", "1d")
        limit: Número máximo de candles
    
    Returns:
        Lista de candles [[timestamp, open, high, low, close, volume], ...]
    
    Raises:
        ExchangeServiceError: Em caso de erro na requisição
    """
    try:
        exchange = get_exchange()
        logger.debug(f"Buscando OHLCV: {symbol}, {timeframe}, limit={limit}")
        
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        logger.info(f"OHLCV obtido: {symbol} - {len(ohlcv)} candles")
        
        return ohlcv
        
    except Exception as e:
        logger.error(f"Erro ao buscar OHLCV para {symbol}: {e}")
        raise ExchangeServiceError(f"Falha ao buscar dados OHLCV: {e}")

def obter_ticker(symbol: str = "BTC/USDT") -> Dict[str, Any]:
    """
    Obtém informações do ticker para um símbolo
    
    Args:
        symbol: Par de trading
    
    Returns:
        Dados do ticker
    """
    try:
        exchange = get_exchange()
        ticker = exchange.fetch_ticker(symbol)
        return ticker
    except Exception as e:
        logger.error(f"Erro ao obter ticker para {symbol}: {e}")
        raise ExchangeServiceError(f"Falha ao obter ticker: {e}")

def obter_preco_atual(symbol: str = "BTC/USDT") -> float:
    """
    Obtém o preço atual de um símbolo
    
    Args:
        symbol: Par de trading
    
    Returns:
        Preço atual
    """
    ticker = obter_ticker(symbol)
    return ticker['last']

def obter_livro_ordens(symbol: str = "BTC/USDT", limit: int = 20) -> Dict[str, Any]:
    """
    Obtém o livro de ordens (order book)
    
    Args:
        symbol: Par de trading
        limit: Número de níveis de preço
    
    Returns:
        Order book com bids e asks
    """
    try:
        exchange = get_exchange()
        orderbook = exchange.fetch_order_book(symbol, limit)
        return orderbook
    except Exception as e:
        logger.error(f"Erro ao obter order book para {symbol}: {e}")
        raise ExchangeServiceError(f"Falha ao obter order book: {e}")

# =============================================================================
# FUNÇÕES DE ORDENS
# =============================================================================

def enviar_ordem_market(
    symbol: str, 
    side: str, 
    amount: float,
    price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Envia ordem market para compra/venda
    
    Args:
        symbol: Par de trading (ex: "BTC/USDT")
        side: Direção da ordem ('buy' ou 'sell')
        amount: Quantidade a ser negociada
        price: Preço opcional para referência
    
    Returns:
        Dados da ordem executada
    
    Raises:
        ExchangeServiceError: Em caso de erro na ordem
        ValueError: Parâmetros inválidos
    """
    side_l = side.lower()
    if side_l not in ('buy', 'sell'):
        raise ValueError("Side deve ser 'buy' ou 'sell'")
    
    if amount <= 0:
        raise ValueError("Amount deve ser maior que zero")
    
    try:
        exchange = get_exchange()
        logger.info(f"Enviando ordem market: {side_l} {amount} {symbol}")
        
        # Verifica se o símbolo é válido
        market = exchange.market(symbol)
        if not market['active']:
            raise ExchangeServiceError(f"Market {symbol} não está ativo")
        
        # Ajusta amount para precision permitida
        amount = exchange.amount_to_precision(symbol, amount)
        
        order_params = {}
        if price:
            order_params['price'] = price
            
        ordem = exchange.create_market_order(symbol, side_l, amount, params=order_params)
        
        logger.info(f"Ordem executada: {ordem['id']} - {side_l} {amount} {symbol}")
        return ordem
        
    except Exception as e:
        logger.error(f"Erro ao enviar ordem market {side_l} {amount} {symbol}: {e}")
        raise ExchangeServiceError(f"Falha ao executar ordem: {e}")

def enviar_ordem_limit(
    symbol: str,
    side: str,
    amount: float,
    price: float,
    time_in_force: str = "GTC"
) -> Dict[str, Any]:
    """
    Envia ordem limitada
    
    Args:
        symbol: Par de trading
        side: 'buy' ou 'sell'
        amount: Quantidade
        price: Preço limite
        time_in_force: GTC, IOC, FOK
    
    Returns:
        Dados da ordem
    """
    side_l = side.lower()
    if side_l not in ('buy', 'sell'):
        raise ValueError("Side deve ser 'buy' ou 'sell'")
    
    if amount <= 0:
        raise ValueError("Amount deve ser maior que zero")
    
    if price <= 0:
        raise ValueError("Price deve ser maior que zero")
    
    try:
        exchange = get_exchange()
        logger.info(f"Enviando ordem limit: {side_l} {amount} {symbol} @ {price}")
        
        market = exchange.market(symbol)
        if not market['active']:
            raise ExchangeServiceError(f"Market {symbol} não está ativo")
        
        # Ajusta precision
        amount = exchange.amount_to_precision(symbol, amount)
        price = exchange.price_to_precision(symbol, price)
        
        params = {'timeInForce': time_in_force}
        ordem = exchange.create_limit_order(symbol, side_l, amount, price, params)
        
        logger.info(f"Ordem limit criada: {ordem['id']}")
        return ordem
        
    except Exception as e:
        logger.error(f"Erro ao enviar ordem limit {side_l} {amount} {symbol} @ {price}: {e}")
        raise ExchangeServiceError(f"Falha ao criar ordem limit: {e}")

def enviar_ordem_stop_loss(
    symbol: str,
    side: str,
    amount: float,
    stop_price: float,
    limit_price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Envia ordem stop-loss
    
    Args:
        symbol: Par de trading
        side: 'buy' ou 'sell'
        amount: Quantidade
        stop_price: Preço de ativação
        limit_price: Preço limite (opcional)
    
    Returns:
        Dados da ordem
    """
    try:
        exchange = get_exchange()
        logger.info(f"Enviando ordem stop-loss: {side} {amount} {symbol} @ {stop_price}")
        
        market = exchange.market(symbol)
        if not market['active']:
            raise ExchangeServiceError(f"Market {symbol} não está ativo")
        
        amount = exchange.amount_to_precision(symbol, amount)
        stop_price = exchange.price_to_precision(symbol, stop_price)
        
        params = {'stopPrice': stop_price}
        if limit_price:
            params['price'] = exchange.price_to_precision(symbol, limit_price)
            ordem = exchange.create_order(symbol, 'stop_loss_limit', side, amount, params.get('price'), params)
        else:
            ordem = exchange.create_order(symbol, 'stop_loss', side, amount, None, params)
        
        logger.info(f"Ordem stop-loss criada: {ordem['id']}")
        return ordem
        
    except Exception as e:
        logger.error(f"Erro ao enviar ordem stop-loss {side} {amount} {symbol}: {e}")
        raise ExchangeServiceError(f"Falha ao criar ordem stop-loss: {e}")

def cancelar_ordem(order_id: str, symbol: str) -> Dict[str, Any]:
    """
    Cancela uma ordem específica
    
    Args:
        order_id: ID da ordem
        symbol: Par de trading
    
    Returns:
        Resposta do cancelamento
    """
    try:
        exchange = get_exchange()
        resultado = exchange.cancel_order(order_id, symbol)
        logger.info(f"Ordem {order_id} cancelada")
        return resultado
    except Exception as e:
        logger.error(f"Erro ao cancelar ordem {order_id}: {e}")
        raise ExchangeServiceError(f"Falha ao cancelar ordem: {e}")

def cancelar_todas_ordens(symbol: str) -> List[Dict[str, Any]]:
    """
    Cancela todas as ordens abertas para um símbolo
    
    Args:
        symbol: Par de trading
    
    Returns:
        Lista de ordens canceladas
    """
    try:
        exchange = get_exchange()
        ordens_abertas = exchange.fetch_open_orders(symbol)
        resultados = []
        
        for ordem in ordens_abertas:
            resultado = exchange.cancel_order(ordem['id'], symbol)
            resultados.append(resultado)
            logger.info(f"Ordem {ordem['id']} cancelada")
        
        logger.info(f"Total de {len(resultados)} ordens canceladas para {symbol}")
        return resultados
    except Exception as e:
        logger.error(f"Erro ao cancelar todas as ordens para {symbol}: {e}")
        raise ExchangeServiceError(f"Falha ao cancelar ordens: {e}")

def obter_ordem(order_id: str, symbol: str) -> Dict[str, Any]:
    """
    Obtém informações de uma ordem específica
    
    Args:
        order_id: ID da ordem
        symbol: Par de trading
    
    Returns:
        Dados da ordem
    """
    try:
        exchange = get_exchange()
        ordem = exchange.fetch_order(order_id, symbol)
        return ordem
    except Exception as e:
        logger.error(f"Erro ao obter ordem {order_id}: {e}")
        raise ExchangeServiceError(f"Falha ao obter ordem: {e}")

def obter_ordens_abertas(symbol: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Obtém lista de ordens abertas
    
    Args:
        symbol: Par de trading (opcional)
    
    Returns:
        Lista de ordens abertas
    """
    try:
        exchange = get_exchange()
        if symbol:
            ordens = exchange.fetch_open_orders(symbol)
        else:
            ordens = exchange.fetch_open_orders()
        return ordens
    except Exception as e:
        logger.error(f"Erro ao obter ordens abertas: {e}")
        raise ExchangeServiceError(f"Falha ao obter ordens abertas: {e}")

def obter_historico_ordens(symbol: Optional[str] = None, since: Optional[int] = None, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Obtém histórico de ordens
    
    Args:
        symbol: Par de trading (opcional)
        since: Timestamp desde quando buscar
        limit: Número máximo de ordens
    
    Returns:
        Lista de ordens do histórico
    """
    try:
        exchange = get_exchange()
        ordens = exchange.fetch_orders(symbol, since, limit)
        return ordens
    except Exception as e:
        logger.error(f"Erro ao obter histórico de ordens: {e}")
        raise ExchangeServiceError(f"Falha ao obter histórico: {e}")

# =============================================================================
# FUNÇÕES DE CONTA E SALDO
# =============================================================================

def obter_saldo(moeda: str = "USDT") -> Dict[str, Any]:
    """
    Obtém saldo de uma moeda específica
    
    Args:
        moeda: Símbolo da moeda (ex: "USDT", "BTC")
    
    Returns:
        Dados do saldo
    """
    try:
        exchange = get_exchange()
        saldo = exchange.fetch_balance()
        return saldo.get(moeda, {})
    except Exception as e:
        logger.error(f"Erro ao obter saldo de {moeda}: {e}")
        raise ExchangeServiceError(f"Falha ao obter saldo: {e}")

def obter_saldo_total() -> Dict[str, Any]:
    """
    Obtém todos os saldos da conta
    
    Returns:
        Todos os saldos
    """
    try:
        exchange = get_exchange()
        saldo_total = exchange.fetch_balance()
        return saldo_total
    except Exception as e:
        logger.error(f"Erro ao obter saldo total: {e}")
        raise ExchangeServiceError(f"Falha ao obter saldo total: {e}")

def obter_saldo_livre(moeda: str) -> float:
    """
    Obtém saldo livre (disponível para trading) de uma moeda
    
    Args:
        moeda: Símbolo da moeda
    
    Returns:
        Saldo livre
    """
    saldo = obter_saldo(moeda)
    return saldo.get('free', 0.0)

# =============================================================================
# FUNÇÕES DE TRADING AVANÇADAS
# =============================================================================

def calcular_quantidade_por_percentual(
    symbol: str,
    side: str,
    percentual: float,
    preco_atual: Optional[float] = None
) -> float:
    """
    Calcula quantidade baseada em percentual do saldo
    
    Args:
        symbol: Par de trading
        side: 'buy' ou 'sell'
        percentual: Percentual do saldo a usar (0-100)
        preco_atual: Preço atual (opcional)
    
    Returns:
        Quantidade calculada
    """
    if percentual <= 0 or percentual > 100:
        raise ValueError("Percentual deve estar entre 0 e 100")
    
    exchange = get_exchange()
    
    if side.lower() == 'buy':
        # Para compra, usa a moeda quote (ex: USDT)
        moeda = symbol.split('/')[1]
        saldo_livre = obter_saldo_livre(moeda)
        if preco_atual is None:
            preco_atual = obter_preco_atual(symbol)
        
        valor_disponivel = saldo_livre * (percentual / 100)
        quantidade = valor_disponivel / preco_atual
        
    else:  # sell
        # Para venda, usa a moeda base (ex: BTC)
        moeda = symbol.split('/')[0]
        saldo_livre = obter_saldo_livre(moeda)
        quantidade = saldo_livre * (percentual / 100)
    
    # Ajusta para precision
    quantidade = exchange.amount_to_precision(symbol, quantidade)
    return float(quantidade)

def obter_info_symbol(symbol: str) -> Dict[str, Any]:
    """
    Obtém informações detalhadas sobre um símbolo
    
    Args:
        symbol: Par de trading
    
    Returns:
        Informações do mercado
    """
    try:
        exchange = get_exchange()
        market = exchange.market(symbol)
        return market
    except Exception as e:
        logger.error(f"Erro ao obter info do symbol {symbol}: {e}")
        raise ExchangeServiceError(f"Falha ao obter info do symbol: {e}")

def obter_precision_lote(symbol: str) -> Dict[str, int]:
    """
    Obtém precision de amount e price para um símbolo
    
    Args:
        symbol: Par de trading
    
    Returns:
        Dict com precision e limits
    """
    market = obter_info_symbol(symbol)
    return {
        'amount_precision': market['precision']['amount'],
        'price_precision': market['precision']['price'],
        'min_amount': market['limits']['amount']['min'],
        'min_cost': market['limits']['cost']['min']
    }

# =============================================================================
# FUNÇÕES DE UTILIDADE
# =============================================================================

def verificar_health() -> bool:
    """
    Verifica se o serviço da exchange está saudável
    
    Returns:
        True se saudável, False caso contrário
    """
    try:
        exchange = get_exchange()
        # Tenta buscar ticker para verificar conectividade
        exchange.fetch_ticker('BTC/USDT')
        return True
    except Exception as e:
        logger.warning(f"Health check falhou: {e}")
        return False

def aguardar_ordem_ser_preenchida(
    order_id: str,
    symbol: str,
    timeout: int = 60,
    check_interval: int = 2
) -> bool:
    """
    Aguarda até que uma ordem seja preenchida ou timeout
    
    Args:
        order_id: ID da ordem
        symbol: Par de trading
        timeout: Tempo máximo de espera em segundos
        check_interval: Intervalo entre verificações
    
    Returns:
        True se preenchida, False se timeout
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            ordem = obter_ordem(order_id, symbol)
            if ordem['status'] == 'closed':
                logger.info(f"Ordem {order_id} preenchida")
                return True
            elif ordem['status'] == 'canceled':
                logger.info(f"Ordem {order_id} cancelada")
                return False
            
            time.sleep(check_interval)
        except Exception as e:
            logger.warning(f"Erro ao verificar ordem {order_id}: {e}")
            time.sleep(check_interval)
    
    logger.warning(f"Timeout aguardando ordem {order_id}")
    return False

# =============================================================================
# ALIAS EM INGLÊS
# =============================================================================

# Market Data
def get_ohlcv(symbol: str = "BTC/USDT", timeframe: str = "15m", limit: int = 100) -> List[List[float]]:
    return pegar_ohlcv(symbol, timeframe, limit)

def get_ticker(symbol: str = "BTC/USDT") -> Dict[str, Any]:
    return obter_ticker(symbol)

def get_current_price(symbol: str = "BTC/USDT") -> float:
    return obter_preco_atual(symbol)

def get_order_book(symbol: str = "BTC/USDT", limit: int = 20) -> Dict[str, Any]:
    return obter_livro_ordens(symbol, limit)

# Orders
def send_market_order(symbol: str, side: str, amount: float, price: Optional[float] = None) -> Dict[str, Any]:
    return enviar_ordem_market(symbol, side, amount, price)

def send_limit_order(symbol: str, side: str, amount: float, price: float, time_in_force: str = "GTC") -> Dict[str, Any]:
    return enviar_ordem_limit(symbol, side, amount, price, time_in_force)

def send_stop_loss_order(symbol: str, side: str, amount: float, stop_price: float, limit_price: Optional[float] = None) -> Dict[str, Any]:
    return enviar_ordem_stop_loss(symbol, side, amount, stop_price, limit_price)

def cancel_order(order_id: str, symbol: str) -> Dict[str, Any]:
    return cancelar_ordem(order_id, symbol)

def cancel_all_orders(symbol: str) -> List[Dict[str, Any]]:
    return cancelar_todas_ordens(symbol)

def get_order(order_id: str, symbol: str) -> Dict[str, Any]:
    return obter_ordem(order_id, symbol)

def get_open_orders(symbol: Optional[str] = None) -> List[Dict[str, Any]]:
    return obter_ordens_abertas(symbol)

def get_order_history(symbol: Optional[str] = None, since: Optional[int] = None, limit: int = 50) -> List[Dict[str, Any]]:
    return obter_historico_ordens(symbol, since, limit)

# Account
def get_balance(currency: str = "USDT") -> Dict[str, Any]:
    return obter_saldo(currency)

def get_total_balance() -> Dict[str, Any]:
    return obter_saldo_total()

def get_free_balance(currency: str) -> float:
    return obter_saldo_livre(currency)

# Advanced Trading
def calculate_quantity_by_percentage(symbol: str, side: str, percentage: float, current_price: Optional[float] = None) -> float:
    return calcular_quantidade_por_percentual(symbol, side, percentage, current_price)

def get_symbol_info(symbol: str) -> Dict[str, Any]:
    return obter_info_symbol(symbol)

def get_lot_precision(symbol: str) -> Dict[str, int]:
    return obter_precision_lote(symbol)

# Utility
def wait_for_order_fill(order_id: str, symbol: str, timeout: int = 60, check_interval: int = 2) -> bool:
    return aguardar_ordem_ser_preenchida(order_id, symbol, timeout, check_interval)