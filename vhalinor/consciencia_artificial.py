"""🧠 Consciência Artificial — representação interna, autocontrole e relato.

Implementa um *Global Workspace* simplificado, onde módulos especializados
(neurônios, modelos, raciocínio) publicam *estados* e o "eu central" integra,
mantém um relato coerente e autoavalia a própria confiança.
"""
from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Deque, Dict, List, Optional


@dataclass
class EstadoConsciencia:
    """Snapshot do estado interno do sistema."""
    timestamp: float = field(default_factory=time.time)
    foco: str = ""                       # ativo / módulo em destaque
    confianca_global: float = 0.0        # [0, 1]
    estabilidade: float = 0.0            # [0, 1] — quão consistente tem sido o foco
    metas: List[str] = field(default_factory=list)
    emocoes: Dict[str, float] = field(default_factory=dict)
    narrativa: str = ""                  # relato interno
    modulos_ativos: Dict[str, float] = field(default_factory=dict)


class ConscienciaArtificial:
    """Integra sinais de outros módulos (neurônios, raciocínio, sentimento)."""

    def __init__(self, historia_max: int = 200) -> None:
        self.buffer: Deque[EstadoConsciencia] = deque(maxlen=historia_max)
        self.ultimo: EstadoConsciencia = EstadoConsciencia()
        self._modulos: Dict[str, float] = {}
        self._foco_anterior: List[str] = []

    # ----- entrada de sinais -----
    def reportar(self, modulo: str, ativacao: float, payload: Optional[Dict[str, Any]] = None) -> None:
        """Um módulo 'publica' sua ativação atual no workspace global."""
        self._modulos[modulo] = float(max(0.0, min(1.0, ativacao)))
        if payload:
            for k, v in payload.items():
                if k == "metas" and isinstance(v, list):
                    self.ultimo.metas = v
                elif k == "emocoes" and isinstance(v, dict):
                    self.ultimo.emocoes.update(v)
                elif k == "narrativa" and isinstance(v, str):
                    self.ultimo.narrativa = v

    def atualizar_foco(self, candidatos: List[str]) -> str:
        """Seleciona o módulo/ativo mais ativado e mantém estabilidade."""
        if not candidatos:
            return ""
        scores = {c: self._modulos.get(c, 0.0) for c in candidatos}
        foco = max(scores, key=scores.get) if scores else ""
        if foco and foco in self._foco_anterior:
            self.ultimo.estabilidade = min(1.0, self.ultimo.estabilidade + 0.1)
        else:
            self.ultimo.estabilidade = max(0.0, self.ultimo.estabilidade - 0.2)
        self._foco_anterior.append(foco)
        if len(self._foco_anterior) > 20:
            self._foco_anterior = self._foco_anterior[-20:]
        self.ultimo.foco = foco
        return foco

    # ----- integração -----
    def integrar(self, confianca_fontes: Optional[Dict[str, float]] = None) -> EstadoConsciencia:
        """Consolida um novo estado de consciência (snapshot)."""
        if confianca_fontes:
            vals = [v for v in confianca_fontes.values() if v is not None]
            if vals:
                self.ultimo.confianca_global = sum(vals) / len(vals)
        self.ultimo.modulos_ativos = dict(self._modulos)
        self.ultimo.timestamp = time.time()
        self.buffer.append(self.ultimo)
        return self.ultimo

    # ----- introspecção -----
    def relatar(self) -> str:
        """Gera um texto curto descrevendo o estado atual do 'eu'."""
        e = self.ultimo
        emocao_top = ""
        if e.emocoes:
            emocao_top = max(e.emocoes, key=e.emocoes.get)
        return (f"Foco: {e.foco or '-'} | conf={e.confianca_global:.2f} | "
                f"estab={e.estabilidade:.2f} | emoção: {emocao_top or '-'}")

    def explicar(self) -> Dict[str, Any]:
        return {
            "foco": self.ultimo.foco,
            "confianca_global": self.ultimo.confianca_global,
            "estabilidade": self.ultimo.estabilidade,
            "narrativa": self.ultimo.narrativa,
            "metas": list(self.ultimo.metas),
            "emocoes": dict(self.ultimo.emocoes),
            "historico": [{"t": s.timestamp, "foco": s.foco, "conf": s.confianca_global} for s in list(self.buffer)[-10:]],
        }
