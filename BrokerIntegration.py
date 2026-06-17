import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import time
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import threading
from queue import Queue

# Data Types
class PlatformType(Enum):
    CTRADER = "CTRADER"
    HOMEBROKER = "HOMEBROKER"

class TabType(Enum):
    EXECUTION = "EXECUTION"
    CALGO = "CALGO"
    SIMULATOR = "SIMULATOR"

class BotStatus(Enum):
    STOPPED = "STOPPED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"

class LevelType(Enum):
    ASK = "ASK"
    BID = "BID"

@dataclass
class AssetQuote:
    symbol: str
    price: float
    change: float
    bid: float
    ask: float
    spread: float

@dataclass
class MarketDepthLevel:
    price: float
    volume: float
    level_type: LevelType

@dataclass
class BotParameter:
    name: str
    value: float
    param_type: str

@dataclass
class CBotInstance:
    id: str
    name: str
    code: str
    status: BotStatus
    win_rate: float
    net_profit: float
    parameters: List[BotParameter]
    logs: List[str]

@dataclass
class ChartDataPoint:
    time: datetime
    value: float

# Mock Services
class SentientCore:
    def perceive_reality(self, volatility: float, sentiment: float):
        # Mock AGI perception
        pass

class cTraderService:
    def __init__(self):
        self.bots = [
            CBotInstance(
                id="bot1",
                name="TrendScalperV2",
                code="""using System;
using cAlgo.API;
using cAlgo.API.Indicators;

[Robot(TimeZone = TimeZones.UTC, AccessRights = AccessRights.FullAccess)]
public class TrendScalperV2 : Robot
{
    [Parameter("Risk %", DefaultValue = 2.0)]
    public double RiskPercent { get; set; }
    
    [Parameter("ATR Period", DefaultValue = 14)]
    public int AtrPeriod { get; set; }
    
    private AverageTrueRange atr;
    private ExponentialMovingAverage emaFast;
    private ExponentialMovingAverage emaSlow;
    
    protected override void OnStart()
    {
        atr = Indicators.AverageTrueRange(AtrPeriod, MovingAverageType.Simple);
        emaFast = Indicators.ExponentialMovingAverage(Bars.ClosePrices, 9);
        emaSlow = Indicators.ExponentialMovingAverage(Bars.ClosePrices, 21);
    }
    
    protected override void OnBar()
    {
        // Trading logic here
        if (emaFast.Result.LastValue > emaSlow.Result.LastValue)
            ExecuteMarketOrder(TradeType.Buy, SymbolName, CalculateVolume());
    }
}""",
                status=BotStatus.STOPPED,
                win_rate=68.5,
                net_profit=1542.30,
                parameters=[
                    BotParameter("Risk %", 2.0, "DOUBLE"),
                    BotParameter("ATR Period", 14, "INT"),
                    BotParameter("Take Profit", 50, "INT"),
                    BotParameter("Stop Loss", 25, "INT")
                ],
                logs=[
                    "[12:30:15] Build Success: 0 errors, 0 warnings",
                    "[12:30:16] Deployed to cTrader Cloud",
                    "[12:30:17] Instance started: EURUSD, M15"
                ]
            ),
            CBotInstance(
                id="bot2",
                name="GridMasterFX",
                code="// Grid trading algorithm for forex pairs",
                status=BotStatus.RUNNING,
                win_rate=72.1,
                net_profit=2310.50,
                parameters=[
                    BotParameter("Grid Size", 10, "INT"),
                    BotParameter("Grid Distance", 15, "DOUBLE"),
                    BotParameter("Max Positions", 5, "INT")
                ],
                logs=["[10:15:22] Grid positions active: 3/5", "[10:15:23] Profit: +$42.50"]
            )
        ]
        self.is_connected = False
        self.simulation_active = False
        self.subscribers = []
        self.market_data_queue = Queue()
    
    def subscribe(self, callback):
        self.subscribers.append(callback)
    
    def connect(self, api_key: str):
        self.is_connected = True
        # Start market data thread
        threading.Thread(target=self._market_data_loop, daemon=True).start()
        threading.Thread(target=self._event_broadcast_loop, daemon=True).start()
    
    def disconnect(self):
        self.is_connected = False
        self.simulation_active = False
    
    def get_market_depth(self, symbol: str) -> List[MarketDepthLevel]:
        # Generate mock market depth
        base_price = 1.0845 if symbol == "EURUSD" else 38.50
        levels = []
        
        # Bids (buy orders)
        for i in range(10, 0, -1):
            price = base_price * (1 - i * 0.0001)
            levels.append(MarketDepthLevel(
                price=price,
                volume=random.uniform(1000, 10000),
                level_type=LevelType.BID
            ))
        
        # Asks (sell orders)
        for i in range(1, 11):
            price = base_price * (1 + i * 0.0001)
            levels.append(MarketDepthLevel(
                price=price,
                volume=random.uniform(1000, 10000),
                level_type=LevelType.ASK
            ))
        
        return levels
    
    def compile_algo(self, bot_id: str, code: str):
        # Mock compilation
        time.sleep(1)  # Simulate compilation time
        return True
    
    def toggle_bot(self, bot_id: str):
        for bot in self.bots:
            if bot.id == bot_id:
                if bot.status == BotStatus.RUNNING:
                    bot.status = BotStatus.STOPPED
                    bot.logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Bot stopped")
                else:
                    bot.status = BotStatus.RUNNING
                    bot.logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Bot started")
                break
    
    def start_simulation(self, speed: int = 1):
        self.simulation_active = True
    
    def stop_simulation(self):
        self.simulation_active = False
    
    def _market_data_loop(self):
        while self.is_connected:
            time.sleep(0.1)  # 10 updates per second
            if self.simulation_active:
                # Generate simulated market event
                event = {
                    "type": "SIMULATION_TICK",
                    "pnl": random.uniform(-10, 15),
                    "data": {"price": random.uniform(1.0800, 1.0900)}
                }
                self.market_data_queue.put(event)
    
    def _event_broadcast_loop(self):
        while self.is_connected:
            try:
                event = self.market_data_queue.get(timeout=0.1)
                for callback in self.subscribers:
                    callback(event)
            except:
                pass

# Main Application
class BrokerIntegrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BRIDGE DE CORRETORAS")
        self.root.geometry("1600x900")
        self.root.configure(bg="#0a0a0a")
        
        # Initialize services
        self.ctrader = cTraderService()
        self.sentient_core = SentientCore()
        
        # State variables
        self.active_platform = PlatformType.CTRADER
        self.active_tab = TabType.EXECUTION
        self.is_connected = False
        self.connection_status = "Desconectado"
        self.selected_asset = "EURUSD"
        self.order_amount = "1.0"
        self.sim_speed = 1
        self.sim_pnl = 0.0
        self.is_autonomous_active = False
        
        # Data containers
        self.quotes: List[AssetQuote] = []
        self.chart_data: List[ChartDataPoint] = []
        self.market_depth: List[MarketDepthLevel] = []
        self.active_bot: Optional[CBotInstance] = None
        self.code_editor = ""
        self.is_compiling = False
        self.sim_logs: List[str] = []
        
        # Setup UI
        self.setup_ui()
        
        # Initial data load
        self.load_initial_data()
        
        # Subscribe to events
        self.ctrader.subscribe(self.handle_ctrader_event)
        
        # Start update loops
        self.start_update_loops()
    
    def setup_ui(self):
        # Main container
        self.main_frame = tk.Frame(self.root, bg="#0a0a0a")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.setup_header()
        
        # Main content
        self.setup_main_content()
    
    def setup_header(self):
        header_frame = tk.Frame(self.main_frame, bg="#1a1a2e", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # Left side: Logo and title
        left_frame = tk.Frame(header_frame, bg="#1a1a2e")
        left_frame.pack(side=tk.LEFT, padx=20)
        
        # Icon
        icon_frame = tk.Frame(left_frame, bg="#064e3b", relief=tk.RAISED, 
                             borderwidth=1, padx=10, pady=10)
        icon_frame.pack(side=tk.LEFT, padx=(0, 15))
        tk.Label(icon_frame, text="🔌", font=("Arial", 16), 
                bg="#064e3b", fg="#10b981").pack()
        
        # Text
        text_frame = tk.Frame(left_frame, bg="#1a1a2e")
        text_frame.pack(side=tk.LEFT)
        
        tk.Label(text_frame, text="BRIDGE DE CORRETORAS", 
                font=("Arial", 16, "bold"), fg="#ffffff", bg="#1a1a2e").pack(anchor=tk.W)
        
        tk.Label(text_frame, text="cTRADER OPEN API • FIX PROTOCOL", 
                font=("Courier", 10), fg="#10b981", bg="#1a1a2e").pack(anchor=tk.W)
        
        # Right side: Controls
        right_frame = tk.Frame(header_frame, bg="#1a1a2e")
        right_frame.pack(side=tk.RIGHT, padx=20)
        
        # Platform switcher
        platform_frame = tk.Frame(right_frame, bg="black", relief=tk.RAISED, 
                                 borderwidth=1, padx=1, pady=1)
        platform_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        self.ctrader_btn = tk.Button(
            platform_frame,
            text="cTrader",
            command=lambda: self.switch_platform(PlatformType.CTRADER),
            font=("Arial", 9),
            bg="#166534" if self.active_platform == PlatformType.CTRADER else "black",
            fg="white" if self.active_platform == PlatformType.CTRADER else "#666666",
            activebackground="#15803d",
            activeforeground="white",
            padx=15,
            pady=5,
            borderwidth=0
        )
        self.ctrader_btn.pack(side=tk.LEFT)
        
        self.homebroker_btn = tk.Button(
            platform_frame,
            text="B3 DMA",
            command=lambda: self.switch_platform(PlatformType.HOMEBROKER),
            font=("Arial", 9),
            bg="#854d0e" if self.active_platform == PlatformType.HOMEBROKER else "black",
            fg="white" if self.active_platform == PlatformType.HOMEBROKER else "#666666",
            activebackground="#a16207",
            activeforeground="white",
            padx=15,
            pady=5,
            borderwidth=0
        )
        self.homebroker_btn.pack(side=tk.LEFT)
        
        # Connection status
        self.connection_label = tk.Label(
            right_frame,
            text="OFFLINE",
            font=("Courier", 10, "bold"),
            bg="#991b1b",
            fg="#ffffff",
            padx=15,
            pady=5,
            relief=tk.RAISED,
            borderwidth=1
        )
        self.connection_label.pack(side=tk.LEFT)
    
    def setup_main_content(self):
        # Main grid container
        content_frame = tk.Frame(self.main_frame, bg="#0a0a0a")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Sidebar (column 0)
        self.setup_sidebar(content_frame)
        
        # Main workspace (column 1)
        self.setup_workspace(content_frame)
    
    def setup_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg="#1a1a2e", relief=tk.RAISED, borderwidth=1)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 1))
        
        # Tabs
        tabs_frame = tk.Frame(sidebar, bg="#1a1a2e")
        tabs_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.execution_btn = tk.Button(
            tabs_frame,
            text="EXECUTION (DOM)",
            command=lambda: self.switch_tab(TabType.EXECUTION),
            font=("Arial", 9, "bold"),
            bg="#1e3a8a" if self.active_tab == TabType.EXECUTION else "transparent",
            fg="#3b82f6" if self.active_tab == TabType.EXECUTION else "#666666",
            activebackground="#1e40af",
            activeforeground="#60a5fa",
            anchor="w",
            padx=20,
            pady=12,
            borderwidth=0,
            relief=tk.FLAT
        )
        self.execution_btn.pack(fill=tk.X)
        
        self.calgo_btn = tk.Button(
            tabs_frame,
            text="cALGO AUTOMATE",
            command=lambda: self.switch_tab(TabType.CALGO),
            font=("Arial", 9, "bold"),
            bg="#4c1d95" if self.active_tab == TabType.CALGO else "transparent",
            fg="#8b5cf6" if self.active_tab == TabType.CALGO else "#666666",
            activebackground="#5b21b6",
            activeforeground="#a78bfa",
            anchor="w",
            padx=20,
            pady=12,
            borderwidth=0,
            relief=tk.FLAT
        )
        self.calgo_btn.pack(fill=tk.X)
        
        self.simulator_btn = tk.Button(
            tabs_frame,
            text="SIMULATOR",
            command=lambda: self.switch_tab(TabType.SIMULATOR),
            font=("Arial", 9, "bold"),
            bg="#854d0e" if self.active_tab == TabType.SIMULATOR else "transparent",
            fg="#f59e0b" if self.active_tab == TabType.SIMULATOR else "#666666",
            activebackground="#92400e",
            activeforeground="#fbbf24",
            anchor="w",
            padx=20,
            pady=12,
            borderwidth=0,
            relief=tk.FLAT
        )
        self.simulator_btn.pack(fill=tk.X)
        
        # Separator
        separator = tk.Frame(sidebar, bg="#334155", height=1)
        separator.pack(fill=tk.X, pady=10)
        
        # Asset list frame
        self.asset_frame = tk.Frame(sidebar, bg="#1a1a2e")
        self.asset_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 10))
        
        # Asset list will be populated dynamically
        self.setup_asset_list()
    
    def setup_asset_list(self):
        # Clear existing widgets
        for widget in self.asset_frame.winfo_children():
            widget.destroy()
        
        if not self.is_connected:
            # Show connection required message
            connect_frame = tk.Frame(self.asset_frame, bg="#1a1a2e")
            connect_frame.pack(expand=True, fill=tk.BOTH, pady=50)
            
            tk.Label(
                connect_frame,
                text="🔒",
                font=("Arial", 24),
                fg="#666666",
                bg="#1a1a2e"
            ).pack(pady=(0, 10))
            
            tk.Label(
                connect_frame,
                text="Conexão Requerida",
                font=("Arial", 10),
                fg="#666666",
                bg="#1a1a2e"
            ).pack(pady=(0, 10))
            
            tk.Button(
                connect_frame,
                text="CONECTAR",
                command=self.connect_to_broker,
                font=("Arial", 10, "bold"),
                bg="#2563eb",
                fg="white",
                activebackground="#1d4ed8",
                activeforeground="white",
                padx=20,
                pady=8
            ).pack()
        else:
            # Show asset list
            for quote in self.quotes:
                self.create_asset_widget(quote)
    
    def create_asset_widget(self, quote: AssetQuote):
        asset_frame = tk.Frame(
            self.asset_frame,
            bg="transparent",
            relief=tk.RAISED,
            borderwidth=1,
            padx=10,
            pady=8
        )
        asset_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Highlight if selected
        if quote.symbol == self.selected_asset:
            asset_frame.configure(bg="#1e3a8a")
        
        # Symbol and price
        top_frame = tk.Frame(asset_frame, bg=asset_frame.cget("bg"))
        top_frame.pack(fill=tk.X)
        
        tk.Label(
            top_frame,
            text=quote.symbol,
            font=("Arial", 11, "bold"),
            fg="#ffffff" if quote.symbol == self.selected_asset else "#e5e7eb",
            bg=asset_frame.cget("bg")
        ).pack(side=tk.LEFT)
        
        price_color = "#10b981" if quote.change >= 0 else "#ef4444"
        tk.Label(
            top_frame,
            text=f"{quote.price:.5f}",
            font=("Courier", 10, "bold"),
            fg=price_color,
            bg=asset_frame.cget("bg")
        ).pack(side=tk.RIGHT)
        
        # Spread and change
        bottom_frame = tk.Frame(asset_frame, bg=asset_frame.cget("bg"))
        bottom_frame.pack(fill=tk.X)
        
        tk.Label(
            bottom_frame,
            text=f"Spread: {quote.spread}",
            font=("Arial", 8),
            fg="#9ca3af",
            bg=asset_frame.cget("bg")
        ).pack(side=tk.LEFT)
        
        tk.Label(
            bottom_frame,
            text=f"{quote.change:+.2f}%",
            font=("Arial", 8),
            fg=price_color,
            bg=asset_frame.cget("bg")
        ).pack(side=tk.RIGHT)
        
        # Bind click event
        asset_frame.bind("<Button-1>", lambda e, s=quote.symbol: self.select_asset(s))
        for child in asset_frame.winfo_children():
            child.bind("<Button-1>", lambda e, s=quote.symbol: self.select_asset(s))
    
    def setup_workspace(self, parent):
        self.workspace = tk.Frame(parent, bg="black")
        self.workspace.grid(row=0, column=1, sticky="nsew")
        
        # Background grid pattern
        self.canvas = tk.Canvas(self.workspace, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_grid()
        
        # Tab content container
        self.tab_content = tk.Frame(self.workspace, bg="transparent")
        self.tab_content.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        
        # Initialize tab content
        self.update_tab_content()
    
    def draw_grid(self):
        """Draw grid pattern on canvas"""
        self.canvas.delete("grid")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Draw vertical lines
        for x in range(0, width, 20):
            self.canvas.create_line(x, 0, x, height, fill="#222222", width=1, tags="grid")
        
        # Draw horizontal lines
        for y in range(0, height, 20):
            self.canvas.create_line(0, y, width, y, fill="#222222", width=1, tags="grid")
        
        # Schedule next update
        self.root.after(100, self.draw_grid)
    
    def update_tab_content(self):
        """Update workspace based on active tab"""
        # Clear current content
        for widget in self.tab_content.winfo_children():
            widget.destroy()
        
        if self.active_tab == TabType.EXECUTION:
            self.setup_execution_tab()
        elif self.active_tab == TabType.CALGO:
            self.setup_calgo_tab()
        elif self.active_tab == TabType.SIMULATOR:
            self.setup_simulator_tab()
    
    def setup_execution_tab(self):
        """Setup execution tab with chart and DOM"""
        # Main container
        main_frame = tk.Frame(self.tab_content, bg="transparent")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel (chart and order entry)
        left_panel = tk.Frame(main_frame, bg="transparent")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Chart frame
        chart_frame = tk.Frame(
            left_panel,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1
        )
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Chart title
        title_frame = tk.Frame(chart_frame, bg="#1a1a2e")
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            title_frame,
            text=self.selected_asset,
            font=("Arial", 14, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        status_frame = tk.Frame(title_frame, bg="#1a1a2e")
        status_frame.pack(side=tk.RIGHT)
        
        tk.Label(
            status_frame,
            text="●",
            font=("Arial", 12),
            fg="#10b981",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Label(
            status_frame,
            text="LIVE FEED",
            font=("Arial", 9),
            fg="#10b981",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        # Matplotlib chart
        self.setup_price_chart(chart_frame)
        
        # Order entry frame
        order_frame = tk.Frame(
            left_panel,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=20,
            pady=20
        )
        order_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Volume input
        volume_frame = tk.Frame(order_frame, bg="#1a1a2e")
        volume_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(
            volume_frame,
            text="Volume (Lots)",
            font=("Arial", 9),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.order_amount_var = tk.StringVar(value=self.order_amount)
        volume_entry = tk.Entry(
            volume_frame,
            textvariable=self.order_amount_var,
            font=("Courier", 12),
            bg="black",
            fg="white",
            insertbackground="white",
            relief=tk.SUNKEN,
            borderwidth=1
        )
        volume_entry.pack(fill=tk.X)
        
        # Sell button
        sell_button = tk.Button(
            order_frame,
            text="VENDER",
            command=lambda: self.execute_order("SELL"),
            font=("Arial", 12, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#ef4444",
            activeforeground="white",
            padx=30,
            pady=15,
            relief=tk.RAISED
        )
        sell_button.pack(side=tk.LEFT, padx=(20, 10))
        
        # Buy button
        buy_button = tk.Button(
            order_frame,
            text="COMPRAR",
            command=lambda: self.execute_order("BUY"),
            font=("Arial", 12, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#22c55e",
            activeforeground="white",
            padx=30,
            pady=15,
            relief=tk.RAISED
        )
        buy_button.pack(side=tk.LEFT)
        
        # Right panel (DOM)
        dom_frame = tk.Frame(
            main_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            width=200
        )
        dom_frame.pack(side=tk.RIGHT, fill=tk.Y)
        dom_frame.pack_propagate(False)
        
        # DOM title
        dom_title = tk.Frame(dom_frame, bg="#374151")
        dom_title.pack(fill=tk.X, pady=(0, 1))
        
        tk.Label(
            dom_title,
            text="DEPTH OF MARKET",
            font=("Arial", 9, "bold"),
            fg="#9ca3af",
            bg="#374151"
        ).pack(pady=8)
        
        # DOM content
        dom_content = tk.Frame(dom_frame, bg="#1a1a2e")
        dom_content.pack(fill=tk.BOTH, expand=True)
        
        self.update_dom(dom_content)
    
    def setup_price_chart(self, parent):
        """Setup matplotlib price chart"""
        # Create figure
        self.fig = Figure(figsize=(10, 4), dpi=80, facecolor='#1a1a2e')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#1a1a2e')
        
        # Configure axes
        self.ax.tick_params(colors='#666666', labelsize=9)
        self.ax.grid(True, color='#222222', linestyle='--', alpha=0.5)
        
        # Plot initial data
        if self.chart_data:
            times = [d.time for d in self.chart_data]
            values = [d.value for d in self.chart_data]
            self.ax.plot(times, values, color='#0ea5e9', linewidth=2)
            self.ax.fill_between(times, values, alpha=0.3, color='#0ea5e9')
        
        # Add to Tkinter
        self.chart_canvas = FigureCanvasTkAgg(self.fig, parent)
        self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
    
    def update_dom(self, parent):
        """Update Depth of Market display"""
        # Clear existing widgets
        for widget in parent.winfo_children():
            widget.destroy()
        
        if not self.market_depth:
            return
        
        # Asks (red)
        asks = [l for l in self.market_depth if l.level_type == LevelType.ASK]
        for level in asks[:10]:  # Show top 10 asks
            dom_row = tk.Frame(parent, bg="#1a1a2e")
            dom_row.pack(fill=tk.X, pady=1)
            
            # Background for volume visualization
            volume_bg = tk.Frame(dom_row, bg="#7f1d1d", height=20)
            volume_bg.pack(side=tk.LEFT, fill=tk.X, expand=True)
            volume_bg.pack_propagate(False)
            
            # Price and volume
            price_label = tk.Label(
                volume_bg,
                text=f"{level.price:.5f}",
                font=("Courier", 9),
                fg="#fca5a5",
                bg="#7f1d1d",
                anchor="w",
                padx=5
            )
            price_label.pack(side=tk.LEFT)
            
            volume_label = tk.Label(
                volume_bg,
                text=f"{level.volume:,.0f}",
                font=("Courier", 9),
                fg="#d1d5db",
                bg="#7f1d1d",
                anchor="e",
                padx=5
            )
            volume_label.pack(side=tk.RIGHT)
        
        # Spread indicator
        spread_frame = tk.Frame(parent, bg="#374151", height=30)
        spread_frame.pack(fill=tk.X, pady=5)
        spread_frame.pack_propagate(False)
        
        current_quote = next((q for q in self.quotes if q.symbol == self.selected_asset), None)
        if current_quote:
            tk.Label(
                spread_frame,
                text=f"SPREAD: {current_quote.spread}",
                font=("Courier", 9, "bold"),
                fg="#fbbf24",
                bg="#374151"
            ).pack(expand=True)
        
        # Bids (green)
        bids = [l for l in self.market_depth if l.level_type == LevelType.BID]
        for level in bids[:10]:  # Show top 10 bids
            dom_row = tk.Frame(parent, bg="#1a1a2e")
            dom_row.pack(fill=tk.X, pady=1)
            
            # Background for volume visualization
            volume_bg = tk.Frame(dom_row, bg="#14532d", height=20)
            volume_bg.pack(side=tk.LEFT, fill=tk.X, expand=True)
            volume_bg.pack_propagate(False)
            
            # Price and volume
            price_label = tk.Label(
                volume_bg,
                text=f"{level.price:.5f}",
                font=("Courier", 9),
                fg="#86efac",
                bg="#14532d",
                anchor="w",
                padx=5
            )
            price_label.pack(side=tk.LEFT)
            
            volume_label = tk.Label(
                volume_bg,
                text=f"{level.volume:,.0f}",
                font=("Courier", 9),
                fg="#d1d5db",
                bg="#14532d",
                anchor="e",
                padx=5
            )
            volume_label.pack(side=tk.RIGHT)
    
    def setup_calgo_tab(self):
        """Setup cAlgo automation tab"""
        main_frame = tk.Frame(self.tab_content, bg="transparent")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bot selector panel
        selector_frame = tk.Frame(
            main_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            width=200
        )
        selector_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        selector_frame.pack_propagate(False)
        
        tk.Label(
            selector_frame,
            text="INSTÂNCIAS cBOT",
            font=("Arial", 9, "bold"),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(pady=10)
        
        # Bot list
        self.bot_list_frame = tk.Frame(selector_frame, bg="#1a1a2e")
        self.bot_list_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        self.update_bot_list()
        
        # Code editor panel
        editor_frame = tk.Frame(main_frame, bg="transparent")
        editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Editor toolbar
        toolbar = tk.Frame(editor_frame, bg="#0f172a", height=40)
        toolbar.pack(fill=tk.X, pady=(0, 1))
        toolbar.pack_propagate(False)
        
        tk.Label(
            toolbar,
            text=f"{self.active_bot.name if self.active_bot else 'No bot'}.cs",
            font=("Courier", 10),
            fg="#9ca3af",
            bg="#0f172a"
        ).pack(side=tk.LEFT, padx=10)
        
        # Toolbar buttons
        button_frame = tk.Frame(toolbar, bg="#0f172a")
        button_frame.pack(side=tk.RIGHT, padx=10)
        
        compile_btn = tk.Button(
            button_frame,
            text="BUILD",
            command=self.compile_bot,
            font=("Arial", 9),
            bg="#374151",
            fg="white",
            padx=15,
            pady=5
        )
        compile_btn.pack(side=tk.LEFT, padx=5)
        
        toggle_btn = tk.Button(
            button_frame,
            text="RODAR" if not self.active_bot or self.active_bot.status != BotStatus.RUNNING else "PARAR",
            command=self.toggle_bot,
            font=("Arial", 9),
            bg="#166534" if not self.active_bot or self.active_bot.status != BotStatus.RUNNING else "#991b1b",
            fg="white",
            padx=15,
            pady=5
        )
        toggle_btn.pack(side=tk.LEFT)
        
        # Code editor
        editor_container = tk.Frame(
            editor_frame,
            bg="#0f172a",
            relief=tk.SUNKEN,
            borderwidth=1
        )
        editor_container.pack(fill=tk.BOTH, expand=True)
        
        self.code_text = scrolledtext.ScrolledText(
            editor_container,
            bg="#0f172a",
            fg="#e5e7eb",
            font=("Courier", 10),
            insertbackground="white",
            wrap=tk.WORD,
            borderwidth=0,
            highlightthickness=0
        )
        self.code_text.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        if self.active_bot:
            self.code_text.insert(1.0, self.active_bot.code)
        
        # Build output
        output_frame = tk.Frame(
            editor_frame,
            bg="black",
            relief=tk.SUNKEN,
            borderwidth=1,
            height=100
        )
        output_frame.pack(fill=tk.X, pady=(10, 0))
        output_frame.pack_propagate(False)
        
        tk.Label(
            output_frame,
            text="BUILD OUTPUT",
            font=("Courier", 9),
            fg="#9ca3af",
            bg="black"
        ).pack(anchor=tk.W, padx=5, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            bg="black",
            fg="#9ca3af",
            font=("Courier", 9),
            height=5,
            borderwidth=0,
            highlightthickness=0
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        if self.active_bot:
            for log in self.active_bot.logs:
                self.output_text.insert(tk.END, log + "\n")
        
        # Parameters panel
        params_frame = tk.Frame(
            main_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            width=250
        )
        params_frame.pack(side=tk.RIGHT, fill=tk.Y)
        params_frame.pack_propagate(False)
        
        tk.Label(
            params_frame,
            text="PARÂMETROS",
            font=("Arial", 9, "bold"),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(pady=10)
        
        # Parameters content
        params_content = tk.Frame(params_frame, bg="#1a1a2e")
        params_content.pack(fill=tk.BOTH, expand=True, padx=10)
        
        self.update_parameters(params_content)
    
    def update_bot_list(self):
        """Update bot list in selector"""
        for widget in self.bot_list_frame.winfo_children():
            widget.destroy()
        
        for bot in self.ctrader.bots:
            bot_frame = tk.Frame(
                self.bot_list_frame,
                bg="#1e3a8a" if self.active_bot and bot.id == self.active_bot.id else "transparent",
                relief=tk.RAISED,
                borderwidth=1,
                padx=10,
                pady=8
            )
            bot_frame.pack(fill=tk.X, pady=2)
            
            # Bot name and status
            top_frame = tk.Frame(bot_frame, bg=bot_frame.cget("bg"))
            top_frame.pack(fill=tk.X)
            
            tk.Label(
                top_frame,
                text="🤖",
                font=("Arial", 12),
                bg=bot_frame.cget("bg")
            ).pack(side=tk.LEFT, padx=(0, 5))
            
            tk.Label(
                top_frame,
                text=bot.name,
                font=("Arial", 9, "bold"),
                fg="#ffffff" if self.active_bot and bot.id == self.active_bot.id else "#e5e7eb",
                bg=bot_frame.cget("bg")
            ).pack(side=tk.LEFT)
            
            status_color = "#10b981" if bot.status == BotStatus.RUNNING else "#6b7280"
            tk.Label(
                top_frame,
                text=bot.status.value,
                font=("Arial", 8),
                fg=status_color,
                bg=bot_frame.cget("bg")
            ).pack(side=tk.RIGHT)
            
            # Win rate
            bottom_frame = tk.Frame(bot_frame, bg=bot_frame.cget("bg"))
            bottom_frame.pack(fill=tk.X, pady=(2, 0))
            
            tk.Label(
                bottom_frame,
                text=f"Win: {bot.win_rate}%",
                font=("Arial", 8),
                fg="#60a5fa",
                bg=bot_frame.cget("bg")
            ).pack(side=tk.LEFT)
            
            # Bind click event
            bot_frame.bind("<Button-1>", lambda e, b=bot: self.select_bot(b))
            for child in bot_frame.winfo_children():
                child.bind("<Button-1>", lambda e, b=bot: self.select_bot(b))
    
    def update_parameters(self, parent):
        """Update parameters display"""
        for widget in parent.winfo_children():
            widget.destroy()
        
        if not self.active_bot:
            return
        
        for param in self.active_bot.parameters:
            param_frame = tk.Frame(parent, bg="#1a1a2e")
            param_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                param_frame,
                text=param.name,
                font=("Arial", 8),
                fg="#9ca3af",
                bg="#1a1a2e"
            ).pack(anchor=tk.W, pady=(0, 2))
            
            entry = tk.Entry(
                param_frame,
                font=("Courier", 9),
                bg="black",
                fg="white",
                relief=tk.SUNKEN,
                borderwidth=1
            )
            entry.pack(fill=tk.X)
            entry.insert(0, str(param.value))
        
        # Performance section
        separator = tk.Frame(parent, bg="#374151", height=1)
        separator.pack(fill=tk.X, pady=20)
        
        perf_frame = tk.Frame(parent, bg="#1a1a2e")
        perf_frame.pack(fill=tk.X)
        
        tk.Label(
            perf_frame,
            text="Performance",
            font=("Arial", 9, "bold"),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Net profit
        profit_frame = tk.Frame(perf_frame, bg="#1a1a2e")
        profit_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(
            profit_frame,
            text="Net Profit",
            font=("Arial", 8),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        profit_color = "#10b981" if self.active_bot.net_profit >= 0 else "#ef4444"
        tk.Label(
            profit_frame,
            text=f"${self.active_bot.net_profit:.2f}",
            font=("Courier", 9, "bold"),
            fg=profit_color,
            bg="#1a1a2e"
        ).pack(side=tk.RIGHT)
        
        # Win rate
        winrate_frame = tk.Frame(perf_frame, bg="#1a1a2e")
        winrate_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(
            winrate_frame,
            text="Win Rate",
            font=("Arial", 8),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            winrate_frame,
            text=f"{self.active_bot.win_rate}%",
            font=("Courier", 9, "bold"),
            fg="#60a5fa",
            bg="#1a1a2e"
        ).pack(side=tk.RIGHT)
    
    def setup_simulator_tab(self):
        """Setup simulator tab"""
        main_frame = tk.Frame(self.tab_content, bg="transparent")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg="transparent")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="⚡",
            font=("Arial", 24),
            fg="#fbbf24",
            bg="transparent"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            header_frame,
            text="SIMULADOR DE TREINAMENTO NEURAL",
            font=("Arial", 16, "bold"),
            fg="#ffffff",
            bg="transparent"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            header_frame,
            text="Backtesting em tempo real alimentando a Rede Neural Geral",
            font=("Arial", 9),
            fg="#9ca3af",
            bg="transparent"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # Controls
        controls_frame = tk.Frame(header_frame, bg="transparent")
        controls_frame.pack(side=tk.RIGHT)
        
        # Speed control
        speed_frame = tk.Frame(controls_frame, bg="black", relief=tk.RAISED, borderwidth=1)
        speed_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            speed_frame,
            text="Velocidade",
            font=("Arial", 8),
            fg="#9ca3af",
            bg="black"
        ).pack(side=tk.LEFT, padx=5)
        
        self.speed_scale = tk.Scale(
            speed_frame,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            bg="black",
            fg="white",
            highlightthickness=0,
            length=100,
            command=self.update_sim_speed
        )
        self.speed_scale.set(self.sim_speed)
        self.speed_scale.pack(side=tk.LEFT, padx=5)
        
        # Control buttons
        start_btn = tk.Button(
            controls_frame,
            text="▶",
            command=self.start_simulation,
            font=("Arial", 14),
            bg="#16a34a",
            fg="white",
            padx=10,
            pady=5
        )
        start_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        stop_btn = tk.Button(
            controls_frame,
            text="⏹",
            command=self.stop_simulation,
            font=("Arial", 14),
            bg="#dc2626",
            fg="white",
            padx=10,
            pady=5
        )
        stop_btn.pack(side=tk.LEFT)
        
        # Content grid
        content_frame = tk.Frame(main_frame, bg="transparent")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column: Stats
        stats_frame = tk.Frame(content_frame, bg="transparent")
        stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # PnL display
        pnl_frame = tk.Frame(
            stats_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=20,
            pady=20
        )
        pnl_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            pnl_frame,
            text="PnL Simulado",
            font=("Arial", 9),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        pnl_color = "#10b981" if self.sim_pnl >= 0 else "#ef4444"
        self.pnl_label = tk.Label(
            pnl_frame,
            text=f"${self.sim_pnl:.2f}",
            font=("Courier", 24, "bold"),
            fg=pnl_color,
            bg="#1a1a2e"
        )
        self.pnl_label.pack()
        
        # AI Status
        ai_frame = tk.Frame(
            stats_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=20,
            pady=20
        )
        ai_frame.pack(fill=tk.X)
        
        status_row = tk.Frame(ai_frame, bg="#1a1a2e")
        status_row.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            status_row,
            text="⚡",
            font=("Arial", 24),
            fg="#fbbf24",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            status_row,
            text="IA TRAINING LINK",
            font=("Arial", 12, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            ai_frame,
            text="ATIVO: Recebendo experiências",
            font=("Arial", 9),
            fg="#10b981",
            bg="#1a1a2e"
        ).pack(anchor=tk.W)
        
        # Right column: Logs
        logs_frame = tk.Frame(content_frame, bg="transparent")
        logs_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        logs_container = tk.Frame(
            logs_frame,
            bg="black",
            relief=tk.RAISED,
            borderwidth=1
        )
        logs_container.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            logs_container,
            text="LOG DE EXECUÇÃO",
            font=("Arial", 9, "bold"),
            fg="#9ca3af",
            bg="black"
        ).pack(anchor=tk.W, padx=10, pady=10)
        
        self.sim_logs_text = scrolledtext.ScrolledText(
            logs_container,
            bg="black",
            fg="#9ca3af",
            font=("Courier", 9),
            borderwidth=0,
            highlightthickness=0
        )
        self.sim_logs_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Add existing logs
        for log in self.sim_logs:
            self.sim_logs_text.insert(tk.END, log + "\n")
    
    # Event Handlers
    def switch_platform(self, platform: PlatformType):
        self.active_platform = platform
        
        # Update button styles
        self.ctrader_btn.config(
            bg="#166534" if platform == PlatformType.CTRADER else "black",
            fg="white" if platform == PlatformType.CTRADER else "#666666"
        )
        self.homebroker_btn.config(
            bg="#854d0e" if platform == PlatformType.HOMEBROKER else "black",
            fg="white" if platform == PlatformType.HOMEBROKER else "#666666"
        )
        
        # Reload data
        self.load_initial_data()
        self.setup_asset_list()
    
    def switch_tab(self, tab: TabType):
        self.active_tab = tab
        
        # Update button styles
        self.execution_btn.config(
            bg="#1e3a8a" if tab == TabType.EXECUTION else "transparent",
            fg="#3b82f6" if tab == TabType.EXECUTION else "#666666"
        )
        self.calgo_btn.config(
            bg="#4c1d95" if tab == TabType.CALGO else "transparent",
            fg="#8b5cf6" if tab == TabType.CALGO else "#666666"
        )
        self.simulator_btn.config(
            bg="#854d0e" if tab == TabType.SIMULATOR else "transparent",
            fg="#f59e0b" if tab == TabType.SIMULATOR else "#666666"
        )
        
        self.update_tab_content()
    
    def connect_to_broker(self):
        self.ctrader.connect("mock_api_key_123")
        self.is_connected = True
        self.connection_status = "CONECTADO: FIX Protocol v4.4"
        self.connection_label.config(
            text="ONLINE (12ms)",
            bg="#166534",
            fg="#ffffff"
        )
        self.setup_asset_list()
    
    def select_asset(self, symbol: str):
        self.selected_asset = symbol
        self.setup_asset_list()
        
        # Update DOM if in execution tab
        if self.active_tab == TabType.EXECUTION:
            self.market_depth = self.ctrader.get_market_depth(symbol)
            self.update_dom(self.tab_content.winfo_children()[0].winfo_children()[2])  # Navigate to DOM frame
    
    def execute_order(self, side: str):
        if not self.is_connected:
            return
        
        asset = next((q for q in self.quotes if q.symbol == self.selected_asset), None)
        if not asset:
            return
        
        price = asset.ask if side == "BUY" else asset.bid
        self.sentient_core.perceive_reality(0.5, 1 if side == "BUY" else -1)
        
        # Show order confirmation
        from tkinter import messagebox
        messagebox.showinfo(
            "Ordem Enviada",
            f"Ordem {side} enviada via cTrader Bridge:\n"
            f"{self.order_amount} lots de {self.selected_asset} @ {price:.5f}"
        )
        
        # Add to simulation logs
        log_msg = f"[EXEC] Ordem Manual Enviada: {side} {self.selected_asset}"
        self.sim_logs.insert(0, log_msg)
        if self.active_tab == TabType.SIMULATOR:
            self.sim_logs_text.insert(1.0, log_msg + "\n")
    
    def select_bot(self, bot: CBotInstance):
        self.active_bot = bot
        self.code_editor = bot.code
        self.update_bot_list()
        
        if self.active_tab == TabType.CALGO:
            self.code_text.delete(1.0, tk.END)
            self.code_text.insert(1.0, bot.code)
            
            self.output_text.delete(1.0, tk.END)
            for log in bot.logs:
                self.output_text.insert(tk.END, log + "\n")
            
            self.update_parameters(self.tab_content.winfo_children()[0].winfo_children()[2])  # Navigate to params frame
    
    def compile_bot(self):
        if not self.active_bot:
            return
        
        self.is_compiling = True
        self.output_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Compiling...\n")
        
        # Simulate compilation
        self.root.after(1000, self.finish_compilation)
    
    def finish_compilation(self):
        self.is_compiling = False
        self.output_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Build Success: 0 errors, 0 warnings\n")
        self.output_text.see(tk.END)
    
    def toggle_bot(self):
        if not self.active_bot:
            return
        
        self.ctrader.toggle_bot(self.active_bot.id)
        
        # Update UI
        if self.active_bot.status == BotStatus.RUNNING:
            self.active_bot.status = BotStatus.STOPPED
        else:
            self.active_bot.status = BotStatus.RUNNING
        
        self.update_bot_list()
    
    def update_sim_speed(self, value):
        self.sim_speed = int(value)
    
    def start_simulation(self):
        self.ctrader.start_simulation(self.sim_speed)
        self.is_autonomous_active = True
        log_msg = f"[{datetime.now().strftime('%H:%M:%S')}] Simulation started at {self.sim_speed}x speed"
        self.sim_logs.insert(0, log_msg)
        if self.active_tab == TabType.SIMULATOR:
            self.sim_logs_text.insert(1.0, log_msg + "\n")
    
    def stop_simulation(self):
        self.ctrader.stop_simulation()
        self.is_autonomous_active = False
        log_msg = f"[{datetime.now().strftime('%H:%M:%S')}] Simulation stopped"
        self.sim_logs.insert(0, log_msg)
        if self.active_tab == TabType.SIMULATOR:
            self.sim_logs_text.insert(1.0, log_msg + "\n")
    
    def load_initial_data(self):
        """Load initial data based on active platform"""
        self.quotes.clear()
        
        if self.active_platform == PlatformType.CTRADER:
            self.quotes = [
                AssetQuote('EURUSD', 1.0845, 0.12, 1.0844, 1.0846, 0.2),
                AssetQuote('GBPUSD', 1.2630, -0.05, 1.2628, 1.2632, 0.4),
                AssetQuote('XAUUSD', 2340.50, 1.2, 2340.10, 2340.90, 0.8),
                AssetQuote('USDJPY', 151.20, 0.3, 151.18, 151.22, 0.4),
            ]
            self.selected_asset = 'EURUSD'
            self.active_bot = self.ctrader.bots[0]
            self.code_editor = self.active_bot.code
        else:
            self.quotes = [
                AssetQuote('PETR4', 38.50, 1.5, 38.48, 38.52, 0.04),
                AssetQuote('VALE3', 62.10, -0.8, 62.05, 62.15, 0.10),
                AssetQuote('WINJ24', 128500, 0.5, 128490, 128510, 20),
            ]
            self.selected_asset = 'PETR4'
            self.active_bot = None
        
        # Initialize chart data
        self.chart_data.clear()
        base_time = datetime.now()
        base_price = 1.0845 if self.active_platform == PlatformType.CTRADER else 38.50
        
        for i in range(50):
            time = base_time - timedelta(minutes=50-i)
            value = base_price * (1 + random.uniform(-0.01, 0.01))
            self.chart_data.append(ChartDataPoint(time, value))
        
        # Get initial market depth
        if self.is_connected:
            self.market_depth = self.ctrader.get_market_depth(self.selected_asset)
    
    def start_update_loops(self):
        """Start periodic update loops"""
        def update_market_data():
            if self.is_connected:
                # Update quotes
                for quote in self.quotes:
                    change = random.uniform(-0.0005, 0.0005)
                    quote.price *= (1 + change)
                    quote.bid = quote.price * 0.9998
                    quote.ask = quote.price * 1.0002
                    quote.change = change * 100
                
                # Update chart
                if self.chart_data:
                    last_value = self.chart_data[-1].value
                    new_value = last_value * (1 + random.uniform(-0.001, 0.001))
                    self.chart_data.append(ChartDataPoint(datetime.now(), new_value))
                    self.chart_data = self.chart_data[-50:]  # Keep last 50 points
                    
                    # Update chart if visible
                    if self.active_tab == TabType.EXECUTION and hasattr(self, 'ax'):
                        self.ax.clear()
                        times = [d.time for d in self.chart_data]
                        values = [d.value for d in self.chart_data]
                        self.ax.plot(times, values, color='#0ea5e9', linewidth=2)
                        self.ax.fill_between(times, values, alpha=0.3, color='#0ea5e9')
                        self.ax.set_facecolor('#1a1a2e')
                        self.ax.tick_params(colors='#666666', labelsize=9)
                        self.ax.grid(True, color='#222222', linestyle='--', alpha=0.5)
                        self.chart_canvas.draw()
                
                # Update DOM if in execution tab
                if self.active_tab == TabType.EXECUTION:
                    self.market_depth = self.ctrader.get_market_depth(self.selected_asset)
                    # Find and update DOM widget
                    for widget in self.tab_content.winfo_children():
                        if isinstance(widget, tk.Frame) and len(widget.winfo_children()) > 2:
                            if widget.winfo_children()[2].winfo_class() == 'Frame':  # DOM frame
                                self.update_dom(widget.winfo_children()[2])
                                break
            
            self.root.after(1000, update_market_data)
        
        update_market_data()
    
    def handle_ctrader_event(self, event):
        """Handle events from cTrader service"""
        if event["type"] == "SIMULATION_TICK":
            self.sim_pnl += event["pnl"]
            
            time_str = datetime.now().strftime("%H:%M:%S")
            log_msg = f"[{time_str}] Tick Processado: PnL {'+' if event['pnl'] > 0 else ''}{event['pnl']:.2f}"
            self.sim_logs.insert(0, log_msg)
            
            if self.active_tab == TabType.SIMULATOR:
                self.sim_logs_text.insert(1.0, log_msg + "\n")
                self.pnl_label.config(
                    text=f"${self.sim_pnl:.2f}",
                    fg="#10b981" if self.sim_pnl >= 0 else "#ef4444"
                )
        elif event["type"] == "ORDER_FILLED":
            time_str = datetime.now().strftime("%H:%M:%S")
            log_msg = f"[{time_str}] ORDEM AUTÔNOMA EXECUTADA: {event['data']['type']} {event['data']['symbol']} @ {event['data']['price']:.5f}"
            self.sim_logs.insert(0, log_msg)
            
            if self.active_tab == TabType.SIMULATOR:
                self.sim_logs_text.insert(1.0, log_msg + "\n")

# Main application
def main():
    root = tk.Tk()
    app = BrokerIntegrationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()