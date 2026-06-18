"""Camada de Estado Global + núcleo multithread do cérebro artificial."""
from .estado import EstadoGlobal
from .regras import RegraCruzamentoMM, RegraRSIMACD, RegraBollingerReversao, RegraBase

__all__ = [
    "EstadoGlobal", "RegraCruzamentoMM", "RegraRSIMACD",
    "RegraBollingerReversao", "RegraBase",
]
