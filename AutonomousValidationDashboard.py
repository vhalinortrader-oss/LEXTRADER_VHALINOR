import tkinter as tk
from tkinter import ttk
import random
import time
import threading
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Enums e tipos
class SystemStatus(Enum):
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class ConnectionStatus(Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    DEGRADED = "DEGRADED"

class RecoveryResult(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"

@dataclass
class HealthStatus:
    status: SystemStatus
    cpu_load: float
    memory_usage: float
    connection: ConnectionStatus
    last_check: datetime
    issues_found: int
    auto_recovery_enabled: bool

@dataclass
class RecoveryLog:
    id: int
    timestamp: datetime
    issue: str
    action: str
    result: RecoveryResult
    agi_intervention: bool


class AutonomousValidationService:
    """Serviço de validação autônoma"""
    
    def __init__(self):
        self.status = HealthStatus(
            status=SystemStatus.HEALTHY,
            cpu_load=35.0,
            memory_usage=42.0,
            connection=ConnectionStatus.CONNECTED,
            last_check=datetime.now(),
            issues_found=0,
            auto_recovery_enabled=True
        )
        self.recovery_logs: List[RecoveryLog] = []
        self.log_counter = 0
        self.running = False
        self.thread = None
        
        # Log inicial
        self.add_log(
            "Sistema inicializado",
            "Validador autônomo iniciado",
            RecoveryResult.SUCCESS,
            False
        )
    
    def start(self):
        """Inicia o monitoramento do sistema"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(
                target=self._monitoring_loop,
                daemon=True
            )
            self.thread.start()
            self.add_log(
                "Monitoramento iniciado",
                "Sistema de validação ativado",
                RecoveryResult.SUCCESS,
                False
            )
    
    def stop(self):
        """Para o monitoramento do sistema"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        self.add_log(
            "Monitoramento interrompido",
            "Sistema de validação desativado",
            RecoveryResult.SUCCESS,
            False
        )
    
    def _monitoring_loop(self):
        """Loop principal de monitoramento"""
        while self.running:
            time.sleep(1)  # Verificar a cada segundo
            
            # Atualizar métricas
            self.update_metrics()
            
            # Verificar problemas
            self.check_for_issues()
    
    def update_metrics(self):
        """Atualiza as métricas do sistema"""
        # Simular variação nas métricas
        cpu_change = random.uniform(-2, 2)
        mem_change = random.uniform(-1, 1)
        
        self.status.cpu_load = max(0, min(100, 
            self.status.cpu_load + cpu_change))
        self.status.memory_usage = max(0, min(100, 
            self.status.memory_usage + mem_change))
        
        # Simular problemas de conexão ocasionais
        if random.random() < 0.02:  # 2% de chance de desconexão
            self.status.connection = ConnectionStatus.DISCONNECTED
            self.add_log(
                "Conexão perdida",
                "Tentando reconectar automaticamente",
                RecoveryResult.PENDING,
                False
            )
        elif random.random() < 0.05:  # 5% de chance de conexão degradada
            self.status.connection = ConnectionStatus.DEGRADED
        else:
            self.status.connection = ConnectionStatus.CONNECTED
        
        self.status.last_check = datetime.now()
        
        # Atualizar status geral
        self.update_overall_status()
    
    def update_overall_status(self):
        """Atualiza o status geral do sistema"""
        issues = []
        
        if self.status.cpu_load > 80:
            issues.append("CPU alta")
        if self.status.memory_usage > 85:
            issues.append("Memória alta")
        if self.status.connection != ConnectionStatus.CONNECTED:
            issues.append("Conexão problemática")
        
        if not issues:
            self.status.status = SystemStatus.HEALTHY
        elif self.status.cpu_load > 90 or self.status.memory_usage > 95:
            self.status.status = SystemStatus.CRITICAL
        else:
            self.status.status = SystemStatus.WARNING
        
        self.status.issues_found = len(issues)
    
    def check_for_issues(self):
        """Verifica e corrige problemas automaticamente"""
        if self.status.auto_recovery_enabled:
            if self.status.cpu_load > 85:
                self.attempt_recovery(
                    "CPU em estado crítico",
                    "Reiniciando processos não essenciais"
                )
            elif self.status.memory_usage > 90:
                self.attempt_recovery(
                    "Memória em estado crítico",
                    "Liberando cache e buffers"
                )
            elif self.status.connection == ConnectionStatus.DISCONNECTED:
                self.attempt_recovery(
                    "Conexão perdida",
                    "Reconectando aos servidores",
                    True
                )
    
    def attempt_recovery(self, issue: str, action: str, 
                        agi_intervention: bool = False):
        """Tenta recuperar o sistema automaticamente"""
        success_rate = 0.9 if not agi_intervention else 0.95
        result = (RecoveryResult.SUCCESS 
                 if random.random() < success_rate 
                 else RecoveryResult.FAILED)
        
        self.add_log(issue, action, result, agi_intervention)
        
        if result == RecoveryResult.SUCCESS:
            # Simular melhoria após recuperação bem-sucedida
            if "CPU" in issue:
                self.status.cpu_load *= 0.7  # Reduzir carga da CPU
            elif "Memória" in issue:
                self.status.memory_usage *= 0.75  # Reduzir uso de memória
            elif "Conexão" in issue:
                self.status.connection = ConnectionStatus.CONNECTED
    
    def add_log(self, issue: str, action: str, result: RecoveryResult, 
               agi_intervention: bool):
        """Adiciona um registro ao log de recuperação"""
        log = RecoveryLog(
            id=self.log_counter,
            timestamp=datetime.now(),
            issue=issue,
            action=action,
            result=result,
            agi_intervention=agi_intervention
        )
        self.recovery_logs.append(log)
        self.log_counter += 1
        
        # Manter apenas os últimos 10 logs
        if len(self.recovery_logs) > 10:
            self.recovery_logs.pop(0)


class AutonomousValidationDashboard:
    """Dashboard de validação autônoma"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Validador Autônomo de Sistema")
        self.root.geometry("1400x800")
        self.root.configure(bg="#0a0a0a")
        
        # Inicializar serviço
        self.validator = AutonomousValidationService()
        self.status = self.validator.status
        self.logs = self.validator.recovery_logs
        self.history: List[Dict[str, Any]] = []
        
        # Configurar UI
        self.setup_ui()
        
        # Iniciar serviço
        self.validator.start()
        
        # Iniciar atualizações
        self.start_updates()
    
    def setup_ui(self):
        """Configura a interface gráfica"""
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg="#0a0a0a")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        self.setup_header()
        
        # Conteúdo principal
        self.setup_content()
    
    def setup_header(self):
        """Configura o cabeçalho da aplicação"""
        header_frame = tk.Frame(self.main_frame, bg="#1a1a2e", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # Logo e título
        left_frame = tk.Frame(header_frame, bg="#1a1a2e")
        left_frame.pack(side=tk.LEFT, padx=20)
        
        # Ícone
        icon_frame = tk.Frame(
            left_frame,
            bg="#064e3b",
            relief=tk.RAISED,
            borderwidth=1,
            padx=10,
            pady=10
        )
        icon_frame.pack(side=tk.LEFT, padx=(0, 15))
        tk.Label(
            icon_frame,
            text="🩺",
            font=("Arial", 16),
            bg="#064e3b",
            fg="#10b981"
        ).pack()
        
        # Texto
        text_frame = tk.Frame(left_frame, bg="#1a1a2e")
        text_frame.pack(side=tk.LEFT)
        
        tk.Label(
            text_frame,
            text="VALIDADOR AUTÔNOMO DE SISTEMA",
            font=("Arial", 16, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        ).pack(anchor=tk.W)
        
        tk.Label(
            text_frame,
            text="SELF-HEALING • PREDICTIVE MAINTENANCE",
            font=("Courier", 10),
            fg="#10b981",
            bg="#1a1a2e"
        ).pack(anchor=tk.W)
        
        # Status do sistema
        right_frame = tk.Frame(header_frame, bg="#1a1a2e")
        right_frame.pack(side=tk.RIGHT, padx=20)
        
        self.status_label = tk.Label(
            right_frame,
            text=f"STATUS: {self.status.status.value}",
            font=("Arial", 10, "bold"),
            bg=self._get_status_color(self.status.status)[0],
            fg=self._get_status_color(self.status.status)[1],
            padx=15,
            pady=8,
            relief=tk.RAISED,
            borderwidth=1
        )
        self.status_label.pack()
    
    def _get_status_color(self, status):
        """Retorna as cores para cada status"""
        colors = {
            SystemStatus.HEALTHY: ("#166534", "#4ade80"),
            SystemStatus.WARNING: ("#854d0e", "#fbbf24"),
            SystemStatus.CRITICAL: ("#991b1b", "#f87171")
        }
        return colors.get(status, ("#374151", "#9ca3af"))
    
    def setup_content(self):
        """Configura o conteúdo principal"""
        content_frame = tk.Frame(self.main_frame, bg="#0a0a0a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configurar grid
        content_frame.grid_columnconfigure(0, weight=2)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Painel esquerdo: Vitals do Sistema
        left_frame = tk.Frame(content_frame, bg="#0a0a0a")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Métricas do sistema
        self.setup_system_metrics(left_frame)
        
        # Gráfico de monitoramento
        self.setup_monitoring_chart(left_frame)
        
        # Painel direito: Logs de Recuperação
        right_frame = tk.Frame(
            content_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1
        )
        right_frame.grid(row=0, column=1, sticky="nsew")
        
        self.setup_recovery_logs(right_frame)
    
    def setup_system_metrics(self, parent_frame):
        """Configura as métricas do sistema"""
        metrics_frame = tk.Frame(parent_frame, bg="#0a0a0a")
        metrics_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Conectividade
        connectivity_frame = tk.Frame(
            metrics_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        connectivity_frame.pack(side=tk.LEFT, fill=tk.BOTH, 
                               expand=True, padx=(0, 10))
        
        tk.Label(
            connectivity_frame,
            text="📶 CONECTIVIDADE",
            font=("Arial", 9),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        self.connectivity_label = tk.Label(
            connectivity_frame,
            text=self.status.connection.value,
            font=("Courier", 16, "bold"),
            fg=self._get_connection_color(self.status.connection),
            bg="#1a1a2e"
        )
        self.connectivity_label.pack(pady=(0, 10))
        
        # Carga CPU
        cpu_frame = tk.Frame(
            metrics_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        cpu_frame.pack(side=tk.LEFT, fill=tk.BOTH, 
                      expand=True, padx=(0, 10))
        
        tk.Label(
            cpu_frame,
            text="⚙️ CARGA CPU",
            font=("Arial", 9),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        self.cpu_label = tk.Label(
            cpu_frame,
            text=f"{self.status.cpu_load:.1f}%",
            font=("Courier", 16, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        self.cpu_label.pack(pady=(0, 10))
        
        # Barra de CPU
        self.cpu_bar_frame = tk.Frame(cpu_frame, bg="#374151", height=8)
        self.cpu_bar_frame.pack(fill=tk.X)
        self.cpu_bar_frame.pack_propagate(False)
        
        self.cpu_bar = tk.Frame(
            self.cpu_bar_frame,
            bg="#3b82f6",
            width=int(self.status.cpu_load * 1.5)
        )
        self.cpu_bar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Uso de Memória
        memory_frame = tk.Frame(
            metrics_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        memory_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(
            memory_frame,
            text="💾 MEMÓRIA",
            font=("Arial", 9),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        self.memory_label = tk.Label(
            memory_frame,
            text=f"{self.status.memory_usage:.1f}%",
            font=("Courier", 16, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        self.memory_label.pack(pady=(0, 10))
        
        # Barra de memória
        self.memory_bar_frame = tk.Frame(memory_frame, 
                                        bg="#374151", height=8)
        self.memory_bar_frame.pack(fill=tk.X)
        self.memory_bar_frame.pack_propagate(False)
        
        self.memory_bar = tk.Frame(
            self.memory_bar_frame,
            bg="#8b5cf6",
            width=int(self.status.memory_usage * 1.5)
        )
        self.memory_bar.pack(side=tk.LEFT, fill=tk.Y)
    
    def _get_connection_color(self, connection):
        """Retorna a cor para cada estado de conexão"""
        colors = {
            ConnectionStatus.CONNECTED: "#10b981",
            ConnectionStatus.DEGRADED: "#fbbf24",
            ConnectionStatus.DISCONNECTED: "#ef4444"
        }
        return colors.get(connection, "#666666")
    
    def setup_monitoring_chart(self, parent_frame):
        """Configura o gráfico de monitoramento"""
        chart_frame = tk.Frame(
            parent_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            chart_frame,
            text="📊 MONITORAMENTO DE RECURSOS EM TEMPO REAL",
            font=("Arial", 11, "bold"),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # Criar figura matplotlib
        self.fig = Figure(figsize=(8, 4), dpi=80, facecolor='#1a1a2e')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#1a1a2e')
        
        # Configurar eixos
        self.ax.set_xlabel('Tempo', color='#666666', fontsize=9)
        self.ax.set_ylabel('Uso (%)', color='#666666', fontsize=9)
        self.ax.tick_params(colors='#666666', labelsize=8)
        self.ax.grid(True, color='#222222', linestyle='--', alpha=0.5)
        self.ax.set_ylim(0, 100)
        
        # Inicializar linhas
        self.cpu_line, = self.ax.plot([], [], color='#3b82f6', 
                                     linewidth=2, label='CPU %')
        self.memory_line, = self.ax.plot([], [], color='#8b5cf6', 
                                        linewidth=2, label='Memory %')
        self.ax.legend(facecolor='#1a1a2e', labelcolor='white', 
                      fontsize=8)
        
        # Adicionar ao Tkinter
        self.chart_canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def setup_recovery_logs(self, parent_frame):
        """Configura os logs de recuperação"""
        logs_frame = tk.Frame(parent_frame, bg="#1a1a2e")
        logs_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        tk.Label(
            logs_frame,
            text="🔧 LOGS DE AUTO-RECUPERAÇÃO",
            font=("Arial", 11, "bold"),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # Canvas para scroll
        self.logs_canvas = tk.Canvas(
            logs_frame,
            bg="#1a1a2e",
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(
            logs_frame,
            orient=tk.VERTICAL,
            command=self.logs_canvas.yview
        )
        
        self.logs_container = tk.Frame(self.logs_canvas, bg="#1a1a2e")
        
        self.logs_container.bind(
            "<Configure>",
            lambda e: self.logs_canvas.configure(
                scrollregion=self.logs_canvas.bbox("all")
            )
        )
        
        self.logs_canvas.create_window(
            (0, 0), 
            window=self.logs_container, 
            anchor="nw"
        )
        self.logs_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.logs_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Atualizar display dos logs
        self.update_logs_display()
    
    def update_logs_display(self):
        """Atualiza a exibição dos logs"""
        # Limpar container
        for widget in self.logs_container.winfo_children():
            widget.destroy()
        
        if not self.logs:
            # Mostrar mensagem quando não há logs
            empty_frame = tk.Frame(
                self.logs_container,
                bg="#1a1a2e",
                relief=tk.FLAT,
                padx=20,
                pady=40
            )
            empty_frame.pack(fill=tk.BOTH, expand=True)
            
            tk.Label(
                empty_frame,
                text="Nenhum incidente registrado.",
                font=("Arial", 11),
                fg="#666666",
                bg="#1a1a2e"
            ).pack()
            
            tk.Label(
                empty_frame,
                text="Sistema está operando normalmente.",
                font=("Courier", 9),
                fg="#444444",
                bg="#1a1a2e"
            ).pack(pady=(5, 0))
        else:
            # Mostrar logs mais recentes primeiro
            for log in reversed(self.logs):
                self.create_log_card(log)
    
    def create_log_card(self, log: RecoveryLog):
        """Cria um card para exibir um log"""
        # Cor do card baseada no resultado
        if log.result == RecoveryResult.SUCCESS:
            bg_color = "#166534"
            border_color = "#4ade80"
            result_color = "#4ade80"
        else:
            bg_color = "#991b1b"
            border_color = "#ef4444"
            result_color = "#ef4444"
        
        card_frame = tk.Frame(
            self.logs_container,
            bg=bg_color + "20",  # Adicionar transparência
            relief=tk.RAISED,
            borderwidth=1,
            highlightbackground=border_color,
            padx=12,
            pady=12
        )
        card_frame.pack(fill=tk.X, pady=5)
        
        # Cabeçalho
        header_frame = tk.Frame(card_frame, bg=bg_color + "20")
        header_frame.pack(fill=tk.X, pady=(0, 8))
        
        tk.Label(
            header_frame,
            text=log.issue,
            font=("Arial", 10, "bold"),
            fg="#ffffff",
            bg=bg_color + "20"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            header_frame,
            text=log.timestamp.strftime("%H:%M:%S"),
            font=("Courier", 8),
            fg="#666666",
            bg=bg_color + "20"
        ).pack(side=tk.RIGHT)
        
        # Ação
        tk.Label(
            card_frame,
            text=log.action,
            font=("Arial", 9),
            fg="#cccccc",
            bg=bg_color + "20",
            wraplength=300,
            justify=tk.LEFT
        ).pack(anchor=tk.W, pady=(0, 8))
        
        # Rodapé
        footer_frame = tk.Frame(card_frame, bg=bg_color + "20")
        footer_frame.pack(fill=tk.X)
        
        tk.Label(
            footer_frame,
            text=log.result.value,
            font=("Arial", 9, "bold"),
            fg=result_color,
            bg=bg_color + "20"
        ).pack(side=tk.LEFT)
        
        if log.agi_intervention:
            agi_frame = tk.Frame(
                footer_frame,
                bg="#4c1d95",
                relief=tk.RAISED,
                borderwidth=1,
                padx=6,
                pady=2
            )
            agi_frame.pack(side=tk.RIGHT)
            
            tk.Label(
                agi_frame,
                text="AGI ACTIVE",
                font=("Courier", 7, "bold"),
                fg="#a855f7",
                bg="#4c1d95"
            ).pack()
    
    def update_chart(self):
        """Atualiza o gráfico com novos dados"""
        if self.history:
            times = list(range(len(self.history)))
            cpu_values = [p['cpu'] for p in self.history]
            memory_values = [p['mem'] for p in self.history]
            
            self.cpu_line.set_data(times, cpu_values)
            self.memory_line.set_data(times, memory_values)
            
            # Ajustar limites
            if times:
                self.ax.set_xlim(0, max(times))
            
            self.ax.set_ylim(0, 100)
            
            self.chart_canvas.draw()
    
    def start_updates(self):
        """Inicia o loop de atualização da interface"""
        def update_loop():
            while True:
                time.sleep(1)  # Atualizar a cada segundo
                
                # Atualizar dados do serviço
                self.status = self.validator.status
                self.logs = self.validator.recovery_logs
                
                # Adicionar ponto ao histórico
                now = datetime.now().strftime("%H:%M:%S")
                new_point = {
                    'time': now,
                    'cpu': self.status.cpu_load,
                    'mem': self.status.memory_usage
                }
                
                self.history.append(new_point)
                if len(self.history) > 20:
                    self.history.pop(0)
                
                # Atualizar UI na thread principal
                self.root.after(0, self.update_ui)
        
        # Iniciar thread de atualização
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
    
    def update_ui(self):
        """Atualiza todos os elementos da interface"""
        # Atualizar status
        bg_color, fg_color = self._get_status_color(self.status.status)
        
        self.status_label.config(
            text=f"STATUS: {self.status.status.value}",
            bg=bg_color,
            fg=fg_color
        )
        
        # Animar status crítico
        if self.status.status == SystemStatus.CRITICAL:
            current_bg = self.status_label.cget("bg")
            new_bg = "#dc2626" if current_bg == "#991b1b" else "#991b1b"
            self.status_label.config(bg=new_bg)
        
        # Atualizar conectividade
        self.connectivity_label.config(
            text=self.status.connection.value,
            fg=self._get_connection_color(self.status.connection)
        )
        
        # Atualizar CPU
        self.cpu_label.config(text=f"{self.status.cpu_load:.1f}%")
        
        # Atualizar cor da barra de CPU
        cpu_color = self._get_cpu_color(self.status.cpu_load)
        self.cpu_bar.config(
            bg=cpu_color,
            width=int(self.status.cpu_load * 1.5)
        )
        
        # Atualizar memória
        self.memory_label.config(text=f"{self.status.memory_usage:.1f}%")
        
        # Atualizar cor da barra de memória
        memory_color = self._get_memory_color(self.status.memory_usage)
        self.memory_bar.config(
            bg=memory_color,
            width=int(self.status.memory_usage * 1.5)
        )
        
        # Atualizar logs
        self.update_logs_display()
        
        # Atualizar gráfico
        self.update_chart()
    
    def _get_cpu_color(self, cpu_load):
        """Retorna a cor baseada na carga da CPU"""
        if cpu_load > 90:
            return "#ef4444"
        elif cpu_load > 80:
            return "#fbbf24"
        return "#3b82f6"
    
    def _get_memory_color(self, memory_usage):
        """Retorna a cor baseada no uso de memória"""
        if memory_usage > 95:
            return "#ef4444"
        elif memory_usage > 85:
            return "#fbbf24"
        return "#8b5cf6"


def main():
    """Função principal da aplicação"""
    root = tk.Tk()
    app = AutonomousValidationDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()