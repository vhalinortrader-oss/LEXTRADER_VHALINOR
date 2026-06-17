import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import threading
import time
import random
from enum import Enum
import asyncio

# Enums para tipos de dados
class TechniqueStatus(Enum):
    CRIANDO = "CRIANDO"
    TESTANDO = "TESTANDO"
    APROVADA = "APROVADA"
    EM_USO = "EM_USO"
    DESCARTADA = "DESCARTADA"

# Estruturas de dados equivalentes às interfaces TypeScript
@dataclass
class Performance:
    win_rate: float
    avg_return: float
    max_drawdown: float
    sharpe_ratio: float

@dataclass
class NeuralTechnique:
    id: str
    name: str
    description: str
    innovation_level: float
    backtest_score: float
    profitability: float
    risk_level: float
    status: TechniqueStatus
    created_at: datetime
    components: List[str]
    performance: Performance

@dataclass
class CreationProcess:
    stage: str
    progress: float
    description: str
    duration: int

@dataclass
class NeuralEvolution:
    generation: int
    population_size: int
    best_fitness: float
    avg_fitness: float
    mutation_rate: float
    crossover_rate: float

@dataclass
class TechniqueTemplate:
    name: str
    description: str
    components: List[str]
    innovation_level: int

class AutonomousNeuralCreatorApp:
    """Aplicação principal que replica a funcionalidade do componente React AutonomousNeuralCreator"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🧠 Criador Neural Autônomo")
        self.root.geometry("1500x1000")
        self.root.configure(bg='#f8fafc')
        
        # Estado da aplicação (equivalente aos useState hooks)
        self.techniques: List[NeuralTechnique] = []
        self.current_creation: Optional[CreationProcess] = None
        self.evolution = NeuralEvolution(
            generation=127,
            population_size=50,
            best_fitness=0.847,
            avg_fitness=0.623,
            mutation_rate=0.15,
            crossover_rate=0.75
        )
        self.is_creating = False
        self.autonomy_level = 94.2
        self.creativity_index = 89.7
        
        # Containers para widgets que precisam ser atualizados
        self.autonomy_badge = None
        self.creativity_badge = None
        self.create_button = None
        self.creation_progress_frame = None
        self.progress_bar = None
        self.progress_label = None
        self.stage_label = None
        self.metrics_labels = {}
        
        # Templates e estágios de criação
        self.initialize_templates()
        self.initialize_creation_stages()
        
        # Configurar estilos
        self.setup_styles()
        
        # Inicializar dados
        self.initialize_data()
        
        # Configurar interface
        self.setup_ui()
        
        # Iniciar thread de evolução (equivalente ao useEffect)
        self.start_evolution_thread()
    
    def setup_styles(self) -> None:
        """Configurar estilos customizados para a aplicação"""
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
        style.configure('Muted.TLabel', foreground='#6b7280')
        
        style.configure('Card.TFrame', 
                       background='white', 
                       relief='solid',
                       borderwidth=1)
    
    # Funções utilitárias (equivalentes às funções do React)
    def get_status_color(self, status: TechniqueStatus) -> str:
        """Obter cor para status (equivalente a getStatusColor)"""
        color_map = {
            TechniqueStatus.CRIANDO: "#f59e0b",
            TechniqueStatus.TESTANDO: "#3b82f6",
            TechniqueStatus.APROVADA: "#10b981",
            TechniqueStatus.EM_USO: "#059669",
            TechniqueStatus.DESCARTADA: "#ef4444"
        }
        return color_map.get(status, "#6b7280")
    
    def get_status_icon(self, status: TechniqueStatus) -> str:
        """Obter ícone para status (equivalente a getStatusIcon)"""
        icon_map = {
            TechniqueStatus.CRIANDO: "🔄",
            TechniqueStatus.TESTANDO: "🧪",
            TechniqueStatus.APROVADA: "✅",
            TechniqueStatus.EM_USO: "⚡",
            TechniqueStatus.DESCARTADA: "⚠️"
        }
        return icon_map.get(status, "📊")
    
    def show_toast(self, message: str) -> None:
        """Mostrar notificação toast"""
        messagebox.showinfo("Criador Neural", message)
    
    # Inicialização de templates e dados
    def initialize_templates(self) -> None:
        """Inicializar templates de técnicas (equivalente aos techniqueTemplates)"""
        self.technique_templates = [
            TechniqueTemplate(
                name='HyperMomentum Fusion',
                description='Combina momentum multi-timeframe com análise fractal e detecção de regime de mercado',
                components=['Momentum Adaptativo', 'Fractais de Mandelbrot', 'Regime Detection', 'Volume Flow'],
                innovation_level=87
            ),
            TechniqueTemplate(
                name='Quantum Arbitrage Engine',
                description='Utiliza princípios de superposição quântica para identificar oportunidades de arbitragem',
                components=['Quantum Entanglement', 'Probabilistic States', 'Multi-Asset Correlation', 'Temporal Shifts'],
                innovation_level=94
            ),
            TechniqueTemplate(
                name='NeuralSwarm Predictor',
                description='Inteligência de enxame combinada com redes neurais profundas para predição de preços',
                components=['Swarm Intelligence', 'Deep LSTM', 'Collective Behavior', 'Emergent Patterns'],
                innovation_level=91
            ),
            TechniqueTemplate(
                name='Chaos Theory Scalper',
                description='Explora a teoria do caos para encontrar ordem em movimentos aparentemente aleatórios',
                components=['Strange Attractors', 'Butterfly Effect', 'Lorenz System', 'Nonlinear Dynamics'],
                innovation_level=89
            ),
            TechniqueTemplate(
                name='Biomimetic Trading AI',
                description='Imita comportamentos de predadores naturais para capturar movimentos de mercado',
                components=['Predator-Prey Models', 'Hunting Strategies', 'Pack Behavior', 'Territory Mapping'],
                innovation_level=85
            )
        ]
    
    def initialize_creation_stages(self) -> None:
        """Inicializar estágios de criação (equivalente aos creationStages)"""
        self.creation_stages = [
            CreationProcess('Análise de Padrões', 0, 'Identificando novos padrões nos dados históricos', 3000),
            CreationProcess('Síntese Neural', 0, 'Combinando elementos de diferentes estratégias', 4000),
            CreationProcess('Otimização Genética', 0, 'Aplicando algoritmos genéticos para refinar a técnica', 5000),
            CreationProcess('Simulação Monte Carlo', 0, 'Testando robustez em múltiplos cenários', 6000),
            CreationProcess('Validação Cruzada', 0, 'Verificando consistência em diferentes períodos', 4000),
            CreationProcess('Implementação', 0, 'Preparando técnica para uso operacional', 2000)
        ]
    
    def initialize_data(self) -> None:
        """Inicializar dados da aplicação (equivalente ao useEffect inicial)"""
        # Técnicas iniciais
        initial_techniques = [
            NeuralTechnique(
                id='1',
                name='HyperMomentum Fusion',
                description='Combina momentum multi-timeframe com análise fractal',
                innovation_level=87.3,
                backtest_score=92.1,
                profitability=18.7,
                risk_level=23.4,
                status=TechniqueStatus.EM_USO,
                created_at=datetime.now(),
                components=['Momentum Adaptativo', 'Fractais', 'Regime Detection'],
                performance=Performance(win_rate=73.2, avg_return=2.4, max_drawdown=8.1, sharpe_ratio=1.85)
            ),
            NeuralTechnique(
                id='2',
                name='Quantum Arbitrage Engine',
                description='Utiliza princípios quânticos para arbitragem',
                innovation_level=94.1,
                backtest_score=87.9,
                profitability=22.3,
                risk_level=19.8,
                status=TechniqueStatus.TESTANDO,
                created_at=datetime.now(),
                components=['Quantum States', 'Superposição', 'Multi-Asset'],
                performance=Performance(win_rate=68.9, avg_return=3.1, max_drawdown=6.7, sharpe_ratio=2.12)
            )
        ]
        self.techniques = initial_techniques
    
    # Função principal de criação (equivalente a createNewTechnique)
    def create_new_technique(self) -> None:
        """Criar nova técnica neural (equivalente a createNewTechnique)"""
        if self.is_creating:
            return
        
        # Iniciar processo em thread separada
        threading.Thread(target=self._creation_worker, daemon=True).start()
    
    def _creation_worker(self) -> None:
        """Worker thread para criação de técnicas"""
        self.is_creating = True
        self.root.after(0, self._update_creation_ui)
        
        # Selecionar template aleatório
        template = random.choice(self.technique_templates)
        
        # Simular processo de criação
        for i, stage in enumerate(self.creation_stages):
            # Atualizar estágio atual
            self.current_creation = CreationProcess(
                stage=stage.stage,
                progress=0,
                description=stage.description,
                duration=stage.duration
            )
            self.root.after(0, self._update_progress_display)
            
            # Animar progresso
            for progress in range(0, 101, 2):
                self.current_creation.progress = progress
                self.root.after(0, self._update_progress_bar)
                time.sleep(stage.duration / 50 / 1000)  # Converter para segundos
        
        # Criar nova técnica
        new_technique = NeuralTechnique(
            id=str(int(time.time())),
            name=f"{template.name} v{random.randint(1, 10)}",
            description=template.description,
            innovation_level=template.innovation_level + (random.random() - 0.5) * 10,
            backtest_score=70 + random.random() * 25,
            profitability=10 + random.random() * 20,
            risk_level=15 + random.random() * 25,
            status=TechniqueStatus.APROVADA,
            created_at=datetime.now(),
            components=template.components,
            performance=Performance(
                win_rate=55 + random.random() * 25,
                avg_return=1 + random.random() * 3,
                max_drawdown=3 + random.random() * 12,
                sharpe_ratio=1 + random.random() * 1.5
            )
        )
        
        # Adicionar à lista
        self.techniques = [new_technique] + self.techniques
        
        # Finalizar processo
        self.current_creation = None
        self.is_creating = False
        self.root.after(0, self._finalize_creation)
        
        # Mostrar notificação
        self.root.after(0, lambda: self.show_toast(f"Nova técnica criada: {new_technique.name}"))
    
    def _update_creation_ui(self) -> None:
        """Atualizar UI durante criação"""
        if self.create_button:
            self.create_button.config(text="🔄 Criando Técnica...", state="disabled")
        
        if self.creation_progress_frame:
            self.creation_progress_frame.grid()
    
    def _update_progress_display(self) -> None:
        """Atualizar display de progresso"""
        if self.stage_label and self.current_creation:
            self.stage_label.config(text=self.current_creation.stage)
    
    def _update_progress_bar(self) -> None:
        """Atualizar barra de progresso"""
        if self.progress_bar and self.current_creation:
            self.progress_bar['value'] = self.current_creation.progress
        
        if self.progress_label and self.current_creation:
            self.progress_label.config(text=f"{self.current_creation.progress:.0f}%")
    
    def _finalize_creation(self) -> None:
        """Finalizar processo de criação"""
        if self.create_button:
            self.create_button.config(text="✨ Liberar Criatividade Neural", state="normal")
        
        if self.creation_progress_frame:
            self.creation_progress_frame.grid_remove()
        
        self.update_metrics_display()
    
    # Configuração da interface gráfica
    def setup_ui(self) -> None:
        """Configurar interface principal"""
        # Frame principal com scroll
        main_canvas = tk.Canvas(self.root, bg='#f8fafc')
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Container principal
        container = ttk.Frame(scrollable_frame, padding="20", style='Card.TFrame')
        container.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=20, pady=20)
        
        # Cabeçalho
        self.setup_header(container)
        
        # Notebook para abas (equivalente ao Tabs do React)
        self.setup_notebook(container)
        
        # Configurar scroll
        main_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        scrollable_frame.columnconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
    
    def setup_header(self, parent: ttk.Frame) -> None:
        """Configurar cabeçalho da aplicação"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Título
        title_label = ttk.Label(header_frame, 
                               text="🧠 Criador Neural Autônomo", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Badges de status
        badges_frame = ttk.Frame(header_frame)
        badges_frame.grid(row=0, column=1, sticky=tk.E)
        
        # Badge autonomia
        self.autonomy_badge = tk.Label(badges_frame, 
                                      text=f"✨ Autonomia: {self.autonomy_level:.1f}%",
                                      bg="#3b82f6",
                                      fg="white",
                                      font=("Arial", 10, "bold"),
                                      padx=10, pady=5)
        self.autonomy_badge.grid(row=0, column=0, padx=(0, 10))
        
        # Badge criatividade
        self.creativity_badge = tk.Label(badges_frame, 
                                        text=f"💡 Criatividade: {self.creativity_index:.1f}%",
                                        bg="#10b981",
                                        fg="white",
                                        font=("Arial", 10, "bold"),
                                        padx=10, pady=5)
        self.creativity_badge.grid(row=0, column=1)
        
        header_frame.columnconfigure(0, weight=1)
    
    def setup_notebook(self, parent: ttk.Frame) -> None:
        """Configurar notebook com abas (equivalente ao Tabs do React)"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Aba Criação Ativa
        creation_frame = ttk.Frame(self.notebook)
        self.notebook.add(creation_frame, text="🎯 Criação Ativa")
        self.setup_creation_tab(creation_frame)
        
        # Aba Técnicas Criadas
        techniques_frame = ttk.Frame(self.notebook)
        self.notebook.add(techniques_frame, text="🧠 Técnicas Criadas")
        self.setup_techniques_tab(techniques_frame)
        
        # Aba Evolução Neural
        evolution_frame = ttk.Frame(self.notebook)
        self.notebook.add(evolution_frame, text="🧬 Evolução Neural")
        self.setup_evolution_tab(evolution_frame)
    
    def setup_creation_tab(self, parent: ttk.Frame) -> None:
        """Configurar aba de criação ativa (equivalente ao TabsContent creation)"""
        creation_container = ttk.Frame(parent, padding="30")
        creation_container.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Botão principal de criação
        self.create_button = tk.Button(creation_container, 
                                      text="✨ Liberar Criatividade Neural",
                                      bg="#3b82f6", fg="white",
                                      font=("Arial", 14, "bold"),
                                      padx=30, pady=15,
                                      cursor="hand2",
                                      command=self.create_new_technique)
        self.create_button.grid(row=0, column=0, pady=(0, 30))
        
        # Frame de progresso (inicialmente oculto)
        self.creation_progress_frame = ttk.LabelFrame(creation_container, 
                                                     text="Processo de Criação", 
                                                     padding="20",
                                                     style='Card.TFrame')
        
        # Estágio atual
        self.stage_label = ttk.Label(self.creation_progress_frame, 
                                    text="",
                                    font=("Arial", 12, "bold"))
        self.stage_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Progresso
        progress_frame = ttk.Frame(self.creation_progress_frame)
        progress_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.progress_label = ttk.Label(progress_frame, text="0%", 
                                       style='Info.TLabel', font=("Arial", 10, "bold"))
        self.progress_label.grid(row=0, column=1, sticky=tk.E, padx=(10, 0))
        
        progress_frame.columnconfigure(0, weight=1)
        
        # Descrição
        self.description_label = ttk.Label(self.creation_progress_frame, 
                                          text="",
                                          style='Muted.TLabel',
                                          font=("Arial", 10))
        self.description_label.grid(row=2, column=0, sticky=tk.W)
        
        self.creation_progress_frame.columnconfigure(0, weight=1)
        
        # Grid de métricas
        metrics_grid = ttk.Frame(creation_container)
        metrics_grid.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=30)
        
        # Técnicas Ativas
        active_card = ttk.LabelFrame(metrics_grid, text="🔗 Técnicas Ativas", padding="20")
        active_card.grid(row=0, column=0, padx=(0, 20), sticky=(tk.W, tk.E))
        
        active_count = len([t for t in self.techniques if t.status == TechniqueStatus.EM_USO])
        self.metrics_labels['active'] = ttk.Label(active_card, text=str(active_count), 
                                                 font=("Arial", 20, "bold"), style='Info.TLabel')
        self.metrics_labels['active'].grid(row=0, column=0)
        
        # Em Desenvolvimento
        dev_card = ttk.LabelFrame(metrics_grid, text="🖥️ Em Desenvolvimento", padding="20")
        dev_card.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        dev_count = len([t for t in self.techniques if t.status in [TechniqueStatus.CRIANDO, TechniqueStatus.TESTANDO]])
        self.metrics_labels['dev'] = ttk.Label(dev_card, text=str(dev_count), 
                                              font=("Arial", 20, "bold"), style='Warning.TLabel')
        self.metrics_labels['dev'].grid(row=0, column=0)
        
        metrics_grid.columnconfigure(0, weight=1)
        metrics_grid.columnconfigure(1, weight=1)
        creation_container.columnconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
    
    def setup_techniques_tab(self, parent: ttk.Frame) -> None:
        """Configurar aba de técnicas criadas (equivalente ao TabsContent techniques)"""
        techniques_container = ttk.Frame(parent, padding="20")
        techniques_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Canvas com scroll para técnicas
        canvas = tk.Canvas(techniques_container, bg='#f8fafc', height=400)
        scrollbar = ttk.Scrollbar(techniques_container, orient="vertical", command=canvas.yview)
        techniques_scrollable = ttk.Frame(canvas)
        
        techniques_scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=techniques_scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Criar cards de técnicas
        for i, technique in enumerate(self.techniques):
            self.create_technique_card(techniques_scrollable, technique, i)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        techniques_container.columnconfigure(0, weight=1)
        techniques_container.rowconfigure(0, weight=1)
        techniques_scrollable.columnconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
    
    def create_technique_card(self, parent: ttk.Frame, technique: NeuralTechnique, index: int) -> None:
        """Criar card individual de técnica"""
        card_frame = ttk.LabelFrame(parent, text="", padding="15", style='Card.TFrame')
        card_frame.grid(row=index, column=0, sticky=(tk.W, tk.E), pady=8, padx=10)
        
        # Header da técnica
        header_frame = ttk.Frame(card_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Nome e ícone
        name_frame = ttk.Frame(header_frame)
        name_frame.grid(row=0, column=0, sticky=tk.W)
        
        status_icon = self.get_status_icon(technique.status)
        ttk.Label(name_frame, text=status_icon, font=("Arial", 12)).grid(row=0, column=0, padx=(0, 5))
        ttk.Label(name_frame, text=technique.name, 
                 font=("Arial", 12, "bold")).grid(row=0, column=1)
        
        # Status badge
        status_color = self.get_status_color(technique.status)
        status_label = tk.Label(header_frame, 
                               text=technique.status.value,
                               bg=status_color,
                               fg="white",
                               font=("Arial", 8, "bold"),
                               padx=8, pady=2)
        status_label.grid(row=0, column=1, sticky=tk.E)
        
        header_frame.columnconfigure(0, weight=1)
        
        # Descrição
        desc_label = ttk.Label(card_frame, text=technique.description, 
                              style='Muted.TLabel', font=("Arial", 9),
                              wraplength=800)
        desc_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        # Grid de métricas
        metrics_frame = ttk.Frame(card_frame)
        metrics_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        metrics_data = [
            ("Inovação", f"{technique.innovation_level:.1f}%", "#3b82f6"),
            ("Backtest", f"{technique.backtest_score:.1f}%", "#10b981"),
            ("Lucro", f"{technique.profitability:.1f}%", "#059669"),
            ("Risco", f"{technique.risk_level:.1f}%", "#f59e0b")
        ]
        
        for i, (label, value, color) in enumerate(metrics_data):
            metric_col = ttk.Frame(metrics_frame)
            metric_col.grid(row=0, column=i, padx=(0, 15) if i < 3 else (0, 0))
            
            ttk.Label(metric_col, text=label, style='Muted.TLabel', 
                     font=("Arial", 8)).grid(row=0, column=0)
            
            value_label = tk.Label(metric_col, text=value, fg=color, 
                                  font=("Arial", 8, "bold"), bg='#f8fafc')
            value_label.grid(row=1, column=0)
        
        # Componentes
        components_frame = ttk.Frame(card_frame)
        components_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        for i, component in enumerate(technique.components):
            comp_badge = tk.Label(components_frame, 
                                 text=component,
                                 bg="#f1f5f9",
                                 fg="#6b7280",
                                 font=("Arial", 8),
                                 relief='solid',
                                 borderwidth=1,
                                 padx=6, pady=2)
            comp_badge.grid(row=i//3, column=i%3, padx=2, pady=2, sticky=tk.W)
        
        card_frame.columnconfigure(0, weight=1)
    
    def setup_evolution_tab(self, parent: ttk.Frame) -> None:
        """Configurar aba de evolução neural (equivalente ao TabsContent evolution)"""
        evolution_container = ttk.Frame(parent, padding="20")
        evolution_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid de métricas evolutivas
        evolution_grid = ttk.Frame(evolution_container)
        evolution_grid.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Card Geração Atual
        gen_card = ttk.LabelFrame(evolution_grid, text="Evolução", padding="15")
        gen_card.grid(row=0, column=0, padx=(0, 10), sticky=(tk.W, tk.E))
        
        gen_frame = ttk.Frame(gen_card)
        gen_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(gen_frame, text="Geração Atual", 
                 style='Muted.TLabel', font=("Arial", 9)).grid(row=0, column=0, sticky=tk.W)
        self.metrics_labels['generation'] = ttk.Label(gen_frame, text=str(self.evolution.generation), 
                                                     font=("Arial", 12, "bold"), style='Info.TLabel')
        self.metrics_labels['generation'].grid(row=0, column=1, sticky=tk.E)
        
        ttk.Label(gen_frame, text="População", 
                 style='Muted.TLabel', font=("Arial", 9)).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        ttk.Label(gen_frame, text=str(self.evolution.population_size), 
                 font=("Arial", 12, "bold")).grid(row=1, column=1, sticky=tk.E, pady=(5, 0))
        
        gen_frame.columnconfigure(0, weight=1)
        
        # Card Fitness
        fitness_card = ttk.LabelFrame(evolution_grid, text="Fitness", padding="15")
        fitness_card.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        fitness_frame = ttk.Frame(fitness_card)
        fitness_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(fitness_frame, text="Melhor Fitness", 
                 style='Muted.TLabel', font=("Arial", 9)).grid(row=0, column=0, sticky=tk.W)
        self.metrics_labels['best_fitness'] = ttk.Label(fitness_frame, 
                                                       text=f"{(self.evolution.best_fitness * 100):.1f}%", 
                                                       font=("Arial", 12, "bold"), style='Success.TLabel')
        self.metrics_labels['best_fitness'].grid(row=0, column=1, sticky=tk.E)
        
        ttk.Label(fitness_frame, text="Fitness Médio", 
                 style='Muted.TLabel', font=("Arial", 9)).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.metrics_labels['avg_fitness'] = ttk.Label(fitness_frame, 
                                                      text=f"{(self.evolution.avg_fitness * 100):.1f}%", 
                                                      font=("Arial", 12, "bold"), style='Info.TLabel')
        self.metrics_labels['avg_fitness'].grid(row=1, column=1, sticky=tk.E, pady=(5, 0))
        
        fitness_frame.columnconfigure(0, weight=1)
        
        evolution_grid.columnconfigure(0, weight=1)
        evolution_grid.columnconfigure(1, weight=1)
        
        # Parâmetros evolutivos
        params_card = ttk.LabelFrame(evolution_container, text="⚙️ Parâmetros Evolutivos", padding="20")
        params_card.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Taxa de mutação
        mutation_frame = ttk.Frame(params_card)
        mutation_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(mutation_frame, text="Taxa de Mutação", 
                 font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(mutation_frame, text=f"{(self.evolution.mutation_rate * 100):.0f}%", 
                 font=("Arial", 10, "bold")).grid(row=0, column=1, sticky=tk.E)
        
        mutation_progress = ttk.Progressbar(mutation_frame, length=300, mode='determinate')
        mutation_progress['value'] = self.evolution.mutation_rate * 100
        mutation_progress.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        mutation_frame.columnconfigure(0, weight=1)
        
        # Taxa de crossover
        crossover_frame = ttk.Frame(params_card)
        crossover_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(crossover_frame, text="Taxa de Crossover", 
                 font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(crossover_frame, text=f"{(self.evolution.crossover_rate * 100):.0f}%", 
                 font=("Arial", 10, "bold")).grid(row=0, column=1, sticky=tk.E)
        
        crossover_progress = ttk.Progressbar(crossover_frame, length=300, mode='determinate')
        crossover_progress['value'] = self.evolution.crossover_rate * 100
        crossover_progress.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        crossover_frame.columnconfigure(0, weight=1)
        params_card.columnconfigure(0, weight=1)
        
        # Card de evolução contínua
        continuous_card = tk.Frame(evolution_container, bg="#eff6ff", relief='solid', borderwidth=1)
        continuous_card.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        continuous_content = tk.Frame(continuous_card, bg="#eff6ff")
        continuous_content.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=20, pady=15)
        
        # Título
        title_frame = tk.Frame(continuous_content, bg="#eff6ff")
        title_frame.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(title_frame, text="📊", font=("Arial", 12)).grid(row=0, column=0, padx=(0, 5))
        
        title_label = tk.Label(title_frame, text="Evolução Contínua Ativa", 
                              bg="#eff6ff", font=("Arial", 10, "bold"))
        title_label.grid(row=0, column=1)
        
        # Descrição
        desc_label = tk.Label(continuous_content, 
                             text="A rede neural está constantemente evoluindo suas técnicas, testando novas combinações e otimizando parâmetros para maximizar performance e minimizar riscos.",
                             bg="#eff6ff", fg="#6b7280", font=("Arial", 9),
                             wraplength=700)
        desc_label.grid(row=1, column=0, sticky=tk.W)
        
        continuous_content.columnconfigure(0, weight=1)
        continuous_card.columnconfigure(0, weight=1)
        evolution_container.columnconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
    
    def update_metrics_display(self) -> None:
        """Atualizar displays de métricas"""
        # Atualizar badges do header
        if self.autonomy_badge:
            self.autonomy_badge.config(text=f"✨ Autonomia: {self.autonomy_level:.1f}%")
        
        if self.creativity_badge:
            self.creativity_badge.config(text=f"💡 Criatividade: {self.creativity_index:.1f}%")
        
        # Atualizar métricas da evolução
        if 'generation' in self.metrics_labels:
            self.metrics_labels['generation'].config(text=str(self.evolution.generation))
        
        if 'best_fitness' in self.metrics_labels:
            self.metrics_labels['best_fitness'].config(text=f"{(self.evolution.best_fitness * 100):.1f}%")
        
        if 'avg_fitness' in self.metrics_labels:
            self.metrics_labels['avg_fitness'].config(text=f"{(self.evolution.avg_fitness * 100):.1f}%")
        
        # Atualizar contadores de técnicas
        if 'active' in self.metrics_labels:
            active_count = len([t for t in self.techniques if t.status == TechniqueStatus.EM_USO])
            self.metrics_labels['active'].config(text=str(active_count))
        
        if 'dev' in self.metrics_labels:
            dev_count = len([t for t in self.techniques if t.status in [TechniqueStatus.CRIANDO, TechniqueStatus.TESTANDO]])
            self.metrics_labels['dev'].config(text=str(dev_count))
    
    def start_evolution_thread(self) -> None:
        """Iniciar thread de evolução (equivalente ao useEffect)"""
        def evolution_worker():
            while True:
                # Atualizar evolução
                self.evolution.generation += 1
                self.evolution.best_fitness = min(1, self.evolution.best_fitness + (random.random() - 0.4) * 0.02)
                self.evolution.avg_fitness = min(0.9, self.evolution.avg_fitness + (random.random() - 0.45) * 0.015)
                
                # Atualizar índices
                self.autonomy_level = max(85, min(99, self.autonomy_level + (random.random() - 0.5) * 3))
                self.creativity_index = max(80, min(97, self.creativity_index + (random.random() - 0.5) * 4))
                
                # Atualizar UI na thread principal
                self.root.after(0, self.update_metrics_display)
                
                time.sleep(8)  # Equivalente ao interval de 8000ms do React
        
        threading.Thread(target=evolution_worker, daemon=True).start()


def main() -> None:
    """Função principal para executar a aplicação (equivalente ao export do React)"""
    root = tk.Tk()
    app = AutonomousNeuralCreatorApp(root)
    
    # Tornar a janela responsiva
    root.minsize(1300, 900)
    
    # Centralizar janela
    root.eval('tk::PlaceWindow . center')
    
    # Iniciar loop principal
    root.mainloop()


if __name__ == "__main__":
    main()
