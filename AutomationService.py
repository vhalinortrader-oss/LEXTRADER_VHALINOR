import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time
import uuid
from abc import ABC, abstractmethod

# --- TYPES ---
class TradingPlatform(str, Enum):
    BINANCE = "BINANCE"
    CTRADER = "CTRADER"
    OLYMPTRADE = "OLYMPTRADE"

class TradeType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class PositionType(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"

class PositionStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    PENDING = "PENDING"

class AlertType(str, Enum):
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    INFO = "INFO"

class MarketTrend(str, Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    SIDEWAYS = "SIDEWAYS"

@dataclass
class TradeSignal:
    type: TradeType
    confidence: float
    timestamp: datetime
    price: float
    platform: TradingPlatform
    symbol: str
    volume: float
    strategy: str
    take_profit: Optional[float] = None
    stop_loss: Optional[float] = None

@dataclass
class AutomationMarketData:
    symbol: str
    bid: float
    ask: float
    high: float
    low: float
    volume: float
    timestamp: datetime
    spread: float
    volatility: float
    trend: MarketTrend

@dataclass
class AutomationPosition:
    id: str
    platform: TradingPlatform
    symbol: str
    type: PositionType
    entry_price: float
    current_price: float
    volume: float
    take_profit: Optional[float]
    stop_loss: Optional[float]
    pnl: float
    pnl_percentage: float
    opened_at: datetime
    status: PositionStatus
    strategy: str

@dataclass
class AutomationAlert:
    id: str
    type: AlertType
    message: str
    priority: int  # 1-10, higher = more urgent
    action_required: bool
    timestamp: datetime

@dataclass
class AutomationMetrics:
    win_rate: float
    profit_loss: float
    total_trades: int
    successful_trades: int
    failed_trades: int
    max_drawdown: float
    sharpe_ratio: float
    average_profit: float
    average_loss: float
    profit_factor: float
    recovery_factor: float

# --- SIMULATED C-TRADER SERVICE ---
class CTraderService:
    """Serviço simulado para cTrader"""
    
    def __init__(self):
        self._connected = False
        self._api_key = ""
    
    async def connect(self, api_key: str) -> bool:
        """Simula conexão com cTrader"""
        print(f"[cTrader] Conectando com chave: {api_key}")
        await asyncio.sleep(1)
        self._connected = random.random() > 0.2  # 80% success rate
        self._api_key = api_key
        return self._connected
    
    def disconnect(self) -> None:
        """Desconecta do cTrader"""
        self._connected = False
        print("[cTrader] Desconectado")
    
    async def place_order(self, symbol: str, order_type: str, volume: float) -> Dict[str, Any]:
        """Simula colocação de ordem"""
        if not self._connected:
            raise ConnectionError("cTrader não conectado")
        
        await asyncio.sleep(0.5)
        
        # Simulate price
        base_prices = {
            "EURUSD": 1.08,
            "GBPUSD": 1.26,
            "USDJPY": 151.5,
            "XAUUSD": 2150.0
        }
        base_price = base_prices.get(symbol, 1.0)
        price = base_price * (1 + (random.random() - 0.5) * 0.001)
        
        return {
            "order_id": f"CT-{int(time.time())}-{random.randint(1000, 9999)}",
            "price": price,
            "status": "EXECUTED"
        }

# --- ADAPTADORES DE PLATAFORMA ---
class PlatformAdapter(ABC):
    """Interface base para adaptadores de plataforma"""
    
    @abstractmethod
    async def connect(self) -> None:
        """Conecta à plataforma"""
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Desconecta da plataforma"""
        pass
    
    @abstractmethod
    async def execute_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Executa uma ordem"""
        pass
    
    @abstractmethod
    async def get_market_data(self, symbol: str) -> AutomationMarketData:
        """Obtém dados de mercado"""
        pass
    
    @abstractmethod
    async def get_current_price(self, symbol: str) -> float:
        """Obtém preço atual"""
        pass
    
    @abstractmethod
    async def close_position(self, position_id: str) -> bool:
        """Fecha uma posição"""
        pass

class BinanceAdapter(PlatformAdapter):
    """Adaptador para Binance"""
    
    def __init__(self):
        self.api_key = "MOCK_BINANCE_KEY"  # Em produção, usar variáveis de ambiente
        self.ws_url = "wss://stream.binance.com:9443/ws"
        self._connected = False
    
    async def connect(self) -> None:
        """Simula conexão com Binance WebSocket"""
        print("[Binance] Simulando conexão com WebSocket...")
        await asyncio.sleep(1)
        self._connected = True
        print("[Binance] Conectado à Binance (Simulado)")
    
    async def disconnect(self) -> None:
        """Desconecta da Binance"""
        if self._connected:
            self._connected = False
            print("[Binance] Desconectado")
    
    async def execute_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Simula execução de ordem na Binance"""
        print(f"[Binance] Executando ordem: {order.get('type')} {order.get('symbol')}")
        await asyncio.sleep(0.3)
        
        return {
            "success": True,
            "order_id": f"BIN-{int(time.time())}",
            "message": "Order executed successfully"
        }
    
    async def get_market_data(self, symbol: str) -> AutomationMarketData:
        """Simula obtenção de dados de mercado da Binance"""
        base_price = 65000 + (random.random() - 0.5) * 2000
        spread = 1.0
        
        return AutomationMarketData(
            symbol=symbol,
            bid=base_price,
            ask=base_price + spread,
            high=base_price * 1.02,
            low=base_price * 0.98,
            volume=10000 + random.random() * 5000,
            timestamp=datetime.now(),
            spread=spread,
            volatility=0.02 + random.random() * 0.01,
            trend=random.choice([MarketTrend.BULLISH, MarketTrend.BEARISH])
        )
    
    async def get_current_price(self, symbol: str) -> float:
        """Obtém preço atual da Binance"""
        base_price = 65000  # BTC price
        return base_price + (random.random() - 0.5) * 100
    
    async def close_position(self, position_id: str) -> bool:
        """Fecha posição na Binance"""
        print(f"[Binance] Fechando posição: {position_id}")
        await asyncio.sleep(0.2)
        return True

class CTraderAdapter(PlatformAdapter):
    """Adaptador para cTrader"""
    
    def __init__(self):
        self.service = CTraderService()
        self._connected = False
    
    async def connect(self) -> None:
        """Conecta ao cTrader usando o serviço"""
        try:
            await self.service.connect("AUTO_BOT_KEY")
            self._connected = self.service._connected
            if self._connected:
                print("[cTrader] Conectado com sucesso")
            else:
                print("[cTrader] Falha na conexão")
        except Exception as e:
            print(f"[cTrader] Erro na conexão: {e}")
            self._connected = False
    
    async def disconnect(self) -> None:
        """Desconecta do cTrader"""
        self.service.disconnect()
        self._connected = False
        print("[cTrader] Desconectado")
    
    async def execute_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Executa ordem no cTrader"""
        try:
            result = await self.service.place_order(
                order.get("symbol", "EURUSD"),
                order.get("type", "BUY"),
                order.get("volume", 0.1)
            )
            return {
                "success": True,
                "order_id": result["order_id"],
                "message": f"Filled at {result['price']}"
            }
        except Exception as e:
            print(f"[cTrader] Falha na ordem: {e}")
            return {
                "success": False,
                "order_id": "",
                "message": "Execution Error"
            }
    
    async def get_market_data(self, symbol: str) -> AutomationMarketData:
        """Obtém dados de mercado do cTrader"""
        base_prices = {
            "EURUSD": 1.08,
            "GBPUSD": 1.26,
            "USDJPY": 151.5
        }
        base_price = base_prices.get(symbol, 1.08)
        spread = 0.0001
        
        return AutomationMarketData(
            symbol=symbol,
            bid=base_price,
            ask=base_price + spread,
            high=base_price * 1.002,
            low=base_price * 0.998,
            volume=5000 + random.random() * 2000,
            timestamp=datetime.now(),
            spread=spread,
            volatility=0.005 + random.random() * 0.002,
            trend=MarketTrend.SIDEWAYS
        )
    
    async def get_current_price(self, symbol: str) -> float:
        """Obtém preço atual do cTrader"""
        base_prices = {
            "EURUSD": 1.08,
            "GBPUSD": 1.26,
            "USDJPY": 151.5
        }
        base_price = base_prices.get(symbol, 1.08)
        return base_price + (random.random() - 0.5) * 0.001
    
    async def close_position(self, position_id: str) -> bool:
        """Fecha posição no cTrader"""
        print(f"[cTrader] Fechando posição: {position_id}")
        return True

class OlympTradeAdapter(PlatformAdapter):
    """Adaptador para OlympTrade"""
    
    def __init__(self):
        self._connected = False
    
    async def connect(self) -> None:
        """Simula conexão com OlympTrade"""
        print("[OlympTrade] Conectando...")
        await asyncio.sleep(0.8)
        self._connected = True
        print("[OlympTrade] Conectado (Simulado)")
    
    async def disconnect(self) -> None:
        """Desconecta da OlympTrade"""
        self._connected = False
        print("[OlympTrade] Desconectado")
    
    async def execute_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Simula execução de ordem na OlympTrade"""
        print(f"[OlympTrade] Executando ordem: {order.get('type')} {order.get('symbol')}")
        await asyncio.sleep(0.4)
        
        return {
            "success": True,
            "order_id": f"OLY-{int(time.time())}",
            "message": "Order placed successfully"
        }
    
    async def get_market_data(self, symbol: str) -> AutomationMarketData:
        """Simula obtenção de dados de mercado da OlympTrade"""
        base_price = 150.0  # Example for Brent
        spread = 0.1
        
        return AutomationMarketData(
            symbol=symbol,
            bid=base_price,
            ask=base_price + spread,
            high=base_price * 1.015,
            low=base_price * 0.985,
            volume=2000 + random.random() * 1000,
            timestamp=datetime.now(),
            spread=spread,
            volatility=0.03 + random.random() * 0.01,
            trend=MarketTrend.BEARISH
        )
    
    async def get_current_price(self, symbol: str) -> float:
        """Obtém preço atual da OlympTrade"""
        return 150.0 + (random.random() - 0.5) * 1.0
    
    async def close_position(self, position_id: str) -> bool:
        """Fecha posição na OlympTrade"""
        print(f"[OlympTrade] Fechando posição: {position_id}")
        return True

# ==================== GERENCIADOR E IA ====================

class MultiPlatformManager:
    """Gerenciador de múltiplas plataformas de trading"""
    
    def __init__(self):
        self.platforms: Dict[TradingPlatform, PlatformAdapter] = {
            TradingPlatform.BINANCE: BinanceAdapter(),
            TradingPlatform.CTRADER: CTraderAdapter(),
            TradingPlatform.OLYMPTRADE: OlympTradeAdapter()
        }
        self.active_connections: Set[TradingPlatform] = set()
        self.positions: Dict[str, AutomationPosition] = {}
        self.alerts: List[AutomationAlert] = []
        self.trade_history: List[TradeSignal] = []
        
        print("⚡ MultiPlatformManager inicializado")
    
    async def connect_all(self) -> None:
        """Conecta a todas as plataformas"""
        print("🌐 Conectando a todas as plataformas...")
        
        for platform, adapter in self.platforms.items():
            try:
                await adapter.connect()
                self.active_connections.add(platform)
                self.add_alert(
                    alert_type=AlertType.SUCCESS,
                    message=f"Conexão estabelecida com {platform.value}",
                    priority=1,
                    action_required=False
                )
                print(f"  ✓ Conectado a {platform.value}")
            except Exception as e:
                self.add_alert(
                    alert_type=AlertType.CRITICAL,
                    message=f"Falha na conexão com {platform.value}: {str(e)}",
                    priority=10,
                    action_required=True
                )
                print(f"  ✗ Falha na conexão com {platform.value}")
    
    async def disconnect_all(self) -> None:
        """Desconecta de todas as plataformas"""
        print("🔌 Desconectando de todas as plataformas...")
        
        for platform, adapter in self.platforms.items():
            try:
                await adapter.disconnect()
                self.active_connections.discard(platform)
                print(f"  ✓ Desconectado de {platform.value}")
            except Exception as e:
                print(f"  ✗ Erro ao desconectar de {platform.value}: {e}")
        
        self.active_connections.clear()
    
    async def execute_trade(self, signal: TradeSignal) -> bool:
        """Executa um trade baseado em um sinal"""
        adapter = self.platforms.get(signal.platform)
        if not adapter:
            print(f"❌ Plataforma {signal.platform} não encontrada")
            return False
        
        try:
            # Prepare order
            order = {
                "type": signal.type.value,
                "symbol": signal.symbol,
                "volume": signal.volume,
                "price": signal.price,
                "take_profit": signal.take_profit,
                "stop_loss": signal.stop_loss
            }
            
            # Execute order
            result = await adapter.execute_order(order)
            
            if result.get("success", False):
                # Create position
                position = AutomationPosition(
                    id=result["order_id"],
                    platform=signal.platform,
                    symbol=signal.symbol,
                    type=PositionType.LONG if signal.type == TradeType.BUY else PositionType.SHORT,
                    entry_price=signal.price,
                    current_price=signal.price,
                    volume=signal.volume,
                    take_profit=signal.take_profit,
                    stop_loss=signal.stop_loss,
                    pnl=0.0,
                    pnl_percentage=0.0,
                    opened_at=datetime.now(),
                    status=PositionStatus.OPEN,
                    strategy=signal.strategy
                )
                
                # Store position
                self.positions[result["order_id"]] = position
                self.trade_history.append(signal)
                
                # Add alert
                self.add_alert(
                    alert_type=AlertType.SUCCESS,
                    message=f"Ordem executada: {signal.type.value} {signal.symbol} na {signal.platform.value}",
                    priority=2,
                    action_required=False
                )
                
                print(f"✅ Ordem executada com sucesso: {result['order_id']}")
                return True
            else:
                error_msg = result.get("message", "Unknown error")
                self.add_alert(
                    alert_type=AlertType.CRITICAL,
                    message=f"Falha na execução: {error_msg}",
                    priority=5,
                    action_required=True
                )
                return False
                
        except Exception as e:
            print(f"❌ Erro na execução do trade: {e}")
            self.add_alert(
                alert_type=AlertType.CRITICAL,
                message=f"Erro na execução do trade: {str(e)}",
                priority=8,
                action_required=True
            )
            return False
    
    async def update_all_positions(self) -> None:
        """Atualiza todas as posições abertas"""
        for position_id, position in list(self.positions.items()):
            if position.status == PositionStatus.OPEN:
                adapter = self.platforms.get(position.platform)
                if adapter and position.platform in self.active_connections:
                    try:
                        # Get current price
                        current_price = await adapter.get_current_price(position.symbol)
                        position.current_price = current_price
                        
                        # Calculate P&L
                        if position.type == PositionType.LONG:
                            diff = current_price - position.entry_price
                        else:  # SHORT
                            diff = position.entry_price - current_price
                        
                        position.pnl = diff * position.volume
                        position.pnl_percentage = (diff / position.entry_price) * 100
                        
                        # Check stop loss / take profit
                        if position.stop_loss and position.take_profit:
                            if position.type == PositionType.LONG:
                                if current_price <= position.stop_loss or current_price >= position.take_profit:
                                    await self.close_position(position_id)
                            else:  # SHORT
                                if current_price >= position.stop_loss or current_price <= position.take_profit:
                                    await self.close_position(position_id)
                    
                    except Exception as e:
                        print(f"Erro ao atualizar posição {position_id}: {e}")
    
    async def close_position(self, position_id: str) -> bool:
        """Fecha uma posição específica"""
        position = self.positions.get(position_id)
        if not position:
            return False
        
        adapter = self.platforms.get(position.platform)
        if not adapter:
            return False
        
        try:
            success = await adapter.close_position(position_id)
            if success:
                position.status = PositionStatus.CLOSED
                position.current_price = await adapter.get_current_price(position.symbol)
                
                # Final P&L calculation
                if position.type == PositionType.LONG:
                    diff = position.current_price - position.entry_price
                else:
                    diff = position.entry_price - position.current_price
                
                position.pnl = diff * position.volume
                position.pnl_percentage = (diff / position.entry_price) * 100
                
                self.add_alert(
                    alert_type=AlertType.SUCCESS,
                    message=f"Posição {position_id} fechada. P&L: ${position.pnl:.2f} ({position.pnl_percentage:.2f}%)",
                    priority=3,
                    action_required=False
                )
                
                return True
        except Exception as e:
            print(f"Erro ao fechar posição {position_id}: {e}")
        
        return False
    
    def add_alert(self, alert_type: AlertType, message: str, priority: int, action_required: bool) -> None:
        """Adiciona um alerta ao sistema"""
        alert = AutomationAlert(
            id=f"alert_{int(time.time())}_{random.randint(1000, 9999)}",
            type=alert_type,
            message=message,
            priority=priority,
            action_required=action_required,
            timestamp=datetime.now()
        )
        
        self.alerts.insert(0, alert)
        if len(self.alerts) > 50:
            self.alerts.pop()
        
        # Print high priority alerts
        if priority >= 5:
            print(f"🚨 ALERTA ({alert_type.value}): {message}")
    
    def get_active_alerts(self) -> List[AutomationAlert]:
        """Retorna alertas ativos"""
        return self.alerts
    
    def get_open_positions(self) -> List[AutomationPosition]:
        """Retorna posições abertas"""
        return [p for p in self.positions.values() if p.status == PositionStatus.OPEN]
    
    def get_platform_status(self) -> Dict[TradingPlatform, bool]:
        """Retorna status das plataformas"""
        return {
            platform: platform in self.active_connections
            for platform in TradingPlatform
        }
    
    def get_trade_history(self, limit: int = 20) -> List[TradeSignal]:
        """Retorna histórico de trades"""
        return self.trade_history[:limit]
    
    def get_performance_metrics(self) -> AutomationMetrics:
        """Retorna métricas de performance (simuladas)"""
        return AutomationMetrics(
            win_rate=65.5,
            profit_loss=1250.40,
            total_trades=42,
            successful_trades=28,
            failed_trades=14,
            max_drawdown=4.2,
            sharpe_ratio=1.8,
            average_profit=80.0,
            average_loss=-45.0,
            profit_factor=1.7,
            recovery_factor=2.1
        )
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas para dashboard"""
        open_positions = self.get_open_positions()
        total_pnl = sum(p.pnl for p in open_positions)
        
        return {
            "connected_platforms": len(self.active_connections),
            "open_positions": len(open_positions),
            "total_pnl": total_pnl,
            "alerts_count": len(self.alerts),
            "trade_count": len(self.trade_history),
            "platform_status": {p.value: s for p, s in self.get_platform_status().items()}
        }

class AISupervisor:
    """Supervisor IA para tomada de decisões"""
    
    def __init__(self, manager: MultiPlatformManager):
        self.manager = manager
        print("🧠 AISupervisor inicializado")
    
    async def analyze_and_decide(self) -> List[TradeSignal]:
        """Analisa o mercado e toma decisões de trading"""
        signals: List[TradeSignal] = []
        
        # Simulação de análise IA (30% chance de sinal)
        if random.random() > 0.7:
            platforms = [
                TradingPlatform.BINANCE,
                TradingPlatform.CTRADER,
                TradingPlatform.OLYMPTRADE
            ]
            
            platform = random.choice(platforms)
            
            # Define symbols based on platform
            if platform == TradingPlatform.BINANCE:
                symbols = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
            elif platform == TradingPlatform.CTRADER:
                symbols = ["EURUSD", "GBPUSD", "USDJPY"]
            else:  # OLYMPTRADE
                symbols = ["BRENT", "GOLD", "SILVER"]
            
            symbol = random.choice(symbols)
            
            # Define base price
            base_prices = {
                "BTC/USDT": 65000,
                "ETH/USDT": 3500,
                "SOL/USDT": 150,
                "EURUSD": 1.08,
                "GBPUSD": 1.26,
                "USDJPY": 151.5,
                "BRENT": 85.0,
                "GOLD": 2150.0,
                "SILVER": 24.5
            }
            
            base_price = base_prices.get(symbol, 100)
            current_price = base_price * (1 + (random.random() - 0.5) * 0.02)
            
            signal = TradeSignal(
                type=random.choice([TradeType.BUY, TradeType.SELL]),
                confidence=0.85 + random.random() * 0.1,
                timestamp=datetime.now(),
                price=current_price,
                platform=platform,
                symbol=symbol,
                volume=random.uniform(0.01, 0.5),
                strategy="AI_HYBRID_SCALP",
                take_profit=current_price * (1.02 if random.random() > 0.5 else 0.98),
                stop_loss=current_price * (0.98 if random.random() > 0.5 else 1.02)
            )
            
            signals.append(signal)
            print(f"🧠 IA gerou sinal: {signal.type.value} {signal.symbol} a ${signal.price:.2f}")
        
        return signals
    
    async def monitor_and_adjust(self) -> None:
        """Monitora posições e ajusta estratégias"""
        open_positions = self.manager.get_open_positions()
        
        for position in open_positions:
            # Simulate AI monitoring logic
            if position.pnl_percentage < -3.0:  # Stop loss trigger
                print(f"🧠 IA detectou stop loss para posição {position.id}")
                # In real implementation, would trigger stop loss
            elif position.pnl_percentage > 2.0:  # Take profit suggestion
                print(f"🧠 IA sugere take profit para posição {position.id}")
                # In real implementation, could suggest partial close
    
    async def run_continuous_monitoring(self, interval_seconds: int = 5):
        """Executa monitoramento contínuo"""
        print(f"🔄 Iniciando monitoramento contínuo (intervalo: {interval_seconds}s)")
        
        try:
            while True:
                # Generate signals
                signals = await self.analyze_and_decide()
                
                # Execute signals
                for signal in signals:
                    await self.manager.execute_trade(signal)
                
                # Update positions
                await self.manager.update_all_positions()
                
                # Monitor and adjust
                await self.monitor_and_adjust()
                
                # Wait for next cycle
                await asyncio.sleep(interval_seconds)
                
        except asyncio.CancelledError:
            print("⏹️ Monitoramento interrompido")
        except Exception as e:
            print(f"❌ Erro no monitoramento: {e}")

# --- INSTÂNCIAS GLOBAIS ---
manager = MultiPlatformManager()
supervisor = AISupervisor(manager)

# --- INTERFACE STREAMLIT ---
def create_streamlit_interface():
    """Cria interface Streamlit para o sistema de automação"""
    import streamlit as st
    
    st.set_page_config(
        page_title="Sistema de Automação Multi-Plataforma",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Sistema de Automação Multi-Plataforma")
    st.markdown("---")
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Controles do Sistema")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔗 Conectar Tudo", use_container_width=True):
                asyncio.run(manager.connect_all())
                st.rerun()
        
        with col2:
            if st.button("🔌 Desconectar Tudo", use_container_width=True):
                asyncio.run(manager.disconnect_all())
                st.rerun()
        
        st.markdown("---")
        st.header("📊 Estatísticas Rápidas")
        
        stats = manager.get_dashboard_stats()
        for key, value in stats.items():
            if key == "platform_status":
                st.subheader("Status das Plataformas")
                for platform, status in value.items():
                    status_icon = "🟢" if status else "🔴"
                    st.markdown(f"{status_icon} {platform}")
            else:
                st.metric(
                    key.replace("_", " ").title(),
                    f"{value:.2f}" if isinstance(value, float) else value
                )
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Dashboard",
        "📈 Posições",
        "🚨 Alertas", 
        "📊 Performance"
    ])
    
    with tab1:
        st.header("📊 Dashboard em Tempo Real")
        
        # Platform status
        st.subheader("Status das Conexões")
        status_cols = st.columns(3)
        platform_status = manager.get_platform_status()
        
        for idx, (platform, is_connected) in enumerate(platform_status.items()):
            with status_cols[idx]:
                status_color = "green" if is_connected else "red"
                status_text = "🟢 CONECTADO" if is_connected else "🔴 DESCONECTADO"
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; border: 2px solid {status_color}; 
                            border-radius: 0.5rem; background: rgba({'0,255,0' if is_connected else '255,0,0'}, 0.1);">
                    <h3 style="margin: 0;">{platform.value}</h3>
                    <p style="font-size: 1.5rem; margin: 0.5rem 0;">{status_text}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Generate AI signal
        st.markdown("---")
        st.subheader("🧠 Decisões da IA")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("⚡ Gerar Sinal IA", type="primary"):
                signals = asyncio.run(supervisor.analyze_and_decide())
                if signals:
                    for signal in signals:
                        st.success(f"Sinal gerado: {signal.type.value} {signal.signal.symbol} a ${signal.price:.2f}")
                else:
                    st.info("Nenhum sinal gerado no momento")
        
        with col2:
            if st.button("🔄 Atualizar Posições"):
                asyncio.run(manager.update_all_positions())
                st.rerun()
    
    with tab2:
        st.header("📈 Posições Abertas")
        
        open_positions = manager.get_open_positions()
        
        if open_positions:
            for position in open_positions:
                with st.container():
                    pnl_color = "green" if position.pnl >= 0 else "red"
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.markdown(f"### {position.symbol}")
                        st.markdown(f"**Plataforma:** {position.platform.value}")
                        st.markdown(f"**Estratégia:** {position.strategy}")
                    
                    with col2:
                        st.metric("Preço Entrada", f"${position.entry_price:.2f}")
                        st.metric("Preço Atual", f"${position.current_price:.2f}")
                    
                    with col3:
                        st.metric("P&L", f"${position.pnl:.2f}", 
                                 delta=f"{position.pnl_percentage:.2f}%")
                        
                        if st.button(f"Fechar {position.id[:8]}...", key=f"close_{position.id}"):
                            success = asyncio.run(manager.close_position(position.id))
                            if success:
                                st.success("Posição fechada!")
                                st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("Nenhuma posição aberta no momento")
    
    with tab3:
        st.header("🚨 Alertas do Sistema")
        
        alerts = manager.get_active_alerts()
        
        if alerts:
            for alert in alerts[:20]:  # Show last 20 alerts
                alert_color = {
                    AlertType.SUCCESS: "green",
                    AlertType.WARNING: "orange",
                    AlertType.CRITICAL: "red",
                    AlertType.INFO: "blue"
                }.get(alert.type, "gray")
                
                st.markdown(f"""
                <div style="border-left: 4px solid {alert_color}; padding-left: 1rem; margin: 0.5rem 0;">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>{alert.type.value}</strong>
                        <small>{alert.timestamp.strftime('%H:%M:%S')}</small>
                    </div>
                    <div>{alert.message}</div>
                    {'<div style="color: red; font-weight: bold;">⚠️ Ação Requerida</div>' if alert.action_required else ''}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum alerta no momento")
    
    with tab4:
        st.header("📊 Métricas de Performance")
        
        metrics = manager.get_performance_metrics()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Taxa de Acerto", f"{metrics.win_rate:.1f}%")
            st.metric("Lucro/Prejuízo Total", f"${metrics.profit_loss:.2f}")
            st.metric("Total de Trades", metrics.total_trades)
            st.metric("Trades Bem Sucedidos", metrics.successful_trades)
            st.metric("Trades Falhos", metrics.failed_trades)
        
        with col2:
            st.metric("Max Drawdown", f"{metrics.max_drawdown:.1f}%")
            st.metric("Índice Sharpe", f"{metrics.sharpe_ratio:.2f}")
            st.metric("Lucro Médio", f"${metrics.average_profit:.2f}")
            st.metric("Prejuízo Médio", f"${metrics.average_loss:.2f}")
            st.metric("Fator de Lucro", f"{metrics.profit_factor:.2f}")
    
    # Auto-refresh
    time.sleep(2)
    st.rerun()

# --- EXEMPLO DE USO ---
async def example_usage():
    """Exemplo de uso do sistema de automação"""
    print("=== Exemplo de Uso do Sistema de Automação ===\n")
    
    # 1. Conectar a todas as plataformas
    print("1. Conectando a todas as plataformas...")
    await manager.connect_all()
    
    # 2. Verificar status
    print("\n2. Status das plataformas:")
    for platform, is_connected in manager.get_platform_status().items():
        print(f"   • {platform.value}: {'🟢 Conectado' if is_connected else '🔴 Desconectado'}")
    
    # 3. Gerar e executar sinal da IA
    print("\n3. Gerando sinal da IA...")
    signals = await supervisor.analyze_and_decide()
    
    if signals:
        print(f"   ✓ {len(signals)} sinal(is) gerado(s)")
        for signal in signals:
            print(f"   • {signal.type.value} {signal.symbol} a ${signal.price:.2f}")
            
            # Executar trade
            print(f"   Executando trade...")
            success = await manager.execute_trade(signal)
            print(f"   {'✅ Sucesso' if success else '❌ Falha'}")
    else:
        print("   ✓ Nenhum sinal no momento")
    
    # 4. Atualizar posições
    print("\n4. Atualizando posições...")
    await manager.update_all_positions()
    
    # 5. Mostrar posições abertas
    open_positions = manager.get_open_positions()
    print(f"\n5. Posições abertas: {len(open_positions)}")
    
    for position in open_positions:
        print(f"   • {position.symbol}: P&L ${position.pnl:.2f} ({position.pnl_percentage:.2f}%)")
    
    # 6. Mostrar alertas recentes
    alerts = manager.get_active_alerts()
    print(f"\n6. Alertas recentes: {len(alerts)}")
    
    for alert in alerts[:3]:
        print(f"   • [{alert.type.value}] {alert.message}")
    
    # 7. Desconectar
    print("\n7. Desconectando...")
    await manager.disconnect_all()
    
    print("\n✅ Exemplo concluído!")

if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())
    
    # To run Streamlit interface:
    # streamlit run automation_system.py
    # Uncomment the line below to run the Streamlit interface
    # create_streamlit_interface()