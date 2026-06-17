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
class DataStatus(Enum):
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    LOADING = "LOADING"
    ERROR = "ERROR"

# Estruturas de dados equivalentes às interfaces TypeScript
@dataclass
class HistoricalDataPoint:
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: int
    symbol: str
    timeframe: str

@dataclass
class DatasetInfo:
    symbol: str
    timeframe: str
    start_date: str
    end_date: str
    total_points: int
    status: DataStatus
    quality: float
    neural_ready: bool

@dataclass
class NeuralDataPrep:
    symbol: str
    features: int
    sequences: int
    training: int
    validation: int
    test: int
    normalization: str
    engineered: bool

class HistoricalDataManagerApp:
    """Aplicação principal que replica a funcionalidade do componente React HistoricalDataManager"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🗄️ Dados Históricos para IA")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#f8fafc')
        
        # Estado da aplicação (equivalente aos useState hooks)
        self.datasets: List[DatasetInfo] = []
        self.neural_prep: List[NeuralDataPrep] = []
        self.download_progress = 0.0
        self.is_downloading = False
        self.total_data_points = 0
        
        # Containers para widgets que precisam ser atualizados
        self.download_button = None
        self.progress_frame = None
        self.progress_bar = None
        self.total_points_badge = None
        self.datasets_frame = None
        self.neural_frame = None
        self.stats_labels = {}
        
        # Thread de download e atualização
        self.download_thread = None
        self.update_thread = None
        self.stop_updates = False
        
        # Configurar estilos
        self.setup_styles()
        
        # Inicializar dados
        self.initialize_data()
        
        # Configurar interface
        self.setup_ui()
        
        # Iniciar atualizações (equivalente ao useEffect)
        self.start_updates()
    
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
    def get_status_color(self, status: DataStatus) -> str:
        """Obter cor para status (equivalente a getStatusColor)"""
        color_map = {
            DataStatus.COMPLETE: "#10b981",
            DataStatus.PARTIAL: "#f59e0b",
            DataStatus.LOADING: "#6b7280",
            DataStatus.ERROR: "#ef4444"
        }
        return color_map.get(status, "#6b7280")
    
    def get_quality_color(self, quality: float) -> str:
        """Obter cor para qualidade (equivalente a getQualityColor)"""
        if quality >= 98:
            return "#10b981"
        elif quality >= 95:
            return "#f59e0b"
        else:
            return "#ef4444"
    
    # Inicialização de dados (equivalente ao useEffect)
    def initialize_data(self) -> None:
        """Inicializar dados históricos simulados"""
        # Simular datasets históricos disponíveis
        mock_datasets = [
            DatasetInfo(
                symbol='PETR4.SA',
                timeframe='1m',
                start_date='2020-01-01',
                end_date='2024-08-25',
                total_points=1847520,
                status=DataStatus.COMPLETE,
                quality=98.5,
                neural_ready=True
            ),
            DatasetInfo(
                symbol='VALE3.SA',
                timeframe='1m',
                start_date='2020-01-01',
                end_date='2024-08-25',
                total_points=1847520,
                status=DataStatus.COMPLETE,
                quality=97.8,
                neural_ready=True
            ),
            {
              "symbol": "ITUB4.SA",
              "timeframe": "5m",
              "start_date": "2020-01-01",
              "end_date": "2024-08-25",
              "total_points": 369504,
              "status": "COMPLETE",
              "quality": 99.1,
              "neural_ready": True
            },
            {
              "symbol": "BBDC4.SA",
              "timeframe": "15m",
              "start_date": "2020-01-01",
              "end_date": "2024-08-25",
              "total_points": 123168,
              "status": "PARTIAL",
              "quality": 94.3,
              "neural_ready": False
            },
            {
              "symbol": "ABEV3.SA",
              "timeframe": "1h",
              "start_date": "2020-01-01",
              "end_date": "2024-08-25",
              "total_points": 30792,
              "status": "COMPLETE",
              "quality": 96.7,
              "neural_ready": True
            },
            {
              "symbol": "MGLU3.SA",
              "timeframe": "1d",
              "start_date": "2015-01-01",
              "end_date": "2024-08-25",
              "total_points": 2470,
              "status": "COMPLETE",
              "quality": 99.5,
              "neural_ready": True
            }
        ]
        
        # Simular preparação neural
        mock_neural_prep = [
            NeuralDataPrep(
                symbol='PETR4.SA',
                features=47,
                sequences=1600000,
                training=1120000,
                validation=320000,
                test=160000,
                normalization='MinMax + Z-Score',
                engineered=True
            ),
            NeuralDataPrep(
                symbol='VALE3.SA',
                features=52,
                sequences=1600000,
                training=1120000,
                validation=320000,
                test=160000,
                normalization='Robust + StandardScaler',
                engineered=True
            ),
            NeuralDataPrep(
                symbol='ITUB4.SA',
                features=45,
                sequences=320000,
                training=224000,
                validation=64000,
                test=32000,
                normalization='Quantile + MinMax',
                engineered=True
            ),
            NeuralDataPrep(
                symbol='ABEV3.SA',
                features=38,
                sequences=26000,
                training=18200,
                validation=5200,
                test=2600,
                normalization='PowerTransformer',
                engineered=True
            )
        ]
        
        self.datasets = mock_datasets
        self.neural_prep = mock_neural_prep
        
        # Calcular total de pontos de dados
        self.total_data_points = sum(dataset.total_points for dataset in self.datasets)
    
    # Função principal de download (equivalente a handleDownloadData)
    def handle_download_data(self) -> None:
        """Processar download de dados (equivalente a handleDownloadData)"""
        if self.is_downloading:
            return
        
        self.is_downloading = True
        self.download_progress = 0.0
        self.update_download_display()
        
        print('Iniciando download de dados históricos...')
        
        # Iniciar thread de download
        self.download_thread = threading.Thread(target=self._download_worker, daemon=True)
        self.download_thread.start()
    
    def _download_worker(self) -> None:
        """Worker thread para simulação de download"""
        while self.download_progress < 100:
            time.sleep(0.5)  # Simular progresso
            increment = random.uniform(2, 8)
            self.download_progress = min(100, self.download_progress + increment)
            
            # Atualizar UI na thread principal
            self.root.after(0, self.update_progress_display)
        
        # Finalizar download
        self.is_downloading = False
        self.root.after(0, self.finish_download)
    
    def update_progress_display(self) -> None:
        """Atualizar display de progresso"""
        if self.progress_bar:
            self.progress_bar['value'] = self.download_progress
    
    def update_download_display(self) -> None:
        """Atualizar display de download"""
        if self.download_button:
            if self.is_downloading:
                self.download_button.config(text="📥 Baixando...", state="disabled")
            else:
                self.download_button.config(text="📥 Atualizar", state="normal")
        
        if self.progress_frame:
            if self.is_downloading:
                self.progress_frame.grid()
            else:
                self.progress_frame.grid_remove()
    
    def finish_download(self) -> None:
        """Finalizar download"""
        self.update_download_display()
    
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
        
        # Frame de progresso
        self.setup_progress_frame(container)
        
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
        
        ttk.Label(left_frame, text="🗄️", font=("Arial", 18)).grid(row=0, column=0, padx=(0, 8))
        ttk.Label(left_frame, text="Dados Históricos para IA", 
                 font=("Arial", 18, "bold")).grid(row=0, column=1)
        
        # Lado direito: badge e botão
        right_frame = ttk.Frame(header_frame)
        right_frame.grid(row=0, column=1, sticky=tk.E)
        
        # Badge total de pontos
        self.total_points_badge = tk.Label(right_frame, 
                                          text=f"📊 {self.total_data_points:,} pontos",
                                          bg="#3b82f6",
                                          fg="white",
                                          font=("Arial", 9, "bold"),
                                          padx=8, pady=4)
        self.total_points_badge.grid(row=0, column=0, padx=(0, 8))
        
        # Botão download
        self.download_button = tk.Button(right_frame, 
                                        text="📥 Atualizar",
                                        bg="#3b82f6", fg="white",
                                        font=("Arial", 10, "bold"),
                                        padx=12, pady=6,
                                        cursor="hand2",
                                        command=self.handle_download_data)
        self.download_button.grid(row=0, column=1)