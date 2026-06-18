"""Wrapper de migração: AutomationDashboard (arquivo do diretório raiz).

Mantém compatibilidade com a estrutura de pacote `lextrader/`.
O conteúdo original permanece em:
- `AutomationDashboard.py`

Observação: este módulo usa Streamlit; ao importar, o código do arquivo
original pode executar chamadas ao Streamlit. Por isso, este wrapper foi
feito para reexportar mantendo comportamento idêntico do arquivo raiz.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_ROOT_FILE = Path(__file__).resolve().parents[3] / "AutomationDashboard.py"

spec = importlib.util.spec_from_file_location("AutomationDashboard", _ROOT_FILE)
if spec is None or spec.loader is None:  # pragma: no cover
    raise ImportError(f"Não foi possível carregar {_ROOT_FILE}")

_mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = _mod
spec.loader.exec_module(_mod)  # type: ignore[union-attr]

if getattr(_mod, "__all__", None):
    for _name in _mod.__all__:  # type: ignore[attr-defined]
        globals()[_name] = getattr(_mod, _name)
else:
    for _name, _val in vars(_mod).items():
        if _name.startswith("_"):
            continue
        globals()[_name] = _val

