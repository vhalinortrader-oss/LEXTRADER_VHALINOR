import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import time
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from enum import Enum
import threading

# Data Types
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

class DecisionType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    CLOSE = "CLOSE"

@dataclass
class DecisionAlgorithm:
    id: str
    name: str
    algo_type: AlgorithmType
    description: str
    accuracy: float
    speed: float
    complexity: float
    confidence: float
    is_active: bool
    decisions: int
    success_rate: float
    avg_response_time: float
    specialization: List[str]

@dataclass
class DecisionNode:
    id: str
    name: str
    input_data: str
    output_data: str
    confidence: float
    execution_time: float
    status: NodeStatus

@dataclass
class MarketDecision:
    id: str
    timestamp: str
    algorithm: str
    decision: DecisionType
    confidence: float
    reasoning: str
    factors: List[str]
    risk: float
    expected_return: float
    timeframe: str

# Initial Data
INITIAL_ALGORITHMS = [
    DecisionAlgorithm(
        id="ensemble",
        name="Ensemble Multi-Algoritmo",
        algo_type=AlgorithmType.ENSEMBLE,
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
        algo_type=AlgorithmType.QUANTUM,
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
        algo_type=AlgorithmType.ML,
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
        name="Otimizador Bayesiano",
        algo_type=AlgorithmType.STATISTICAL,
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
        name="Agente de Reforço (RL)",
        algo_type=AlgorithmType.ML,
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
        algo_type=AlgorithmType.HYBRID,
        description="Combina lógica fuzzy com regras de especialistas para decisões em incerteza",
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
        name="Algoritmo Genético",
        algo_type=AlgorithmType.HYBRID,
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

INITIAL_FLOW = [
    DecisionNode("1", "Coleta de Dados", "Market Data", "Processed Data", 98.5, 0.02, NodeStatus.COMPLETED),
    DecisionNode("2", "Pré-processamento", "Raw Data", "Clean Data", 96.7, 0.08, NodeStatus.COMPLETED),
    DecisionNode("3", "Feature Engineering", "Clean Data", "Features", 94.2, 0.15, NodeStatus.COMPLETED),
    DecisionNode("4", "Análise Ensemble", "Features", "Predictions", 89.3, 0.23, NodeStatus.PROCESSING),
    DecisionNode("5", "Validação Cruzada", "Predictions", "Validated", 0, 0, NodeStatus.WAITING),
    DecisionNode("6", "Execução de Decisão", "Validated", "Action", 0, 0, NodeStatus.WAITING)
]

INITIAL_DECISIONS = [
    MarketDecision(
        id="dec-1",
        timestamp="2024-01-15 15:42:23",
        algorithm="Ensemble Multi-Algoritmo",
        decision=DecisionType.BUY,
        confidence=87.4,
        reasoning="Confluência de sinais: breakout técnico + momentum positivo + volume acima da média",
        factors=["RSI(14): 45.2", "MACD: Bullish Cross", "Volume: +234%", "Support: 42,100"],
        risk=2.3,
        expected_return=5.7,
        timeframe="4H"
    ),
    MarketDecision(
        id="dec-2",
        timestamp="2024-01-15 15:38:47",
        algorithm="Rede Neural Quântica",
        decision=DecisionType.SELL,
        confidence=92.1,
        reasoning="Padrão de reversão detectado com alta probabilidade baseado em análise quântica",
        factors=["Quantum State: Bearish", "Volatility: Increasing", "Resistance: 42,800", "Divergence: Confirmed"],
        risk=1.8,
        expected_return=4.2,
        timeframe="1H"
    ),
    MarketDecision(
        id="dec-3",
        timestamp="2024-01-15 15:35:12",
        algorithm="LSTM Adaptativo",
        decision=DecisionType.HOLD,
        confidence=76.8,
        reasoning="Mercado em consolidação, aguardando breakout definitivo da faixa atual",
        factors=["Trend: Sideways", "ATR: Low", "Volume: Decreasing", "Support/Resistance: Strong"],
        risk=1.2,
        expected_return=2.1,
        timeframe="2H"
    )
]

# Main Application
class DecisionEngine:
    def __init__(self, root):
        self.root = root
        self.root.title("Decision Engine - Sistema de Consenso Algorítmico")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0a0a0a")
        
        # State
        self.algorithms = INITIAL_ALGORITHMS.copy()
        self.decision_flow = INITIAL_FLOW.copy()
        self.recent_decisions = INITIAL_DECISIONS.copy()
        
        self.is_processing = False
        self.current_decisions = 14520
        self.system_load = 67.3
        self.active_tab = "ALGORITHMS"
        
        # UI Components
        self.setup_ui()
        
        # Start live metrics
        self.start_live_metrics()
    
    def get_algo_color(self, algo_type: AlgorithmType) -> Dict[str, str]:
        """Get color scheme for algorithm type"""
        colors = {
            AlgorithmType.ML: {"text": "#60a5fa", "border": "#3b82f6", "bg": "#1e40af20"},
            AlgorithmType.STATISTICAL: {"text": "#10b981", "border": "#059669", "bg": "#065f4620"},
            AlgorithmType.HYBRID: {"text": "#a855f7", "border": "#7c3aed", "bg": "#4c1d9520"},
            AlgorithmType.QUANTUM: {"text": "#ec4899", "border": "#db2777", "bg": "#83184320"},
            AlgorithmType.ENSEMBLE: {"text": "#fbbf24", "border": "#f59e0b", "bg": "#854d0e20"}
        }
        return colors.get(algo_type, {"text": "#9ca3af", "border": "#6b7280", "bg": "#37415120"})
    
    def get_decision_color(self, decision: DecisionType) -> str:
        """Get color for decision type"""
        colors = {
            DecisionType.BUY: "#10b981",
            DecisionType.SELL: "#ef4444",
            DecisionType.HOLD: "#fbbf24",
            DecisionType.CLOSE: "#9ca3af"
        }
        return colors.get(decision, "#9ca3af")
    
    def setup_ui(self):
        """Setup the complete user interface"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg="#0a0a0a")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header stats
        self.setup_stats()
        
        # Main content panel
        self.setup_main_panel()
    
    def setup_stats(self):
        """Setup statistics header"""
        stats_frame = tk.Frame(self.main_frame, bg="transparent")
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Active algorithms
        algo_frame = tk.Frame(
            stats_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=10
        )
        algo_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(
            algo_frame,
            text="ALGORITMOS ATIVOS",
            font=("Arial", 8),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        active_count = sum(1 for a in self.algorithms if a.is_active)
        total_count = len(self.algorithms)
        self.active_algo_label = tk.Label(
            algo_frame,
            text=f"{active_count} / {total_count}",
            font=("Courier", 18, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        self.active_algo_label.pack(anchor=tk.W)
        
        # Progress bar
        progress_frame = tk.Frame(algo_frame, bg="#1a1a2e", height=4)
        progress_frame.pack(fill=tk.X, pady=(5, 0))
        progress_frame.pack_propagate(False)
        
        progress_width = int((active_count / total_count) * 100)
        self.algo_progress = tk.Frame(
            progress_frame,
            bg="#10b981",
            width=progress_width
        )
        self.algo_progress.pack(side=tk.LEFT, fill=tk.Y)
        
        # Average success rate
        success_frame = tk.Frame(
            stats_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=10
        )
        success_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(
            success_frame,
            text="TAXA DE SUCESSO MÉDIA",
            font=("Arial", 8),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        avg_success = sum(a.success_rate for a in self.algorithms if a.is_active)
        avg_success /= active_count if active_count > 0 else 1
        
        self.success_label = tk.Label(
            success_frame,
            text=f"{avg_success:.1f}%",
            font=("Courier", 18, "bold"),
            fg="#0ea5e9",
            bg="#1a1a2e"
        )
        self.success_label.pack(anchor=tk.W)
        
        # Progress bar
        success_progress_frame = tk.Frame(success_frame, bg="#1a1a2e", height=4)
        success_progress_frame.pack(fill=tk.X, pady=(5, 0))
        success_progress_frame.pack_propagate(False)
        
        self.success_progress = tk.Frame(
            success_progress_frame,
            bg="#0ea5e9",
            width=int(avg_success)
        )
        self.success_progress.pack(side=tk.LEFT, fill=tk.Y)
        
        # Today's decisions
        decisions_frame = tk.Frame(
            stats_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=10
        )
        decisions_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(
            decisions_frame,
            text="DECISÕES HOJE",
            font=("Arial", 8),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.decisions_label = tk.Label(
            decisions_frame,
            text=f"{self.current_decisions:,}",
            font=("Courier", 18, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        self.decisions_label.pack(anchor=tk.W)
        
        # System load
        load_frame = tk.Frame(
            stats_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=10
        )
        load_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(
            load_frame,
            text="CARGA DO SISTEMA",
            font=("Arial", 8),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        load_color = "#ef4444" if self.system_load > 90 else "#fbbf24"
        self.load_label = tk.Label(
            load_frame,
            text=f"{self.system_load:.1f}%",
            font=("Courier", 18, "bold"),
            fg=load_color,
            bg="#1a1a2e"
        )
        self.load_label.pack(anchor=tk.W)
        
        # Progress bar
        load_progress_frame = tk.Frame(load_frame, bg="#1a1a2e", height=4)
        load_progress_frame.pack(fill=tk.X, pady=(5, 0))
        load_progress_frame.pack_propagate(False)
        
        self.load_progress = tk.Frame(
            load_progress_frame,
            bg=load_color,
            width=int(self.system_load)
        )
        self.load_progress.pack(side=tk.LEFT, fill=tk.Y)
    
    def setup_main_panel(self):
        """Setup the main content panel"""
        main_panel = tk.Frame(
            self.main_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1
        )
        main_panel.pack(fill=tk.BOTH, expand=True)
        
        # Toolbar
        self.setup_toolbar(main_panel)
        
        # Tab content
        self.setup_tab_content(main_panel)
        
        # Footer
        self.setup_footer(main_panel)
    
    def setup_toolbar(self, parent):
        """Setup the toolbar with tab buttons"""
        toolbar = tk.Frame(parent, bg="#0f172a", height=50)
        toolbar.pack(fill=tk.X)
        toolbar.pack_propagate(False)
        
        # Left side: Tab buttons
        left_frame = tk.Frame(toolbar, bg="#0f172a")
        left_frame.pack(side=tk.LEFT, padx=10)
        
        self.algo_tab_btn = tk.Button(
            left_frame,
            text="ALGORITMOS",
            command=lambda: self.switch_tab("ALGORITHMS"),
            font=("Arial", 9, "bold"),
            bg="#1e3a8a" if self.active_tab == "ALGORITHMS" else "transparent",
            fg="#60a5fa" if self.active_tab == "ALGORITHMS" else "#666666",
            activebackground="#1e40af",
            activeforeground="#93c5fd",
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        self.algo_tab_btn.pack(side=tk.LEFT)
        
        self.flow_tab_btn = tk.Button(
            left_frame,
            text="FLUXO DE DECISÃO",
            command=lambda: self.switch_tab("FLOW"),
            font=("Arial", 9, "bold"),
            bg="#1e3a8a" if self.active_tab == "FLOW" else "transparent",
            fg="#60a5fa" if self.active_tab == "FLOW" else "#666666",
            activebackground="#1e40af",
            activeforeground="#93c5fd",
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        self.flow_tab_btn.pack(side=tk.LEFT)
        
        self.decisions_tab_btn = tk.Button(
            left_frame,
            text="HISTÓRICO",
            command=lambda: self.switch_tab("DECISIONS"),
            font=("Arial", 9, "bold"),
            bg="#1e3a8a" if self.active_tab == "DECISIONS" else "transparent",
            fg="#60a5fa" if self.active_tab == "DECISIONS" else "#666666",
            activebackground="#1e40af",
            activeforeground="#93c5fd",
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        self.decisions_tab_btn.pack(side=tk.LEFT)
        
        # Right side: Action button
        right_frame = tk.Frame(toolbar, bg="#0f172a")
        right_frame.pack(side=tk.RIGHT, padx=10)
        
        self.process_btn = tk.Button(
            right_frame,
            text="EXECUTAR DECISÃO",
            command=self.run_decision_process,
            font=("Arial", 9, "bold"),
            bg="#166534",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            relief=tk.RAISED,
            padx=20,
            pady=8,
            state="normal" if not self.is_processing else "disabled"
        )
        self.process_btn.pack()
    
    def setup_tab_content(self, parent):
        """Setup the tab content area"""
        # Container for tab content
        self.tab_content = tk.Frame(parent, bg="#0a0a0a")
        self.tab_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initialize with algorithms tab
        self.show_algorithms_tab()
    
    def setup_footer(self, parent):
        """Setup the footer with system info"""
        footer = tk.Frame(parent, bg="#0f172a", height=80)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        # Content
        content_frame = tk.Frame(footer, bg="#0f172a")
        content_frame.pack(fill=tk.BOTH, padx=15, pady=10)
        
        # Icon
        tk.Label(
            content_frame,
            text="💻",
            font=("Arial", 20),
            fg="#0ea5e9",
            bg="#0f172a"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Text
        text_frame = tk.Frame(content_frame, bg="#0f172a")
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(
            text_frame,
            text="SISTEMA DE CONSENSO ALGORÍTMICO",
            font=("Arial", 10, "bold"),
            fg="#ffffff",
            bg="#0f172a"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        tk.Label(
            text_frame,
            text="O sistema combina decisões de múltiplos algoritmos usando votação ponderada " +
                 "e análise de consenso para produzir decisões mais robustas e confiáveis. " +
                 "A arquitetura híbrida permite adaptação dinâmica a regimes de mercado voláteis.",
            font=("Arial", 8),
            fg="#9ca3af",
            bg="#0f172a",
            wraplength=800,
            justify=tk.LEFT
        ).pack(anchor=tk.W)
    
    def show_algorithms_tab(self):
        """Show algorithms tab content"""
        self.clear_tab_content()
        
        # Create scrollable frame
        canvas = tk.Canvas(self.tab_content, bg="#0a0a0a", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.tab_content, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0a0a0a")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create algorithm cards
        for i, algo in enumerate(self.algorithms):
            self.create_algorithm_card(scrollable_frame, algo, i)
    
    def create_algorithm_card(self, parent, algo: DecisionAlgorithm, index: int):
        """Create a card for an algorithm"""
        card_frame = tk.Frame(
            parent,
            bg="#0a0a0a" if algo.is_active else "#1a1a2e40",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        card_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Header
        header_frame = tk.Frame(card_frame, bg=card_frame.cget("bg"))
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Left: Title and type
        left_frame = tk.Frame(header_frame, bg=card_frame.cget("bg"))
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        title_frame = tk.Frame(left_frame, bg=card_frame.cget("bg"))
        title_frame.pack(anchor=tk.W)
        
        tk.Label(
            title_frame,
            text=algo.name,
            font=("Arial", 11, "bold"),
            fg="#ffffff" if algo.is_active else "#666666",
            bg=card_frame.cget("bg")
        ).pack(side=tk.LEFT)
        
        colors = self.get_algo_color(algo.algo_type)
        type_label = tk.Label(
            title_frame,
            text=algo.algo_type.value,
            font=("Arial", 8, "bold"),
            fg=colors["text"] if algo.is_active else "#666666",
            bg=card_frame.cget("bg"),
            padx=5,
            pady=2
        )
        type_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Description
        tk.Label(
            left_frame,
            text=algo.description,
            font=("Arial", 9),
            fg="#9ca3af" if algo.is_active else "#666666",
            bg=card_frame.cget("bg"),
            wraplength=600,
            justify=tk.LEFT
        ).pack(anchor=tk.W, pady=(2, 0))
        
        # Right: Toggle switch
        right_frame = tk.Frame(header_frame, bg=card_frame.cget("bg"))
        right_frame.pack(side=tk.RIGHT)
        
        self.create_toggle_switch(right_frame, algo)
        
        # Metrics
        metrics_frame = tk.Frame(card_frame, bg=card_frame.cget("bg"))
        metrics_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Accuracy
        acc_frame = tk.Frame(metrics_frame, bg=card_frame.cget("bg"))
        acc_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Label(
            acc_frame,
            text="Precisão",
            font=("Arial", 8),
            fg="#9ca3af" if algo.is_active else "#666666",
            bg=card_frame.cget("bg")
        ).pack(anchor=tk.W)
        
        # Progress bar for accuracy
        prog_frame = tk.Frame(acc_frame, bg="#1a1a2e", height=4)
        prog_frame.pack(fill=tk.X, pady=(2, 0))
        prog_frame.pack_propagate(False)
        
        acc_bar = tk.Frame(
            prog_frame,
            bg="#10b981" if algo.is_active else "#666666",
            width=int(algo.accuracy)
        )
        acc_bar.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(
            acc_frame,
            text=f"{algo.accuracy}%",
            font=("Arial", 9),
            fg="#ffffff" if algo.is_active else "#666666",
            bg=card_frame.cget("bg")
        ).pack(anchor=tk.E)
        
        # Speed
        speed_frame = tk.Frame(metrics_frame, bg=card_frame.cget("bg"))
        speed_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        tk.Label(
            speed_frame,
            text="Velocidade",
            font=("Arial", 8),
            fg="#9ca3af" if algo.is_active else "#666666",
            bg=card_frame.cget("bg")
        ).pack(anchor=tk.W)
        
        # Progress bar for speed
        prog_frame = tk.Frame(speed_frame, bg="#1a1a2e", height=4)
        prog_frame.pack(fill=tk.X, pady=(2, 0))
        prog_frame.pack_propagate(False)
        
        speed_bar = tk.Frame(
            prog_frame,
            bg="#3b82f6" if algo.is_active else "#666666",
            width=int(algo.speed)
        )
        speed_bar.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(
            speed_frame,
            text=f"{algo.speed}",
            font=("Arial", 9),
            fg="#ffffff" if algo.is_active else "#666666",
            bg=card_frame.cget("bg")
        ).pack(anchor=tk.E)
        
        # Specializations
        spec_frame = tk.Frame(card_frame, bg=card_frame.cget("bg"))
        spec_frame.pack(fill=tk.X)
        
        for spec in algo.specialization:
            spec_label = tk.Label(
                spec_frame,
                text=spec,
                font=("Arial", 8),
                fg="#9ca3af" if algo.is_active else "#666666",
                bg="#1a1a2e" if algo.is_active else "#0a0a0a",
                padx=5,
                pady=2,
                relief=tk.RAISED,
                borderwidth=1
            )
            spec_label.pack(side=tk.LEFT, padx=(0, 5))
    
    def create_toggle_switch(self, parent, algo: DecisionAlgorithm):
        """Create a toggle switch for algorithm activation"""
        switch_frame = tk.Frame(parent, bg=parent.cget("bg"))
        switch_frame.pack()
        
        # Create canvas for switch
        switch_canvas = tk.Canvas(
            switch_frame,
            width=40,
            height=20,
            bg=parent.cget("bg"),
            highlightthickness=0
        )
        switch_canvas.pack()
        
        # Draw switch
        if algo.is_active:
            switch_canvas.create_rectangle(0, 0, 40, 20, fill="#10b981", outline="")
            switch_canvas.create_oval(22, 2, 38, 18, fill="white", outline="")
        else:
            switch_canvas.create_rectangle(0, 0, 40, 20, fill="#6b7280", outline="")
            switch_canvas.create_oval(2, 2, 18, 18, fill="white", outline="")
        
        # Bind click event
        switch_canvas.bind("<Button-1>", lambda e, a=algo: self.toggle_algorithm(a))
    
    def show_flow_tab(self):
        """Show decision flow tab content"""
        self.clear_tab_content()
        
        # Create scrollable frame
        canvas = tk.Canvas(self.tab_content, bg="#0a0a0a", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.tab_content, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0a0a0a")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Center the flow
        container = tk.Frame(scrollable_frame, bg="#0a0a0a")
        container.pack(expand=True, pady=20)
        
        # Create flow nodes
        for i, node in enumerate(self.decision_flow):
            self.create_flow_node(container, node, i)
            
            # Add connector line (except for last node)
            if i < len(self.decision_flow) - 1:
                line_frame = tk.Frame(container, bg="#0a0a0a", height=20)
                line_frame.pack()
                line_frame.pack_propagate(False)
                
                line_canvas = tk.Canvas(
                    line_frame,
                    width=300,
                    height=20,
                    bg="#0a0a0a",
                    highlightthickness=0
                )
                line_canvas.pack()
                
                # Draw line
                line_color = "#0ea5e9" if self.decision_flow[i+1].status != NodeStatus.WAITING else "#374151"
                line_canvas.create_line(150, 0, 150, 20, fill=line_color, width=2)
    
    def create_flow_node(self, parent, node: DecisionNode, index: int):
        """Create a flow node"""
        # Determine colors based on status
        if node.status == NodeStatus.PROCESSING:
            bg_color = "#854d0e"
            border_color = "#f59e0b"
            text_color = "#ffffff"
        elif node.status == NodeStatus.COMPLETED:
            bg_color = "#065f46"
            border_color = "#10b981"
            text_color = "#ffffff"
        else:  # WAITING or ERROR
            bg_color = "#374151"
            border_color = "#6b7280"
            text_color = "#9ca3af"
        
        node_frame = tk.Frame(
            parent,
            bg=bg_color,
            relief=tk.RAISED,
            borderwidth=2,
            highlightbackground=border_color,
            padx=20,
            pady=15
        )
        node_frame.pack()
        
        # Header with number and name
        header_frame = tk.Frame(node_frame, bg=bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Node number
        num_frame = tk.Frame(header_frame, bg=bg_color)
        num_frame.pack(side=tk.LEFT, padx=(0, 15))
        
        num_circle = tk.Canvas(
            num_frame,
            width=30,
            height=30,
            bg=bg_color,
            highlightthickness=0
        )
        num_circle.pack()
        num_circle.create_oval(2, 2, 28, 28, fill="#1a1a2e", outline="")
        num_circle.create_text(15, 15, text=str(index + 1), fill=text_color, 
                              font=("Arial", 12, "bold"))
        
        # Node info
        info_frame = tk.Frame(header_frame, bg=bg_color)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(
            info_frame,
            text=node.name,
            font=("Arial", 12, "bold"),
            fg=text_color,
            bg=bg_color
        ).pack(anchor=tk.W)
        
        # Input/Output
        io_frame = tk.Frame(info_frame, bg=bg_color)
        io_frame.pack(anchor=tk.W, pady=(2, 0))
        
        tk.Label(
            io_frame,
            text=node.input_data,
            font=("Courier", 9),
            fg="#9ca3af" if node.status != NodeStatus.WAITING else "#666666",
            bg=bg_color
        ).pack(side=tk.LEFT)
        
        tk.Label(
            io_frame,
            text=" → ",
            font=("Courier", 9),
            fg="#666666",
            bg=bg_color
        ).pack(side=tk.LEFT)
        
        tk.Label(
            io_frame,
            text=node.output_data,
            font=("Courier", 9),
            fg="#9ca3af" if node.status != NodeStatus.WAITING else "#666666",
            bg=bg_color
        ).pack(side=tk.LEFT)
        
        # Right side: Status and timing
        right_frame = tk.Frame(header_frame, bg=bg_color)
        right_frame.pack(side=tk.RIGHT)
        
        # Status icon
        status_text = "✓" if node.status == NodeStatus.COMPLETED else \
                     "⟳" if node.status == NodeStatus.PROCESSING else \
                     "⏱" if node.status == NodeStatus.WAITING else "⚠"
        
        status_color = "#10b981" if node.status == NodeStatus.COMPLETED else \
                      "#fbbf24" if node.status == NodeStatus.PROCESSING else "#666666"
        
        tk.Label(
            right_frame,
            text=status_text,
            font=("Arial", 16),
            fg=status_color,
            bg=bg_color
        ).pack(anchor=tk.E)
        
        # Execution time
        if node.execution_time > 0:
            tk.Label(
                right_frame,
                text=f"{node.execution_time:.2f}s",
                font=("Courier", 9),
                fg="#9ca3af",
                bg=bg_color
            ).pack(anchor=tk.E, pady=(2, 0))
    
    def show_decisions_tab(self):
        """Show recent decisions tab content"""
        self.clear_tab_content()
        
        # Create scrollable frame
        canvas = tk.Canvas(self.tab_content, bg="#0a0a0a", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.tab_content, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0a0a0a")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create decision cards
        for decision in self.recent_decisions:
            self.create_decision_card(scrollable_frame, decision)
    
    def create_decision_card(self, parent, decision: MarketDecision):
        """Create a card for a market decision"""
        card_frame = tk.Frame(
            parent,
            bg="#0a0a0a",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        card_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Header
        header_frame = tk.Frame(card_frame, bg="#0a0a0a")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Left: Decision and timeframe
        left_frame = tk.Frame(header_frame, bg="#0a0a0a")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        decision_color = self.get_decision_color(decision.decision)
        tk.Label(
            left_frame,
            text=decision.decision.value,
            font=("Arial", 14, "bold"),
            fg=decision_color,
            bg="#0a0a0a"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            left_frame,
            text=f"@{decision.timeframe}",
            font=("Arial", 10),
            fg="#9ca3af",
            bg="#0a0a0a"
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        # Timestamp and algorithm
        tk.Label(
            left_frame,
            text=f"{decision.timestamp} | {decision.algorithm}",
            font=("Courier", 9),
            fg="#666666",
            bg="#0a0a0a"
        ).pack(anchor=tk.W, pady=(2, 0))
        
        # Right: Confidence
        right_frame = tk.Frame(header_frame, bg="#0a0a0a")
        right_frame.pack(side=tk.RIGHT)
        
        tk.Label(
            right_frame,
            text=f"{decision.confidence:.1f}%",
            font=("Courier", 16, "bold"),
            fg="#ffffff",
            bg="#0a0a0a"
        ).pack(anchor=tk.E)
        
        tk.Label(
            right_frame,
            text="CONFIANÇA",
            font=("Arial", 8),
            fg="#666666",
            bg="#0a0a0a"
        ).pack(anchor=tk.E)
        
        # Reasoning
        reasoning_frame = tk.Frame(card_frame, bg="#0a0a0a")
        reasoning_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            reasoning_frame,
            text=f'"{decision.reasoning}"',
            font=("Arial", 10, "italic"),
            fg="#d1d5db",
            bg="#0a0a0a",
            wraplength=800,
            justify=tk.LEFT
        ).pack(anchor=tk.W)
        
        # Factors
        factors_frame = tk.Frame(card_frame, bg="#0a0a0a")
        factors_frame.pack(fill=tk.X, pady=(0, 10))
        
        for factor in decision.factors:
            factor_label = tk.Label(
                factors_frame,
                text=factor,
                font=("Courier", 9),
                fg="#9ca3af",
                bg="#1a1a2e",
                padx=8,
                pady=4,
                relief=tk.RAISED,
                borderwidth=1
            )
            factor_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Risk and return
        metrics_frame = tk.Frame(card_frame, bg="#0a0a0a")
        metrics_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Separator
        separator = tk.Frame(metrics_frame, bg="#374151", height=1)
        separator.pack(fill=tk.X, pady=(0, 10))
        
        # Risk
        risk_frame = tk.Frame(metrics_frame, bg="#0a0a0a")
        risk_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(
            risk_frame,
            text="⚠",
            font=("Arial", 12),
            fg="#fbbf24",
            bg="#0a0a0a"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Label(
            risk_frame,
            text=f"Risco: {decision.risk}%",
            font=("Arial", 10),
            fg="#d1d5db",
            bg="#0a0a0a"
        ).pack(side=tk.LEFT)
        
        # Expected return
        return_frame = tk.Frame(metrics_frame, bg="#0a0a0a")
        return_frame.pack(side=tk.LEFT)
        
        tk.Label(
            return_frame,
            text="🎯",
            font=("Arial", 12),
            fg="#10b981",
            bg="#0a0a0a"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Label(
            return_frame,
            text=f"Retorno Esp: +{decision.expected_return}%",
            font=("Arial", 10),
            fg="#10b981",
            bg="#0a0a0a"
        ).pack(side=tk.LEFT)
    
    def clear_tab_content(self):
        """Clear the current tab content"""
        for widget in self.tab_content.winfo_children():
            widget.destroy()
    
    def switch_tab(self, tab_name: str):
        """Switch between tabs"""
        self.active_tab = tab_name
        
        # Update button styles
        self.algo_tab_btn.config(
            bg="#1e3a8a" if tab_name == "ALGORITHMS" else "transparent",
            fg="#60a5fa" if tab_name == "ALGORITHMS" else "#666666"
        )
        self.flow_tab_btn.config(
            bg="#1e3a8a" if tab_name == "FLOW" else "transparent",
            fg="#60a5fa" if tab_name == "FLOW" else "#666666"
        )
        self.decisions_tab_btn.config(
            bg="#1e3a8a" if tab_name == "DECISIONS" else "transparent",
            fg="#60a5fa" if tab_name == "DECISIONS" else "#666666"
        )
        
        # Show appropriate tab content
        if tab_name == "ALGORITHMS":
            self.show_algorithms_tab()
        elif tab_name == "FLOW":
            self.show_flow_tab()
        elif tab_name == "DECISIONS":
            self.show_decisions_tab()
    
    def toggle_algorithm(self, algo: DecisionAlgorithm):
        """Toggle algorithm activation"""
        algo.is_active = not algo.is_active
        
        # Update UI
        active_count = sum(1 for a in self.algorithms if a.is_active)
        
        # Update active algorithms count
        total_count = len(self.algorithms)
        self.active_algo_label.config(text=f"{active_count} / {total_count}")
        
        # Update progress bar
        self.algo_progress.config(width=int((active_count / total_count) * 100))
        
        # Update success rate
        avg_success = sum(a.success_rate for a in self.algorithms if a.is_active)
        avg_success /= active_count if active_count > 0 else 1
        self.success_label.config(text=f"{avg_success:.1f}%")
        self.success_progress.config(width=int(avg_success))
        
        # Refresh algorithms tab
        if self.active_tab == "ALGORITHMS":
            self.show_algorithms_tab()
    
    def run_decision_process(self):
        """Run the decision process simulation"""
        if self.is_processing:
            return
        
        self.is_processing = True
        self.process_btn.config(state="disabled", text="PROCESSANDO...")
        
        # Reset flow
        self.decision_flow = [
            DecisionNode("1", "Coleta de Dados", "Market Data", "Processed Data", 
                        random.random() * 20 + 80, 0.02, NodeStatus.PROCESSING),
            DecisionNode("2", "Pré-processamento", "Raw Data", "Clean Data", 0, 0, NodeStatus.WAITING),
            DecisionNode("3", "Feature Engineering", "Clean Data", "Features", 0, 0, NodeStatus.WAITING),
            DecisionNode("4", "Análise Ensemble", "Features", "Predictions", 0, 0, NodeStatus.WAITING),
            DecisionNode("5", "Validação Cruzada", "Predictions", "Validated", 0, 0, NodeStatus.WAITING),
            DecisionNode("6", "Execução de Decisão", "Validated", "Action", 0, 0, NodeStatus.WAITING)
        ]
        
        # Run simulation in separate thread
        def simulate_flow():
            for i in range(len(self.decision_flow)):
                time.sleep(0.6)  # Delay per step
                
                # Update current node
                self.decision_flow[i] = DecisionNode(
                    self.decision_flow[i].id,
                    self.decision_flow[i].name,
                    self.decision_flow[i].input_data,
                    self.decision_flow[i].output_data,
                    random.random() * 10 + 85,
                    random.random() * 0.5,
                    NodeStatus.COMPLETED
                )
                
                # Update next node if exists
                if i + 1 < len(self.decision_flow):
                    self.decision_flow[i + 1] = DecisionNode(
                        self.decision_flow[i + 1].id,
                        self.decision_flow[i + 1].name,
                        self.decision_flow[i + 1].input_data,
                        self.decision_flow[i + 1].output_data,
                        0,
                        0,
                        NodeStatus.PROCESSING
                    )
                
                # Update UI
                self.root.after(0, lambda idx=i: self.update_flow_ui(idx))
            
            # Finish
            time.sleep(0.5)
            self.root.after(0, self.finish_decision_process)
        
        threading.Thread(target=simulate_flow, daemon=True).start()
    
    def update_flow_ui(self, current_index: int):
        """Update flow UI during simulation"""
        if self.active_tab == "FLOW":
            self.show_flow_tab()
    
    def finish_decision_process(self):
        """Finish the decision process"""
        self.is_processing = False
        self.process_btn.config(state="normal", text="EXECUTAR DECISÃO")
        
        # Add a new decision
        new_decision = MarketDecision(
            id=f"dec-{int(time.time())}",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            algorithm="Ensemble Multi-Algoritmo",
            decision=random.choice([DecisionType.BUY, DecisionType.SELL]),
            confidence=random.random() * 15 + 80,
            reasoning="Processo de decisão manual concluído com sucesso.",
            factors=["Manual Trigger", "Live Analysis"],
            risk=1.5,
            expected_return=3.2,
            timeframe="15m"
        )
        
        self.recent_decisions.insert(0, new_decision)
        self.current_decisions += 1
        self.decisions_label.config(text=f"{self.current_decisions:,}")
        
        # Refresh decisions tab if active
        if self.active_tab == "DECISIONS":
            self.show_decisions_tab()
    
    def start_live_metrics(self):
        """Start live metrics updates"""
        def update_metrics():
            # Update system load
            new_load = max(30, min(99, self.system_load + (random.random() - 0.5) * 5))
            self.system_load = new_load
            
            load_color = "#ef4444" if new_load > 90 else "#fbbf24"
            self.load_label.config(text=f"{new_load:.1f}%", fg=load_color)
            self.load_progress.config(bg=load_color, width=int(new_load))
            
            # Update decisions count
            if random.random() > 0.7:
                increment = random.randint(1, 3)
                self.current_decisions += increment
                self.decisions_label.config(text=f"{self.current_decisions:,}")
            
            # Schedule next update
            self.root.after(2000, update_metrics)
        
        update_metrics()

# Main application
def main():
    root = tk.Tk()
    app = DecisionEngine(root)
    root.mainloop()

if __name__ == "__main__":
    main()