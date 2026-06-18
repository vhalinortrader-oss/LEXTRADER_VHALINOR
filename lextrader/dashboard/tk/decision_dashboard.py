"""Wrapper de migração (Tkinter): possíveis componentes de dashboard do DecisionEngine.

Arquivo raiz relacionado: `DecisionEngine.py`.

Cria uma camada de import para facilitar a organização sem remover compatibilidade.
"""

from __future__ import annotations

from lextrader.decision.decision_engine import DecisionEngine  # type: ignore

__all__ = ["DecisionEngine"]

