import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import time
import random

# Enums e tipos de dados
class TradeType(Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    BUY = "BUY"
    SELL = "SELL"

class AlertType(Enum):
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    SUCCESS = "SUCCESS"
    INFO = "INFO"

class TradingPlatform(Enum):
    BINANCE = "BINANCE"
    C_TRADER = "CTRADER"
    OLYMPTRADE = "OLYMPTRADE"
    METATRADER = "METATRADER"

@dataclass
class TradeSignal:
    symbol: str
    type: TradeType
    platform: TradingPlatform
    timestamp: datetime
    price: float
    volume: float = 1.0

@dataclass
class AutomationPosition:
    id: str
    symbol: str
    type: TradeType
    entry_price: float
    current_price: float
    pnl: float
    pnl_percentage: float
    platform: TradingPlatform
    opened_at: datetime
    size: float = 1.0

@dataclass
class AutomationAlert:
    id: str
    type: AlertType
    message: str
    timestamp: datetime
    platform: Optional[TradingPlatform] = None

@dataclass
class AutomationMetrics:
    profit_loss: float
    win_rate: float
    successful_trades: int
    failed_trades: int
    total_trades: int
    sharpe_ratio: float
    max_drawdown: float
    timestamp: datetime

# Serviço de Automação (simulado)
class AutomationManager:
    """Gerencia conexões e operações com plataformas de trading"""
    
    def __init__(self):
        self.connected_platforms: Dict[TradingPlatform, bool] = {}
        self.open_positions: List[AutomationPosition] = []
        self.trade_history: List[TradeSignal] = []
        self.active_alerts: List[AutomationAlert] = []
        self.performance_metrics: Optional[AutomationMetrics] = None
        
        # Inicializar métricas
        self.update_performance_metrics()
    
    async def connect_all(self) -> bool:
        """Conecta a todas as plataformas"""
        self.connected_platforms = {
            TradingPlatform.BINANCE: True,
            TradingPlatform.C_TRADER: True,
            TradingPlatform.OLYMPTRADE: True,
            TradingPlatform.METATRADER: True
        }
        
        # Adicionar alerta de conexão
        self.add_alert(
            AlertType.SUCCESS,
            "Todas as plataformas conectadas com sucesso"
        )
        
        return True
    
    async def disconnect_all(self) -> bool:
        """Desconecta de todas as plataformas"""
        self.connected_platforms = {
            platform: False 
            for platform in self.connected_platforms
        }
        
        self.add_alert(
            AlertType.INFO,
            "Todas as plataformas desconectadas"
        )
        
        return True
    
    async def update_all_positions(self):
        """Atualiza preços das posições abertas"""
        for position in self.open_positions:
            # Simular variação de preço
            variation = random.uniform(-0.05, 0.05)
            position.current_price = position.entry_price * (1 + variation)
            
            # Calcular P&L
            if position.type == TradeType.LONG:
                position.pnl = (position.current_price - position.entry_price) * position.size * 100
            else:  # SHORT
                position.pnl = (position.entry_price - position.current_price) * position.size * 100
            
            position.pnl_percentage = (position.pnl / (position.entry_price * position.size * 100)) * 100
    
    async def execute_trade(self, signal: TradeSignal) -> bool:
        """Executa uma operação de trading"""
        # Simular execução
        position = AutomationPosition(
            id=f"pos_{len(self.open_positions) + 1}_{int(time.time())}",
            symbol=signal.symbol,
            type=TradeType.LONG if signal.type == TradeType.BUY else TradeType.SHORT,
            entry_price=signal.price,
            current_price=signal.price,
            pnl=0.0,
            pnl_percentage=0.0,
            platform=signal.platform,
            opened_at=datetime.now()
        )
        
        self.open_positions.append(position)
        self.trade_history.append(signal)
        
        # Adicionar alerta
        self.add_alert(
            AlertType.SUCCESS,
            f"{signal.type.value} executado em {signal.symbol} via {signal.platform.value}"
        )
        
        # Atualizar métricas
        self.update_performance_metrics()
        
        return True
    
    def add_alert(self, alert_type: AlertType, message: str):
        """Adiciona um alerta ao sistema"""
        alert = AutomationAlert(
            id=f"alert_{int(time.time())}",
            type=alert_type,
            message=message,
            timestamp=datetime.now()
        )
        
        self.active_alerts.append(alert)
        
        # Manter apenas últimos 20 alertas
        if len(self.active_alerts) > 20:
            self.active_alerts = self.active_alerts[-20:]
    
    def get_open_positions(self) -> List[AutomationPosition]:
        """Retorna posições abertas"""
        return self.open_positions.copy()
    
    def get_active_alerts(self) -> List[AutomationAlert]:
        """Retorna alertas ativos"""
        return self.active_alerts.copy()
    
    def get_trade_history(self) -> List[TradeSignal]:
        """Retorna histórico de trades"""
        return self.trade_history.copy()
    
    def get_platform_status(self) -> Dict[TradingPlatform, bool]:
        """Retorna status das plataformas"""
        return self.connected_platforms.copy()
    
    def get_performance_metrics(self) -> Optional[AutomationMetrics]:
        """Retorna métricas de performance"""
        return self.performance_metrics
    
    def update_performance_metrics(self):
        """Atualiza métricas de performance"""
        total_trades = len(self.trade_history)
        successful_trades = len([t for t in self.trade_history 
                               if random.random() > 0.3])  # Simulação
        
        failed_trades = total_trades - successful_trades
        win_rate = (successful_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Calcular P&L total baseado nas posições abertas
        total_pnl = sum(pos.pnl for pos in self.open_positions)
        
        self.performance_metrics = AutomationMetrics(
            profit_loss=total_pnl,
            win_rate=win_rate,
            successful_trades=successful_trades,
            failed_trades=failed_trades,
            total_trades=total_trades,
            sharpe_ratio=random.uniform(0.5, 2.5),
            max_drawdown=random.uniform(0.1, 5.0),
            timestamp=datetime.now()
        )

class AutomationSupervisor:
    """Supervisiona análise e decisões de trading"""
    
    def __init__(self, manager: AutomationManager):
        self.manager = manager
    
    async def analyze_and_decide(self) -> List[TradeSignal]:
        """Analisa mercado e gera sinais de trading"""
        signals = []
        
        # Gerar sinais aleatórios para demonstração
        if random.random() > 0.5:  # 50% chance de sinal
            platforms = list(TradingPlatform)
            symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "ADAUSDT", "SOLUSDT"]
            
            num_signals = random.randint(1, 3)
            for _ in range(num_signals):
                signal = TradeSignal(
                    symbol=random.choice(symbols),
                    type=random.choice([TradeType.BUY, TradeType.SELL]),
                    platform=random.choice(platforms),
                    timestamp=datetime.now(),
                    price=random.uniform(100, 50000)
                )
                signals.append(signal)
        
        return signals

class AutomationService:
    """Serviço principal de automação"""
    
    def __init__(self):
        self.manager = AutomationManager()
        self.supervisor = AutomationSupervisor(self.manager)

# Configuração do Streamlit
st.set_page_config(
    page_title="Dashboard de Automação Multiplataforma",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background-color: #111827 !important;
        color: #d1d5db !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .automation-panel {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .automation-header {
        background: linear-gradient(90deg, #1e40af 0%, #1d4ed8 100%);
        border-bottom: 1px solid #3b82f6;
        padding: 16px 24px;
        border-radius: 12px 12px 0 0;
    }
    
    .status-indicator {
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        border: 1px solid;
    }
    
    .status-online {
        background-color: rgba(34, 197, 94, 0.2);
        border-color: rgba(34, 197, 94, 0.5);
        color: #4ade80;
    }
    
    .status-offline {
        background-color: rgba(239, 68, 68, 0.2);
        border-color: rgba(239, 68, 68, 0.5);
        color: #f87171;
    }
    
    .trading-active {
        background: linear-gradient(135deg, rgba(234, 179, 8, 0.3), rgba(234, 179, 8, 0.1));
        border: 1px solid rgba(234, 179, 8, 0.5);
        color: #fbbf24;
    }
    
    .trading-inactive {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.3), rgba(37, 99, 235, 0.1));
        border: 1px solid rgba(37, 99, 235, 0.5);
        color: #60a5fa;
    }
    
    .position-card {
        background-color: rgba(0, 0, 0, 0.4);
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 12px;
        transition: all 0.3s ease;
    }
    
    .position-card:hover {
        border-color: #3b82f6;
        transform: translateY(-2px);
    }
    
    .alert-critical {
        background-color: rgba(239, 68, 68, 0.2);
        border: 1px solid rgba(239, 68, 68, 0.5);
        color: #f87171;
    }
    
    .alert-success {
        background-color: rgba(34, 197, 94, 0.2);
        border: 1px solid rgba(34, 197, 94, 0.5);
        color: #4ade80;
    }
    
    .alert-warning {
        background-color: rgba(234, 179, 8, 0.2);
        border: 1px solid rgba(234, 179, 8, 0.5);
        color: #fbbf24;
    }
    
    .alert-info {
        background-color: rgba(96, 165, 250, 0.2);
        border: 1px solid rgba(96, 165, 250, 0.5);
        color: #93c5fd;
    }
    
    .platform-status {
        background-color: rgba(0, 0, 0, 0.4);
        border: 1px solid #374151;
        border-radius: 6px;
        padding: 12px;
        margin-bottom: 8px;
    }
    
    .metric-box {
        background-color: rgba(0, 0, 0, 0.4);
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    
    .metric-label {
        font-size: 10px;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .positive {
        color: #4ade80;
    }
    
    .negative {
        color: #f87171;
    }
    
    .neutral {
        color: #60a5fa;
    }
    
    h1, h2, h3, h4 {
        color: white !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .stButton > button {
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: bold !important;
        border: 1px solid !important;
    }
</style>
""", unsafe_allow_html=True)

class AutomationDashboard:
    """Dashboard de automação de trading"""
    
    def __init__(self):
        self.automation_service = AutomationService()
        self.is_connected = False
        self.is_trading_active = False
        
        # Inicializar estado da sessão
        if 'automation_data' not in st.session_state:
            st.session_state.automation_data = {
                'is_connected': False,
                'is_trading_active': False,
                'last_update': None,
                'positions': [],
                'alerts': [],
                'history': [],
                'platform_status': {},
                'metrics': None
            }
        
        # Inicializar intervalos
        if 'interval_running' not in st.session_state:
            st.session_state.interval_running = False
    
    async def connect_all(self):
        """Conecta a todas as plataformas"""
        success = await self.automation_service.manager.connect_all()
        if success:
            st.session_state.automation_data['is_connected'] = True
            self.is_connected = True
            await self.start_monitoring()
            st.rerun()
    
    async def disconnect_all(self):
        """Desconecta de todas as plataformas"""
        success = await self.automation_service.manager.disconnect_all()
        if success:
            st.session_state.automation_data['is_connected'] = False
            st.session_state.automation_data['is_trading_active'] = False
            self.is_connected = False
            self.is_trading_active = False
            st.session_state.interval_running = False
            st.rerun()
    
    async def start_monitoring(self):
        """Inicia monitoramento contínuo"""
        st.session_state.interval_running = True
    
    async def update_data(self):
        """Atualiza dados do dashboard"""
        if not st.session_state.automation_data['is_connected']:
            return
        
        # Atualizar posições
        await self.automation_service.manager.update_all_positions()
        
        # Se trading ativo, gerar e executar sinais
        if st.session_state.automation_data['is_trading_active']:
            signals = await self.automation_service.supervisor.analyze_and_decide()
            for signal in signals:
                await self.automation_service.manager.execute_trade(signal)
        
        # Atualizar estado da sessão
        st.session_state.automation_data['positions'] = self.automation_service.manager.get_open_positions()
        st.session_state.automation_data['alerts'] = self.automation_service.manager.get_active_alerts()
        st.session_state.automation_data['history'] = self.automation_service.manager.get_trade_history()
        st.session_state.automation_data['platform_status'] = self.automation_service.manager.get_platform_status()
        st.session_state.automation_data['metrics'] = self.automation_service.manager.get_performance_metrics()
        st.session_state.automation_data['last_update'] = datetime.now()
    
    def toggle_trading(self):
        """Alterna estado do trading"""
        st.session_state.automation_data['is_trading_active'] = not st.session_state.automation_data['is_trading_active']
        self.is_trading_active = st.session_state.automation_data['is_trading_active']
        
        # Adicionar alerta
        status = "ATIVADO" if self.is_trading_active else "DESATIVADO"
        self.automation_service.manager.add_alert(
            AlertType.INFO,
            f"Modo de Trading {status}"
        )
        st.rerun()
    
    def render_header(self):
        """Renderiza cabeçalho do dashboard"""
        is_connected = st.session_state.automation_data['is_connected']
        is_trading_active = st.session_state.automation_data['is_trading_active']
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            st.markdown("""
            <div class="automation-header">
                <h1 style="margin: 0; display: flex; align-items: center; gap: 12px;">
                    <span style="color: #60a5fa;">🌐</span>
                    AUTOMAÇÃO MULTIPLATAFORMA
                </h1>
                <div style="color: #60a5fa; font-size: 11px; font-family: 'JetBrains Mono', monospace; letter-spacing: 2px; margin-top: 4px;">
                    BINANCE • CTRADER • OLYMPTRADE • METATRADER
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            status_class = "status-online" if is_connected else "status-offline"
            status_text = "SISTEMA ONLINE" if is_connected else "OFFLINE"
            st.markdown(f"""
            <div class="status-indicator {status_class}">
                <span>{"🟢" if is_connected else "🔴"}</span>
                {status_text}
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            col3_1, col3_2 = st.columns(2)
            
            with col3_1:
                # Botão conectar/desconectar
                if is_connected:
                    if st.button("🔌 Desconectar", use_container_width=True):
                        asyncio.run(self.disconnect_all())
                else:
                    if st.button("🔗 Conectar", use_container_width=True):
                        asyncio.run(self.connect_all())
            
            with col3_2:
                # Botão iniciar/pausar trading
                trading_class = "trading-active" if is_trading_active else "trading-inactive"
                trading_text = "⏸️ Pausar IA" if is_trading_active else "▶️ Iniciar IA"
                trading_disabled = not is_connected
                
                if st.button(trading_text, 
                           disabled=trading_disabled,
                           use_container_width=True):
                    self.toggle_trading()
    
    def render_platform_status(self):
        """Renderiza status das plataformas"""
        st.markdown("""
        <div class="automation-panel">
            <h3 style="margin-top: 0; display: flex; align-items: center; gap: 8px;">
                <span style="color: #9ca3af;">🖥️</span>
                STATUS DAS PLATAFORMAS
            </h3>
        """, unsafe_allow_html=True)
        
        platform_status = st.session_state.automation_data['platform_status']
        
        if not platform_status:
            st.info("Nenhuma plataforma conectada.")
        else:
            for platform, status in platform_status.items():
                status_color = "🟢" if status else "🔴"
                status_text = "CONECTADO" if status else "DESCONECTADO"
                status_class = "positive" if status else "negative"
                
                st.markdown(f"""
                <div class="platform-status">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-family: 'JetBrains Mono', monospace; color: white;">
                            {platform.value}
                        </span>
                        <span class="{status_class}" style="font-size: 10px; font-weight: bold; padding: 2px 8px; border-radius: 12px; background-color: rgba(255,255,255,0.1);">
                            {status_color} {status_text}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def render_performance_metrics(self):
        """Renderiza métricas de performance"""
        st.markdown("""
        <div class="automation-panel">
            <h3 style="margin-top: 0; display: flex; align-items: center; gap: 8px;">
                <span style="color: #9ca3af;">⚡</span>
                PERFORMANCE
            </h3>
        """, unsafe_allow_html=True)
        
        metrics = st.session_state.automation_data['metrics']
        
        if not metrics:
            st.info("Sem dados de performance.")
        else:
            # Métricas principais
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="metric-box">
                    <div class="metric-label">Lucro Total</div>
                    <div class="metric-value {}">${:.2f}</div>
                </div>
                """.format(
                    "positive" if metrics.profit_loss >= 0 else "negative",
                    metrics.profit_loss
                ), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="metric-box">
                    <div class="metric-label">Win Rate</div>
                    <div class="metric-value neutral">{:.1f}%</div>
                </div>
                """.format(metrics.win_rate), unsafe_allow_html=True)
            
            # Gráfico de barras
            data = pd.DataFrame({
                'Resultado': ['Sucesso', 'Falha'],
                'Quantidade': [metrics.successful_trades, metrics.failed_trades]
            })
            
            fig = px.bar(
                data,
                x='Quantidade',
                y='Resultado',
                orientation='h',
                color='Resultado',
                color_discrete_map={'Sucesso': '#10b981', 'Falha': '#ef4444'}
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#d1d5db'),
                height=200,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def render_open_positions(self):
        """Renderiza posições abertas"""
        positions = st.session_state.automation_data['positions']
        
        st.markdown(f"""
        <div class="automation-panel" style="height: 400px; overflow-y: auto;">
            <h3 style="margin-top: 0; display: flex; align-items: center; gap: 8px;">
                <span style="color: #9ca3af;">📊</span>
                POSIÇÕES ABERTAS ({len(positions)})
            </h3>
        """, unsafe_allow_html=True)
        
        if not positions:
            st.markdown("""
            <div style="text-align: center; padding: 60px; border: 2px dashed #374151; border-radius: 8px; color: #6b7280;">
                Aguardando sinais de entrada...
            </div>
            """, unsafe_allow_html=True)
        else:
            for position in positions[-10:]:  # Mostrar apenas últimas 10
                pnl_class = "positive" if position.pnl >= 0 else "negative"
                type_class = "positive" if position.type == TradeType.LONG else "negative"
                type_text = "LONG" if position.type == TradeType.LONG else "SHORT"
                
                st.markdown(f"""
                <div class="position-card">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                        <div>
                            <span style="background-color: rgba(34, 197, 94, 0.2); color: #4ade80; font-size: 10px; padding: 2px 8px; border-radius: 12px; font-weight: bold; margin-right: 8px;">
                                {type_text}
                            </span>
                            <span style="font-weight: bold; color: white;">{position.symbol}</span>
                            <span style="font-size: 10px; color: #9ca3af; background-color: #374151; padding: 2px 6px; border-radius: 4px; margin-left: 8px;">
                                {position.platform.value}
                            </span>
                        </div>
                        <div style="text-align: right;">
                            <div class="metric-value {pnl_class}" style="font-size: 16px;">
                                {"+" if position.pnl >= 0 else ""}${position.pnl:.2f}
                            </div>
                            <div style="font-size: 10px; color: #9ca3af;">
                                {position.pnl_percentage:.2f}%
                            </div>
                        </div>
                    </div>
                    <div style="font-size: 10px; color: #6b7280;">
                        Entrada: ${position.entry_price:.4f} | Atual: ${position.current_price:.4f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def render_alerts(self):
        """Renderiza alertas do sistema"""
        alerts = st.session_state.automation_data['alerts']
        
        st.markdown("""
        <div class="automation-panel" style="height: 250px; overflow-y: auto;">
            <h3 style="margin-top: 0; display: flex; align-items: center; gap: 8px;">
                <span style="color: #9ca3af;">⚠️</span>
                ALERTAS DO SISTEMA
            </h3>
        """, unsafe_allow_html=True)
        
        if not alerts:
            st.info("Nenhum alerta no momento.")
        else:
            for alert in alerts[-10:]:  # Mostrar apenas últimos 10
                alert_class = f"alert-{alert.type.value.lower()}"
                
                st.markdown(f"""
                <div class="{alert_class}" style="padding: 8px; border-radius: 6px; margin-bottom: 8px; font-size: 11px; font-family: 'JetBrains Mono', monospace;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 4px; opacity: 0.7;">
                        <span>[{alert.type.value}]</span>
                        <span>{alert.timestamp.strftime('%H:%M:%S')}</span>
                    </div>
                    <div>{alert.message}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def render_trade_history(self):
        """Renderiza histórico de trades"""
        history = st.session_state.automation_data['history']
        
        st.markdown("""
        <div class="automation-panel" style="height: 250px; overflow-y: auto;">
            <h3 style="margin-top: 0; display: flex; align-items: center; gap: 8px;">
                <span style="color: #9ca3af;">📝</span>
                HISTÓRICO RECENTE
            </h3>
        """, unsafe_allow_html=True)
        
        if not history:
            st.info("Nenhum trade no histórico.")
        else:
            for trade in reversed(history[-20:]):  # Mostrar apenas últimos 20
                type_color = "#4ade80" if trade.type == TradeType.BUY else "#f87171"
                
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #374151; padding: 4px 0; font-size: 10px; font-family: 'JetBrains Mono', monospace; color: #9ca3af; hover:{{color: white}}">
                    <span>{trade.timestamp.strftime('%H:%M:%S')}</span>
                    <span style="color: {type_color};">{trade.type.value}</span>
                    <span>{trade.symbol}</span>
                    <span>{trade.platform.value}</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def run(self):
        """Executa o dashboard principal"""
        # Atualizar dados se monitoramento ativo
        if st.session_state.interval_running:
            asyncio.run(self.update_data())
        
        # Renderizar header
        self.render_header()
        
        # Layout principal
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Coluna esquerda: Status e Métricas
            self.render_platform_status()
            self.render_performance_metrics()
        
        with col2:
            # Coluna direita: Posições, Alertas e Histórico
            self.render_open_positions()
            
            col2_1, col2_2 = st.columns(2)
            
            with col2_1:
                self.render_alerts()
            
            with col2_2:
                self.render_trade_history()
        
        # Auto-refresh se conectado
        if st.session_state.automation_data['is_connected']:
            time.sleep(3)
            st.rerun()

# Função principal
def main():
    st.title("🤖 Dashboard de Automação de Trading")
    
    # Inicializar dashboard
    dashboard = AutomationDashboard()
    
    # Executar dashboard
    dashboard.run()

if __name__ == "__main__":
    main()