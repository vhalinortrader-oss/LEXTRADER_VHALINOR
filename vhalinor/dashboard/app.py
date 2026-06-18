"""Dashboard Tkinter com 4 abas: Carteira, Gráfico, Trades, Cérebro."""
from __future__ import annotations

import json
import time
import tkinter as tk
from tkinter import ttk
from typing import Any, Optional

from ..utils import logger
from ..brain.brain import Brain


def _make_chart(df, ax):
    try:
        import matplotlib
        matplotlib.use("TkAgg")
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    except Exception as exc:  # pragma: no cover
        ax.delete("all")
        ax.create_text(10, 10, anchor="nw", text=f"matplotlib indisponível: {exc}")
        return
    fig = Figure(figsize=(6, 3), dpi=100)
    a = fig.add_subplot(111)
    if df is not None and not df.empty and "close" in df.columns:
        a.plot(df.index, df["close"], color="#3fa7ff", linewidth=1.4, label="close")
        if "SMA_20" in df.columns:
            a.plot(df.index, df["SMA_20"], color="#ffb84d", linewidth=1.0, label="SMA20")
        if "SMA_50" in df.columns:
            a.plot(df.index, df["SMA_50"], color="#ff5e5e", linewidth=1.0, label="SMA50")
        a.set_title("Preço + Médias")
        a.legend(loc="best", fontsize=8)
    canvas = FigureCanvasTkAgg(fig, master=ax)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


def run_dashboard(orchestrator=None, symbol: str = "BTC-USD", interval_ms: int = 5000) -> None:
    """Abre a janela Tkinter. Usa o `orchestrator` ou cria um novo."""
    try:
        import tkinter as tk
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(f"Tkinter indisponível: {exc}")

    if orchestrator is None:
        from ..orchestrator import Orchestrator
        orchestrator = Orchestrator(initial_capital=10_000.0)

    root = tk.Tk()
    root.title(f"LEXTRADER-IAG 5.0 — {symbol}")
    root.geometry("1100x700")
    root.configure(bg="#0e1320")

    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass
    style.configure("TNotebook", background="#0e1320", borderwidth=0)
    style.configure("TNotebook.Tab", background="#1a2238", foreground="#dde6ff", padding=(14, 6))
    style.map("TNotebook.Tab", background=[("selected", "#3fa7ff")], foreground=[("selected", "#0e1320")])
    style.configure("TFrame", background="#0e1320")
    style.configure("TLabel", background="#0e1320", foreground="#dde6ff")
    style.configure("Header.TLabel", background="#0e1320", foreground="#3fa7ff", font=("Consolas", 14, "bold"))
    style.configure("Stat.TLabel", background="#0e1320", foreground="#dde6ff", font=("Consolas", 11))
    style.configure("Treeview", background="#11182a", fieldbackground="#11182a", foreground="#dde6ff")
    style.configure("Treeview.Heading", background="#1a2238", foreground="#dde6ff")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=8, pady=8)

    # --- abas ---
    tab_portfolio = ttk.Frame(notebook)
    tab_chart = ttk.Frame(notebook)
    tab_trades = ttk.Frame(notebook)
    tab_brain = ttk.Frame(notebook)
    notebook.add(tab_portfolio, text="💼 Carteira")
    notebook.add(tab_chart, text="📈 Gráfico")
    notebook.add(tab_trades, text="📜 Trades")
    notebook.add(tab_brain, text="🧠 Cérebro")

    # Carteira
    lbl_title = ttk.Label(tab_portfolio, text="Visão Geral", style="Header.TLabel")
    lbl_title.pack(anchor="w", padx=12, pady=(12, 4))
    lbl_capital = ttk.Label(tab_portfolio, text="Capital: R$ -", style="Stat.TLabel")
    lbl_capital.pack(anchor="w", padx=12)
    lbl_equity = ttk.Label(tab_portfolio, text="Equity: R$ -", style="Stat.TLabel")
    lbl_equity.pack(anchor="w", padx=12)
    lbl_decision = ttk.Label(tab_portfolio, text="Última decisão: -", style="Stat.TLabel")
    lbl_decision.pack(anchor="w", padx=12, pady=(0, 8))
    tree = ttk.Treeview(tab_portfolio, columns=("metric", "value"), show="headings", height=8)
    tree.heading("metric", text="Métrica")
    tree.heading("value", text="Valor")
    tree.column("metric", width=180)
    tree.column("value", width=200)
    tree.pack(fill="x", padx=12, pady=8)

    # Gráfico
    chart_frame = ttk.Frame(tab_chart)
    chart_frame.pack(fill="both", expand=True, padx=8, pady=8)

    # Trades
    cols = ("opened_at", "symbol", "side", "entry", "exit", "pnl", "reason")
    trades_tree = ttk.Treeview(tab_trades, columns=cols, show="headings", height=20)
    for c, w in zip(cols, (140, 80, 60, 90, 90, 90, 140)):
        trades_tree.heading(c, text=c)
        trades_tree.column(c, width=w, anchor="w")
    trades_tree.pack(fill="both", expand=True, padx=8, pady=8)

    # Cérebro
    brain_text = tk.Text(tab_brain, bg="#11182a", fg="#dde6ff",
                         font=("Consolas", 11), insertbackground="#dde6ff", wrap="word")
    brain_text.pack(fill="both", expand=True, padx=8, pady=8)

    def _refresh():
        try:
            decision = orchestrator.step(symbol, period="6mo", interval="1d")
            stats = orchestrator.executor.stats()
            lbl_capital.config(text=f"Capital: R$ {stats.get('capital', 0):,.2f}")
            lbl_equity.config(text=f"Equity:   R$ {orchestrator.executor.equity:,.2f}")
            lbl_decision.config(text=f"Última decisão: {decision.action} "
                                    f"(score={decision.score:+.2f}, conf={decision.confidence:.2f})")
            tree.delete(*tree.get_children())
            tree.insert("", "end", values=("trades", stats.get("trades", 0)))
            tree.insert("", "end", values=("winrate", f"{stats.get('winrate', 0)*100:.1f}%"))
            tree.insert("", "end", values=("pnl", f"R$ {stats.get('pnl', 0):,.2f}"))
            tree.insert("", "end", values=("abertas", stats.get("open", 0)))
            tree.insert("", "end", values=("regime", decision.context.get("regime", "?").value
                                          if hasattr(decision.context.get("regime"), "value") else "-"))

            for w in chart_frame.winfo_children():
                w.destroy()
            df = decision.context.get("df")
            _make_chart(df, chart_frame)

            trades_tree.delete(*trades_tree.get_children())
            for tr in orchestrator.db.closed_trades(limit=200):
                trades_tree.insert("", "end", values=(
                    tr.get("opened_at", ""), tr.get("symbol", ""), tr.get("side", ""),
                    f"{tr.get('entry', 0):.2f}", f"{tr.get('exit_price', 0):.2f}",
                    f"{tr.get('pnl', 0):+.2f}", tr.get("reason", "")
                ))

            brain_text.delete("1.0", "end")
            brain_text.insert("end", f"=== {symbol} ===\n")
            brain_text.insert("end", f"{decision.rationale}\n\n")
            for s in decision.signals:
                brain_text.insert("end", f"• {s.name:<10} score={s.score:+.2f}  "
                                         f"conf={s.confidence:.2f}  peso={s.weight:.2f}\n")
                if s.detail:
                    brain_text.insert("end", f"    detalhe: {json.dumps(s.detail, ensure_ascii=False)[:160]}\n")
        except Exception as exc:  # pragma: no cover
            brain_text.delete("1.0", "end")
            brain_text.insert("end", f"Erro ao atualizar: {exc}\n")
        root.after(int(interval_ms), _refresh)

    root.after(200, _refresh)
    root.mainloop()
