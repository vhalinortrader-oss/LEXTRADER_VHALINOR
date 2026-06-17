import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass, field
from typing import List, Literal, Dict, Any, Optional
from datetime import datetime
import threading
import time
import random
from enum import Enum

class AlgorithmType(Enum):
    ML = "ML"
    STATISTICAL = "STATISTICAL"
    HYBRID = "HYBRID"
    QUANTUM = "QUANTUM"
    ENSEMBLE = "ENSEMBLE"

class NodeStatus(Enum):
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    WAITING = "WAITING"
    ERROR = "ERROR"

class Decision(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    CLOSE = "CLOSE"

@dataclass
class DecisionAlgorithm:
    id: str
    name: str
    type: AlgorithmType
    description: str
    accuracy: float
    speed: float
    complexity: float
    confidence: float
    is_active: bool
    decisions: int
    success_rate: float
    avg_response_time: float
    specialization: List[str] = field(default_factory=list)

@dataclass
class DecisionNode:
    id: str
    name: str
    input: str
    output: str
    confidence: float
    execution_time: float
    status: NodeStatus

@dataclass
class MarketDecision:
    timestamp: str
    algorithm: str
    decision: Decision
    confidence: float
    reasoning: str
    factors: List[str]
    risk: float
    expected_return: float
    timeframe: str

class AdvancedDecisionAlgorithmsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Algoritmos de Decisão Avançados")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f8fafc')
        
        # Estado da aplicação
        self.selected_algorithm = "ensemble"
        self.is_processing = False
        self.current_decisions = 0
        self.system_load = 67.3
        
        # Configurar estilo
        self.setup_styles()
        
        # Inicializar dados
        self.setup_data()
        
        # Configurar interface
        self.setup_ui()
        
        # Iniciar thread de atualização
        self.start_update_thread()
    
    def setup_styles(self):
        """Configurar estilos customizados"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar cores personalizadas
        style.configure('Primary.TButton', 
                       background='#3b82f6', 
                       foreground='white',
                       focuscolor='none')
        
        style.configure('Success.TLabel', foreground='#10b981')
        style.configure('Warning.TLabel', foreground='#f59e0b')
        style.configure('Error.TLabel', foreground='#ef4444')
        style.configure('Info.TLabel', foreground='#6366f1')
        
        style.configure('Card.TFrame', 
                       background='white', 
                       relief='solid',
                       borderwidth=1)
    
    def setup_data(self):
        """Inicializar dados dos algoritmos"""
        self.algorithms = [
            DecisionAlgorithm(
                id="ensemble",
                name="Ensemble Multi-Algoritmo",
                type=AlgorithmType.ENSEMBLE,
                description="Combina múltiplos algoritmos usando voting e stacking para decisões mais robustas",
                accuracy=94.7,
                speed=85.2,
                complexity=95.8,
                confidence=89.3,
                is_active=True,
                decisions=2847,
                success_rate=87.4,
                avg_response_time=0.23,
                specialization=["Análise Multi-Modal", "Consenso Algorítmico", "Meta-Learning"]
            ),
            DecisionAlgorithm(
                id="quantum_nn",
                name="Rede Neural Quântica",
                type=AlgorithmType.QUANTUM,
                description="Utiliza computação quântica simulada para processamento paralelo de cenários",
                accuracy=91.3,
                speed=92.7,
                complexity=98.5,
                confidence=85.9,
                is_active=True,
                decisions=1623,
                success_rate=83.2,
                avg_response_time=0.08,
                specialization=["Superposição", "Entrelaçamento", "Túnel Quântico"]
            ),
            DecisionAlgorithm(
                id="adaptive_lstm",
                name="LSTM Adaptativo Profundo",
                type=AlgorithmType.ML,
                description="Rede LSTM com arquitetura adaptativa que se reconfigura baseada em condições de mercado",
                accuracy=88.9,
                speed=78.4,
                complexity=87.3,
                confidence=82.7,
                is_active=True,
                decisions=3241,
                success_rate=79.6,
                avg_response_time=0.45,
                specialization=["Séries Temporais", "Memória Longa", "Adaptação Dinâmica"]
            ),
            DecisionAlgorithm(
                id="bayesian_optimizer",
                name="Otimizador Bayesiano Multi-Objetivo",
                type=AlgorithmType.STATISTICAL,
                description="Optimiza múltiplos objetivos simultaneamente usando inferência bayesiana",
                accuracy=86.4,
                speed=71.8,
                complexity=82.1,
                confidence=78.9,
                is_active=True,
                decisions=1876,
                success_rate=81.3,
                avg_response_time=0.67,
                specialization=["Otimização", "Incerteza", "Multi-Objetivo"]
            ),
            DecisionAlgorithm(
                id="reinforcement_agent",
                name="Agente de Aprendizado por Reforço",
                type=AlgorithmType.ML,
                description="Agente que aprende estratégias ótimas através de interação com o ambiente de mercado",
                accuracy=89.7,
                speed=83.6,
                complexity=91.4,
                confidence=86.1,
                is_active=True,
                decisions=2156,
                success_rate=84.8,
                avg_response_time=0.31,
                specialization=["Q-Learning", "Policy Gradient", "Actor-Critic"]
            ),
            DecisionAlgorithm(
                id="fuzzy_expert",
                name="Sistema Especialista Fuzzy",
                type=AlgorithmType.HYBRID,
                description="Combina lógica fuzzy com regras de especialistas para decisões em condições de incerteza",
                accuracy=84.2,
                speed=94.7,
                complexity=73.9,
                confidence=76.4,
                is_active=False,
                decisions=1432,
                success_rate=77.9,
                avg_response_time=0.12,
                specialization=["Lógica Fuzzy", "Regras Especialistas", "Incerteza"]
            ),
            DecisionAlgorithm(
                id="genetic_algorithm",
                name="Algoritmo Genético Evolutivo",
                type=AlgorithmType.HYBRID,
                description="Evolui estratégias de trading através de seleção natural e mutação genética",
                accuracy=87.1,
                speed=76.3,
                complexity=88.7,
                confidence=81.5,
                is_active=True,
                decisions=998,
                success_rate=82.7,
                avg_response_time=0.89,
                specialization=["Evolução", "Otimização Genética", "Seleção Natural"]
            )
        ]
        
        self.decision_flow = [
            DecisionNode("1", "Coleta de Dados", "Market Data", "Processed Data", 98.5, 0.02, NodeStatus.COMPLETED),
            DecisionNode("2", "Pré-processamento", "Raw Data", "Clean Data", 96.7, 0.08, NodeStatus.COMPLETED),
            DecisionNode("3", "Feature Engineering", "Clean Data", "Features", 94.2, 0.15, NodeStatus.COMPLETED),
            DecisionNode("4", "Análise Ensemble", "Features", "Predictions", 89.3, 0.23, NodeStatus.PROCESSING),
            DecisionNode("5", "Validação Cruzada", "Predictions", "Validated", 0, 0, NodeStatus.WAITING),
            DecisionNode("6", "Execução de Decisão", "Validated", "Action", 0, 0, NodeStatus.WAITING)
        ]
        
        self.recent_decisions = [
            MarketDecision(
                timestamp="2024-01-15 15:42:23",
                algorithm="Ensemble Multi-Algoritmo",
                decision=Decision.BUY,
                confidence=87.4,
                reasoning="Confluência de sinais: breakout técnico + momentum positivo + volume acima da média",
                factors=["RSI(14): 45.2", "MACD: Bullish Cross", "Volume: +234%", "Support: 42,100"],
                risk=2.3,
                expected_return=5.7,
                timeframe="4H"
            ),
            MarketDecision(
                timestamp="2024-01-15 15:38:47",
                algorithm="Rede Neural Quântica",
                decision=Decision.SELL,
                confidence=92.1,
                reasoning="Padrão de reversão detectado com alta probabilidade baseado em análise quântica",
                factors=["Quantum State: Bearish", "Volatility: Increasing", "Resistance: 42,800", "Divergence: Confirmed"],
                risk=1.8,
                expected_return=4.2,
                timeframe="1H"
            ),
            MarketDecision(
                timestamp="2024-01-15 15:35:12",
                algorithm="LSTM Adaptativo",
                decision=Decision.HOLD,
                confidence=76.8,
                reasoning="Mercado em consolidação, aguardando breakout definitivo da faixa atual",
                factors=["Trend: Sideways", "ATR: Low", "Volume: Decreasing", "Support/Resistance: Strong"],
                risk=1.2,
                expected_return=2.1,
                timeframe="2H"
            )
        ]
    
    def setup_ui(self):
        """Configurar interface principal"""
        # Frame principal com padding
        main_frame = ttk.Frame(self.root, padding="20", style='Card.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Cabeçalho
        self.setup_header(main_frame)
        
        # Métricas do sistema
        self.setup_metrics_panel(main_frame)
        
        # Notebook para abas
        self.setup_notebook(main_frame)
        
        # Sistema de consenso
        self.setup_consensus_panel(main_frame)
        
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
    
    def setup_header(self, parent):
        """Configurar cabeçalho"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Título
        title_label = ttk.Label(header_frame, 
                               text="🧠 Algoritmos de Decisão Avançados", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Status e botão
        control_frame = ttk.Frame(header_frame)
        control_frame.grid(row=0, column=1, sticky=tk.E)
        
        # Badge de algoritmos ativos
        active_count = len([a for a in self.algorithms if a.is_active])
        status_label = ttk.Label(control_frame, 
                                text=f"🔧 {active_count} Ativos", 
                                style='Success.TLabel',
                                font=("Arial", 10, "bold"))
        status_label.grid(row=0, column=0, padx=(0, 10))
        
        # Botão executar
        self.execute_btn = ttk.Button(control_frame, 
                                     text="⚡ Executar Decisão", 
                                     command=self.run_decision_process,
                                     style='Primary.TButton')
        self.execute_btn.grid(row=0, column=1)
        
        header_frame.columnconfigure(0, weight=1)
    
    def setup_metrics_panel(self, parent):
        """Configurar painel de métricas"""
        metrics_frame = ttk.LabelFrame(parent, text="📊 Métricas do Sistema", padding="15")
        metrics_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Grid de métricas
        metrics_grid = ttk.Frame(metrics_frame)
        metrics_grid.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.metrics_labels = {}
        
        # Configurar métricas
        self.create_metric_widget(metrics_grid, "decisions_today", "Decisões Hoje", 
                                 str(self.current_decisions), 0)
        
        active_algos = [a for a in self.algorithms if a.is_active]
        avg_success = sum(a.success_rate for a in active_algos) / len(active_algos) if active_algos else 0
        self.create_metric_widget(metrics_grid, "success_rate", "Taxa Sucesso Média", 
                                 f"{avg_success:.1f}%", 1)
        
        avg_response = sum(a.avg_response_time for a in active_algos) / len(active_algos) if active_algos else 0
        self.create_metric_widget(metrics_grid, "response_time", "Tempo Resposta", 
                                 f"{avg_response:.2f}s", 2)
        
        self.create_metric_widget(metrics_grid, "system_load", "Carga Sistema", 
                                 f"{self.system_load:.1f}%", 3)
        
        # Configurar colunas
        for i in range(4):
            metrics_grid.columnconfigure(i, weight=1)
    
    def create_metric_widget(self, parent, key, label, value, column):
        """Criar widget de métrica individual"""
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=column, padx=10, pady=5)
        
        value_label = ttk.Label(frame, text=value, font=("Arial", 16, "bold"), 
                               style='Info.TLabel')
        value_label.grid(row=0, column=0)
        
        desc_label = ttk.Label(frame, text=label, font=("Arial", 9))
        desc_label.grid(row=1, column=0)
        
        self.metrics_labels[key] = value_label
    
    def setup_notebook(self, parent):
        """Configurar notebook com abas"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Aba Algoritmos
        algorithms_frame = ttk.Frame(self.notebook)
        self.notebook.add(algorithms_frame, text="🤖 Algoritmos")
        self.setup_algorithms_tab(algorithms_frame)
        
        # Aba Fluxo
        flow_frame = ttk.Frame(self.notebook)
        self.notebook.add(flow_frame, text="🔀 Fluxo de Decisão")
        self.setup_flow_tab(flow_frame)
        
        # Aba Decisões
        decisions_frame = ttk.Frame(self.notebook)
        self.notebook.add(decisions_frame, text="📈 Decisões Recentes")
        self.setup_decisions_tab(decisions_frame)
    
    def setup_algorithms_tab(self, parent):
        """Configurar aba de algoritmos"""
        canvas = tk.Canvas(parent, bg='#f8fafc')
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.algorithm_widgets = {}
        
        for i, algo in enumerate(self.algorithms):
            self.create_algorithm_card(scrollable_frame, algo, i)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        scrollable_frame.columnconfigure(0, weight=1)
    
    def create_algorithm_card(self, parent, algo, index):
        """Criar card individual do algoritmo"""
        # Frame principal do card
        card_frame = ttk.LabelFrame(parent, 
                                   text=f"{algo.name} ({algo.type.value})", 
                                   padding="15",
                                   style='Card.TFrame')
        card_frame.grid(row=index, column=0, sticky=(tk.W, tk.E), pady=8, padx=10)
        
        # Descrição
        desc_label = ttk.Label(card_frame, text=algo.description, 
                              wraplength=800, font=("Arial", 9))
        desc_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        # Frame para métricas
        metrics_frame = ttk.Frame(card_frame)
        metrics_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Criar barras de progresso para métricas
        metrics = [
            ("Precisão", algo.accuracy, "#10b981"),
            ("Velocidade", algo.speed, "#3b82f6"),
            ("Complexidade", algo.complexity, "#f59e0b"),
            ("Confiança", algo.confidence, "#8b5cf6")
        ]
        
        for j, (name, value, color) in enumerate(metrics):
            metric_frame = ttk.Frame(metrics_frame)
            metric_frame.grid(row=j//2, column=j%2, padx=10, pady=2, sticky=(tk.W, tk.E))
            
            ttk.Label(metric_frame, text=f"{name}: {value:.1f}%", 
                     font=("Arial", 8)).grid(row=0, column=0, sticky=tk.W)
            
            # Simular barra de progresso com Label colorido
            progress_frame = ttk.Frame(metric_frame, relief='sunken', borderwidth=1)
            progress_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
            
            progress_width = int(value * 2)  # Escala para pixels
            progress_label = tk.Label(progress_frame, 
                                    text="", 
                                    bg=color, 
                                    width=progress_width//8 if progress_width > 0 else 1,
                                    height=1)
            progress_label.grid(row=0, column=0, sticky=tk.W)
            
            metric_frame.columnconfigure(0, weight=1)
        
        # Especialização
        if algo.specialization:
            spec_text = ", ".join(algo.specialization)
            ttk.Label(card_frame, 
                     text=f"Especialização: {spec_text}", 
                     font=("Arial", 8),
                     wraplength=800).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Estatísticas
        stats_text = f"Decisões: {algo.decisions} | Taxa Sucesso: {algo.success_rate}% | Tempo Médio: {algo.avg_response_time}s"
        ttk.Label(card_frame, text=stats_text, font=("Arial", 8)).grid(row=3, column=0, sticky=tk.W)
        
        # Botão toggle
        toggle_text = "Desativar" if algo.is_active else "Ativar"
        toggle_btn = ttk.Button(card_frame, 
                               text=toggle_text,
                               command=lambda: self.toggle_algorithm(algo.id))
        toggle_btn.grid(row=3, column=1, sticky=tk.E)
        
        # Status visual
        status_color = "#10b981" if algo.is_active else "#6b7280"
        status_label = tk.Label(card_frame, 
                               text="● ATIVO" if algo.is_active else "● INATIVO",
                               fg=status_color,
                               font=("Arial", 8, "bold"))
        status_label.grid(row=0, column=2, sticky=tk.E)
        
        self.algorithm_widgets[algo.id] = {
            'toggle_btn': toggle_btn,
            'status_label': status_label
        }
        
        card_frame.columnconfigure(0, weight=1)
    
    def setup_flow_tab(self, parent):
        """Configurar aba de fluxo de decisão"""
        flow_label = ttk.Label(parent, 
                              text="🔀 Fluxo de Processamento de Decisão", 
                              font=("Arial", 14, "bold"))
        flow_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 15))
        
        # Frame principal do fluxo
        flow_main_frame = ttk.Frame(parent)
        flow_main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Criar visualização do fluxo
        self.flow_widgets = []
        for i, node in enumerate(self.decision_flow):
            self.create_flow_node(flow_main_frame, node, i)
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
    
    def create_flow_node(self, parent, node, index):
        """Criar nó individual do fluxo"""
        node_frame = ttk.Frame(parent, style='Card.TFrame', padding="10")
        node_frame.grid(row=index, column=0, sticky=(tk.W, tk.E), pady=3, padx=5)
        
        # Ícone de status
        status_icons = {
            NodeStatus.COMPLETED: "✅",
            NodeStatus.PROCESSING: "🔄",
            NodeStatus.WAITING: "⏳",
            NodeStatus.ERROR: "❌"
        }
        
        icon_label = ttk.Label(node_frame, 
                              text=status_icons.get(node.status, "⏳"), 
                              font=("Arial", 12))
        icon_label.grid(row=0, column=0, padx=(0, 10))
        
        # Número do nó
        num_label = tk.Label(node_frame, 
                            text=str(index + 1), 
                            bg="#3b82f6", 
                            fg="white",
                            font=("Arial", 10, "bold"),
                            width=3, 
                            height=1)
        num_label.grid(row=0, column=1, padx=(0, 10))
        
        # Informações do nó
        info_frame = ttk.Frame(node_frame)
        info_frame.grid(row=0, column=2, sticky=(tk.W, tk.E))
        
        ttk.Label(info_frame, text=node.name, 
                 font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(info_frame, 
                 text=f"{node.input} → {node.output}", 
                 font=("Arial", 8)).grid(row=1, column=0, sticky=tk.W)
        
        # Métricas
        metrics_frame = ttk.Frame(node_frame)
        metrics_frame.grid(row=0, column=3, sticky=tk.E)
        
        confidence_text = f"{node.confidence:.1f}%" if node.confidence > 0 else "-"
        time_text = f"{node.execution_time}s" if node.execution_time > 0 else "-"
        
        ttk.Label(metrics_frame, text=confidence_text, 
                 font=("Arial", 10, "bold"), 
                 style='Info.TLabel').grid(row=0, column=0, sticky=tk.E)
        ttk.Label(metrics_frame, text=time_text, 
                 font=("Arial", 8)).grid(row=1, column=0, sticky=tk.E)
        
        node_frame.columnconfigure(2, weight=1)
        
        self.flow_widgets.append({
            'frame': node_frame,
            'icon': icon_label,
            'confidence': metrics_frame.winfo_children()[0] if metrics_frame.winfo_children() else None
        })
    
    def setup_decisions_tab(self, parent):
        """Configurar aba de decisões recentes"""
        decisions_label = ttk.Label(parent, 
                                   text="📈 Decisões Recentes", 
                                   font=("Arial", 14, "bold"))
        decisions_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 15))
        
        # Canvas com scroll para decisões
        canvas = tk.Canvas(parent, bg='#f8fafc')
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        self.decisions_frame = ttk.Frame(canvas)
        
        self.decisions_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.decisions_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Criar cards de decisões
        for i, decision in enumerate(self.recent_decisions):
            self.create_decision_card(self.decisions_frame, decision, i)
        
        canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        self.decisions_frame.columnconfigure(0, weight=1)
    
    def create_decision_card(self, parent, decision, index):
        """Criar card individual de decisão"""
        # Cores por tipo de decisão
        decision_colors = {
            Decision.BUY: "#10b981",
            Decision.SELL: "#ef4444", 
            Decision.HOLD: "#f59e0b",
            Decision.CLOSE: "#3b82f6"
        }
        
        decision_icons = {
            Decision.BUY: "📈",
            Decision.SELL: "📉",
            Decision.HOLD: "🎯",
            Decision.CLOSE: "👁"
        }
        
        card_frame = ttk.LabelFrame(parent, 
                                   text=f"{decision_icons.get(decision.decision, '•')} {decision.decision.value} - {decision.confidence}% confiança",
                                   padding="15")
        card_frame.grid(row=index, column=0, sticky=(tk.W, tk.E), pady=8, padx=10)
        
        # Algoritmo e timestamp
        info_text = f"Algoritmo: {decision.algorithm} | {decision.timestamp}"
        ttk.Label(card_frame, text=info_text, font=("Arial", 8)).grid(row=0, column=0, sticky=tk.W)
        
        # Raciocínio
        ttk.Label(card_frame, text=decision.reasoning, 
                 wraplength=800, font=("Arial", 9)).grid(row=1, column=0, sticky=tk.W, pady=(8, 0))
        
        # Fatores
        if decision.factors:
            factors_text = " | ".join(decision.factors)
            ttk.Label(card_frame, text=f"Fatores: {factors_text}", 
                     font=("Arial", 8), wraplength=800).grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        
        # Métricas da decisão
        metrics_frame = ttk.Frame(card_frame)
        metrics_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(8, 0))
        
        # Grid de métricas
        risk_label = ttk.Label(metrics_frame, text=f"Risco: {decision.risk}%", 
                              style='Error.TLabel', font=("Arial", 9, "bold"))
        risk_label.grid(row=0, column=0, padx=(0, 20))
        
        return_label = ttk.Label(metrics_frame, text=f"Retorno: {decision.expected_return}%", 
                                style='Success.TLabel', font=("Arial", 9, "bold"))
        return_label.grid(row=0, column=1, padx=(0, 20))
        
        timeframe_label = ttk.Label(metrics_frame, text=f"Timeframe: {decision.timeframe}", 
                                   style='Info.TLabel', font=("Arial", 9, "bold"))
        timeframe_label.grid(row=0, column=2)
        
        card_frame.columnconfigure(0, weight=1)
    
    def setup_consensus_panel(self, parent):
        """Configurar painel de sistema de consenso"""
        consensus_frame = ttk.LabelFrame(parent, 
                                        text="🔗 Sistema de Consenso Algorítmico", 
                                        padding="15")
        consensus_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        # Descrição
        desc_text = ("O sistema combina decisões de múltiplos algoritmos usando votação ponderada "
                    "e análise de consenso para produzir decisões mais robustas e confiáveis.")
        ttk.Label(consensus_frame, text=desc_text, 
                 wraplength=900, font=("Arial", 9)).grid(row=0, column=0, pady=(0, 15))
        
        # Métricas de consenso
        consensus_metrics_frame = ttk.Frame(consensus_frame)
        consensus_metrics_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Grid de métricas de consenso
        self.create_consensus_metric(consensus_metrics_frame, "89.7%", "Consenso Atual", 0)
        active_count = len([a for a in self.algorithms if a.is_active])
        self.create_consensus_metric(consensus_metrics_frame, str(active_count), "Algoritmos Ativos", 1)
        self.create_consensus_metric(consensus_metrics_frame, "0.31s", "Tempo Consenso", 2)
        
        for i in range(3):
            consensus_metrics_frame.columnconfigure(i, weight=1)
        
        consensus_frame.columnconfigure(0, weight=1)
    
    def create_consensus_metric(self, parent, value, label, column):
        """Criar métrica individual de consenso"""
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=column, padx=20)
        
        ttk.Label(frame, text=value, font=("Arial", 18, "bold"), 
                 style='Info.TLabel').grid(row=0, column=0)
        ttk.Label(frame, text=label, font=("Arial", 9)).grid(row=1, column=0)
    
    def toggle_algorithm(self, algorithm_id):
        """Alternar estado do algoritmo"""
        for algo in self.algorithms:
            if algo.id == algorithm_id:
                algo.is_active = not algo.is_active
                
                # Atualizar widgets
                if algorithm_id in self.algorithm_widgets:
                    widgets = self.algorithm_widgets[algorithm_id]
                    widgets['toggle_btn'].config(text="Desativar" if algo.is_active else "Ativar")
                    
                    status_color = "#10b981" if algo.is_active else "#6b7280"
                    status_text = "● ATIVO" if algo.is_active else "● INATIVO"
                    widgets['status_label'].config(text=status_text, fg=status_color)
                
                break
        
        self.update_metrics_display()
    
    def run_decision_process(self):
        """Executar processo de decisão"""
        if self.is_processing:
            return
        
        self.is_processing = True
        self.execute_btn.config(text="🔄 Processando...", state="disabled")
        
        # Executar em thread separada
        threading.Thread(target=self._decision_process_worker, daemon=True).start()
    
    def _decision_process_worker(self):
        """Worker para processo de decisão"""
        # Simular processo de decisão
        for i in range(len(self.decision_flow)):
            time.sleep(0.8)  # Simular tempo de processamento
            
            # Atualizar status dos nós
            for j, node in enumerate(self.decision_flow):
                if j == i:
                    node.status = NodeStatus.PROCESSING
                    node.confidence = min(100, node.confidence + random.uniform(5, 15))
                elif j < i:
                    node.status = NodeStatus.COMPLETED
                    if node.confidence == 0:
                        node.confidence = random.uniform(85, 99)
                        node.execution_time = random.uniform(0.1, 0.5)
                else:
                    node.status = NodeStatus.WAITING
            
            # Atualizar UI na thread principal
            self.root.after(0, self.update_flow_display)
        
        # Finalizar todos os nós
        for node in self.decision_flow:
            node.status = NodeStatus.COMPLETED
            if node.confidence == 0:
                node.confidence = random.uniform(85, 99)
                node.execution_time = random.uniform(0.1, 0.5)
        
        self.root.after(0, self._finish_decision_process)
    
    def _finish_decision_process(self):
        """Finalizar processo de decisão"""
        self.is_processing = False
        self.execute_btn.config(text="⚡ Executar Decisão", state="normal")
        self.update_flow_display()
        messagebox.showinfo("Sucesso", "Processo de decisão executado com sucesso!")
    
    def update_flow_display(self):
        """Atualizar exibição do fluxo"""
        status_icons = {
            NodeStatus.COMPLETED: "✅",
            NodeStatus.PROCESSING: "🔄",
            NodeStatus.WAITING: "⏳",
            NodeStatus.ERROR: "❌"
        }
        
        for i, (node, widgets) in enumerate(zip(self.decision_flow, self.flow_widgets)):
            if 'icon' in widgets and widgets['icon']:
                widgets['icon'].config(text=status_icons.get(node.status, "⏳"))
    
    def update_metrics_display(self):
        """Atualizar exibição das métricas"""
        active_algos = [a for a in self.algorithms if a.is_active]
        
        self.metrics_labels['decisions_today'].config(text=str(self.current_decisions))
        
        if active_algos:
            avg_success = sum(a.success_rate for a in active_algos) / len(active_algos)
            avg_response = sum(a.avg_response_time for a in active_algos) / len(active_algos)
            self.metrics_labels['success_rate'].config(text=f"{avg_success:.1f}%")
            self.metrics_labels['response_time'].config(text=f"{avg_response:.2f}s")
        else:
            self.metrics_labels['success_rate'].config(text="0%")
            self.metrics_labels['response_time'].config(text="0s")
        
        self.metrics_labels['system_load'].config(text=f"{self.system_load:.1f}%")
    
    def start_update_thread(self):
        """Iniciar thread de atualização periódica"""
        def update_worker():
            while True:
                time.sleep(2)
                
                # Atualizar métricas
                self.current_decisions += random.randint(0, 3)
                self.system_load = max(30, min(95, self.system_load + random.uniform(-3, 3)))
                
                # Atualizar confiança dos nós em processamento
                for node in self.decision_flow:
                    if node.status == NodeStatus.PROCESSING:
                        node.confidence = min(100, node.confidence + random.uniform(0, 2))
                
                # Atualizar UI
                self.root.after(0, self.update_metrics_display)
                self.root.after(0, self.update_flow_display)
        
        threading.Thread(target=update_worker, daemon=True).start()

def main():
    """Função principal para executar a aplicação"""
    root = tk.Tk()
    app = AdvancedDecisionAlgorithmsApp(root)
    
    # Tornar a janela responsiva
    root.minsize(1000, 700)
    
    # Centralizar janela
    root.eval('tk::PlaceWindow . center')
    
    # Iniciar loop principal
    root.mainloop()

if __name__ == "__main__":
    main()
