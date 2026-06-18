"""💭 Sentiência Artificial — valência afetiva e modulação de comportamento."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Deque, Dict, Optional


class Valência(str, Enum):
    """Eixos afetivos básicos (modelo circumplexo simplificado)."""
    ALEGRIA = "alegria"
    MEDO = "medo"
    RAIVA = "raiva"
    NOJO = "nojo"
    TRISTEZA = "tristeza"
    SURPRESA = "surpresa"
    CURIOSIDADE = "curiosidade"
    CONFIANCA = "confianca"


@dataclass
class EstadoAfetivo:
    valencias: Dict[str, float]   # em [-1, 1]
    intensidade: float           # [0, 1]
    recompensa_interna: float    # [-1, 1]


class SentienciaArtificial:
    """Mantém um estado emocional que modula aprendizagem e decisão."""

    def __init__(self, janela: int = 50) -> None:
        self.janela = int(janela)
        self.historico: Deque[EstadoAfetivo] = deque(maxlen=self.janela)
        self.estado = EstadoAfetivo(
            valencias={v.value: 0.0 for v in Valência}, intensidade=0.0, recompensa_interna=0.0)

    # ----- estímulos -----
    def estimular(self, evento: str, intensidade: float = 0.5) -> None:
        """Associa um evento a uma valência dominante e atualiza o estado."""
        intensidade = float(max(0.0, min(1.0, intensidade)))
        mapa: Dict[str, Valência] = {
            "win": Valência.ALEGRIA, "lucro": Valência.ALEGRIA, "acerto": Valência.ALEGRIA,
            "loss": Valência.TRISTEZA, "prejuizo": Valência.TRISTEZA, "erro": Valência.TRISTEZA,
            "volatilidade": Valência.MEDO, "choque": Valência.MEDO,
            "oportunidade": Valência.CURIOSIDADE, "novo": Valência.CURIOSIDADE,
            "fraude": Valência.RAIVA, "manipulacao": Valência.RAIVA,
        }
        chave = evento.lower()
        val = mapa.get(chave, Valência.CURIOSIDADE)
        self.estado.valencias[val.value] = float(
            max(-1.0, min(1.0, self.estado.valencias[val.value] + intensidade)))
        # eventos positivos elevam confiança
        if val in (Valência.ALEGRIA, Valência.CONFIANCA):
            self.estado.valencias[Valência.CONFIANCA.value] += 0.1 * intensidade
        elif val in (Valência.MEDO, Valência.TRISTEZA):
            self.estado.valencias[Valência.CONFIANCA.value] -= 0.1 * intensidade
        self._normalizar()

    def decair(self, fator: float = 0.95) -> None:
        """Decaimento natural das emoções em direção ao neutro."""
        for k in self.estado.valencias:
            self.estado.valencias[k] *= float(fator)
        self._normalizar()

    # ----- saída -----
    def recompensa(self, retorno: float) -> float:
        """Converte retorno de mercado em 'recompensa afetiva' (RL afetivo)."""
        # prazer/dor via Tanh — limita extremos e cria sinal suave
        from math import tanh
        self.estado.recompensa_interna = float(tanh(retorno * 5))
        self.estimular("win" if retorno > 0 else "loss",
                       intensidade=min(1.0, abs(retorno) * 3))
        return self.estado.recompensa_interna

    def modulador_aprendizado(self) -> float:
        """Retorna um multiplicador de taxa de aprendizado em [0.5, 1.5]."""
        # confiança alta → aprende mais rápido; medo/raiva → desacelera
        c = self.estado.valencias.get(Valência.CONFIANCA.value, 0.0)
        m = self.estado.valencias.get(Valência.MEDO.value, 0.0)
        ra = self.estado.valencias.get(Valência.RAIVA.value, 0.0)
        return float(max(0.5, min(1.5, 1.0 + 0.3 * c - 0.4 * m - 0.2 * ra)))

    def emocao_dominante(self) -> Optional[Valência]:
        if not self.estado.valencias:
            return None
        k = max(self.estado.valencias, key=lambda x: abs(
            self.estado.valencias[x]))
        if abs(self.estado.valencias[k]) < 0.05:
            return None
        try:
            return Valência(k)
        except ValueError:
            return None

    def snapshot(self) -> Dict[str, float]:
        return {
            **{f"val_{k}": v for k, v in self.estado.valencias.items()},
            "intensidade": self.estado.intensidade,
            "recompensa": self.estado.recompensa_interna,
        }

    # ----- util -----
    def _normalizar(self) -> None:
        vals = list(self.estado.valencias.values())
        self.estado.intensidade = float(
            min(1.0, max(abs(v) for v in vals) if vals else 0.0))
        self.historico.append(EstadoAfetivo(
            valencias=dict(self.estado.valencias),
            intensidade=self.estado.intensidade,
            recompensa_interna=self.estado.recompensa_interna,
        ))
