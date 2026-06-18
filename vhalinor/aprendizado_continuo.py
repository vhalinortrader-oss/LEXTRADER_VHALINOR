"""📈 Aprendizado Contínuo — EWC + buffer de replay para evitar esquecimento catastrófico."""
from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Deque, Dict, Iterable, List, Optional, Tuple

import numpy as np

from .utils import logger


@dataclass
class AmostraReplay:
    x: np.ndarray
    y: Any
    peso: float = 1.0
    tarefa: str = "default"


@dataclass
class Tarefa:
    nome: str
    n_features: int


class AprendizadoContinuo:
    """Replay buffer + regularização EWC simplificada (diagonal Fisher)."""

    def __init__(self, capacidade_replay: int = 5000, ewc_lambda: float = 400.0) -> None:
        self.replay: Deque[AmostraReplay] = deque(maxlen=int(capacidade_replay))
        self.ewc_lambda = float(ewc_lambda)
        self._pesos_anteriores: Optional[Dict[str, np.ndarray]] = None
        self._fisher: Optional[Dict[str, np.ndarray]] = None
        self._tarefas: List[Tarefa] = []
        self.metricas: List[Dict[str, float]] = []

    # ----- API -----
    def registrar_tarefa(self, nome: str, n_features: int) -> None:
        self._tarefas.append(Tarefa(nome=nome, n_features=n_features))

    def adicionar_amostra(self, x: np.ndarray, y: Any, tarefa: str = "default", peso: float = 1.0) -> None:
        self.replay.append(AmostraReplay(x=np.asarray(x, dtype=float), y=y, peso=peso, tarefa=tarefa))

    def amostrar_replay(self, n: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        if not self.replay:
            return np.empty((0,)), np.empty((0,)), np.empty((0,))
        n = min(n, len(self.replay))
        idx = np.random.choice(len(self.replay), size=n, replace=False)
        xs = np.stack([self.replay[i].x for i in idx])
        ys = np.array([self.replay[i].y for i in idx])
        pesos = np.array([self.replay[i].peso for i in idx], dtype=float)
        return xs, ys, pesos

    # ----- EWC -----
    def calcular_fisher(self, modelo) -> Dict[str, np.ndarray]:
        """Calcula a diagonal da matriz Fisher Information a partir de amostras de replay."""
        fisher: Dict[str, np.ndarray] = {}
        if not self.replay:
            return fisher
        xs, ys, _ = self.amostrar_replay(min(128, len(self.replay)))
        try:
            modelo.zero_grad()
            loss = modelo.perda_replay(xs, ys)
            loss.backward()
            for nome, p in modelo.named_parameters():
                if p.grad is not None:
                    fisher[nome] = (p.grad.detach().cpu().numpy() ** 2).copy()
        except Exception as exc:  # pragma: no cover
            logger.debug(f"[continuo] Fisher não calculado: {exc}")
        return fisher

    def consolidar(self, modelo) -> None:
        """Salva pesos atuais como 'ancestrais' para a próxima consolidação."""
        self._pesos_anteriores = {n: p.detach().cpu().clone().numpy()
                                  for n, p in modelo.named_parameters()}
        self._fisher = self.calcular_fisher(model)

    def perda_ewc(self, modelo) -> float:
        if self._pesos_anteriores is None or self._fisher is None:
            return 0.0
        total = 0.0
        try:
            for n, p in modelo.named_parameters():
                if n in self._pesos_anteriores and n in self._fisher:
                    diff = p.detach().cpu().numpy() - self._pesos_anteriores[n]
                    total += float((self._fisher[n] * diff ** 2).sum())
        except Exception as exc:  # pragma: no cover
            logger.debug(f"[continuo] EWC erro: {exc}")
        return float(self.ewc_lambda * total)

    def esquecer_fraco(self, limite: int = 2000) -> int:
        if len(self.replay) <= limite:
            return 0
        self.replay = deque(sorted(self.replay, key=lambda a: a.peso, reverse=True)[:limite], maxlen=limite)
        return 1
