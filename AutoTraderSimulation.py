import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import time
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import threading

# Enums and Types
class LogType(Enum):
    INFO = "INFO"
    ACTION = "ACTION"
    PROFIT = "PROFIT"
    LOSS = "LOSS"

class PositionType(Enum):
    BUY = "BUY"
    SELL = "SELL"

@dataclass
class Position:
    entry_price: float
    size: float
    type: PositionType

@dataclass
class SimulationLog:
    step: int
    message: str
    type: LogType
    timestamp: str

# Mock AGI/ML Services (Replace with actual implementations)
class ContinuousLearner:
    def predict_with_knowledge(self, sample: Dict[str, float]) -> Dict[str, float]:
        # Mock prediction logic
        return {
            'prediction': 0.5 + (random.random() - 0.5) * 0.3,
            'confidence': random.uniform(0.6, 0.95)
        }

class SentientCore:
    def __init__(self):
        self.confidence = 70.0
        self.stability = 80.0
    
    def get_vector(self) -> Dict[str, float]:
        return {
            'confidence': self.confidence,
            'stability': self.stability
        }
    
    def add_thought(self, thought: str):
        # Store thought for AGI processing
        pass
    
    def perceive_reality(self, volatility: float, pnl: float):
        # Adjust emotional vector based on market performance
        self.confidence = max(10, min(100, self.confidence + (pnl * 0.1)))
        self.stability = max(10, min(100, self.stability - (volatility * 5)))

# Main Simulation Engine
class AutoTraderSimulation:
    def __init__(self):
        self.is_running = False
        self.balance = 10000.0
        self.positions: List[Position] = []
        self.history: List[Dict[str, float]] = [{'step': 0, 'balance': 10000.0}]
        self.logs: List[SimulationLog] = []
        self.current_step = 0
        self.market_price = 100.0
        
        # Initialize AGI services
        self.continuous_learner = ContinuousLearner()
        self.sentient_core = SentientCore()
        
        # Initial logs
        self.add_log("Inicializando AutoTrader Neural...", LogType.INFO)
        self.add_log(f"Saldo Inicial: ${self.balance:.2f}", LogType.INFO)
    
    def add_log(self, message: str, log_type: LogType):
        log = SimulationLog(
            step=self.current_step,
            message=message,
            type=log_type,
            timestamp=datetime.now().strftime("%H:%M:%S")
        )
        self.logs.append(log)
        # Keep last 100 logs
        if len(self.logs) > 100:
            self.logs.pop(0)
    
    def generate_market_sample(self) -> Dict[str, float]:
        # Random walk with trend
        volatility = 0.02  # 2%
        change = (random.random() - 0.5) * volatility * self.market_price
        new_price = self.market_price + change
        
        return {
            'price': new_price,
            'rsi': 30 + random.random() * 40,
            'macd': (random.random() - 0.5),
            'volatility': volatility,
            'volume_normalized': random.random()
        }
    
    def execute_step(self):
        if not self.is_running:
            return
        
        self.current_step += 1
        sample = self.generate_market_sample()
        self.market_price = sample['price']
        
        # 1. Consult AGI (Advisor)
        prediction = self.continuous_learner.predict_with_knowledge(sample)
        emotion = self.sentient_core.get_vector()
        
        # Decision logic (Adjusted by AGI)
        decision = 'HOLD'
        threshold = 0.6
        adjusted_threshold = threshold - (emotion['confidence'] / 500)
        
        if prediction['prediction'] > (0.5 + adjusted_threshold / 2):
            decision = 'BUY'
        elif prediction['prediction'] < (0.5 - adjusted_threshold / 2):
            decision = 'SELL'
        
        # 2. Execute action
        current_balance = self.balance
        active_positions = self.positions.copy()
        pnl = 0.0
        
        if decision == 'BUY':
            size = self.calculate_position_size(current_balance)
            if current_balance >= size:
                active_positions.append(Position(
                    entry_price=sample['price'],
                    size=size,
                    type=PositionType.BUY
                ))
                current_balance -= size  # Blocked margin
                self.add_log(
                    f"COMPRA @ {sample['price']:.2f} | Confiança: {(prediction['confidence'] * 100):.0f}%",
                    LogType.ACTION
                )
                self.sentient_core.add_thought("Oportunidade de compra detectada. Confiança neural elevada.")
        
        elif decision == 'SELL' and active_positions:
            # Close all positions (Simplification)
            for pos in active_positions:
                profit = (sample['price'] - pos.entry_price) * (pos.size / pos.entry_price)
                current_balance += pos.size + profit
                pnl += profit
            active_positions = []
            
            log_type = LogType.PROFIT if pnl >= 0 else LogType.LOSS
            self.add_log(f"VENDA @ {sample['price']:.2f} | PnL: ${pnl:.2f}", log_type)
            
            # Feedback for AGI
            self.sentient_core.perceive_reality(sample['volatility'], pnl)
        
        # Update state
        self.balance = current_balance
        self.positions = active_positions
        
        equity = self.calculate_equity(current_balance, active_positions, sample['price'])
        self.history.append({'step': self.current_step, 'balance': equity})
    
    def calculate_position_size(self, current_balance: float) -> float:
        emotion = self.sentient_core.get_vector()
        risk_pct = 0.1  # Base 10%
        
        if emotion['confidence'] > 80:
            risk_pct = 0.15
        if emotion['stability'] < 30:
            risk_pct = 0.05
        
        return current_balance * risk_pct
    
    def calculate_equity(self, cash: float, active_pos: List[Position], current_price: float) -> float:
        equity = cash
        for pos in active_pos:
            val = (current_price / pos.entry_price) * pos.size
            equity += val
        return equity
    
    def reset_simulation(self):
        self.is_running = False
        self.balance = 10000.0
        self.positions = []
        self.history = [{'step': 0, 'balance': 10000.0}]
        self.logs = []
        self.current_step = 0
        self.market_price = 100.0
        self.add_log("Simulação Reiniciada.", LogType.INFO)

# Tkinter Dashboard
class AutoTraderDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("SIMULADOR AUTOTRADER NEURAL")
        self.root.geometry("1400x800")
        self.root.configure(bg="#0a0a0a")
        
        # Initialize simulation
        self.simulation = AutoTraderSimulation()
        
        # Setup UI
        self.setup_ui()
        
        # Start update loop
        self.update_interval = 1000  # 1 second
        self.update_ui()
    
    def setup_ui(self):
        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#0a0a0a")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.setup_header()
        
        # Content
        self.setup_content()
    
    def setup_header(self):
        header_frame = tk.Frame(self.main_frame, bg="#1a1a2e", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # Logo and title
        left_frame = tk.Frame(header_frame, bg="#1a1a2e")
        left_frame.pack(side=tk.LEFT, padx=20)
        
        # Icon
        icon_frame = tk.Frame(left_frame, bg="#064e3b", relief=tk.RAISED, borderwidth=1, padx=10, pady=10)
        icon_frame.pack(side=tk.LEFT, padx=(0, 15))
        tk.Label(icon_frame, text="▶", font=("Arial", 16), bg="#064e3b", fg="#10b981").pack()
        
        # Text
        text_frame = tk.Frame(left_frame, bg="#1a1a2e")
        text_frame.pack(side=tk.LEFT)
        
        tk.Label(text_frame, text="SIMULADOR AUTOTRADER NEURAL", 
                font=("Arial", 16, "bold"), fg="#ffffff", bg="#1a1a2e").pack(anchor=tk.W)
        
        tk.Label(text_frame, text="BACKTESTING EM TEMPO REAL • MOTOR AGI", 
                font=("Courier", 10), fg="#10b981", bg="#1a1a2e").pack(anchor=tk.W)
        
        # Control buttons
        right_frame = tk.Frame(header_frame, bg="#1a1a2e")
        right_frame.pack(side=tk.RIGHT, padx=20)
        
        # Net worth display
        net_worth_frame = tk.Frame(right_frame, bg="#1a1a2e")
        net_worth_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(net_worth_frame, text="Patrimônio Líquido", 
                font=("Arial", 8), fg="#666666", bg="#1a1a2e").pack(anchor=tk.E)
        
        self.equity_label = tk.Label(net_worth_frame, text="$10,000.00", 
                                    font=("Courier", 18, "bold"), fg="#10b981", bg="#1a1a2e")
        self.equity_label.pack()
        
        # Control buttons
        button_frame = tk.Frame(right_frame, bg="#1a1a2e")
        button_frame.pack(side=tk.LEFT)
        
        self.run_button = tk.Button(
            button_frame,
            text="EXECUTAR",
            command=self.toggle_simulation,
            font=("Arial", 10, "bold"),
            bg="#166534",
            fg="#ffffff",
            activebackground="#15803d",
            activeforeground="#ffffff",
            padx=20,
            pady=8,
            borderwidth=1,
            relief=tk.RAISED
        )
        self.run_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.reset_button = tk.Button(
            button_frame,
            text="↻",
            command=self.reset_simulation,
            font=("Arial", 12),
            bg="#374151",
            fg="#ffffff",
            activebackground="#4b5563",
            activeforeground="#ffffff",
            padx=10,
            pady=8,
            borderwidth=1,
            relief=tk.RAISED
        )
        self.reset_button.pack(side=tk.LEFT)
    
    def setup_content(self):
        content_frame = tk.Frame(self.main_frame, bg="#0a0a0a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configure grid
        content_frame.grid_columnconfigure(0, weight=2)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel: Charts and stats
        left_frame = tk.Frame(content_frame, bg="#0a0a0a")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Equity chart
        self.setup_equity_chart(left_frame)
        
        # Statistics
        self.setup_statistics(left_frame)
        
        # Right panel: Terminal log
        right_frame = tk.Frame(content_frame, bg="#1a1a2e", relief=tk.RAISED, borderwidth=1)
        right_frame.grid(row=0, column=1, sticky="nsew")
        
        self.setup_terminal_log(right_frame)
    
    def setup_equity_chart(self, parent_frame):
        chart_frame = tk.Frame(parent_frame, bg="#1a1a2e", relief=tk.RAISED, borderwidth=1)
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        tk.Label(chart_frame, text="📊 CURVA DE EQUITY", 
                font=("Arial", 11, "bold"), fg="#666666", bg="#1a1a2e").pack(anchor=tk.W, padx=15, pady=10)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(10, 4), dpi=80, facecolor='#1a1a2e')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#1a1a2e')
        
        # Configure axes
        self.ax.set_xlabel('Passos', color='#666666', fontsize=9)
        self.ax.set_ylabel('Equity ($)', color='#666666', fontsize=9)
        self.ax.tick_params(colors='#666666', labelsize=8)
        self.ax.grid(True, color='#222222', linestyle='--', alpha=0.5)
        
        # Initial empty plot
        self.equity_line, = self.ax.plot([], [], color='#3b82f6', linewidth=2)
        
        # Add to Tkinter
        self.chart_canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
    
    def setup_statistics(self, parent_frame):
        stats_frame = tk.Frame(parent_frame, bg="#0a0a0a")
        stats_frame.pack(fill=tk.X)
        
        # Stats grid
        stats_data = [
            ("Passos Simulados", "0", "#ffffff"),
            ("Posições Abertas", "0", "#fbbf24"),
            ("Lucro Total", "$0.00", "#10b981")
        ]
        
        for i, (title, value, color) in enumerate(stats_data):
            stat_frame = tk.Frame(stats_frame, bg="black", relief=tk.RAISED, borderwidth=1)
            stat_frame.grid(row=0, column=i, padx=(0, 10) if i < 2 else 0, sticky="nsew")
            stat_frame.columnconfigure(0, weight=1)
            
            tk.Label(stat_frame, text=title, font=("Arial", 8), 
                    fg="#666666", bg="black").pack(pady=(10, 2))
            
            value_label = tk.Label(stat_frame, text=value, font=("Courier", 16, "bold"), 
                                  fg=color, bg="black")
            value_label.pack(pady=(0, 10))
            
            # Store references for updates
            if title == "Passos Simulados":
                self.steps_label = value_label
            elif title == "Posições Abertas":
                self.positions_label = value_label
            elif title == "Lucro Total":
                self.profit_label = value_label
        
        # Equal column weights
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        stats_frame.grid_columnconfigure(2, weight=1)
    
    def setup_terminal_log(self, parent_frame):
        log_frame = tk.Frame(parent_frame, bg="#000000")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(log_frame, text="NEURAL_EXECUTION_LOG", 
                font=("Courier", 10, "bold"), fg="#10b981", bg="#000000").pack(anchor=tk.W, pady=(0, 10))
        
        # Create scrolled text widget
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            bg="#000000",
            fg="#cccccc",
            font=("Courier", 9),
            insertbackground="#ffffff",
            wrap=tk.WORD,
            height=20,
            borderwidth=0,
            highlightthickness=0
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for different log types
        self.log_text.tag_config("INFO", foreground="#666666")
        self.log_text.tag_config("ACTION", foreground="#3b82f6")
        self.log_text.tag_config("PROFIT", foreground="#10b981")
        self.log_text.tag_config("LOSS", foreground="#ef4444")
        
        # Status bar
        status_frame = tk.Frame(log_frame, bg="#000000")
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(status_frame, text="⚡ AGI ACTIVE", 
                font=("Courier", 8), fg="#fbbf24", bg="#000000").pack(side=tk.LEFT)
        
        tk.Label(status_frame, text="🛡️ RISK: ADAPTIVE", 
                font=("Courier", 8), fg="#10b981", bg="#000000").pack(side=tk.RIGHT)
    
    def toggle_simulation(self):
        self.simulation.is_running = not self.simulation.is_running
        
        if self.simulation.is_running:
            self.run_button.config(text="PAUSAR", bg="#854d0e", activebackground="#a16207")
            self.simulation.add_log("Simulação em execução...", LogType.INFO)
        else:
            self.run_button.config(text="EXECUTAR", bg="#166534", activebackground="#15803d")
            self.simulation.add_log("Simulação pausada.", LogType.INFO)
    
    def reset_simulation(self):
        self.simulation.reset_simulation()
        self.run_button.config(text="EXECUTAR", bg="#166534", activebackground="#15803d")
    
    def update_ui(self):
        # Execute simulation step if running
        if self.simulation.is_running:
            self.simulation.execute_step()
        
        # Update equity display
        equity = self.simulation.calculate_equity(
            self.simulation.balance,
            self.simulation.positions,
            self.simulation.market_price
        )
        
        # Update equity label with color coding
        equity_text = f"${equity:,.2f}"
        equity_color = "#10b981" if equity >= 10000 else "#ef4444"
        self.equity_label.config(text=equity_text, fg=equity_color)
        
        # Update statistics
        self.steps_label.config(text=str(self.simulation.current_step))
        self.positions_label.config(text=str(len(self.simulation.positions)))
        
        total_profit = equity - 10000
        profit_text = f"${total_profit:+,.2f}"
        profit_color = "#10b981" if total_profit >= 0 else "#ef4444"
        self.profit_label.config(text=profit_text, fg=profit_color)
        
        # Update chart
        self.update_chart()
        
        # Update terminal log
        self.update_terminal_log()
        
        # Schedule next update
        self.root.after(self.update_interval, self.update_ui)
    
    def update_chart(self):
        if len(self.simulation.history) > 1:
            steps = [h['step'] for h in self.simulation.history]
            balances = [h['balance'] for h in self.simulation.history]
            
            # Update plot data
            self.equity_line.set_data(steps, balances)
            
            # Adjust axes limits
            self.ax.relim()
            self.ax.autoscale_view()
            
            # Redraw canvas
            self.chart_canvas.draw()
    
    def update_terminal_log(self):
        # Clear and repopulate log display
        self.log_text.delete(1.0, tk.END)
        
        for log in self.simulation.logs[-20:]:  # Show last 20 logs
            timestamp = f"[{log.timestamp}]"
            log_type = log.type.value
            message = log.message
            
            # Insert with appropriate formatting
            self.log_text.insert(tk.END, f"{timestamp} ", "INFO")
            self.log_text.insert(tk.END, f"{log_type:8} ", log.type.value)
            self.log_text.insert(tk.END, f"{message}\n")
        
        # Scroll to bottom
        self.log_text.see(tk.END)

def main():
    root = tk.Tk()
    app = AutoTraderDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()