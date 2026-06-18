"""🤔 Raciocínio Avançado — dedução, indução, abdução, contrafactual e planejamento."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class TipoInferencia(str, Enum):
    DEDUTIVA = "dedutiva"
    INDUTIVA = "indutiva"
    ABDUTIVA = "abdutiva"
    CONTRAFACTUAL = "contrafactual"


@dataclass
class Premissa:
    texto: str
    verdade: float = 1.0   # crença em [0, 1]


@dataclass
class Regra:
    antecedente: List[str]
    consequente: str
    peso: float = 1.0


@dataclass
class ResultadoRaciocinio:
    tipo: TipoInferencia
    conclusao: str
    confianca: float
    trilha: List[str] = field(default_factory=list)


class RaciocinioAvancado:
    """Motor simbólico-neural leve para raciocínio aproximado."""

    def __init__(self) -> None:
        self.regras: List[Regra] = []
        self.premissas: Dict[str, Premissa] = {}
        self.causal: Dict[str, List[str]] = {}     # causa -> [efeitos]
        self.contrafactual_cache: Dict[str, ResultadoRaciocinio] = {}

    # ----- gestão de conhecimento -----
    def adicionar_premissa(self, chave: str, texto: str, verdade: float = 1.0) -> None:
        self.premissas[chave] = Premissa(
            texto=texto, verdade=float(max(0, min(1, verdade))))

    def adicionar_regra(self, antecedentes: List[str], consequente: str, peso: float = 1.0) -> None:
        self.regras.append(Regra(antecedente=list(
            antecedentes), consequente=consequente, peso=float(peso)))

    def adicionar_causa(self, causa: str, efeito: str) -> None:
        self.causal.setdefault(causa, []).append(efeito)

    # ----- inferências -----
    def deduzir(self, chaves_observadas: List[str]) -> ResultadoRaciocinio:
        """Dada a observação de antecedentes, dispara regras e retorna o consequente mais forte."""
        obs = set(chaves_observadas)
        candidatos: Dict[str, float] = {}
        trilha: List[str] = []
        for r in self.regras:
            if all(a in obs for a in r.antecedente):
                for a in r.antecedente:
                    trilha.append(f"obs: {a}")
                candidatos[r.consequente] = candidatos.get(
                    r.consequente, 0.0) + r.peso
                trilha.append(
                    f"regra: {r.antecedente} -> {r.consequente} (peso {r.peso})")
        if not candidatos:
            return ResultadoRaciocinio(TipoInferencia.DEDUTIVA, "indeterminado", 0.0, trilha)
        total = sum(candidatos.values()) or 1.0
        melhor, score = max(candidatos.items(), key=lambda x: x[1])
        return ResultadoRaciocinio(TipoInferencia.DEDUTIVA, melhor, min(1.0, score / total), trilha)

    def induzir(self, pares: List[Tuple[List[str], str]]) -> Regra:
        """Aprende uma regra a partir de exemplos (par (antecedentes, consequente))."""
        if not pares:
            return Regra([], "indeterminado", 0.0)
        contagem: Dict[Tuple[str, ...], Dict[str, float]] = {}
        for ant, cons in pares:
            k = tuple(sorted(ant))
            contagem.setdefault(k, {})
            contagem[k][cons] = contagem[k].get(cons, 0.0) + 1.0
        melhor_ant, melhor_cons, melhor_score = max(
            ((k, c, s) for k, cm in contagem.items() for c, s in cm.items()),
            key=lambda x: x[2],
            default=([], "indeterminado", 0.0),
        )
        regra = Regra(list(melhor_ant), melhor_cons,
                      melhor_score / sum(contagem[melhor_ant].values()))
        self.regras.append(regra)
        return regra

    def abduzir(self, observacao: str) -> ResultadoRaciocinio:
        """Encontra a causa mais plausível para uma observação."""
        candidatos: Dict[str, float] = {}
        for causa, efeitos in self.causal.items():
            if observacao in efeitos:
                candidatos[causa] = candidatos.get(causa, 0.0) + 1.0
        for r in self.regras:
            if r.consequente == observacao:
                for a in r.antecedente:
                    candidatos[a] = candidatos.get(a, 0.0) + r.peso
        if not candidatos:
            return ResultadoRaciocinio(TipoInferencia.ABDUTIVA, "sem causa conhecida", 0.0)
        melhor, score = max(candidatos.items(), key=lambda x: x[1])
        return ResultadoRaciocinio(TipoInferencia.ABDUTIVA, melhor, min(1.0, score / (sum(candidatos.values()) or 1.0)))

    def contrafactual(self, mundo: Dict[str, Any], mudar: str, valor: Any) -> ResultadoRaciocinio:
        """Pergunta: 'o que teria acontecido se ...?' (limitado)."""
        mundo = dict(mundo)
        mundo[mudar] = valor
        chaves = [k for k, v in mundo.items() if v]
        r = self.deduzir(chaves)
        r.tipo = TipoInferencia.CONTRAFACTUAL
        r.trilha.append(f"hipotético: {mudar}={valor}")
        self.contrafactual_cache[mudar] = r
        return r
