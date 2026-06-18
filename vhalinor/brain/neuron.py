"""Classe base `Neuron` — unidade cognitiva especializada."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional


@dataclass
class NeuronSignal:
    """Sinal emitido por um neurônio."""
    name: str
    score: float            # [-1, 1] — confiança direcional (1 = compra forte, -1 = venda forte)
    confidence: float       # [0, 1] — quão seguro o neurônio está
    detail: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0     # peso do neurônio no cérebro

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class Neuron:
    """Classe base de todos os neurônios especializados."""

    name: str = "BaseNeuron"
    weight: float = 1.0

    def __init__(self, weight: Optional[float] = None) -> None:
        if weight is not None:
            self.weight = float(weight)
        self.last_signal: Optional[NeuronSignal] = None
        self.memory: Dict[str, Any] = {}

    def process(self, context: Dict[str, Any]) -> NeuronSignal:
        """Recebe o contexto de mercado e retorna um sinal. Subclasses obrigatórias."""
        raise NotImplementedError

    def remember(self, key: str, value: Any) -> None:
        self.memory[key] = value

    def recall(self, key: str, default: Any = None) -> Any:
        return self.memory.get(key, default)
