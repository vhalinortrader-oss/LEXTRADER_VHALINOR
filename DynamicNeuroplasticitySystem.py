import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from enum import Enum
import time
from typing import List, Dict, Any
import random

# ==================== ENUMS ====================
class NeuronType(Enum):
    FAST_DECISION = "FAST_DECISION"
    PATTERN_RECOGNITION = "PATTERN_RECOGNITION"
    RISK_ASSESSMENT = "RISK_ASSESSMENT"
    OPTIMIZATION = "OPTIMIZATION"

class AutonomousAction(Enum):
    CREATE_NEURON = "CREATE_NEURON"
    PRUNE_NEURON = "PRUNE_NEURON"
    STRENGTHEN_CONNECTION = "STRENGTHEN_CONNECTION"
    OPTIMIZE_PATHWAY = "OPTIMIZE_PATHWAY"

class LearningMode(Enum):
    SUPERVISED = "SUPERVISED"
    REINFORCEMENT = "REINFORCEMENT"
    UNSUPERVISED = "UNSUPERVISED"
    TRANSFER = "TRANSFER"

# ==================== CLASSES DE DADOS ====================
class DynamicNeuron:
    def __init__(self, id: str, layer_id: str):
        self.id = id
        self.layer_id = layer_id
        self.created_at = datetime.now()
        self.synapses = random.randint(50, 300)
        self.activation_level = 60 + random.random() * 40
        self.learning_rate = 0.0001 + random.random() * 0.001
        self.efficiency = 70 + random.random() * 30
        self.decision_speed = 1 + random.random() * 20
        self.type = random.choice(list(NeuronType))
        self.is_active = random.random() > 0.2
        self.connections = []
        self.last_activated = datetime.now()
        self.energy_consumption = 0.1 + random.random() * 0.5
    
    def to_dict(self):
        return {
            'id': self.id,
            'layer_id': self.layer_id,
            'activation_level': self.activation_level,
            'efficiency': self.efficiency,
            'synapses': self.synapses,
            'type': self.type.value,
            'is_active': self.is_active,
            'energy_consumption': self.energy_consumption,
            'created_at': self.created_at.strftime("%H:%M:%S")
        }

class NeuralGrowth:
    def __init__(self, layer_id: str, layer_name: str):
        self.layer_id = layer_id
        self.layer_name = layer_name
        self.current_neurons = random.randint(500, 2500)
        self.max_capacity = self.current_neurons * 2
        self.growth_rate = 1 + random.random() * 4
        self.efficiency = 80 + random.random() * 20
        self.avg_decision_time = 3 + random.random() * 15
        self.new_neurons_created = random.randint(20, 100)
        self.pruning_rate = random.random() * 1.5
        self.learning_mode = random.choice(list(LearningMode))
        self.specialization = random.choice(["Visual", "Linguística", "Executiva", "Memória", "Sensorial"])
    
    def to_dict(self):
        return {
            'layer_id': self.layer_id,
            'layer_name': self.layer_name,
            'current_neurons': self.current_neurons,
            'max_capacity': self.max_capacity,
            'growth_rate': self.growth_rate,
            'efficiency': self.efficiency,
            'avg_decision_time': self.avg_decision_time,
            'new_neurons_created': self.new_neurons_created,
            'pruning_rate': self.pruning_rate,
            'learning_mode': self.learning_mode.value,
            'specialization': self.specialization
        }

class AutonomousDecision:
    def __init__(self):
        self.timestamp = datetime.now()
        self.action = random.choice(list(AutonomousAction))
        self.layer_affected = random.choice(['INPUT', 'PATTERN', 'DECISION', 'RISK'])
        self.reason = random.choice([
            'Otimização de latência detectada',
            'Redução de entropia sináptica',
            'Aumento de demanda computacional',
            'Padrão de uso identificado',
            'Otimização de consumo energético'
        ])
        self.impact = 5 + random.random() * 25
        self.decision_time_improvement = random.random() * 15
        self.confidence = 70 + random.random() * 30
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp.strftime("%H:%M:%S"),
            'action': self.action.value,
            'layer_affected': self.layer_affected,
            'reason': self.reason,
            'impact': self.impact,
            'decision_time_improvement': self.decision_time_improvement,
            'confidence': self.confidence
        }

class PerformanceMetrics:
    def __init__(self, timestamp: datetime):
        self.timestamp = timestamp
        self.timeLabel = timestamp.strftime("%H:%M")
        self.decision_speed = 80 + random.random() * 20
        self.accuracy = 85 + random.random() * 15
        self.efficiency = 75 + random.random() * 25
        self.energy_consumption = 50 + random.random() * 50
        self.memory_usage = 60 + random.random() * 40
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'timeLabel': self.timeLabel,
            'decision_speed': self.decision_speed,
            'accuracy': self.accuracy,
            'efficiency': self.efficiency,
            'energy_consumption': self.energy_consumption,
            'memory_usage': self.memory_usage
        }

# ==================== FUNÇÕES AUXILIARES ====================
def get_neuron_type_color(neuron_type: NeuronType) -> str:
    color_map = {
        NeuronType.FAST_DECISION: "#10b981",  # Green
        NeuronType.PATTERN_RECOGNITION: "#8b5cf6",  # Purple
        NeuronType.RISK_ASSESSMENT: "#ef4444",  # Red
        NeuronType.OPTIMIZATION: "#3b82f6"  # Blue
    }
    return color_map[neuron_type]

def get_action_color(action: AutonomousAction) -> Dict[str, str]:
    color_map = {
        AutonomousAction.CREATE_NEURON: {'text': 'green', 'bg': 'rgba(34, 197, 94, 0.1)', 'border': 'green'},
        AutonomousAction.PRUNE_NEURON: {'text': 'red', 'bg': 'rgba(239, 68, 68, 0.1)', 'border': 'red'},
        AutonomousAction.STRENGTHEN_CONNECTION: {'text': 'yellow', 'bg': 'rgba(234, 179, 8, 0.1)', 'border': 'yellow'},
        AutonomousAction.OPTIMIZE_PATHWAY: {'text': 'blue', 'bg': 'rgba(59, 130, 246, 0.1)', 'border': 'blue'}
    }
    return color_map.get(action, {'text': 'gray', 'bg': 'rgba(75, 85, 99, 0.1)', 'border': 'gray'})

# ==================== APLICAÇÃO STREAMLIT ====================
def main():
    # Configuração da página
    st.set_page_config(
        page_title="Neuroplasticidade Dinâmica",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Estilos CSS personalizados
    st.markdown("""
        <style>
        .main {
            background-color: #0a0a0a;
            color: #e5e5e5;
        }
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #111827 100%);
        }
        .metric-card {
            background-color: rgba(17, 24, 39, 0.7);
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 0.5rem;
            padding: 1rem;
            text-align: center;
        }
        .neuron-card {
            background-color: rgba(17, 24, 39, 0.7);
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 0.5rem;
            padding: 1rem;
            transition: all 0.3s ease;
        }
        .neuron-card:hover {
            border-color: rgba(16, 185, 129, 0.5);
            transform: translateY(-2px);
        }
        .decision-card {
            background-color: rgba(17, 24, 39, 0.7);
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 0.5rem;
        }
        .active-tab {
            background-color: rgba(34, 197, 94, 0.1);
            color: #4ade80;
            border-bottom: 2px solid #10b981;
        }
        .inactive-tab {
            color: #9ca3af;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Inicialização do estado da sessão
    if 'neurons' not in st.session_state:
        st.session_state.neurons = []
        for i in range(20):
            st.session_state.neurons.append(DynamicNeuron(f"neuron-{i}", f"layer-{i % 5}"))
    
    if 'neural_growth' not in st.session_state:
        layers = [
            ('input', 'Input Processing'),
            ('pattern', 'Pattern Rec.'),
            ('decision', 'Decision Engine'),
            ('risk', 'Risk Analysis'),
            ('exec', 'Execution Opt.')
        ]
        st.session_state.neural_growth = [NeuralGrowth(lid, lname) for lid, lname in layers]
    
    if 'autonomous_decisions' not in st.session_state:
        st.session_state.autonomous_decisions = [AutonomousDecision() for _ in range(10)]
    
    if 'performance_history' not in st.session_state:
        st.session_state.performance_history = []
        for i in range(20):
            timestamp = datetime.now() - timedelta(minutes=(20-i)*5)
            st.session_state.performance_history.append(PerformanceMetrics(timestamp))
    
    if 'global_decision_speed' not in st.session_state:
        st.session_state.global_decision_speed = 85.3
        st.session_state.neuroplasticity_index = 92.7
        st.session_state.total_neurons_created = 316
        st.session_state.total_energy_consumed = 1245.7
        st.session_state.learning_cycles = 42
        st.session_state.is_autonomous_mode = True
        st.session_state.active_tab = 'dashboard'
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <div style="padding: 0.5rem; background-color: rgba(34, 197, 94, 0.1); 
                         border-radius: 0.5rem; border: 1px solid rgba(34, 197, 94, 0.5);">
                    <span style="color: #10b981; font-size: 1.5rem;">🧠</span>
                </div>
                <div>
                    <h1 style="color: white; margin: 0; font-size: 1.5rem;">NEUROPLASTICIDADE DINÂMICA</h1>
                    <p style="color: #10b981; font-family: monospace; font-size: 0.8rem; margin: 0;">
                        REDE AUTÔNOMA • {'MODO AUTO' if st.session_state.is_autonomous_mode else 'MODO MANUAL'}
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        col2a, col2b = st.columns(2)
        with col2a:
            if st.button("➕ Forçar Gênese", use_container_width=True):
                new_neuron = DynamicNeuron(f"MANUAL-{datetime.now().timestamp()}", "manual")
                st.session_state.neurons.insert(0, new_neuron)
                st.session_state.total_neurons_created += 1
                st.rerun()
        
        with col2b:
            auto_mode = st.session_state.is_autonomous_mode
            if st.button(f"{'⏸️' if auto_mode else '▶️'} {'AUTO ON' if auto_mode else 'AUTO OFF'}", 
                        use_container_width=True,
                        type="primary" if auto_mode else "secondary"):
                st.session_state.is_autonomous_mode = not auto_mode
                st.rerun()
    
    # Navegação por tabs
    tabs = st.columns(5)
    tab_names = ['Dashboard', 'Neurônios', 'Crescimento', 'Decisões IA', 'Performance']
    tab_ids = ['dashboard', 'neurons', 'growth', 'decisions', 'performance']
    
    for i, (tab, name, tab_id) in enumerate(zip(tabs, tab_names, tab_ids)):
        with tab:
            if st.button(name, use_container_width=True, 
                        type="primary" if st.session_state.active_tab == tab_id else "secondary"):
                st.session_state.active_tab = tab_id
                st.rerun()
    
    st.divider()
    
    # Conteúdo baseado na tab ativa
    if st.session_state.active_tab == 'dashboard':
        render_dashboard()
    elif st.session_state.active_tab == 'neurons':
        render_neurons_tab()
    elif st.session_state.active_tab == 'growth':
        render_growth_tab()
    elif st.session_state.active_tab == 'decisions':
        render_decisions_tab()
    elif st.session_state.active_tab == 'performance':
        render_performance_tab()
    
    # Simulação de atualização automática
    if st.session_state.is_autonomous_mode:
        time.sleep(2)
        perform_autonomous_updates()
        st.rerun()

def render_dashboard():
    """Renderiza o dashboard principal"""
    # Métricas principais
    metrics_data = [
        {"label": "Velocidade", "value": f"{st.session_state.global_decision_speed:.1f}%", "color": "yellow"},
        {"label": "Plasticidade", "value": f"{st.session_state.neuroplasticity_index:.1f}", "color": "purple"},
        {"label": "Neurônios", "value": str(len(st.session_state.neurons)), "color": "blue"},
        {"label": "Energia", "value": f"{st.session_state.total_energy_consumed:.0f}W", "color": "green"},
        {"label": "Ciclos", "value": str(st.session_state.learning_cycles), "color": "white"},
        {"label": "Eficiência", "value": "94.2%", "color": "red"}
    ]
    
    cols = st.columns(6)
    for i, col in enumerate(cols):
        with col:
            metric = metrics_data[i]
            color_map = {
                "yellow": "#fbbf24",
                "purple": "#8b5cf6",
                "blue": "#3b82f6",
                "green": "#10b981",
                "white": "#ffffff",
                "red": "#ef4444"
            }
            st.markdown(f"""
                <div class="metric-card">
                    <div style="color: {color_map[metric['color']]}; font-size: 1.5rem; margin-bottom: 0.5rem;">
                        {get_metric_icon(metric['label'])}
                    </div>
                    <div style="font-size: 0.7rem; color: #9ca3af; text-transform: uppercase;">
                        {metric['label']}
                    </div>
                    <div style="font-family: monospace; font-size: 1.2rem; font-weight: bold; 
                            color: {color_map[metric['color']]}; margin-top: 0.5rem;">
                        {metric['value']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Performance Temporal")
        performance_df = pd.DataFrame([p.to_dict() for p in st.session_state.performance_history])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=performance_df['timeLabel'],
            y=performance_df['decision_speed'],
            name='Velocidade',
            line=dict(color='#3b82f6', width=3),
            mode='lines'
        ))
        fig.add_trace(go.Scatter(
            x=performance_df['timeLabel'],
            y=performance_df['accuracy'],
            name='Acurácia',
            line=dict(color='#10b981', width=3),
            mode='lines'
        ))
        fig.add_trace(go.Scatter(
            x=performance_df['timeLabel'],
            y=performance_df['efficiency'],
            name='Eficiência',
            line=dict(color='#8b5cf6', width=3),
            mode='lines'
        ))
        
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            margin=dict(l=0, r=0, t=30, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🌐 Distribuição Neural")
        growth_df = pd.DataFrame([g.to_dict() for g in st.session_state.neural_growth])
        
        colors = ['#3b82f6', '#10b981', '#8b5cf6', '#ef4444', '#f59e0b']
        
        fig = go.Figure(data=[
            go.Bar(
                x=growth_df['current_neurons'],
                y=growth_df['layer_id'],
                orientation='h',
                marker_color=colors,
                text=growth_df['current_neurons'],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            margin=dict(l=0, r=0, t=30, b=0),
            yaxis_title="Camada",
            xaxis_title="Neurônios"
        )
        st.plotly_chart(fig, use_container_width=True)

def render_neurons_tab():
    """Renderiza a tab de neurônios"""
    st.subheader("🧠 Neurônios Ativos")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_type = st.selectbox("Tipo de Neurônio", ["Todos"] + [t.value for t in NeuronType])
    with col2:
        filter_status = st.selectbox("Status", ["Todos", "Ativos", "Latentes"])
    with col3:
        filter_layer = st.selectbox("Camada", ["Todas"] + list(set(n.layer_id for n in st.session_state.neurons)))
    
    # Filtrar neurônios
    filtered_neurons = st.session_state.neurons
    if filter_type != "Todos":
        filtered_neurons = [n for n in filtered_neurons if n.type.value == filter_type]
    if filter_status == "Ativos":
        filtered_neurons = [n for n in filtered_neurons if n.is_active]
    elif filter_status == "Latentes":
        filtered_neurons = [n for n in filtered_neurons if not n.is_active]
    if filter_layer != "Todas":
        filtered_neurons = [n for n in filtered_neurons if n.layer_id == filter_layer]
    
    # Cards de neurônios
    cols = st.columns(3)
    for idx, neuron in enumerate(filtered_neurons[:12]):  # Limitar a 12 para performance
        with cols[idx % 3]:
            neuron_dict = neuron.to_dict()
            color = get_neuron_type_color(neuron.type)
            
            st.markdown(f"""
                <div class="neuron-card">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <div style="width: 8px; height: 8px; border-radius: 50%; background-color: {color};"></div>
                            <span style="font-size: 0.8rem; font-weight: bold; color: white;">
                                {neuron.type.value.replace('_', ' ')}
                            </span>
                        </div>
                        <span style="font-size: 0.7rem; padding: 0.2rem 0.5rem; border-radius: 0.25rem; 
                                border: 1px solid {'#10b981' if neuron.is_active else '#6b7280'}; 
                                color: {'#10b981' if neuron.is_active else '#9ca3af'};">
                            {'ATIVO' if neuron.is_active else 'LATENTE'}
                        </span>
                    </div>
                    
                    <div style="font-size: 0.7rem; font-family: monospace; color: #9ca3af;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                            <span>Ativação</span>
                            <div style="display: flex; align-items: center; gap: 0.5rem; width: 60%;">
                                <div style="flex: 1; background-color: #1f2937; height: 4px; border-radius: 2px; overflow: hidden;">
                                    <div style="height: 100%; background-color: {color}; width: {neuron.activation_level}%;"></div>
                                </div>
                                <span style="color: white;">{neuron.activation_level:.0f}%</span>
                            </div>
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                            <span>Eficiência</span>
                            <span style="color: #8b5cf6;">{neuron.efficiency:.1f}%</span>
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                            <span>Sinapses</span>
                            <span style="color: #fbbf24;">{neuron.synapses}</span>
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; padding-top: 0.5rem; border-top: 1px solid #374151;">
                            <span>Energia</span>
                            <span style="color: #10b981;">{neuron.energy_consumption:.2f}W</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

def render_growth_tab():
    """Renderiza a tab de crescimento neural"""
    st.subheader("📊 Crescimento por Camada")
    
    growth_df = pd.DataFrame([g.to_dict() for g in st.session_state.neural_growth])
    
    fig = go.Figure(data=[
        go.Bar(
            x=growth_df['layer_name'],
            y=growth_df['current_neurons'],
            name='Neurônios Atuais',
            marker_color='#10b981',
            text=growth_df['current_neurons'],
            textposition='auto'
        ),
        go.Bar(
            x=growth_df['layer_name'],
            y=growth_df['new_neurons_created'],
            name='Novos Neurônios',
            marker_color='#3b82f6',
            text=growth_df['new_neurons_created'],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        barmode='group',
        title="Crescimento Neural por Camada",
        xaxis_title="Camada",
        yaxis_title="Quantidade",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela detalhada
    st.subheader("📋 Detalhes por Camada")
    display_df = growth_df[['layer_name', 'current_neurons', 'growth_rate', 'efficiency', 
                           'avg_decision_time', 'learning_mode', 'specialization']]
    display_df.columns = ['Camada', 'Neurônios', 'Taxa Cresc.', 'Eficiência', 
                         'Tempo Decisão', 'Modo Aprend.', 'Especialização']
    
    st.dataframe(
        display_df,
        use_container_width=True,
        column_config={
            "Eficiência": st.column_config.ProgressColumn(
                format="%.1f%%",
                min_value=0,
                max_value=100
            ),
            "Taxa Cresc.": st.column_config.NumberColumn(
                format="%.2f%%"
            )
        }
    )

def render_decisions_tab():
    """Renderiza a tab de decisões autônomas"""
    st.subheader("🤖 Decisões Autônomas da IA")
    
    decisions = st.session_state.autonomous_decisions
    
    for decision in decisions[:10]:  # Mostrar apenas as 10 mais recentes
        decision_dict = decision.to_dict()
        colors = get_action_color(decision.action)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
                <div class="decision-card">
                    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                        <span style="font-size: 0.8rem; font-weight: bold; padding: 0.2rem 0.5rem; 
                                border-radius: 0.25rem; border: 1px solid {colors['border']}; 
                                color: {colors['text']}; background-color: {colors['bg']};">
                            {decision.action.value}
                        </span>
                        <span style="font-size: 0.7rem; font-family: monospace; color: #9ca3af;">
                            {decision_dict['timestamp']}
                        </span>
                    </div>
                    <p style="font-size: 0.8rem; color: #e5e5e5; margin: 0;">
                        {decision.reason}
                    </p>
                    <div style="font-size: 0.7rem; color: #9ca3af; margin-top: 0.5rem;">
                        Camada Afetada: {decision.layer_affected}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style="text-align: right;">
                    <div style="font-family: monospace; font-size: 1.2rem; font-weight: bold; color: #10b981;">
                        +{decision.impact:.1f}%
                    </div>
                    <div style="font-size: 0.7rem; color: #9ca3af; text-transform: uppercase;">
                        Impacto
                    </div>
                    <div style="font-size: 0.7rem; color: #3b82f6; margin-top: 0.5rem;">
                        Confiança: {decision.confidence:.0f}%
                    </div>
                </div>
            """, unsafe_allow_html=True)

def render_performance_tab():
    """Renderiza a tab de performance detalhada"""
    st.subheader("🔬 Análise de Performance Detalhada")
    
    performance_df = pd.DataFrame([p.to_dict() for p in st.session_state.performance_history])
    
    # Gráficos de métricas
    metrics = ['decision_speed', 'accuracy', 'efficiency', 'energy_consumption', 'memory_usage']
    metric_names = ['Velocidade', 'Acurácia', 'Eficiência', 'Consumo Energia', 'Uso Memória']
    colors = ['#3b82f6', '#10b981', '#8b5cf6', '#ef4444', '#f59e0b']
    
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=metric_names,
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    for i, (metric, name, color) in enumerate(zip(metrics, metric_names, colors)):
        row = i // 3 + 1
        col = i % 3 + 1
        
        fig.add_trace(
            go.Scatter(
                x=performance_df['timeLabel'],
                y=performance_df[metric],
                name=name,
                line=dict(color=color, width=2),
                mode='lines+markers',
                marker=dict(size=4)
            ),
            row=row, col=col
        )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=600,
        showlegend=False,
        title_text="Métricas de Performance ao Longo do Tempo"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Estatísticas
    st.subheader("📊 Estatísticas Consolidadas")
    
    stats_cols = st.columns(4)
    stats = [
        ("Média Velocidade", f"{performance_df['decision_speed'].mean():.1f}%"),
        ("Pico Eficiência", f"{performance_df['efficiency'].max():.1f}%"),
        ("Média Energia", f"{performance_df['energy_consumption'].mean():.1f}W"),
        ("Estabilidade", "94.7%")
    ]
    
    for col, (label, value) in zip(stats_cols, stats):
        with col:
            st.metric(label, value)

def get_metric_icon(metric_label: str) -> str:
    """Retorna ícone para métrica"""
    icons = {
        "Velocidade": "⚡",
        "Plasticidade": "🧠",
        "Neurônios": "🔗",
        "Energia": "🔋",
        "Ciclos": "🔄",
        "Eficiência": "🎯"
    }
    return icons.get(metric_label, "📊")

def perform_autonomous_updates():
    """Executa atualizações autônomas no sistema"""
    # Atualizar neurônios
    for neuron in st.session_state.neurons:
        neuron.activation_level = max(0, min(100, neuron.activation_level + (random.random() - 0.5) * 10))
        neuron.efficiency = max(50, min(100, neuron.efficiency + (random.random() - 0.4) * 2))
        neuron.is_active = random.random() > 0.1
    
    # Atualizar métricas globais
    st.session_state.global_decision_speed = min(99.9, st.session_state.global_decision_speed + (random.random() - 0.4))
    st.session_state.neuroplasticity_index = min(99.9, st.session_state.neuroplasticity_index + (random.random() - 0.45))
    st.session_state.total_energy_consumed += random.random() * 0.5
    st.session_state.learning_cycles += 1
    
    # Adicionar novo ponto de performance
    new_perf = PerformanceMetrics(datetime.now())
    st.session_state.performance_history.append(new_perf)
    if len(st.session_state.performance_history) > 50:  # Manter apenas últimos 50 pontos
        st.session_state.performance_history = st.session_state.performance_history[-50:]
    
    # Adicionar nova decisão autônoma ocasionalmente
    if random.random() > 0.7:
        new_decision = AutonomousDecision()
        st.session_state.autonomous_decisions.insert(0, new_decision)
        if len(st.session_state.autonomous_decisions) > 20:  # Manter apenas últimas 20 decisões
            st.session_state.autonomous_decisions = st.session_state.autonomous_decisions[:20]

if __name__ == "__main__":
    main()