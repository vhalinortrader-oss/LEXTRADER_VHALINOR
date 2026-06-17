import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import random
from typing import List, Dict, Any, Optional
from enum import Enum

# Configuração da página
st.set_page_config(
    page_title="Scanner de Oportunidade Quântica",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Enums e Classes de Tipos
class TradingAction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    EXTREME = "EXTREME"

class TimeHorizon(str, Enum):
    INTRADAY = "INTRADAY"
    SHORT_TERM = "SHORT_TERM"
    MEDIUM_TERM = "MEDIUM_TERM"
    LONG_TERM = "LONG_TERM"

class QuantumMetrics:
    def __init__(self, entanglement: float, coherence: float, superposition: float):
        self.entanglement = entanglement
        self.coherence = coherence
        self.superposition = superposition

class TradingSignal:
    def __init__(self, symbol: str, action: TradingAction, confidence: float,
                 time_horizon: TimeHorizon, risk_level: RiskLevel,
                 quantum_metrics: Optional[QuantumMetrics] = None):
        self.symbol = symbol
        self.action = action
        self.confidence = confidence
        self.time_horizon = time_horizon
        self.risk_level = risk_level
        self.quantum_metrics = quantum_metrics
        self.timestamp = datetime.now()

# Gerar sinais de exemplo
def generate_sample_signals() -> List[TradingSignal]:
    symbols = ["BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD", "DOT/USD", 
               "BNB/USD", "XRP/USD", "DOGE/USD", "AVAX/USD", "MATIC/USD"]
    
    signals = []
    
    for symbol in symbols[:6]:  # Gerar 6 sinais
        action = random.choice([TradingAction.BUY, TradingAction.SELL])
        confidence = random.uniform(0.6, 0.95)
        time_horizon = random.choice(list(TimeHorizon))
        risk_level = random.choice(list(RiskLevel))
        
        quantum_metrics = QuantumMetrics(
            entanglement=random.uniform(0.5, 0.95),
            coherence=random.uniform(0.6, 0.99),
            superposition=random.uniform(0.4, 0.9)
        )
        
        signal = TradingSignal(
            symbol=symbol,
            action=action,
            confidence=confidence,
            time_horizon=time_horizon,
            risk_level=risk_level,
            quantum_metrics=quantum_metrics
        )
        
        signals.append(signal)
    
    # Ordenar por confiança (maior primeiro)
    signals.sort(key=lambda x: x.confidence, reverse=True)
    
    return signals

# Inicialização
if 'trading_signals' not in st.session_state:
    st.session_state.trading_signals = generate_sample_signals()

if 'last_scan' not in st.session_state:
    st.session_state.last_scan = datetime.now()

if 'scans_active' not in st.session_state:
    st.session_state.scans_active = 12

# CSS Customizado
st.markdown("""
<style>
    .stApp {
        background-color: #0a0a0a;
        color: #d1d5db;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .quantum-scanner {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 0.5rem;
        padding: 1rem;
        position: relative;
        overflow: hidden;
        height: 600px;
        display: flex;
        flex-direction: column;
    }
    
    .radio-icon {
        position: absolute;
        top: 1rem;
        right: 1rem;
        opacity: 0.1;
        font-size: 4rem;
        animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite;
    }
    
    @keyframes ping {
        75%, 100% {
            transform: scale(1.2);
            opacity: 0;
        }
    }
    
    .scanner-title {
        color: #d1d5db;
        font-size: 0.875rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        position: relative;
        z-index: 10;
    }
    
    .signal-card {
        background-color: rgba(0, 0, 0, 0.4);
        border: 1px solid #374151;
        border-radius: 0.375rem;
        padding: 0.75rem;
        margin-bottom: 0.75rem;
        transition: all 0.3s;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .signal-card:hover {
        border-color: rgba(14, 165, 233, 0.5);
        transform: translateY(-1px);
    }
    
    .signal-gradient {
        position: absolute;
        left: 0;
        top: 0;
        width: 0.25rem;
        height: 100%;
        background: linear-gradient(to bottom, transparent, #0ea5e9, transparent);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .signal-card:hover .signal-gradient {
        opacity: 1;
    }
    
    .signal-header {
        display: flex;
        justify-content: space-between;
        align-items: start;
        margin-bottom: 0.5rem;
    }
    
    .symbol-section {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .symbol-text {
        font-weight: bold;
        color: white;
        font-size: 0.875rem;
    }
    
    .action-badge {
        padding: 0.125rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.5625rem;
        font-weight: bold;
        text-transform: uppercase;
    }
    
    .action-buy {
        background-color: rgba(5, 150, 105, 0.5);
        color: #34d399;
    }
    
    .action-sell {
        background-color: rgba(220, 38, 38, 0.5);
        color: #f87171;
    }
    
    .time-horizon {
        color: #9ca3af;
        font-size: 0.625rem;
        font-family: monospace;
        margin-top: 0.125rem;
    }
    
    .confidence-section {
        text-align: right;
    }
    
    .confidence-value {
        font-size: 1.25rem;
        font-weight: bold;
        font-family: monospace;
        color: white;
    }
    
    .confidence-label {
        color: #9ca3af;
        font-size: 0.5625rem;
        text-transform: uppercase;
    }
    
    .signal-footer {
        display: flex;
        align-items: center;
        gap: 1rem;
        color: #9ca3af;
        font-size: 0.625rem;
        border-top: 1px solid #374151;
        padding-top: 0.5rem;
        margin-top: 0.5rem;
    }
    
    .metrics-item {
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .risk-high {
        color: #f87171;
    }
    
    .risk-extreme {
        color: #ef4444;
    }
    
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        color: #6b7280;
        gap: 0.75rem;
    }
    
    .pulse-icon {
        animation: pulse 1s ease-in-out infinite;
        opacity: 0.5;
        font-size: 2rem;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    .empty-text {
        text-align: center;
        font-size: 0.75rem;
        font-family: monospace;
        line-height: 1.2;
    }
    
    .scanner-footer {
        margin-top: auto;
        padding-top: 0.5rem;
        border-top: 1px solid #374151;
        color: #6b7280;
        font-size: 0.5625rem;
        font-family: monospace;
        display: flex;
        justify-content: space-between;
    }
    
    .live-indicator {
        color: #0ea5e9;
        animation: pulse 1s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

# Componente principal
def render_opportunity_scanner(signals: List[TradingSignal]):
    st.markdown("""
    <div class="quantum-scanner">
        <div class="radio-icon">📡</div>
        
        <div class="scanner-title">
            <span style="color: #0ea5e9;">🎯</span>
            SCANNER DE OPORTUNIDADE QUÂNTICA
        </div>
        
        <div style="flex: 1; overflow-y: auto; padding-right: 0.25rem; position: relative; z-index: 10;">
    """, unsafe_allow_html=True)
    
    if not signals:
        st.markdown("""
        <div class="empty-state">
            <div class="pulse-icon">⚛️</div>
            <div class="empty-text">
                ESCANEANDO MULTIVERSO...<br/>
                CALCULANDO PROBABILIDADES
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for signal in signals:
            # Determinar classes baseadas na ação
            action_class = "action-buy" if signal.action == TradingAction.BUY else "action-sell"
            action_text = "COMPRAR" if signal.action == TradingAction.BUY else "VENDER"
            
            # Determinar classe de risco
            risk_class = "risk-extreme" if signal.risk_level == RiskLevel.EXTREME else "risk-high"
            
            st.markdown(f"""
            <div class="signal-card">
                <div class="signal-gradient"></div>
                
                <div class="signal-header">
                    <div>
                        <div class="symbol-section">
                            <span class="symbol-text">{signal.symbol}</span>
                            <span class="action-badge {action_class}">{action_text}</span>
                        </div>
                        <div class="time-horizon">
                            Horizonte: {signal.time_horizon.value.replace('_', ' ')}
                        </div>
                    </div>
                    
                    <div class="confidence-section">
                        <div class="confidence-value">{(signal.confidence * 100):.0f}%</div>
                        <div class="confidence-label">Confiança</div>
                    </div>
                </div>
                
                <div class="signal-footer">
                    <div class="metrics-item">
                        <span>⚛️</span>
                        Emaranhamento: {signal.quantum_metrics.entanglement:.2f}
                    </div>
                    <div class="metrics-item {risk_class}">
                        <span>⚠️</span>
                        Risco: {signal.risk_level.value}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
        </div>
        
        <div class="scanner-footer">
            <span>SCANS ATIVOS: {scans_active}</span>
            <span class="live-indicator">AO VIVO</span>
        </div>
    </div>
    """.format(scans_active=st.session_state.scans_active), unsafe_allow_html=True)

# Barra lateral com controles
with st.sidebar:
    st.markdown("### ⚙️ Controles do Scanner")
    
    if st.button("🔄 Atualizar Sinais"):
        st.session_state.trading_signals = generate_sample_signals()
        st.session_state.last_scan = datetime.now()
        st.session_state.scans_active = random.randint(10, 15)
        st.success("Sinais atualizados!")
    
    if st.button("🎯 Focar em Alta Confiança"):
        # Filtrar sinais com alta confiança
        filtered_signals = [s for s in st.session_state.trading_signals if s.confidence > 0.8]
        if filtered_signals:
            st.session_state.trading_signals = filtered_signals
            st.success(f"{len(filtered_signals)} sinais de alta confiança!")
        else:
            st.warning("Nenhum sinal com confiança > 80%")
    
    st.markdown("---")
    st.markdown("### 📊 Filtros")
    
    # Filtro por ação
    action_filter = st.selectbox(
        "Ação",
        ["TODAS", "COMPRAR", "VENDER"],
        index=0
    )
    
    # Filtro por risco
    risk_filter = st.multiselect(
        "Nível de Risco",
        [r.value for r in RiskLevel],
        default=[r.value for r in RiskLevel]
    )
    
    # Slider de confiança mínima
    min_confidence = st.slider(
        "Confiança Mínima (%)",
        min_value=0,
        max_value=100,
        value=60
    )
    
    if st.button("🔍 Aplicar Filtros"):
        filtered_signals = st.session_state.trading_signals.copy()
        
        # Aplicar filtro de ação
        if action_filter != "TODAS":
            action_value = TradingAction.BUY if action_filter == "COMPRAR" else TradingAction.SELL
            filtered_signals = [s for s in filtered_signals if s.action == action_value]
        
        # Aplicar filtro de risco
        if risk_filter:
            filtered_signals = [s for s in filtered_signals if s.risk_level.value in risk_filter]
        
        # Aplicar filtro de confiança
        filtered_signals = [s for s in filtered_signals if s.confidence * 100 >= min_confidence]
        
        st.session_state.trading_signals = filtered_signals
        st.success(f"{len(filtered_signals)} sinais filtrados")
    
    st.markdown("---")
    st.markdown("### 📈 Estatísticas")
    
    total_signals = len(st.session_state.trading_signals)
    buy_signals = len([s for s in st.session_state.trading_signals if s.action == TradingAction.BUY])
    sell_signals = total_signals - buy_signals
    
    col_stats1, col_stats2 = st.columns(2)
    
    with col_stats1:
        st.metric("Total de Sinais", total_signals)
    
    with col_stats2:
        avg_confidence = np.mean([s.confidence * 100 for s in st.session_state.trading_signals]) if st.session_state.trading_signals else 0
        st.metric("Confiança Média", f"{avg_confidence:.1f}%")
    
    st.markdown(f"**Compra:** {buy_signals} | **Venda:** {sell_signals}")
    
    st.markdown(f"*Último scan:* {st.session_state.last_scan.strftime('%H:%M:%S')}")

# Renderizar o scanner
st.title("🎯 Scanner de Oportunidade Quântica")

# Atualização automática
auto_refresh = st.sidebar.checkbox("Atualização Automática", value=False)
refresh_interval = st.sidebar.slider("Intervalo (segundos)", 5, 60, 10)

# Renderizar o componente
render_opportunity_scanner(st.session_state.trading_signals)

# Botão para adicionar novo sinal (simulado)
if st.button("➕ Simular Novo Sinal", use_container_width=True):
    symbols = ["BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD", "DOT/USD", 
               "BNB/USD", "XRP/USD", "DOGE/USD", "AVAX/USD", "MATIC/USD"]
    
    new_symbol = random.choice([s for s in symbols if s not in [sig.symbol for sig in st.session_state.trading_signals]])
    
    if new_symbol:
        action = random.choice([TradingAction.BUY, TradingAction.SELL])
        confidence = random.uniform(0.7, 0.95)
        time_horizon = random.choice(list(TimeHorizon))
        risk_level = random.choice(list(RiskLevel))
        
        quantum_metrics = QuantumMetrics(
            entanglement=random.uniform(0.5, 0.95),
            coherence=random.uniform(0.6, 0.99),
            superposition=random.uniform(0.4, 0.9)
        )
        
        new_signal = TradingSignal(
            symbol=new_symbol,
            action=action,
            confidence=confidence,
            time_horizon=time_horizon,
            risk_level=risk_level,
            quantum_metrics=quantum_metrics
        )
        
        st.session_state.trading_signals.append(new_signal)
        st.session_state.trading_signals.sort(key=lambda x: x.confidence, reverse=True)
        st.rerun()
    else:
        st.warning("Todas as symbols já estão sendo monitoradas")

# Informações adicionais
st.markdown("---")
col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.markdown("**⚛️ Métricas Quânticas**")
    if st.session_state.trading_signals:
        avg_entanglement = np.mean([s.quantum_metrics.entanglement for s in st.session_state.trading_signals])
        st.metric("Emaranhamento Médio", f"{avg_entanglement:.2f}")

with col_info2:
    st.markdown("**📊 Distribuição de Risco**")
    if st.session_state.trading_signals:
        high_risk = len([s for s in st.session_state.trading_signals if s.risk_level in [RiskLevel.HIGH, RiskLevel.EXTREME]])
        st.metric("Alto Risco", high_risk)

with col_info3:
    st.markdown("**⏱️ Horizonte Temporal**")
    if st.session_state.trading_signals:
        intraday = len([s for s in st.session_state.trading_signals if s.time_horizon == TimeHorizon.INTRADAY])
        st.metric("Intraday", intraday)

# Atualização automática
if auto_refresh:
    time.sleep(refresh_interval)
    
    # Simular mudança aleatória nos sinais existentes
    for signal in st.session_state.trading_signals:
        if random.random() < 0.1:  # 10% de chance de mudança
            signal.confidence = max(0.1, min(0.99, signal.confidence + random.uniform(-0.05, 0.05)))
    
    # Ordenar novamente por confiança
    st.session_state.trading_signals.sort(key=lambda x: x.confidence, reverse=True)
    
    st.session_state.last_scan = datetime.now()
    st.rerun()