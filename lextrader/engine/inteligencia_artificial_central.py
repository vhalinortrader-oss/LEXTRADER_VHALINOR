"""Wrapper de migração: Inteligencia_artificial_central (arquivo do diretório raiz).

Este módulo existe para suportar a estrutura de pacote `lextrader/`.
O conteúdo original permanece em:
- `Inteligencia_artificial_central.py`

Importa tudo do arquivo raiz para manter compatibilidade.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_ROOT_FILE = Path(__file__).resolve().parents[2] / "Inteligencia_artificial_central.py"

spec = importlib.util.spec_from_file_location("Inteligencia_artificial_central", _ROOT_FILE)
if spec is None or spec.loader is None:  # pragma: no cover
    raise ImportError(f"Não foi possível carregar {_ROOT_FILE}")

_mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = _mod
spec.loader.exec_module(_mod)  # type: ignore[union-attr]

# Reexporta nomes públicos do módulo raiz
for _name in getattr(_mod, "__all__", []):
    globals()[_name] = getattr(_mod, _name)

# Se __all__ não existir, reexporta tudo que não seja privado
if not getattr(_mod, "__all__", None):
    for _name, _val in vars(_mod).items():
        if _name.startswith("_"):
            continue
        globals()[_name] = _val

