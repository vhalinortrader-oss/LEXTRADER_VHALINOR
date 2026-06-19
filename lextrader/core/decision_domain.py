from __future__ import annotations

import random
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Callable, List, Optional, Sequence


class AlgorithmType(Enum):
    ML = "ML"
    STATISTICAL = "STATISTICAL"
    HYBRID = "HYBRID"
    QUANTUM = "QUANTUM"
    ENSEMBLE = "ENSEMBLE"


class NodeStatus(Enum):
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    WAITING = "WAITING"
    ERROR = "ERROR"


class DecisionType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    CLOSE = "CLOSE"


@dataclass
class DecisionAlgorithm:
    id: str
    name: str
    algo_type: AlgorithmType
    description: str
    accuracy: float
    speed: float
    complexity: float
    confidence: float
    is_active: bool
    decisions: int
    success_rate: float
    avg_response_time: float
    specialization: List[str]


@dataclass
class DecisionNode:
    id: str
    name: str
    input_data: str
    output_data: str
    confidence: float
    execution_time: float
    status: NodeStatus


@dataclass
class MarketDecision:
    id: str
    timestamp: str
    algorithm: str
    decision: DecisionType
    confidence: float
    reasoning: str
    factors: List[str]
    risk: float
    expected_return: float
    timeframe: str


# Data used by the simulator/service.
INITIAL_ALGORITHMS: List[DecisionAlgorithm] = [
    DecisionAlgorithm(
        id="ensemble",
        name="Ensemble Multi-Algoritmo",
        algo_type=AlgorithmType.ENSEMBLE,
        description="Combina múltiplos algoritmos usando voting e stacking para decisões mais robustas",
        accuracy=94.7,
        speed=85.2,
        complexity=95.8,
        confidence=89.3,
        is_active=True,
        decisions=2847,
        success_rate=87.4,
        avg_response_time=0.23,
        specialization=["Análise Multi-Modal", "Consenso Algorítmico", "Meta-Learning"],
    ),
    DecisionAlgorithm(
        id="quantum_nn",
        name="Rede Neural Quântica",
        algo_type=AlgorithmType.QUANTUM,
        description="Utiliza computação quântica simulada para processamento paralelo de cenários",
        accuracy=91.3,
        speed=92.7,
        complexity=98.5,
        confidence=85.9,
        is_active=True,
        decisions=1623,
        success_rate=83.2,
        avg_response_time=0.08,
        specialization=["Superposição", "Entrelaçamento", "Túnel Quântico"],
    ),
    DecisionAlgorithm(
        id="adaptive_lstm",
        name="LSTM Adaptativo Profundo",
        algo_type=AlgorithmType.ML,
        description="Rede LSTM com arquitetura adaptativa que se reconfigura baseada em condições de mercado",
        accuracy=88.9,
        speed=78.4,
        complexity=87.3,
        confidence=82.7,
        is_active=True,
        decisions=3241,
        success_rate=79.6,
        avg_response_time=0.45,
        specialization=["Séries Temporais", "Memória Longa", "Adaptação Dinâmica"],
    ),
    DecisionAlgorithm(
        id="bayesian_optimizer",
        name="Otimizador Bayesiano",
        algo_type=AlgorithmType.STATISTICAL,
        description="Optimiza múltiplos objetivos simultaneamente usando inferência bayesiana",
        accuracy=86.4,
        speed=71.8,
        complexity=82.1,
        confidence=78.9,
        is_active=True,
        decisions=1876,
        success_rate=81.3,
        avg_response_time=0.67,
        specialization=["Otimização", "Incerteza", "Multi-Objetivo"],
    ),
    DecisionAlgorithm(
        id="reinforcement_agent",
        name="Agente de Reforço (RL)",
        algo_type=AlgorithmType.ML,
        description="Agente que aprende estratégias ótimas através de interação com o ambiente de mercado",
        accuracy=89.7,
        speed=83.6,
        complexity=91.4,
        confidence=86.1,
        is_active=True,
        decisions=2156,
        success_rate=84.8,
        avg_response_time=0.31,
        specialization=["Q-Learning", "Policy Gradient", "Actor-Critic"],
    ),
    DecisionAlgorithm(
        id="fuzzy_expert",
        name="Sistema Especialista Fuzzy",
        algo_type=AlgorithmType.HYBRID,
        description="Combina lógica fuzzy com regras de especialistas para decisões em incerteza",
        accuracy=84.2,
        speed=94.7,
        complexity=73.9,
        confidence=76.4,
        is_active=False,
        decisions=1432,
        success_rate=77.9,
        avg_response_time=0.12,
        specialization=["Lógica Fuzzy", "Regras Especialistas", "Incerteza"],
    ),
    DecisionAlgorithm(
        id="genetic_algorithm",
        name="Algoritmo Genético",
        algo_type=AlgorithmType.HYBRID,
        description="Evolui estratégias de trading através de seleção natural e mutação genética",
        accuracy=87.1,
        speed=76.3,
        complexity=88.7,
        confidence=81.5,
        is_active=True,
        decisions=998,
        success_rate=82.7,
        avg_response_time=0.89,
        specialization=["Evolução", "Otimização Genética", "Seleção Natural"],
    ),
]


INITIAL_FLOW: List[DecisionNode] = [
    DecisionNode("1", "Coleta de Dados", "Market Data", "Processed Data", 98.5, 0.02, NodeStatus.COMPLETED),
    DecisionNode(
        "2", "Pré-processamento", "Raw Data", "Clean Data", 96.7, 0.08, NodeStatus.COMPLETED
    ),
    DecisionNode(
        "3", "Feature Engineering", "Clean Data", "Features", 94.2, 0.15, NodeStatus.COMPLETED
    ),
    DecisionNode("4", "Análise Ensemble", "Features", "Predictions", 89.3, 0.23, NodeStatus.PROCESSING),
    DecisionNode("5", "Validação Cruzada", "Predictions", "Validated", 0, 0, NodeStatus.WAITING),
    DecisionNode("6", "Execução de Decisão", "Validated", "Action", 0, 0, NodeStatus.WAITING),
]


INITIAL_DECISIONS: List[MarketDecision] = [
    MarketDecision(
        id="dec-1",
        timestamp="2024-01-15 15:42:23",
        algorithm="Ensemble Multi-Algoritmo",
        decision=DecisionType.BUY,
        confidence=87.4,
        reasoning="Confluência de sinais: breakout técnico + momentum positivo + volume acima da média",
        factors=["RSI(14): 45.2", "MACD: Bullish Cross", "Volume: +234%", "Support: 42,100"],
        risk=2.3,
        expected_return=5.7,
        timeframe="4H",
    ),
    MarketDecision(
        id="dec-2",
        timestamp="2024-01-15 15:38:47",
        algorithm="Rede Neural Quântica",
        decision=DecisionType.SELL,
        confidence=92.1,
        reasoning="Padrão de reversão detectado com alta probabilidade baseado em análise quântica",
        factors=["Quantum State: Bearish", "Volatility: Increasing", "Resistance: 42,800", "Divergence: Confirmed"],
        risk=1.8,
        expected_return=4.2,
        timeframe="1H",
    ),
    MarketDecision(
        id="dec-3",
        timestamp="2024-01-15 15:35:12",
        algorithm="LSTM Adaptativo",
        decision=DecisionType.HOLD,
        confidence=76.8,
        reasoning="Mercado em consolidação, aguardando breakout definitivo da faixa atual",
        factors=["Trend: Sideways", "ATR: Low", "Volume: Decreasing", "Support/Resistance: Strong"],
        risk=1.2,
        expected_return=2.1,
        timeframe="2H",
    ),
]


def build_new_market_decision(*, rng: random.Random, now: Optional[datetime] = None) -> MarketDecision:
    now = now or datetime.now()
    return MarketDecision(
        id=f"dec-{int(time.time())}",
        timestamp=now.strftime("%Y-%m-%d %H:%M:%S"),
        algorithm="Ensemble Multi-Algoritmo",
        decision=rng.choice([DecisionType.BUY, DecisionType.SELL]),
        confidence=float(rng.random() * 15 + 80),
        reasoning="Processo de decisão manual concluído com sucesso.",
        factors=["Manual Trigger", "Live Analysis"],
        risk=1.5,
        expected_return=3.2,
        timeframe="15m",
    )


def default_sleep(_seconds: float) -> None:
    # injectable for tests
    time.sleep(_seconds)


def simulate_flow_steps(
    *,
    initial_flow: Sequence[DecisionNode],
    step_sleep_seconds: float,
    rng: random.Random,
    sleep_fn: Callable[[float], None] = default_sleep,
) -> List[List[DecisionNode]]:
    """Runs a deterministic (seeded) simulation and returns snapshots of flow per step."""
    flow: List[DecisionNode] = [*initial_flow]
    snapshots: List[List[DecisionNode]] = []

    # Ensure first node already starts as PROCESSING/COMPLETED depending on the snapshot we want.
    for i in range(len(flow)):
        sleep_fn(step_sleep_seconds)
        current = flow[i]
        flow[i] = DecisionNode(
            current.id,
            current.name,
            current.input_data,
            current.output_data,
            float(rng.random() * 10 + 85),
            float(rng.random() * 0.5),
            NodeStatus.COMPLETED,
        )
        if i + 1 < len(flow):
            nxt = flow[i + 1]
            flow[i + 1] = DecisionNode(
                nxt.id,
                nxt.name,
                nxt.input_data,
                nxt.output_data,
                0.0,
                0.0,
                NodeStatus.PROCESSING,
            )
        snapshots.append([*flow])

    return snapshots

