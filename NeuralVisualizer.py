import streamlit as st
import plotly.graph_objects as go
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple
import time
import random
from datetime import datetime
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Visualizador Neural Quântico",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Classes de dados
@dataclass
class NeuralNode:
    """Representa um nó neural na visualização"""
    x: float  # Posição X em porcentagem (0-100)
    y: float  # Posição Y em porcentagem (0-100)
    active: bool  # Estado de ativação
    layer: int  # Camada neural (0-4)
    activation_level: float  # Nível de ativação (0-1)
    last_activation: datetime = None
    connections: List[int] = None  # Índices dos nós conectados
    
    def __post_init__(self):
        if self.connections is None:
            self.connections = []
        if self.last_activation is None:
            self.last_activation = datetime.now()

@dataclass
class QuantumLayer:
    """Representa uma camada quântica"""
    name: str
    qubits: int
    coherence: float  # Coerência quântica (0-1)
    entanglement_level: float  # Nível de emaranhamento (0-1)

# Classe de visualização neural melhorada
class EnhancedNeuralVisualizer:
    def __init__(self, num_nodes: int = 50):
        self.num_nodes = num_nodes
        self.nodes: List[NeuralNode] = []
        self.quantum_layers: List[QuantumLayer] = []
        self.activation_history: List[float] = []
        self.coherence_history: List[float] = []
        self.initialize_nodes()
        self.initialize_quantum_layers()
    
    def initialize_nodes(self):
        """Inicializa os nós neurais com posições organizadas por camadas"""
        self.nodes = []
        
        # Definir camadas neurais (input, hidden1, hidden2, hidden3, output)
        layers = 5
        nodes_per_layer = self.num_nodes // layers
        
        for layer in range(layers):
            for i in range(nodes_per_layer):
                # Posição organizada por camadas
                x = 10 + layer * 20 + random.uniform(-5, 5)  # Dispersão horizontal
                y = 20 + (i / nodes_per_layer) * 60 + random.uniform(-8, 8)  # Dispersão vertical
                
                node = NeuralNode(
                    x=x,
                    y=y,
                    active=random.random() > 0.5,
                    layer=layer,
                    activation_level=random.uniform(0.3, 0.9) if random.random() > 0.5 else 0,
                    connections=[]
                )
                self.nodes.append(node)
        
        # Criar conexões entre camadas
        self.create_neural_connections()
    
    def create_neural_connections(self):
        """Cria conexões neurais entre camadas"""
        layers = 5
        nodes_per_layer = self.num_nodes // layers
        
        for layer in range(layers - 1):
            current_layer_nodes = range(layer * nodes_per_layer, (layer + 1) * nodes_per_layer)
            next_layer_nodes = range((layer + 1) * nodes_per_layer, (layer + 2) * nodes_per_layer)
            
            # Cada nó se conecta a 3-5 nós da próxima camada
            for node_idx in current_layer_nodes:
                num_connections = random.randint(3, 5)
                connections = random.sample(list(next_layer_nodes), min(num_connections, len(next_layer_nodes)))
                self.nodes[node_idx].connections = connections
    
    def initialize_quantum_layers(self):
        """Inicializa as camadas quânticas"""
        self.quantum_layers = [
            QuantumLayer("Qubit Encoding", 8, 0.95, 0.85),
            QuantumLayer("Entanglement", 12, 0.87, 0.92),
            QuantumLayer("Superposition", 10, 0.91, 0.88),
            QuantumLayer("Measurement", 6, 0.83, 0.75)
        ]
    
    def update_activation(self):
        """Atualiza o estado de ativação dos nós com padrão neural"""
        # Padrão de ativação em onda
        time_factor = time.time() * 2
        
        for i, node in enumerate(self.nodes):
            # Base aleatória com padrão periódico
            base_chance = 0.3
            layer_factor = 0.1 * node.layer
            time_pattern = np.sin(time_factor + i * 0.1) * 0.3 + 0.5
            
            activation_prob = base_chance + layer_factor + time_pattern
            activation_prob = max(0, min(1, activation_prob))
            
            node.active = random.random() < activation_prob
            
            if node.active:
                node.activation_level = random.uniform(0.6, 1.0)
                node.last_activation = datetime.now()
            else:
                node.activation_level = max(0, node.activation_level - 0.1)
    
    def update_quantum_metrics(self):
        """Atualiza métricas quânticas com variação realista"""
        for layer in self.quantum_layers:
            # Pequena variação nas métricas
            layer.coherence = max(0.7, min(0.99, layer.coherence + random.uniform(-0.02, 0.02)))
            layer.entanglement_level = max(0.6, min(0.98, layer.entanglement_level + random.uniform(-0.03, 0.03)))
        
        # Atualizar histórico
        avg_coherence = np.mean([layer.coherence for layer in self.quantum_layers])
        self.coherence_history.append(avg_coherence)
        if len(self.coherence_history) > 100:
            self.coherence_history.pop(0)
        
        avg_activation = np.mean([node.activation_level for node in self.nodes])
        self.activation_history.append(avg_activation)
        if len(self.activation_history) > 100:
            self.activation_history.pop(0)
    
    def get_architecture_stats(self) -> dict:
        """Retorna estatísticas da arquitetura"""
        active_nodes = sum(1 for node in self.nodes if node.active)
        total_connections = sum(len(node.connections) for node in self.nodes)
        
        return {
            'total_nodes': len(self.nodes),
            'active_nodes': active_nodes,
            'activation_rate': active_nodes / len(self.nodes) * 100,
            'total_connections': total_connections,
            'avg_coherence': np.mean([layer.coherence for layer in self.quantum_layers]) * 100,
            'quantum_layers': len(self.quantum_layers),
            'total_qubits': sum(layer.qubits for layer in self.quantum_layers)
        }

# Inicialização do visualizador
if 'neural_viz' not in st.session_state:
    st.session_state.neural_viz = EnhancedNeuralVisualizer(50)

if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

# CSS Customizado
st.markdown("""
<style>
    .stApp {
        background-color: #0a0a0a;
        color: #d1d5db;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .neural-container {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 0.5rem;
        padding: 1rem;
        position: relative;
        overflow: hidden;
        height: 600px;
    }
    
    .grid-overlay {
        position: absolute;
        inset: 0;
        background-image: 
            linear-gradient(rgba(14, 165, 233, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(14, 165, 233, 0.1) 1px, transparent 1px);
        background-size: 20px 20px;
        pointer-events: none;
    }
    
    .gradient-bg {
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse at center, 
            rgba(14, 165, 233, 0.2) 0%, 
            rgba(17, 24, 39, 0.6) 40%, 
            rgba(10, 10, 10, 1) 100%);
        pointer-events: none;
    }
    
    .stats-overlay {
        position: absolute;
        bottom: 0.5rem;
        left: 0.5rem;
        background-color: rgba(0, 0, 0, 0.7);
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        border: 1px solid #374151;
        font-family: monospace;
        font-size: 0.75rem;
        color: #0ea5e9;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .architecture-label {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        font-family: monospace;
        font-size: 0.625rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        background-color: rgba(0, 0, 0, 0.7);
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        border: 1px solid #374151;
    }
    
    .pulse-dot {
        display: inline-block;
        width: 0.5rem;
        height: 0.5rem;
        border-radius: 50%;
        background-color: #10b981;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .layer-indicator {
        position: absolute;
        left: 0.5rem;
        top: 0.5rem;
        display: flex;
        gap: 0.25rem;
        flex-direction: column;
    }
    
    .layer-dot {
        width: 0.75rem;
        height: 0.75rem;
        border-radius: 50%;
        border: 1px solid;
    }
    
    .layer-input { background-color: #3b82f6; border-color: #60a5fa; }
    .layer-hidden { background-color: #8b5cf6; border-color: #a78bfa; }
    .layer-output { background-color: #10b981; border-color: #34d399; }
    
    .control-panel {
        background-color: #1f2937;
        border: 1px solid #374151;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    .metric-card {
        background-color: rgba(0, 0, 0, 0.3);
        border: 1px solid #374151;
        border-radius: 0.25rem;
        padding: 0.75rem;
    }
    
    .quantum-badge {
        display: inline-block;
        padding: 0.125rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.625rem;
        font-weight: bold;
        margin-right: 0.25rem;
        margin-bottom: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Função para criar visualização Plotly
def create_neural_visualization(neural_viz: EnhancedNeuralVisualizer):
    """Cria visualização interativa dos nós neurais"""
    
    # Preparar dados para o gráfico
    node_x = [node.x for node in neural_viz.nodes]
    node_y = [node.y for node in neural_viz.nodes]
    node_active = [node.active for node in neural_viz.nodes]
    node_size = [5 + node.activation_level * 10 for node in neural_viz.nodes]
    node_color = ['#38bdf8' if active else '#0c4a6e' for active in node_active]
    node_opacity = [1.0 if active else 0.4 for active in node_active]
    
    # Criar traces para conexões
    connection_traces = []
    for i, node in enumerate(neural_viz.nodes):
        for conn_idx in node.connections:
            if conn_idx < len(neural_viz.nodes):
                conn_node = neural_viz.nodes[conn_idx]
                # Linha de conexão
                connection_traces.append(
                    go.Scatter(
                        x=[node.x, conn_node.x],
                        y=[node.y, conn_node.y],
                        mode='lines',
                        line=dict(
                            color='#0ea5e9',
                            width=0.5 + min(node.activation_level, conn_node.activation_level) * 1.5,
                            dash='dot' if not (node.active and conn_node.active) else 'solid'
                        ),
                        opacity=0.3 * (node.activation_level + conn_node.activation_level) / 2,
                        hoverinfo='none',
                        showlegend=False
                    )
                )
    
    # Criar trace para nós
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers',
        marker=dict(
            size=node_size,
            color=node_color,
            opacity=node_opacity,
            line=dict(
                color='#ffffff',
                width=1
            )
        ),
        text=[f"Nó {i}<br>Ativação: {node.activation_level:.2%}<br>Camada: {node.layer}" 
              for i, node in enumerate(neural_viz.nodes)],
        hoverinfo='text',
        name='Nós Neurais'
    )
    
    # Criar traces para halos ativos
    halo_traces = []
    for i, node in enumerate(neural_viz.nodes):
        if node.active:
            halo_traces.append(
                go.Scatter(
                    x=[node.x],
                    y=[node.y],
                    mode='markers',
                    marker=dict(
                        size=node_size[i] * 2.5,
                        color='#38bdf8',
                        opacity=0.2,
                        line=dict(width=0)
                    ),
                    hoverinfo='none',
                    showlegend=False
                )
            )
    
    # Combinar todos os traces
    all_traces = connection_traces + halo_traces + [node_trace]
    
    # Criar layout
    layout = go.Layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(14, 165, 233, 0.1)',
            zeroline=False,
            range=[0, 100],
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(14, 165, 233, 0.1)',
            zeroline=False,
            range=[0, 100],
            showticklabels=False
        ),
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        height=500,
        hovermode='closest'
    )
    
    return go.Figure(data=all_traces, layout=layout)

# Barra lateral com controles
with st.sidebar:
    st.markdown("### ⚙️ Controles de Visualização")
    
    # Controle de número de nós
    num_nodes = st.slider("Número de Nós", 20, 100, 50, 10)
    if num_nodes != st.session_state.neural_viz.num_nodes:
        st.session_state.neural_viz = EnhancedNeuralVisualizer(num_nodes)
    
    # Controle de velocidade de atualização
    update_speed = st.slider("Velocidade (segundos)", 1, 10, 2)
    
    # Opções de visualização
    show_connections = st.checkbox("Mostrar Conexões", value=True)
    show_halos = st.checkbox("Mostrar Halos", value=True)
    
    # Botão para reiniciar visualização
    if st.button("🔄 Reiniciar Visualização"):
        st.session_state.neural_viz = EnhancedNeuralVisualizer(num_nodes)
        st.success("Visualização reiniciada!")
    
    st.markdown("---")
    st.markdown("### 📊 Arquitetura Quântica")
    
    for layer in st.session_state.neural_viz.quantum_layers:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"**{layer.name}**")
        with col2:
            st.markdown(f"`{layer.qubits} Q`")
        
        # Barras de progresso para métricas quânticas
        st.progress(layer.coherence, text=f"Coerência: {layer.coherence:.1%}")
        st.progress(layer.entanglement_level, text=f"Emaranhamento: {layer.entanglement_level:.1%}")

# Layout principal
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### 🧠 Visualizador Neural Quântico")
    
    # Container principal da visualização
    st.markdown('<div class="neural-container">', unsafe_allow_html=True)
    st.markdown('<div class="grid-overlay"></div>', unsafe_allow_html=True)
    st.markdown('<div class="gradient-bg"></div>', unsafe_allow_html=True)
    
    # Criar e exibir visualização Plotly
    fig = create_neural_visualization(st.session_state.neural_viz)
    st.plotly_chart(fig, use_container_width=True)
    
    # Overlay de estatísticas
    stats = st.session_state.neural_viz.get_architecture_stats()
    st.markdown(f"""
    <div class="stats-overlay">
        <div class="pulse-dot"></div>
        COERÊNCIA QUÂNTICA: {stats['avg_coherence']:.1f}%
    </div>
    """, unsafe_allow_html=True)
    
    # Rótulo de arquitetura
    st.markdown("""
    <div class="architecture-label">
        Arquitetura: Híbrida QNN-VQC • {total_qubits} Qubits
    </div>
    """.format(total_qubits=stats['total_qubits']), unsafe_allow_html=True)
    
    # Indicadores de camada
    st.markdown("""
    <div class="layer-indicator">
        <div class="layer-dot layer-input" title="Camada de Entrada"></div>
        <div class="layer-dot layer-hidden" title="Camadas Ocultas"></div>
        <div class="layer-dot layer-hidden" title="Camadas Ocultas"></div>
        <div class="layer-dot layer-output" title="Camada de Saída"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 📈 Métricas em Tempo Real")
    
    # Estatísticas principais
    col_metric1, col_metric2 = st.columns(2)
    
    with col_metric1:
        st.metric("Nós Ativos", f"{stats['active_nodes']}/{stats['total_nodes']}")
    
    with col_metric2:
        st.metric("Taxa de Ativação", f"{stats['activation_rate']:.1f}%")
    
    # Gráfico de histórico de coerência
    if st.session_state.neural_viz.coherence_history:
        st.markdown("**Histórico de Coerência**")
        coherence_df = pd.DataFrame({
            'Tempo': range(len(st.session_state.neural_viz.coherence_history)),
            'Coerência': st.session_state.neural_viz.coherence_history
        })
        
        fig_coherence = px.line(
            coherence_df, 
            x='Tempo', 
            y='Coerência',
            line_shape='spline'
        )
        
        fig_coherence.update_layout(
            height=150,
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(range=[0.7, 1.0], showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        )
        
        fig_coherence.update_traces(line_color='#0ea5e9')
        
        st.plotly_chart(fig_coherence, use_container_width=True, config={'displayModeBar': False})
    
    # Gráfico de histórico de ativação
    if st.session_state.neural_viz.activation_history:
        st.markdown("**Histórico de Ativação**")
        activation_df = pd.DataFrame({
            'Tempo': range(len(st.session_state.neural_viz.activation_history)),
            'Ativação': st.session_state.neural_viz.activation_history
        })
        
        fig_activation = px.area(
            activation_df, 
            x='Tempo', 
            y='Ativação',
            line_shape='spline'
        )
        
        fig_activation.update_layout(
            height=150,
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(range=[0, 1], showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        )
        
        fig_activation.update_traces(line_color='#10b981', fill='tozeroy')
        
        st.plotly_chart(fig_activation, use_container_width=True, config={'displayModeBar': False})
    
    # Badges de status quântico
    st.markdown("### 🔬 Status Quântico")
    
    for layer in st.session_state.neural_viz.quantum_layers:
        coherence_color = "#10b981" if layer.coherence > 0.9 else "#f59e0b" if layer.coherence > 0.8 else "#ef4444"
        entanglement_color = "#8b5cf6" if layer.entanglement_level > 0.9 else "#a855f7" if layer.entanglement_level > 0.8 else "#c084fc"
        
        col_q1, col_q2 = st.columns(2)
        
        with col_q1:
            st.markdown(f'<div class="metric-card" style="border-left: 3px solid {coherence_color};">', unsafe_allow_html=True)
            st.markdown(f"**{layer.name}**")
            st.markdown(f"Coerência: <span style='color: {coherence_color};'>{layer.coherence:.1%}</span>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_q2:
            st.markdown(f'<div class="metric-card" style="border-left: 3px solid {entanglement_color};">', unsafe_allow_html=True)
            st.markdown(" ")
            st.markdown(f"Emaranhamento: <span style='color: {entanglement_color};'>{layer.entanglement_level:.1%}</span>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# Painel de controle inferior
st.markdown("### 🎛️ Painel de Controle")
col_control1, col_control2, col_control3 = st.columns(3)

with col_control1:
    st.markdown("**🔧 Configurações de Rede**")
    neural_density = st.select_slider(
        "Densidade Neural",
        options=["Baixa", "Média", "Alta", "Máxima"],
        value="Média"
    )
    
    connection_strength = st.slider(
        "Força das Conexões",
        min_value=0.1,
        max_value=2.0,
        value=1.0,
        step=0.1
    )

with col_control2:
    st.markdown("**⚛️ Parâmetros Quânticos**")
    decoherence_rate = st.slider(
        "Taxa de Decoerência",
        min_value=0.0,
        max_value=0.1,
        value=0.02,
        step=0.005,
        format="%.3f"
    )
    
    superposition_level = st.slider(
        "Nível de Superposição",
        min_value=0.0,
        max_value=1.0,
        value=0.8,
        step=0.05
    )

with col_control3:
    st.markdown("**📊 Monitoramento**")
    
    auto_update = st.checkbox("Atualização Automática", value=True)
    
    if st.button("📸 Capturar Estado Atual"):
        # Simular captura de estado
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.success(f"Estado capturado: neural_state_{timestamp}.qnn")
    
    if st.button("📊 Exportar Dados"):
        # Simular exportação
        st.info("Dados exportados para análise")

# Rodapé informativo
st.markdown("---")
col_footer1, col_footer2 = st.columns(2)

with col_footer1:
    st.markdown("**🧩 Sobre a Visualização**")
    st.markdown("""
    Este visualizador representa uma rede neural quântica híbrida (QNN-VQC) com:
    - **Nós azuis claros**: Neurônios ativos
    - **Nós azuis escuros**: Neurônios inativos
    - **Linhas**: Conexões sinápticas
    - **Halos**: Pulsos de ativação quântica
    """)

with col_footer2:
    st.markdown("**⚡ Performance**")
    current_time = datetime.now().strftime("%H:%M:%S")
    processing_rate = f"{stats['total_connections'] * 2:.0f} ops/ms"
    
    st.markdown(f"""
    - Última atualização: {current_time}
    - Taxa de processamento: {processing_rate}
    - Latência quântica: < 5µs
    - Fidelidade: > 99.8%
    """)

# Atualização automática
if auto_update:
    time.sleep(update_speed)
    
    # Atualizar estados
    st.session_state.neural_viz.update_activation()
    st.session_state.neural_viz.update_quantum_metrics()
    st.session_state.last_update = datetime.now()
    
    # Recarregar a página
    st.rerun()