import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import asyncio
import threading
import time
from dataclasses import dataclass, field
from enum import Enum

# Enums e tipos de dados
class SeverityLevel(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class ResourceType(Enum):
    CPU = "CPU"
    MEMORY = "MEMORY"
    DISK = "DISK"
    NETWORK = "NETWORK"

@dataclass
class PredictionResult:
    resourceType: ResourceType
    predictions: List[float]
    confidence: float
    timestamp: datetime

@dataclass
class SystemIncident:
    type: str
    description: str
    severity: SeverityLevel
    probability: float
    timestamp: datetime

@dataclass
class SecurityRisk:
    type: str
    level: str
    description: str
    probability: float
    timestamp: datetime

# Simulação do serviço de predição
class AdvancedPredictionService:
    """Serviço de predição avançada (simulado)"""
    
    async def predict_resources(self) -> List[PredictionResult]:
        """Predição de recursos do sistema"""
        await asyncio.sleep(0.1)  # Simulação de processamento
        
        # Gera dados simulados
        time_points = 10
        base_cpu = np.random.uniform(30, 50)
        cpu_trend = np.random.uniform(-0.5, 1.0)
        
        cpu_predictions = [
            min(100, max(0, base_cpu + (cpu_trend * i) + np.random.normal(0, 5)))
            for i in range(time_points)
        ]
        
        return [
            PredictionResult(
                resourceType=ResourceType.CPU,
                predictions=cpu_predictions,
                confidence=np.random.uniform(0.7, 0.95),
                timestamp=datetime.now()
            )
        ]
    
    async def predict_incidents(self) -> List[SystemIncident]:
        """Predição de incidentes do sistema"""
        await asyncio.sleep(0.1)
        
        incident_types = [
            "CPU Overload",
            "Memory Leak",
            "Disk Space Critical",
            "Network Latency Spike",
            "Service Degradation"
        ]
        
        incidents = []
        if np.random.random() > 0.6:  # 40% chance de incidente
            for i in range(np.random.randint(1, 4)):
                incident = SystemIncident(
                    type=np.random.choice(incident_types),
                    description=f"Potential {np.random.choice(incident_types).lower()} detected",
                    severity=np.random.choice(list(SeverityLevel)),
                    probability=np.random.uniform(0.3, 0.9),
                    timestamp=datetime.now() - timedelta(minutes=np.random.randint(1, 60))
                )
                incidents.append(incident)
        
        return incidents
    
    async def predict_security(self) -> List[SecurityRisk]:
        """Predição de riscos de segurança"""
        await asyncio.sleep(0.1)
        
        risk_types = [
            "Brute Force Attempt",
            "Suspicious Traffic",
            "Unauthorized Access",
            "Data Exfiltration",
            "Malware Detection"
        ]
        
        risks = []
        if np.random.random() > 0.7:  # 30% chance de risco
            for i in range(np.random.randint(1, 3)):
                risk = SecurityRisk(
                    type=np.random.choice(risk_types),
                    level=np.random.choice(["LOW", "MEDIUM", "HIGH"]),
                    description=f"Potential security threat: {np.random.choice(risk_types)}",
                    probability=np.random.uniform(0.2, 0.8),
                    timestamp=datetime.now() - timedelta(minutes=np.random.randint(5, 120))
                )
                risks.append(risk)
        
        return risks

# Instância do serviço
advancedPredictor = AdvancedPredictionService()

# Configuração do Streamlit
st.set_page_config(
    page_title="Painel de Previsão Preditiva Avançada",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    .stApp {
        background-color: #0a0a0a;
        color: #d1d5db;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .matrix-panel {
        background: linear-gradient(135deg, #111827 0%, #1e293b 100%);
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .matrix-header {
        background: linear-gradient(90deg, #0c4a6e 0%, #1e40af 100%);
        border-bottom: 1px solid #1e40af;
        padding: 15px 20px;
        border-radius: 8px 8px 0 0;
    }
    
    .cpu-chart {
        background: linear-gradient(180deg, rgba(6, 182, 212, 0.1) 0%, rgba(6, 182, 212, 0) 100%);
    }
    
    .anomaly-box {
        transition: background-color 0.3s;
        border-radius: 4px;
    }
    
    .anomaly-box:hover {
        filter: brightness(1.2);
    }
    
    .critical-incident {
        background-color: rgba(220, 38, 38, 0.2);
        border: 1px solid rgba(220, 38, 38, 0.5);
    }
    
    .warning-incident {
        background-color: rgba(234, 179, 8, 0.2);
        border: 1px solid rgba(234, 179, 8, 0.5);
    }
    
    .normal-incident {
        background-color: rgba(30, 64, 175, 0.2);
        border: 1px solid rgba(30, 64, 175, 0.5);
    }
    
    .refresh-button {
        background-color: #1e293b;
        border: 1px solid #475569;
        border-radius: 6px;
        padding: 8px 12px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .refresh-button:hover {
        background-color: #334155;
        border-color: #64748b;
    }
    
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #06b6d4;
        text-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
    }
    
    .subtitle {
        font-size: 10px;
        color: #06b6d4;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    h1, h2, h3, h4 {
        color: white !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
</style>
""", unsafe_allow_html=True)

class PredictionDashboard:
    """Classe principal do dashboard de predição"""
    
    def __init__(self):
        self.predictions: List[PredictionResult] = []
        self.incidents: List[SystemIncident] = []
        self.risks: List[SecurityRisk] = []
        self.loading = False
        self.last_update = None
        
        # Inicializar estado do Streamlit
        if 'data_initialized' not in st.session_state:
            st.session_state.data_initialized = False
            st.session_state.auto_refresh = True
    
    async def refresh_data(self):
        """Atualiza os dados do dashboard"""
        self.loading = True
        
        try:
            # Buscar dados dos serviços de predição
            preds = await advancedPredictor.predict_resources()
            incs = await advancedPredictor.predict_incidents()
            sec = await advancedPredictor.predict_security()
            
            self.predictions = preds
            self.incidents = (incs + self.incidents)[:5]  # Manter apenas os 5 mais recentes
            self.risks = sec
            self.last_update = datetime.now()
            
        except Exception as e:
            st.error(f"Erro ao atualizar dados: {e}")
        finally:
            self.loading = False
    
    def create_cpu_chart(self):
        """Cria gráfico de previsão de CPU com cone de incerteza"""
        cpu_data = next((p for p in self.predictions if p.resourceType == ResourceType.CPU), None)
        
        if not cpu_data:
            # Dados de exemplo
            time_points = list(range(10))
            base_values = [45 + i * 2 + np.random.normal(0, 3) for i in range(10)]
            upper_values = [min(100, v + (i * 2)) for i, v in enumerate(base_values)]
            lower_values = [max(0, v - (i * 2)) for i, v in enumerate(base_values)]
        else:
            time_points = list(range(len(cpu_data.predictions)))
            base_values = cpu_data.predictions
            upper_values = [min(100, v + (i * 2)) for i, v in enumerate(base_values)]
            lower_values = [max(0, v - (i * 2)) for i, v in enumerate(base_values)]
        
        # Criar gráfico com Plotly
        fig = go.Figure()
        
        # Adicionar cone de incerteza
        fig.add_trace(go.Scatter(
            x=time_points + time_points[::-1],
            y=upper_values + lower_values[::-1],
            fill='toself',
            fillcolor='rgba(6, 182, 212, 0.1)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Cone de Incerteza',
            hoverinfo='skip'
        ))
        
        # Adicionar linha principal
        fig.add_trace(go.Scatter(
            x=time_points,
            y=base_values,
            mode='lines',
            line=dict(color='#06b6d4', width=3),
            name='Previsão de Carga',
            fill='tonexty',
            fillcolor='rgba(6, 182, 212, 0.2)'
        ))
        
        # Configurar layout
        fig.update_layout(
            title="Horizonte de Carga (CPU)",
            title_font=dict(size=14, color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#d1d5db'),
            height=300,
            margin=dict(l=40, r=40, t=50, b=40),
            hovermode='x unified',
            showlegend=False,
            xaxis=dict(
                title="Tempo (minutos)",
                gridcolor='#374151',
                zerolinecolor='#374151'
            ),
            yaxis=dict(
                title="Carga (%)",
                range=[0, 100],
                gridcolor='#374151',
                zerolinecolor='#374151'
            )
        )
        
        return fig
    
    def create_heatmap(self):
        """Cria mapa de calor de anomalias"""
        # Gerar dados de exemplo para o mapa de calor
        data = np.random.rand(6, 8)  # 6 linhas, 8 colunas
        
        fig = go.Figure(data=go.Heatmap(
            z=data,
            colorscale=[
                [0, '#1e293b'],      # Baixo
                [0.4, '#1e40af'],    # Médio-baixo
                [0.7, '#f59e0b'],    # Médio-alto
                [0.9, '#ef4444'],    # Alto
                [1, '#dc2626']       # Crítico
            ],
            colorbar=dict(
                title="Intensidade",
                titleside="right",
                titlefont=dict(color='white'),
                tickfont=dict(color='white')
            ),
            hovertemplate='Cluster %{x},%{y}: %{z:.1%} Carga<extra></extra>'
        ))
        
        fig.update_layout(
            title="Mapa de Calor de Anomalias",
            title_font=dict(size=14, color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300,
            margin=dict(l=40, r=40, t=50, b=40),
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(8)),
                ticktext=[f"C{i+1}" for i in range(8)],
                gridcolor='#374151'
            ),
            yaxis=dict(
                tickmode='array',
                tickvals=list(range(6)),
                ticktext=[f"R{i+1}" for i in range(6)],
                gridcolor='#374151'
            )
        )
        
        return fig
    
    def render_header(self):
        """Renderiza o cabeçalho do dashboard"""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("""
            <div class="matrix-header">
                <h1 style="margin: 0; display: flex; align-items: center; gap: 10px;">
                    <span style="color: #06b6d4;">●</span>
                    PREVISÃO PREDITIVA AVANÇADA
                </h1>
                <div class="subtitle">CONE DE INCERTEZA • DETECÇÃO DE ANOMALIAS</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Atualizar", key="refresh_btn", type="secondary"):
                asyncio.run(self.refresh_data())
            
            # Auto-refresh toggle
            auto_refresh = st.checkbox(
                "Auto-refresh (3s)", 
                value=st.session_state.auto_refresh,
                key="auto_refresh_toggle"
            )
            st.session_state.auto_refresh = auto_refresh
    
    def render_metrics(self):
        """Renderiza métricas principais"""
        col1, col2, col3, col4 = st.columns(4)
        
        cpu_pred = next((p for p in self.predictions if p.resourceType == ResourceType.CPU), None)
        
        with col1:
            st.markdown("""
            <div class="matrix-panel" style="text-align: center;">
                <div style="color: #9ca3af; font-size: 12px;">CONFIANÇA CPU</div>
                <div class="metric-value">{:.1f}%</div>
            </div>
            """.format((cpu_pred.confidence * 100) if cpu_pred else 75.5), 
            unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="matrix-panel" style="text-align: center;">
                <div style="color: #9ca3af; font-size: 12px;">INCIDENTES ATIVOS</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(len(self.incidents)), 
            unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="matrix-panel" style="text-align: center;">
                <div style="color: #9ca3af; font-size: 12px;">RISCO SEGURANÇA</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(len(self.risks)), 
            unsafe_allow_html=True)
        
        with col4:
            last_update_str = self.last_update.strftime("%H:%M:%S") if self.last_update else "N/A"
            st.markdown(f"""
            <div class="matrix-panel" style="text-align: center;">
                <div style="color: #9ca3af; font-size: 12px;">ÚLTIMA ATUALIZAÇÃO</div>
                <div class="metric-value">{last_update_str}</div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_incident_log(self):
        """Renderiza log de incidentes"""
        st.markdown("""
        <div class="matrix-panel">
            <h3 style="margin-top: 0; display: flex; align-items: center; gap: 8px;">
                ⚠️ LOG DE PREDIÇÃO DE INCIDENTES (NLP)
            </h3>
        """, unsafe_allow_html=True)
        
        if not self.incidents:
            st.info("✅ Sistema estável. Nenhuma anomalia prevista.")
        else:
            for incident in self.incidents:
                severity_class = {
                    SeverityLevel.CRITICAL: "critical-incident",
                    SeverityLevel.HIGH: "warning-incident",
                    SeverityLevel.MEDIUM: "warning-incident",
                    SeverityLevel.LOW: "normal-incident"
                }.get(incident.severity, "normal-incident")
                
                st.markdown(f"""
                <div class="{severity_class}" style="padding: 12px; margin-bottom: 8px; border-radius: 6px;">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <div style="font-weight: bold; color: {'#ef4444' if incident.severity == SeverityLevel.CRITICAL else '#fbbf24'};">
                                {incident.type}
                            </div>
                            <div style="color: #9ca3af; font-size: 12px; margin-top: 4px;">
                                {incident.description}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="color: #06b6d4; font-family: monospace; font-weight: bold;">
                                {incident.probability*100:.0f}% PROB
                            </div>
                            <div style="color: #6b7280; font-size: 10px;">
                                {incident.timestamp.strftime('%H:%M:%S')}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def render_security_risks(self):
        """Renderiza riscos de segurança"""
        if self.risks:
            st.markdown("""
            <div class="matrix-panel">
                <h3 style="margin-top: 0; display: flex; align-items: center; gap: 8px;">
                    🛡️ RISCO DE SEGURANÇA
                </h3>
            """, unsafe_allow_html=True)
            
            for risk in self.risks:
                level_color = {
                    "HIGH": "#ef4444",
                    "MEDIUM": "#f59e0b",
                    "LOW": "#06b6d4"
                }.get(risk.level, "#9ca3af")
                
                st.markdown(f"""
                <div style="background-color: rgba(30, 41, 59, 0.5); border: 1px solid #374151; 
                         padding: 12px; margin-bottom: 8px; border-radius: 6px;">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <div style="font-weight: bold; color: white;">
                                {risk.type}
                            </div>
                            <div style="color: #9ca3af; font-size: 12px; margin-top: 4px;">
                                {risk.description}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="color: {level_color}; font-weight: bold;">
                                {risk.level}
                            </div>
                            <div style="color: #06b6d4; font-family: monospace; font-size: 14px;">
                                {risk.probability*100:.0f}%
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    def run(self):
        """Executa o dashboard principal"""
        # Inicializar dados se necessário
        if not st.session_state.data_initialized:
            asyncio.run(self.refresh_data())
            st.session_state.data_initialized = True
        
        # Renderizar header
        self.render_header()
        
        # Renderizar métricas
        self.render_metrics()
        
        # Layout principal em colunas
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de CPU
            st.markdown("<div class='matrix-panel'>", unsafe_allow_html=True)
            cpu_chart = self.create_cpu_chart()
            st.plotly_chart(cpu_chart, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            # Mapa de calor
            st.markdown("<div class='matrix-panel'>", unsafe_allow_html=True)
            heatmap = self.create_heatmap()
            st.plotly_chart(heatmap, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Log de incidentes
        self.render_incident_log()
        
        # Riscos de segurança
        self.render_security_risks()
        
        # Auto-refresh lógico
        if st.session_state.auto_refresh:
            time.sleep(3)
            st.rerun()

# Função principal
def main():
    st.title("🧠 Painel de Previsão Preditiva Avançada")
    
    # Inicializar dashboard
    dashboard = PredictionDashboard()
    
    # Executar dashboard
    dashboard.run()

if __name__ == "__main__":
    main()