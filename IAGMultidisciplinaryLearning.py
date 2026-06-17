import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
from typing import List, Literal
from datetime import datetime
import threading
import time
import random
from enum import Enum

# Enums para tipos de dados
class SourceType(Enum):
    HISTORICAL = "HISTORICAL"
    NEWS = "NEWS"
    SOCIAL = "SOCIAL"
    ECONOMIC = "ECONOMIC"
    BEHAVIORAL = "BEHAVIORAL"

class ImpactLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class InsightCategory(Enum):
    PATTERN = "PATTERN"
    TREND = "TREND"
    ANOMALY = "ANOMALY"
    OPPORTUNITY = "OPPORTUNITY"

# Estruturas de dados equivalentes às interfaces TypeScript
@dataclass
class LearningSource:
    id: str
    name: str
    type: SourceType
    data_points: int
    learning_rate: float
    accuracy: float
    influence: float
    last_update: datetime
    insights: List[str]
    patterns: int

@dataclass
class CrossDomainConnection:
    source: str
    target: str
    correlation: float
    strength: float
    insight: str
    discovered_at: datetime

@dataclass
class HolisticInsight:
    id: str
    title: str
    description: str
    confidence: float
    sources: List[str]
    impact: ImpactLevel
    category: InsightCategory
    timestamp: datetime

class IAGMultidisciplinaryLearningApp:
    """Aplicação principal que replica a funcionalidade do componente React IAGMultidisciplinaryLearning"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("📚 Aprendizado Multidisciplinar IAG")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#f8fafc')
        
        # Estado da aplicação (equivalente aos useState hooks)
        self.learning_sources: List[LearningSource] = []
        self.cross_domain_connections: List[CrossDomainConnection] = []
        self.holistic_insights: List[HolisticInsight] = []
        self.overall_learning_rate = 0.0
        self.knowledge_integration = 0.0
        
        # Containers para widgets que precisam ser atualizados
        self.learning_badge = None
        self.integration_badge = None
        self.sources_frame = None
        self.connections_frame = None
        self.insights_frame = None
        self.metrics_labels = {}
        
        # Thread de atualização
        self.update_thread = None
        self.stop_updates = False
        
        # Configurar estilos
        self.setup_styles()
        
        # Configurar interface
        self.setup_ui()
        
        # Iniciar aprendizado (equivalente ao useEffect)
        self.start_learning_engine()
    
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
    def get_source_type_icon(self, source_type: SourceType) -> str:
        """Obter ícone para tipo de fonte (equivalente a getSourceTypeIcon)"""
        icon_map = {
            SourceType.HISTORICAL: "🗄️",
            SourceType.NEWS: "📄",
            SourceType.SOCIAL: "👥",
            SourceType.ECONOMIC: "📊",
            SourceType.BEHAVIORAL: "🧠"
        }
        return icon_map.get(source_type, "📚")
    
    def get_impact_color(self, impact: ImpactLevel) -> str:
        """Obter cor para impacto (equivalente a getImpactColor)"""
        color_map = {
            ImpactLevel.CRITICAL: "#8b5cf6",
            ImpactLevel.HIGH: "#10b981",
            ImpactLevel.MEDIUM: "#f59e0b",
            ImpactLevel.LOW: "#6b7280"
        }
        return color_map.get(impact, "#6b7280")
    
    def get_category_icon(self, category: InsightCategory) -> str:
        """Obter ícone para categoria (equivalente a getCategoryIcon)"""
        icon_map = {
            InsightCategory.PATTERN: "📈",
            InsightCategory.TREND: "📊",
            InsightCategory.ANOMALY: "🔄",
            InsightCategory.OPPORTUNITY: "💡"
        }
        return icon_map.get(category, "📚")
    
    # Funções de inicialização (equivalentes às funções do React)
    def init_learning_sources(self) -> List[LearningSource]:
        """Inicializar fontes de aprendizado (equivalente a initLearningSources)"""
        return [
            LearningSource(
                id='historical',
                name='Dados Históricos de Mercado',
                type=SourceType.HISTORICAL,
                data_points=47382000,
                learning_rate=94.7,
                accuracy=96.8,
                influence=28.5,
                last_update=datetime.now(),
                insights=[
                    'Padrões sazonais em commodities identificados',
                    'Correlações de longo prazo entre índices',
                    'Ciclos de volatilidade mapeados'
                ],
                patterns=18742
            ),
            LearningSource(
                id='news',
                name='Análise de Notícias Financeiras',
                type=SourceType.NEWS,
                data_points=12947000,
                learning_rate=91.3,
                accuracy=89.2,
                influence=22.8,
                last_update=datetime.now(),
                insights=[
                    'Impacto de headlines nas primeiras 15min',
                    'Correlação entre sentiment de notícias e preço',
                    'Padrões de reação por setor'
                ],
                patterns=7834
            ),
            LearningSource(
                id='social',
                name='Redes Sociais e Sentiment',
                type=SourceType.SOCIAL,
                data_points=28374000,
                learning_rate=87.6,
                accuracy=82.4,
                influence=18.7,
                last_update=datetime.now(),
                insights=[
                    'Influenciadores que movem mercados',
                    'Trending topics que impactam trading',
                    'Comportamento retail vs institucional'
                ],
                patterns=12456
            ),
            LearningSource(
                id='economic',
                name='Relatórios Econômicos',
                type=SourceType.ECONOMIC,
                data_points=5683000,
                learning_rate=96.1,
                accuracy=94.7,
                influence=24.3,
                last_update=datetime.now(),
                insights=[
                    'Leading indicators mais eficazes',
                    'Timing de reação a dados macro',
                    'Divergências entre expectativa e realidade'
                ],
                patterns=3721
            ),
            LearningSource(
                id='behavioral',
                name='Comportamento de Mercado',
                type=SourceType.BEHAVIORAL,
                data_points=19264000,
                learning_rate=89.4,
                accuracy=87.9,
                influence=19.2,
                last_update=datetime.now(),
                insights=[
                    'Psicologia de massas em crashes',
                    'Padrões de FOMO e panic selling',
                    'Comportamento em diferentes volatilidades'
                ],
                patterns=9187
            )
        ]
    
    def generate_cross_domain_connections(self) -> List[CrossDomainConnection]:
        """Gerar conexões cross-domain (equivalente a generateCrossDomainConnections)"""
        return [
            CrossDomainConnection(
                source='Dados Históricos',
                target='Sentiment Social',
                correlation=0.73,
                strength=89.4,
                insight='Sentiment extremo antecede reversões históricas em 72% dos casos',
                discovered_at=datetime.now()
            ),
            CrossDomainConnection(
                source='Notícias Econômicas',
                target='Comportamento Retail',
                correlation=0.68,
                strength=82.7,
                insight='Retail trading aumenta 34% nas 2h após releases econômicos importantes',
                discovered_at=datetime.now()
            ),
            CrossDomainConnection(
                source='Padrões Técnicos',
                target='Eventos Geopolíticos',
                correlation=0.81,
                strength=91.2,
                insight='Breakouts falham 67% mais durante tensões geopolíticas',
                discovered_at=datetime.now()
            )
        ]
    
    def generate_holistic_insights(self) -> List[HolisticInsight]:
        """Gerar insights holísticos (equivalente a generateHolisticInsights)"""
        return [
            HolisticInsight(
                id='insight_001',
                title='Convergência Multi-Domínio Detectada',
                description='Análise cruzada de 5 domínios indica alta probabilidade de movimento direcional forte no EUR/USD nas próximas 48h',
                confidence=94.3,
                sources=['Histórico', 'Notícias', 'Social', 'Econômico'],
                impact=ImpactLevel.HIGH,
                category=InsightCategory.OPPORTUNITY,
                timestamp=datetime.now()
            ),
            HolisticInsight(
                id='insight_002',
                title='Anomalia Comportamental Emergente',
                description='Padrão atípico identificado: institucionais reduzindo posições enquanto retail aumenta, sugere cautela',
                confidence=87.9,
                sources=['Comportamental', 'Histórico', 'Social'],
                impact=ImpactLevel.MEDIUM,
                category=InsightCategory.ANOMALY,
                timestamp=datetime.now()
            ),
            HolisticInsight(
                id='insight_003',
                title='Padrão Sazonal Confirmado',
                description='Dados de 15 anos confirmam: volatilidade de commodities aumenta 23% na terceira semana do mês',
                confidence=91.7,
                sources=['Histórico', 'Econômico'],
                impact=ImpactLevel.MEDIUM,
                category=InsightCategory.PATTERN,
                timestamp=datetime.now()
            )
        ]
    
    def update_learning_metrics(self) -> None:
        """Atualizar métricas de aprendizado (equivalente a updateLearningMetrics)"""
        # Atualizar fontes de aprendizado
        updated_sources = []
        for source in self.learning_sources:
            updated_source = LearningSource(
                id=source.id,
                name=source.name,
                type=source.type,
                data_points=source.data_points + random.randint(0, 10000),
                learning_rate=max(80, min(99, source.learning_rate + (random.random() - 0.4) * 2)),
                accuracy=max(75, min(99, source.accuracy + (random.random() - 0.3) * 1.5)),
                influence=source.influence,
                last_update=datetime.now(),
                insights=source.insights,
                patterns=source.patterns + random.randint(0, 50)
            )
            updated_sources.append(updated_source)
        
        self.learning_sources = updated_sources
        self.cross_domain_connections = self.generate_cross_domain_connections()
        self.holistic_insights = self.generate_holistic_insights()
        
        # Calcular métricas gerais
        if self.learning_sources:
            self.overall_learning_rate = sum(s.learning_rate for s in self.learning_sources) / len(self.learning_sources)
            self.knowledge_integration = sum(s.accuracy for s in self.learning_sources) / len(self.learning_sources)
        
        # Atualizar UI na thread principal
        self.root.after(0, self.update_ui)
    
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
        
        # Lado esquerdo: ícone e título
        left_frame = ttk.Frame(header_frame)
        left_frame.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(left_frame, text="📚", font=("Arial", 18)).grid(row=0, column=0, padx=(0, 8))
        ttk.Label(left_frame, text="📚 Aprendizado Multidisciplinar IAG", 
                 font=("Arial", 18, "bold")).grid(row=0, column=1)
        
        # Lado direito: badges
        right_frame = ttk.Frame(header_frame)
        right_frame.grid(row=0, column=1, sticky=tk.E)
        
        # Badge aprendizado
        self.learning_badge = tk.Label(right_frame, 
                                      text=f"🔄 Aprendendo: {self.overall_learning_rate:.1f}%",
                                      bg="#3b82f6",
                                      fg="white",
                                      font=("Arial", 9, "bold"),
                                      padx=8, pady=4)
        self.learning_badge.grid(row=0, column=0, padx=(0, 8))
        
        # Badge integração
        self.integration_badge = tk.Label(right_frame, 
                                         text=f"🔗 Integração: {self.knowledge_integration:.1f}%",
                                         bg="#10b981",
                                         fg="white",
                                         font=("Arial", 9, "bold"),
                                         padx=8, pady=4)
        self.integration_badge.grid(row=0, column=1)
        
        header_frame.columnconfigure(0, weight=1)
    
    def setup_notebook(self, parent: ttk.Frame) -> None:
        """Configurar notebook com abas (equivalente ao Tabs do React)"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Aba Fontes
        sources_frame = ttk.Frame(self.notebook)
        self.notebook.add(sources_frame, text="📊 Fontes")
        self.setup_sources_tab(sources_frame)
        
        # Aba Conexões
        connections_frame = ttk.Frame(self.notebook)
        self.notebook.add(connections_frame, text="🔗 Conexões")
        self.setup_connections_tab(connections_frame)
        
        # Aba Insights
        insights_frame = ttk.Frame(self.notebook)
        self.notebook.add(insights_frame, text="💡 Insights")
        self.setup_insights_tab(insights_frame)
        
        # Aba Métricas
        metrics_frame = ttk.Frame(self.notebook)
        self.notebook.add(metrics_frame, text="📈 Métricas")
        self.setup_metrics_tab(metrics_frame)
    
    def setup_sources_tab(self, parent: ttk.Frame) -> None:
        """Configurar aba de fontes (equivalente ao TabsContent fontes)"""
        sources_container = ttk.Frame(parent, padding="20")
        sources_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Header
        header_frame = ttk.Frame(sources_container)
        header_frame.grid(row=0, column=0, pady=(0, 20))
        
        title_label = tk.Label(header_frame, text="Fontes de Conhecimento Ativas",
                              font=("Arial", 14, "bold"), fg="#3b82f6", bg='#f8fafc')
        title_label.grid(row=0, column=0, pady=(0, 8))
        
        desc_label = tk.Label(header_frame, 
                             text="IAG processando múltiplas fontes para formar visão holística do mercado",
                             font=("Arial", 10), fg="#6b7280", bg='#f8fafc')
        desc_label.grid(row=1, column=0)
        
        # Frame scrollável para fontes
        self.sources_frame = self.create_scrollable_frame(sources_container, height=400)
        self.sources_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        sources_container.columnconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
    
    def setup_connections_tab(self, parent: ttk.Frame) -> None:
        """Configurar aba de conexões (equivalente ao TabsContent conexões)"""
        # Container da aba
        connections_container = ttk.Frame(parent, padding="20")
        connections_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Header
        header_frame = ttk.Frame(connections_container)
        header_frame.grid(row=0, column=0, pady=(0, 20))
        
        title_label = tk.Label(header_frame, text="Conexões Cross-Domain",
                              font=("Arial", 14, "bold"), fg="#3b82f6", bg='#f8fafc')
        title_label.grid(row=0, column=0, pady=(0, 8))
        
        desc_label = tk.Label(header_frame, 
                             text="Correlações descobertas entre diferentes domínios de conhecimento",
                             font=("Arial", 10), fg="#6b7280", bg='#f8fafc')
        desc_label.grid(row=1, column=0)
        
        # Frame scrollável para conexões
        self.connections_frame = self.create_scrollable_frame(connections_container, height=400)
        self.connections_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        connections_container.columnconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
    
    def setup_insights_tab(self, parent: ttk.Frame) -> None:
        """Configurar aba de insights (equivalente ao TabsContent insights)"""
        # Container da aba
        insights_container = ttk.Frame(parent, padding="20")
        insights_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Header
        header_frame = ttk.Frame(insights_container)
        header_frame.grid(row=0, column=0, pady=(0, 20))
        
        title_label = tk.Label(header_frame, text="Insights Holísticos",
                              font=("Arial", 14, "bold"), fg="#3b82f6", bg='#f8fafc')
        title_label.grid(row=0, column=0, pady=(0, 8))
        
        desc_label = tk.Label(header_frame, 
                             text="Conclusões integradas de múltiplas fontes de conhecimento",
                             font=("Arial", 10), fg="#6b7280", bg='#f8fafc')
        desc_label.grid(row=1, column=0)
        
        # Frame scrollável para insights
        self.insights_frame = self.create_scrollable_frame(insights_container, height=400)
        self.insights_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        insights_container.columnconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
    
    def setup_metrics_tab(self, parent: ttk.Frame) -> None:
        """Configurar aba de métricas (equivalente ao TabsContent métricas)"""
        # Container da aba
        metrics_container = ttk.Frame(parent, padding="20")
        metrics_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Header
        header_frame = ttk.Frame(metrics_container)
        header_frame.grid(row=0, column=0, pady=(0, 20))
        
        title_label = tk.Label(header_frame, text="Métricas de Aprendizado",
                              font=("Arial", 14, "bold"), fg="#3b82f6", bg='#f8fafc')
        title_label.grid(row=0, column=0, pady=(0, 8))
        
        desc_label = tk.Label(header_frame, 
                             text="Visão geral das métricas de aprendizado e integração",
                             font=("Arial", 10), fg="#6b7280", bg='#f8fafc')
        desc_label.grid(row=1, column=0)
        
        # Grid de métricas principais
        main_metrics_grid = ttk.Frame(metrics_container)
        main_metrics_grid.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Total de pontos de dados
        total_data_points = sum(source.data_points for source in self.learning_sources)
        total_data_points_label = tk.Label(main_metrics_grid, text=f"{total_data_points:,}",
                                           font=("Arial", 24, "bold"), fg="#3b82f6")
        total_data_points_label.grid(row=0, column=0, sticky=tk.W)
        
        # Total de padrões identificados
        total_patterns = sum(source.patterns for source in self.learning_sources)
        total_patterns_label = tk.Label(main_metrics_grid, text=f"{total_patterns:,}",
                                        font=("Arial", 24, "bold"), fg="#3b82f6")
        total_patterns_label.grid(row=0, column=1, sticky=tk.W)
        
        # Distribuição do conhecimento (gráfico de pizza)
        knowledge_distribution_label = tk.Label(metrics_container, text="Distribuição do Conhecimento",
                                                font=("Arial", 12, "bold"), fg="#3b82f6")
        knowledge_distribution_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        # Criar gráfico de pizza (placeholder)
        pie_chart_placeholder = tk.Canvas(metrics_container, width=400, height=300, bg='white')
        pie_chart_placeholder.grid(row=3, column=0, sticky=tk.W)
        
        # Exibir dados principais na aba de métricas
        self.metrics_labels['total_data_points'] = total_data_points_label
        self.metrics_labels['total_patterns'] = total_patterns_label
        self.metrics_labels['knowledge_distribution'] = pie_chart_placeholder
        
        metrics_container.columnconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
    
    def create_scrollable_frame(self, parent: ttk.Frame, height: int) -> ttk.Frame:
        """Criar frame scrollável"""
        canvas = tk.Canvas(parent, bg='#f8fafc', height=height)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        scrollable_frame.columnconfigure(0, weight=1)
        
        return scrollable_frame
    
    def update_ui(self) -> None:
        """Atualizar toda a interface"""
        # Atualizar badges do header
        if self.learning_badge:
            self.learning_badge.config(text=f"🔄 Aprendendo: {self.overall_learning_rate:.1f}%")
        if self.integration_badge:
            self.integration_badge.config(text=f"🔗 Integração: {self.knowledge_integration:.1f}%")
        
        # Atualizar conteúdo das abas
        self.update_sources_display()
        self.update_connections_display()
        self.update_insights_display()
        self.update_metrics_display()
    
    def update_sources_display(self) -> None:
        """Atualizar display de fontes"""
        # Limpar frame
        for widget in self.sources_frame.winfo_children():
            widget.destroy()
        
        # Criar cards para cada fonte
        for i, source in enumerate(self.learning_sources):
            self.create_source_card(self.sources_frame, source, i)
    
    def create_source_card(self, parent: ttk.Frame, source: LearningSource, index: int) -> None:
        """Criar card individual de fonte de aprendizado"""
        card_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        card_frame.grid(row=index, column=0, sticky=(tk.W, tk.E), pady=8, padx=10)
        
        # Header do card
        header_frame = ttk.Frame(card_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 12))
        
        # Lado esquerdo: ícone e nome
        left_frame = ttk.Frame(header_frame)
        left_frame.grid(row=0, column=0, sticky=tk.W)
        
        icon = self.get_source_type_icon(source.type)
        ttk.Label(left_frame, text=icon, font=("Arial", 12)).grid(row=0, column=0, padx=(0, 8))
        
        ttk.Label(left_frame, text=source.name, 
                 font=("Arial", 11, "bold")).grid(row=0, column=1)
        
        # Lado direito: badge de padrões
        patterns_badge = tk.Label(header_frame, text=f"{source.patterns:,} padrões",
                                 bg="white", fg="#6b7280", font=("Arial", 8, "bold"),
                                 relief='solid', borderwidth=1, padx=6, pady=2)
        patterns_badge.grid(row=0, column=1, sticky=tk.E)
        
        header_frame.columnconfigure(0, weight=1)
        
        # Grid de métricas
        metrics_grid = ttk.Frame(card_frame)
        metrics_grid.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 12))
        
        # Taxa de aprendizado
        learning_frame = ttk.Frame(metrics_grid)
        learning_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        learning_header = ttk.Frame(learning_frame)
        learning_header.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(learning_header, text="Taxa de Aprendizado", 
                 font=("Arial", 8), style='Muted.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(learning_header, text=f"{source.learning_rate:.1f}%", 
                 font=("Arial", 8, "bold"), style='Info.TLabel').grid(row=0, column=1, sticky=tk.E)
        
        learning_progress = ttk.Progressbar(learning_frame, length=200, mode='determinate')
        learning_progress['value'] = source.learning_rate
        learning_progress.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        learning_header.columnconfigure(0, weight=1)
        learning_frame.columnconfigure(0, weight=1)
        
        # Precisão
        accuracy_frame = ttk.Frame(metrics_grid)
        accuracy_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        accuracy_header = ttk.Frame(accuracy_frame)
        accuracy_header.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(accuracy_header, text="Precisão", 
                 font=("Arial", 8), style='Muted.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(accuracy_header, text=f"{source.accuracy:.1f}%", 
                 font=("Arial", 8, "bold"), style='Success.TLabel').grid(row=0, column=1, sticky=tk.E)
        
        accuracy_progress = ttk.Progressbar(accuracy_frame, length=200, mode='determinate')
        accuracy_progress['value'] = source.accuracy
        accuracy_progress.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        accuracy_header.columnconfigure(0, weight=1)
        accuracy_frame.columnconfigure(0, weight=1)
        
        metrics_grid.columnconfigure(0, weight=1)
        metrics_grid.columnconfigure(1, weight=1)
        
        # Dados
        data_frame = ttk.Frame(card_frame)
        data_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 12))
        
        # Pontos de dados
        ttk.Label(data_frame, text="Pontos de Dados", 
                 font=("Arial", 8), style='Muted.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(data_frame, text=f"{source.data_points:,}", 
                 font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W)
        
        # Influência
        ttk.Label(data_frame, text="Influência", 
                 font=("Arial", 8), style='Muted.TLabel').grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(data_frame, text=f"{source.influence:.1f}%", 
                 font=("Arial", 10, "bold"), fg="#3b82f6").grid(row=1, column=1, sticky=tk.W)
        
        data_frame.columnconfigure(0, weight=1)
        data_frame.columnconfigure(1, weight=1)
        
        # Insights recentes
        insights_frame = ttk.Frame(card_frame)
        insights_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(insights_frame, text="Insights Recentes", 
                 font=("Arial", 8, "bold"), style='Muted.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        for i, insight in enumerate(source.insights[:2]):
            ttk.Label(insights_frame, text=f"• {insight}", 
                     font=("Arial", 8)).grid(row=i+1, column=0, sticky=tk.W)
        
        insights_frame.columnconfigure(0, weight=1)
        
        card_frame.columnconfigure(0, weight=1)
    
    def update_connections_display(self) -> None:
        """Atualizar display de conexões"""
        # Limpar frame
        for widget in self.connections_frame.winfo_children():
            widget.destroy()
        
        # Criar cards para cada conexão
        for i, connection in enumerate(self.cross_domain_connections):
            self.create_connection_card(self.connections_frame, connection, i)
    
    def create_connection_card(self, parent: ttk.Frame, connection: CrossDomainConnection, index: int) -> None:
        """Criar card individual de conexão cross-domain"""
        card_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        card_frame.grid(row=index, column=0, sticky=(tk.W, tk.E), pady=8, padx=10)
        
        # Header do card
        header_frame = ttk.Frame(card_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 12))
        
        # Lado esquerdo: ícone e descrição
        left_frame = ttk.Frame(header_frame)
        left_frame.grid(row=0, column=0, sticky=tk.W)
        
        icon = "🔗"
        ttk.Label(left_frame, text=icon, font=("Arial", 12)).grid(row=0, column=0, padx=(0, 8))
        
        description = f"{connection.source} ↔ {connection.target}"
        ttk.Label(left_frame, text=description, 
                 font=("Arial", 11, "bold")).grid(row=0, column=1)
        
        # Lado direito: badge de força
        strength_badge = tk.Label(header_frame, text=f"{connection.strength:.0f}% força",
                                 bg="white", fg="#6b7280", font=("Arial", 8, "bold"),
                                 relief='solid', borderwidth=1, padx=6, pady=2)
        strength_badge.grid(row=0, column=1, sticky=tk.E)
        
        # Cor do badge com base na força
        if connection.strength > 85:
            strength_badge.config(bg="#10b981", fg="white")
        elif connection.strength > 70:
            strength_badge.config(bg="#f59e0b", fg="white")
        else:
            strength_badge.config(bg="#ef4444", fg="white")
        
        header_frame.columnconfigure(0, weight=1)
        
        # Grid de métricas da conexão
        metrics_grid = ttk.Frame(card_frame)
        metrics_grid.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 12))
        
        # Correlação
        correlation_frame = ttk.Frame(metrics_grid)
        correlation_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        correlation_header = ttk.Frame(correlation_frame)
        correlation_header.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(correlation_header, text="Correlação", 
                 font=("Arial", 8), style='Muted.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(correlation_header, text=f"{connection.correlation:.2f}", 
                 font=("Arial", 8, "bold"), style='Info.TLabel').grid(row=0, column=1, sticky=tk.E)
        
        correlation_progress = ttk.Progressbar(correlation_frame, length=200, mode='determinate')
        correlation_progress['value'] = connection.correlation * 100
        correlation_progress.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        correlation_header.columnconfigure(0, weight=1)
        correlation_frame.columnconfigure(0, weight=1)
        
        # Insight da conexão
        ttk.Label(metrics_grid, text="Insight:", 
                 font=("Arial", 8, "bold"), style='Muted.TLabel').grid(row=1, column=0, sticky=tk.W)
        
        ttk.Label(metrics_grid, text=connection.insight, 
                 font=("Arial", 8)).grid(row=2, column=0, sticky=tk.W)
        
        # Data da descoberta
        discovered_at = connection.discovered_at.strftime("%d/%m %H:%M")
        ttk.Label(metrics_grid, text=f"Descoberto em: {discovered_at}", 
                 font=("Arial", 8, "italic"), style='Muted.TLabel').grid(row=3, column=0, sticky=tk.W)
        
        card_frame.columnconfigure(0, weight=1)
    
    def update_insights_display(self) -> None:
        """Atualizar display de insights"""
        # Limpar frame
        for widget in self.insights_frame.winfo_children():
            widget.destroy()
        
        # Criar cards para cada insight
        for i, insight in enumerate(self.holistic_insights):
            self.create_insight_card(self.insights_frame, insight, i)
    
    def create_insight_card(self, parent: ttk.Frame, insight: HolisticInsight, index: int) -> None:
        """Criar card individual de insight holístico"""
        card_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        card_frame.grid(row=index, column=0, sticky=(tk.W, tk.E), pady=8, padx=10)
        
        # Header do card
        header_frame = ttk.Frame(card_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 12))
        
        # Lado esquerdo: ícone e título
        left_frame = ttk.Frame(header_frame)
        left_frame.grid(row=0, column=0, sticky=tk.W)
        
        icon = self.get_category_icon(insight.category)
        ttk.Label(left_frame, text=icon, font=("Arial", 12)).grid(row=0, column=0, padx=(0, 8))
        
        ttk.Label(left_frame, text=insight.title, 
                 font=("Arial", 11, "bold")).grid(row=0, column=1)
        
        # Lado direito: badge de impacto
        impact_badge = tk.Label(header_frame, text=insight.impact.name,
                                bg=self.get_impact_color(insight.impact),
                                fg="white",
                                font=("Arial", 8, "bold"),
                                padx=6, pady=4)
        impact_badge.grid(row=0, column=1, sticky=tk.E)
        
        header_frame.columnconfigure(0, weight=1)
        
        # Descrição do insight
        ttk.Label(card_frame, text=insight.description, 
                 font=("Arial", 9)).grid(row=1, column=0, sticky=tk.W)
        
        # Grid de métricas do insight
        metrics_grid = ttk.Frame(card_frame)
        metrics_grid.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Confiança
        ttk.Label(metrics_grid, text="Confiança:", 
                 font=("Arial", 8, "bold"), style='Muted.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(metrics_grid, text=f"{insight.confidence:.1f}%", 
                 font=("Arial", 8, "bold"), style='Info.TLabel').grid(row=1, column=0, sticky=tk.W)
        
        # Data e hora
        timestamp = insight.timestamp.strftime("%d/%m %H:%M")
        ttk.Label(metrics_grid, text="Descoberto em:", 
                 font=("Arial", 8, "bold"), style='Muted.TLabel').grid(row=0, column=1, sticky=tk.E)
        
        ttk.Label(metrics_grid, text=timestamp, 
                 font=("Arial", 8, "bold"), style='Info.TLabel').grid(row=1, column=1, sticky=tk.E)
        
        metrics_grid.columnconfigure(0, weight=1)
        metrics_grid.columnconfigure(1, weight=1)
        
        # Fontes do insight
        sources_frame = ttk.Frame(card_frame)
        sources_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(sources_frame, text="Fontes:", 
                 font=("Arial", 8, "bold"), style='Muted.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        for i, source in enumerate(insight.sources):
            ttk.Label(sources_frame, text=f"• {source}", 
                     font=("Arial", 8)).grid(row=i+1, column=0, sticky=tk.W)
        
        card_frame.columnconfigure(0, weight=1)
    
    def update_metrics_display(self) -> None:
        """Atualizar display de métricas"""
        # Atualizar total de pontos de dados
        total_data_points = sum(source.data_points for source in self.learning_sources)
        if self.metrics_labels.get('total_data_points'):
            self.metrics_labels['total_data_points'].config(text=f"{total_data_points:,}")
        
        # Atualizar total de padrões identificados
        total_patterns = sum(source.patterns for source in self.learning_sources)
        if self.metrics_labels.get('total_patterns'):
            self.metrics_labels['total_patterns'].config(text=f"{total_patterns:,}")
        
        # Atualizar gráfico de pizza (placeholder)
        if self.metrics_labels.get('knowledge_distribution'):
            pie_chart = self.metrics_labels['knowledge_distribution']
            pie_chart.delete("all")  # Limpar gráfico anterior
            
            # Exemplo de gráfico de pizza (dados aleatórios)
            data = [random.randint(10, 100) for _ in range(5)]
            total = sum(data)
            start_angle = 0
            
            for value in data:
                extent = 360 * value / total
                pie_chart.create_arc((10, 10, 390, 290), start=start_angle, extent=extent, fill=self.get_random_color(), outline="white", width=2)
                start_angle += extent
    
    def get_random_color(self) -> str:
        """Gerar cor aleatória para o gráfico de pizza"""
        r = lambda: random.randint(0, 255)
        return f"#{r():02x}{r():02x}{r():02x}"
    
    def start_learning_engine(self) -> None:
        """Iniciar motor de aprendizado (equivalente ao useEffect)"""
        # Inicialização
        self.learning_sources = self.init_learning_sources()
        self.cross_domain_connections = self.generate_cross_domain_connections()
        self.holistic_insights = self.generate_holistic_insights()
        
        # Calcular métricas iniciais
        if self.learning_sources:
            self.overall_learning_rate = sum(s.learning_rate for s in self.learning_sources) / len(self.learning_sources)
            self.knowledge_integration = sum(s.accuracy for s in self.learning_sources) / len(self.learning_sources)
        
        # Primeira atualização da UI
        self.update_ui()
        
        def learning_worker():
            while not self.stop_updates:
                time.sleep(6)  # Equivalente ao interval de 6000ms
                
                if not self.stop_updates:
                    self.update_learning_metrics()
        
        self.update_thread = threading.Thread(target=learning_worker, daemon=True)
        self.update_thread.start()
    
    def __del__(self):
        """Destrutor para parar thread de atualização"""
        self.stop_updates = True


def main() -> None:
    """Função principal para executar a aplicação (equivalente ao export do React)"""
    root = tk.Tk()
    app = IAGMultidisciplinaryLearningApp(root)
    
    # Tornar a janela responsiva
    root.minsize(1400, 900)
    
    # Centralizar janela
    root.eval('tk::PlaceWindow . center')
    
    # Iniciar loop principal
    root.mainloop()


if __name__ == "__main__":
    main()