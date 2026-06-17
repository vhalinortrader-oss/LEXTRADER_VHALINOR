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
class ConditionStatus(Enum):
    FAVORABLE = "FAVORABLE"
    NEUTRAL = "NEUTRAL"
    UNFAVORABLE = "UNFAVORABLE"

class OperationalAction(Enum):
    OPERATE = "OPERATE"
    PRESERVE_CAPITAL = "PRESERVE_CAPITAL"
    REDUCE_EXPOSURE = "REDUCE_EXPOSURE"
    INCREASE_ALLOCATION = "INCREASE_ALLOCATION"

# Estruturas de dados equivalentes às interfaces TypeScript
@dataclass
class MarketCondition:
    indicator: str
    value: float
    status: ConditionStatus
    weight: float
    reasoning: str

@dataclass
class OperationalDecision:
    action: OperationalAction
    confidence: float
    reasoning: List[str]
    risk_assessment: float
    expected_outcome: str
    timestamp: datetime

class IAGConsciousnessEngineApp:
    """Aplicação principal que replica a funcionalidade do componente React IAGConsciousnessEngine"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("👁️ Consciência Operacional IAG")
        self.root.geometry("1500x1000")
        self.root.configure(bg='#f8fafc')
        
        # Estado da aplicação (equivalente aos useState hooks)
        self.consciousness_level = 94.7
        self.is_operating = True
        self.market_conditions: List[MarketCondition] = []
        self.current_decision: OperationalDecision = None
        self.capital_preserved = 0.0
        self.risk_awareness = 96.3
        
        # Containers para widgets que precisam ser atualizados
        self.consciousness_badge = None
        self.status_badge = None
        self.decision_frame = None
        self.conditions_frame = None
        self.metrics_labels = {}
        self.control_button = None
        
        # Thread de atualização
        self.update_thread = None
        self.stop_updates = False
        
        # Configurar estilos
        self.setup_styles()
        
        # Configurar interface
        self.setup_ui()
        
        # Iniciar motor de consciência (equivalente ao useEffect)
        self.start_consciousness_engine()
    
    def setup_styles(self) -> None:
        """Configurar estilos customizados para a aplicação"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar cores personalizadas
        style.configure('Primary.TButton', 
                       background='#3b82f6', 
                       foreground='white',
                       focuscolor='none')
        
        style.configure('Danger.TButton', 
                       background='#ef4444', 
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
    def get_condition_color(self, status: ConditionStatus) -> str:
        """Obter cor para status da condição (equivalente a getConditionColor)"""
        color_map = {
            ConditionStatus.FAVORABLE: "#10b981",
            ConditionStatus.NEUTRAL: "#6b7280",
            ConditionStatus.UNFAVORABLE: "#ef4444"
        }
        return color_map.get(status, "#6b7280")
    
    def get_action_icon(self, action: OperationalAction) -> str:
        """Obter ícone para ação (equivalente a getActionIcon)"""
        icon_map = {
            OperationalAction.OPERATE: "▶️",
            OperationalAction.PRESERVE_CAPITAL: "🛡️",
            OperationalAction.REDUCE_EXPOSURE: "📉",
            OperationalAction.INCREASE_ALLOCATION: "📈"
        }
        return icon_map.get(action, "📊")
    
    def get_action_color(self, action: OperationalAction) -> str:
        """Obter cor para ação (equivalente a getActionColor)"""
        color_map = {
            OperationalAction.OPERATE: "#10b981",
            OperationalAction.PRESERVE_CAPITAL: "#f59e0b",
            OperationalAction.REDUCE_EXPOSURE: "#ef4444",
            OperationalAction.INCREASE_ALLOCATION: "#3b82f6"
        }
        return color_map.get(action, "#6b7280")
    
    # Funções principais (equivalentes às funções do React)
    def init_market_conditions(self) -> List[MarketCondition]:
        """Inicializar condições de mercado (equivalente a initMarketConditions)"""
        return [
            MarketCondition(
                indicator='Volatilidade de Mercado',
                value=18.5,
                status=ConditionStatus.NEUTRAL,
                weight=0.25,
                reasoning='VIX em níveis normais, mas com tendência de alta'
            ),
            MarketCondition(
                indicator='Liquidez Global',
                value=87.3,
                status=ConditionStatus.FAVORABLE,
                weight=0.20,
                reasoning='Spreads apertados e volume consistente'
            ),
            MarketCondition(
                indicator='Sentimento Institucional',
                value=72.1,
                status=ConditionStatus.FAVORABLE,
                weight=0.18,
                reasoning='Flow positivo de grandes investidores'
            ),
            MarketCondition(
                indicator='Correlações Anômalas',
                value=34.6,
                status=ConditionStatus.UNFAVORABLE,
                weight=0.15,
                reasoning='Aumento de correlações entre ativos descorrelacionados'
            ),
            MarketCondition(
                indicator='Eventos Geopolíticos',
                value=61.8,
                status=ConditionStatus.NEUTRAL,
                weight=0.12,
                reasoning='Tensões moderadas sem impacto sistêmico imediato'
            ),
            MarketCondition(
                indicator='Ciclo de Bancos Centrais',
                value=78.9,
                status=ConditionStatus.FAVORABLE,
                weight=0.10,
                reasoning='Política monetária suportiva mantida'
            )
        ]
    
    def evaluate_operational_decision(self, conditions: List[MarketCondition]) -> OperationalDecision:
        """Avaliar decisão operacional (equivalente a evaluateOperationalDecision)"""
        # Calcular score ponderado
        weighted_score = 0.0
        for condition in conditions:
            if condition.status == ConditionStatus.FAVORABLE:
                score = 1.0
            elif condition.status == ConditionStatus.NEUTRAL:
                score = 0.5
            else:
                score = 0.0
            weighted_score += score * condition.weight
        
        confidence = weighted_score * 100
        risk_level = 100 - confidence
        
        if confidence > 75:
            return OperationalDecision(
                action=OperationalAction.OPERATE,
                confidence=confidence,
                reasoning=[
                    'Condições de mercado favoráveis identificadas',
                    'Múltiplos indicadores confirmam ambiente propício',
                    'Risco sistêmico em níveis aceitáveis',
                    'Oportunidades de alpha detectadas'
                ],
                risk_assessment=risk_level,
                expected_outcome='Operação com agressividade normal',
                timestamp=datetime.now()
            )
        elif confidence > 50:
            return OperationalDecision(
                action=OperationalAction.REDUCE_EXPOSURE,
                confidence=confidence,
                reasoning=[
                    'Condições mistas identificadas',
                    'Alguns indicadores mostram cautela',
                    'Redução preventiva de exposição recomendada',
                    'Manutenção de posições defensivas'
                ],
                risk_assessment=risk_level,
                expected_outcome='Operação reduzida e seletiva',
                timestamp=datetime.now()
            )
        else:
            return OperationalDecision(
                action=OperationalAction.PRESERVE_CAPITAL,
                confidence=confidence,
                reasoning=[
                    'Condições desfavoráveis dominam o cenário',
                    'Múltiplos sinais de alerta detectados',
                    'Preservação de capital é prioridade',
                    'Aguardar melhoria das condições'
                ],
                risk_assessment=risk_level,
                expected_outcome='Suspensão temporária de operações',
                timestamp=datetime.now()
            )
    
    def update_consciousness(self) -> None:
        """Atualizar consciência (equivalente a updateConsciousness)"""
        # Atualizar condições de mercado
        conditions = self.init_market_conditions()
        for condition in conditions:
            condition.value = max(0, min(100, condition.value + (random.random() - 0.5) * 10))
            # Determinar status baseado no valor
            if condition.value > 70:
                condition.status = ConditionStatus.FAVORABLE
            elif condition.value > 40:
                condition.status = ConditionStatus.NEUTRAL
            else:
                condition.status = ConditionStatus.UNFAVORABLE
        
        self.market_conditions = conditions
        
        # Avaliar decisão operacional
        decision = self.evaluate_operational_decision(conditions)
        self.current_decision = decision
        
        # Atualizar consciência baseada na qualidade das condições
        avg_condition = sum(c.value for c in conditions) / len(conditions)
        self.consciousness_level = max(85, min(99, avg_condition + random.random() * 5))
        
        # Simular preservação de capital
        if decision.action == OperationalAction.PRESERVE_CAPITAL:
            self.capital_preserved += 0.1
        
        # Atualizar awareness de risco
        self.risk_awareness = max(90, min(99, 96 + (random.random() - 0.5) * 6))
        
        # Atualizar UI na thread principal
        self.root.after(0, self.update_ui)
    
    def toggle_operation(self) -> None:
        """Alternar operação (equivalente ao onClick do botão)"""
        self.is_operating = not self.is_operating
        self.update_control_button()
    
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
        
        # Decisão operacional atual
        self.setup_decision_section(container)
        
        # Condições de mercado
        self.setup_conditions_section(container)
        
        # Métricas de consciência
        self.setup_metrics_section(container)
        
        # Controle manual
        self.setup_control_section(container)
        
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
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 30))
        
        # Lado esquerdo: ícone e título
        left_frame = ttk.Frame(header_frame)
        left_frame.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(left_frame, text="👁️", font=("Arial", 18)).grid(row=0, column=0, padx=(0, 8))
        ttk.Label(left_frame, text="🧠 Consciência Operacional IAG", 
                 font=("Arial", 18, "bold")).grid(row=0, column=1)
        
        # Lado direito: badges
        right_frame = ttk.Frame(header_frame)
        right_frame.grid(row=0, column=1, sticky=tk.E)
        
        # Badge consciência
        self.consciousness_badge = tk.Label(right_frame, 
                                           text=f"🧠 Consciência: {self.consciousness_level:.1f}%",
                                           bg="#3b82f6",
                                           fg="white",
                                           font=("Arial", 9, "bold"),
                                           padx=8, pady=4)
        self.consciousness_badge.grid(row=0, column=0, padx=(0, 8))
        
        # Badge status
        status_text = "📊 ATIVO" if self.is_operating else "⏸️ STANDBY"
        status_color = "#10b981" if self.is_operating else "#6b7280"
        self.status_badge = tk.Label(right_frame, 
                                    text=status_text,
                                    bg=status_color,
                                    fg="white",
                                    font=("Arial", 9, "bold"),
                                    padx=8, pady=4)
        self.status_badge.grid(row=0, column=1)
        
        header_frame.columnconfigure(0, weight=1)
    
    def setup_decision_section(self, parent: ttk.Frame) -> None:
        """Configurar seção de decisão operacional"""
        self.decision_frame = ttk.Frame(parent)
        self.decision_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 30))
        
        self.decision_frame.columnconfigure(0, weight=1)
    
    def setup_conditions_section(self, parent: ttk.Frame) -> None:
        """Configurar seção de condições de mercado"""
        conditions_section = ttk.Frame(parent)
        conditions_section.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 30))
        
        # Título
        title_frame = ttk.Frame(conditions_section)
        title_frame.grid(row=0, column=0, sticky=tk.W, pady=(0, 15))
        
        ttk.Label(title_frame, text="⚡", font=("Arial", 12)).grid(row=0, column=0, padx=(0, 5))
        ttk.Label(title_frame, text="Análise de Condições de Mercado", 
                 font=("Arial", 12, "bold")).grid(row=0, column=1)
        
        # Frame para condições
        self.conditions_frame = ttk.Frame(conditions_section)
        self.conditions_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        conditions_section.columnconfigure(0, weight=1)
        self.conditions_frame.columnconfigure(0, weight=1)
    
    def setup_metrics_section(self, parent: ttk.Frame) -> None:
        """Configurar seção de métricas de consciência"""
        metrics_section = ttk.Frame(parent)
        metrics_section.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 30))
        
        # Título
        title_frame = ttk.Frame(metrics_section)
        title_frame.grid(row=0, column=0, sticky=tk.W, pady=(0, 15))
        
        ttk.Label(title_frame, text="📊", font=("Arial", 12)).grid(row=0, column=0, padx=(0, 5))
        ttk.Label(title_frame, text="Métricas de Consciência", 
                 font=("Arial", 12, "bold")).grid(row=0, column=1)
        
        # Labels para métricas
        metrics_grid = ttk.GridFrame(metrics_section)
        metrics_grid.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Capital Preservado
        capital_label = ttk.Label(metrics_grid, text="Capital Preservado", 
                                  style='Muted.TLabel', font=("Arial", 9))
        capital_label.grid(row=0, column=0, padx=(0, 20))
        
        capital_value = ttk.Label(metrics_grid, text=f"{self.capital_preserved:.1f}%", 
                                  style='Success.TLabel', font=("Arial", 16, "bold"))
        capital_value.grid(row=1, column=0, padx=(0, 20))
        
        # Awareness de Risco
        risk_label = ttk.Label(metrics_grid, text="Awareness de Risco", 
                              style='Muted.TLabel', font=("Arial", 9))
        risk_label.grid(row=0, column=1)
        
        risk_value = ttk.Label(metrics_grid, text=f"{self.risk_awareness:.1f}%", 
                              style='Info.TLabel', font=("Arial", 16, "bold"))
        risk_value.grid(row=1, column=1)
        
        metrics_grid.columnconfigure(0, weight=1)
        metrics_grid.columnconfigure(1, weight=1)
    
    def setup_control_section(self, parent: ttk.Frame) -> None:
        """Configurar seção de controle manual"""
        control_section = ttk.Frame(parent)
        control_section.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 30))
        
        # Botão de controle
        self.control_button = ttk.Button(control_section, text="Pausar Consciência", 
                                        style='Danger.TButton', command=self.toggle_operation)
        self.control_button.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        control_section.columnconfigure(0, weight=1)
    
    def update_ui(self) -> None:
        """Atualizar toda a interface"""
        # Atualizar badges do header
        if self.consciousness_badge:
            self.consciousness_badge.config(text=f"🧠 Consciência: {self.consciousness_level:.1f}%")
        
        # Atualizar seção de decisão
        self.update_decision_display()
        
        # Atualizar condições de mercado
        self.update_conditions_display()
        
        # Atualizar métricas
        self.update_metrics_display()
    
    def update_decision_display(self) -> None:
        """Atualizar display de decisão operacional"""
        # Limpar frame
        for widget in self.decision_frame.winfo_children():
            widget.destroy()
        
        if not self.current_decision:
            return
        
        decision = self.current_decision
        
        # Ação principal
        action_frame = ttk.Frame(self.decision_frame)
        action_frame.grid(row=0, column=0, pady=(0, 20))
        
        action_color = self.get_action_color(decision.action)
        action_icon = self.get_action_icon(decision.action)
        action_text = decision.action.value.replace('_', ' ')
        
        action_button = tk.Label(action_frame, 
                                text=f"{action_icon} {action_text}",
                                bg=action_color, fg="white",
                                font=("Arial", 14, "bold"),
                                padx=20, pady=10)
        action_button.grid(row=0, column=0)
        
        # Grid de métricas de confiança
        metrics_grid = ttk.Frame(self.decision_frame)
        metrics_grid.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Confiança
        confidence_frame = ttk.Frame(metrics_grid)
        confidence_frame.grid(row=0, column=0, padx=(0, 20))
        
        ttk.Label(confidence_frame, text="Nível de Confiança", 
                 style='Muted.TLabel', font=("Arial", 9)).grid(row=0, column=0)
        ttk.Label(confidence_frame, text=f"{decision.confidence:.1f}%", 
                 style='Info.TLabel', font=("Arial", 16, "bold")).grid(row=1, column=0)
        
        # Risco
        risk_frame = ttk.Frame(metrics_grid)
        risk_frame.grid(row=0, column=1)
        
        ttk.Label(risk_frame, text="Avaliação de Risco", 
                 style='Muted.TLabel', font=("Arial", 9)).grid(row=0, column=0)
        ttk.Label(risk_frame, text=f"{decision.risk_assessment:.1f}%", 
                 style='Warning.TLabel', font=("Arial", 16, "bold")).grid(row=1, column=0)
        
        metrics_grid.columnconfigure(0, weight=1)
        metrics_grid.columnconfigure(1, weight=1)
        
        # Raciocínio da IAG
        reasoning_frame = tk.Frame(self.decision_frame, bg="#f1f5f9", relief='solid', borderwidth=1)
        reasoning_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        reasoning_content = tk.Frame(reasoning_frame, bg="#f1f5f9")
        reasoning_content.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=15, pady=12)
        
        # Título do raciocínio
        title_frame = tk.Frame(reasoning_content, bg="#f1f5f9")
        title_frame.grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        
        ttk.Label(title_frame, text="🎯", font=("Arial", 12)).grid(row=0, column=0, padx=(0, 5))
        reasoning_title = tk.Label(title_frame, text="Raciocínio da IAG",
                                  bg="#f1f5f9", font=("Arial", 10, "bold"))
        reasoning_title.grid(row=0, column=1)
        
        # Lista de raciocínio
        for i, reason in enumerate(decision.reasoning):
            reason_frame = tk.Frame(reasoning_content, bg="#f1f5f9")
            reason_frame.grid(row=i+1, column=0, sticky=tk.W, pady=1)
            
            ttk.Label(reason_frame, text="✅", font=("Arial", 8)).grid(row=0, column=0, padx=(0, 5))
            reason_label = tk.Label(reason_frame, text=reason, bg="#f1f5f9", 
                                   font=("Arial", 9), wraplength=600)
            reason_label.grid(row=0, column=1, sticky=tk.W)
        
        # Resultado esperado
        outcome_frame = tk.Frame(reasoning_content, bg="#f1f5f9")
        outcome_frame.grid(row=len(decision.reasoning)+2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        separator = tk.Frame(outcome_frame, bg="#d1d5db", height=1)
        separator.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 8))
        
        outcome_label = tk.Label(outcome_frame, 
                                text=f"Resultado Esperado: {decision.expected_outcome}",
                                bg="#f1f5f9", fg="#3b82f6", font=("Arial", 10, "bold"))
        outcome_label.grid(row=1, column=0, sticky=tk.W)
        
        outcome_frame.columnconfigure(0, weight=1)
        reasoning_content.columnconfigure(0, weight=1)
        reasoning_frame.columnconfigure(0, weight=1)
        
        self.decision_frame.columnconfigure(0, weight=1)
    
    def update_conditions_display(self) -> None:
        """Atualizar display das condições de mercado"""
        # Limpar frame
        for widget in self.conditions_frame.winfo_children():
            widget.destroy()
        
        # Adicionar condições atualizadas
        for condition in self.market_conditions:
            condition_frame = ttk.Frame(self.conditions_frame)
            condition_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
            
            # Indicador e status
            indicator_label = ttk.Label(condition_frame, text=condition.indicator, 
                                        font=("Arial", 10, "bold"))
            indicator_label.grid(row=0, column=0, sticky=tk.W)
            
            status_badge = ttk.Label(condition_frame, text=condition.status.value, 
                                    background=self.get_condition_color(condition.status),
                                    foreground="white",
                                    font=("Arial", 9, "bold"),
                                    padding=(8, 4))
            status_badge.grid(row=0, column=1, padx=(8, 0))
            
            # Valor e peso
            value_label = ttk.Label(condition_frame, text=f"{condition.value:.1f}",
                                   font=("Arial", 10, "bold"))
            value_label.grid(row=1, column=0, sticky=tk.W)
            
            weight_label = ttk.Label(condition_frame, text=f"Peso: {condition.weight*100:.0f}%",
                                    style='Muted.TLabel', font=("Arial", 9))
            weight_label.grid(row=1, column=1, sticky=tk.E)
        
        self.conditions_frame.columnconfigure(0, weight=1)
    
    def update_metrics_display(self) -> None:
        """Atualizar display das métricas de consciência"""
        if not self.metrics_labels:
            return
        
        # Atualizar capital preservado
        capital_label = self.metrics_labels.get("capital_preserved")
        if capital_label:
            capital_label.config(text=f"{self.capital_preserved:.1f}%")
        
        # Atualizar awareness de risco
        risk_label = self.metrics_labels.get("risk_awareness")
        if risk_label:
            risk_label.config(text=f"{self.risk_awareness:.1f}%")
    
    def update_control_button(self) -> None:
        """Atualizar estado do botão de controle"""
        if self.control_button:
            new_text = "Pausar Consciência" if self.is_operating else "Ativar Consciência"
            new_style = 'Danger.TButton' if self.is_operating else 'Primary.TButton'
            self.control_button.config(text=new_text, style=new_style)
    
    def start_consciousness_engine(self) -> None:
        """Iniciar motor de consciência (equivalente ao useEffect)"""
        def consciousness_worker():
            # Primeira atualização
            self.update_consciousness()
            
            while not self.stop_updates:
                time.sleep(8)  # Equivalente ao interval de 8000ms
                
                if not self.stop_updates:
                    self.update_consciousness()
        
        self.update_thread = threading.Thread(target=consciousness_worker, daemon=True)
        self.update_thread.start()
    
    def __del__(self):
        """Destrutor para parar thread de atualização"""
        self.stop_updates = True


def main() -> None:
    """Função principal para executar a aplicação (equivalente ao export do React)"""
    root = tk.Tk()
    app = IAGConsciousnessEngineApp(root)
    
    # Tornar a janela responsiva
    root.minsize(1300, 900)
    
    # Centralizar janela
    root.eval('tk::PlaceWindow . center')
    
    # Iniciar loop principal
    root.mainloop()


if __name__ == "__main__":
    main()