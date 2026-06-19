from __future__ import annotations

import random
import threading
import time
from typing import Dict, List

try:
    from pydantic import BaseModel  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    # Minimal fallback to keep the service importable without pydantic.
    class BaseModel:  # type: ignore
        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)



# We load the Tk-based DecisionEngine from the repo root (DecisionEngine.py)
# but use it in a headless adapter: we only keep its data-model in memory.
# This avoids depending on tkinter widgets.

from pathlib import Path
import importlib.util
import sys


_ROOT_FILE = Path(__file__).resolve().parents[3] / "DecisionEngine.py"

spec = importlib.util.spec_from_file_location("DecisionEngineRoot", _ROOT_FILE)
if spec is None or spec.loader is None:  # pragma: no cover
    raise ImportError(f"Não foi possível carregar {_ROOT_FILE}")

_mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = _mod
spec.loader.exec_module(_mod)  # type: ignore[union-attr]

DecisionAlgorithm = _mod.DecisionAlgorithm
DecisionNode = _mod.DecisionNode
MarketDecision = _mod.MarketDecision
AlgorithmType = _mod.AlgorithmType
NodeStatus = _mod.NodeStatus
DecisionType = _mod.DecisionType


class DecisionAlgorithmDTO(BaseModel):
    id: str
    name: str
    algo_type: str
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


class DecisionFlowNodeDTO(BaseModel):
    id: str
    name: str
    input_data: str
    output_data: str
    confidence: float
    execution_time: float
    status: str


class MarketDecisionDTO(BaseModel):
    id: str
    timestamp: str
    algorithm: str
    decision: str
    confidence: float
    reasoning: str
    factors: List[str]
    risk: float
    expected_return: float
    timeframe: str


class DecisionStateResponse(BaseModel):
    algorithms: List[DecisionAlgorithmDTO]
    decision_flow: List[DecisionFlowNodeDTO]
    recent_decisions: List[MarketDecisionDTO]
    is_processing: bool
    current_decisions: int
    system_load: float
    active_tab: str


class RunDecisionResponse(BaseModel):
    ok: bool
    message: str


class ToggleAlgorithmResponse(BaseModel):
    ok: bool
    algorithm_id: str
    is_active: bool


def _algo_to_dto(a: DecisionAlgorithm) -> DecisionAlgorithmDTO:
    return DecisionAlgorithmDTO(
        id=a.id,
        name=a.name,
        algo_type=a.algo_type.value if hasattr(a.algo_type, "value") else str(a.algo_type),
        description=a.description,
        accuracy=float(a.accuracy),
        speed=float(a.speed),
        complexity=float(a.complexity),
        confidence=float(a.confidence),
        is_active=bool(a.is_active),
        decisions=int(a.decisions),
        success_rate=float(a.success_rate),
        avg_response_time=float(a.avg_response_time),
        specialization=list(a.specialization),
    )


def _node_to_dto(n: DecisionNode) -> DecisionFlowNodeDTO:
    return DecisionFlowNodeDTO(
        id=n.id,
        name=n.name,
        input_data=n.input_data,
        output_data=n.output_data,
        confidence=float(n.confidence),
        execution_time=float(n.execution_time),
        status=n.status.value if hasattr(n.status, "value") else str(n.status),
    )


def _decision_to_dto(d: MarketDecision) -> MarketDecisionDTO:
    return MarketDecisionDTO(
        id=d.id,
        timestamp=d.timestamp,
        algorithm=d.algorithm,
        decision=d.decision.value if hasattr(d.decision, "value") else str(d.decision),
        confidence=float(d.confidence),
        reasoning=d.reasoning,
        factors=list(d.factors),
        risk=float(d.risk),
        expected_return=float(d.expected_return),
        timeframe=d.timeframe,
    )


class DecisionService:
    def __init__(self) -> None:
        # Pull initial data from module constants
        self._lock = threading.Lock()

        self._algorithms: List[DecisionAlgorithm] = [
            *getattr(_mod, "INITIAL_ALGORITHMS"),
        ]
        # copy objects (dataclasses). shallow copy is okay here.
        self._decision_flow: List[DecisionNode] = [*getattr(_mod, "INITIAL_FLOW")]
        self._recent_decisions: List[MarketDecision] = [*getattr(_mod, "INITIAL_DECISIONS")]

        self._is_processing: bool = False
        self._current_decisions: int = 14520
        self._system_load: float = 67.3
        self._active_tab: str = "ALGORITHMS"

        self._start_live_metrics()

    def get_state(self) -> DecisionStateResponse:
        with self._lock:
            return DecisionStateResponse(
                algorithms=[_algo_to_dto(a) for a in self._algorithms],
                decision_flow=[_node_to_dto(n) for n in self._decision_flow],
                recent_decisions=[_decision_to_dto(d) for d in self._recent_decisions],
                is_processing=self._is_processing,
                current_decisions=self._current_decisions,
                system_load=self._system_load,
                active_tab=self._active_tab,
            )

    def toggle(self, algorithm_id: str) -> ToggleAlgorithmResponse:
        with self._lock:
            found = False
            for a in self._algorithms:
                if a.id == algorithm_id:
                    a.is_active = not a.is_active
                    found = True
                    return ToggleAlgorithmResponse(ok=True, algorithm_id=a.id, is_active=a.is_active)
            if not found:
                return ToggleAlgorithmResponse(ok=False, algorithm_id=algorithm_id, is_active=False)

    def run(self) -> RunDecisionResponse:
        with self._lock:
            if self._is_processing:
                return RunDecisionResponse(ok=False, message="Já está processando")
            self._is_processing = True

        # Simulate the same flow logic as in DecisionEngine.py but in headless mode.
        def _simulate():
            # Reset flow
            with self._lock:
                self._decision_flow = [
                    DecisionNode("1", "Coleta de Dados", "Market Data", "Processed Data", random.random() * 20 + 80, 0.02, NodeStatus.PROCESSING),
                    DecisionNode("2", "Pré-processamento", "Raw Data", "Clean Data", 0, 0, NodeStatus.WAITING),
                    DecisionNode("3", "Feature Engineering", "Clean Data", "Features", 0, 0, NodeStatus.WAITING),
                    DecisionNode("4", "Análise Ensemble", "Features", "Predictions", 0, 0, NodeStatus.WAITING),
                    DecisionNode("5", "Validação Cruzada", "Predictions", "Validated", 0, 0, NodeStatus.WAITING),
                    DecisionNode("6", "Execução de Decisão", "Validated", "Action", 0, 0, NodeStatus.WAITING),
                ]

            for i in range(len(self._decision_flow)):
                time.sleep(0.6)
                with self._lock:
                    current = self._decision_flow[i]
                    self._decision_flow[i] = DecisionNode(
                        current.id,
                        current.name,
                        current.input_data,
                        current.output_data,
                        random.random() * 10 + 85,
                        random.random() * 0.5,
                        NodeStatus.COMPLETED,
                    )

                    if i + 1 < len(self._decision_flow):
                        nxt = self._decision_flow[i + 1]
                        self._decision_flow[i + 1] = DecisionNode(
                            nxt.id,
                            nxt.name,
                            nxt.input_data,
                            nxt.output_data,
                            0,
                            0,
                            NodeStatus.PROCESSING,
                        )

            time.sleep(0.5)

            with self._lock:
                # Finish
                self._is_processing = False

                new_decision = MarketDecision(
                    id=f"dec-{int(time.time())}",
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                    algorithm="Ensemble Multi-Algoritmo",
                    decision=random.choice([DecisionType.BUY, DecisionType.SELL]),
                    confidence=random.random() * 15 + 80,
                    reasoning="Processo de decisão manual concluído com sucesso.",
                    factors=["Manual Trigger", "Live Analysis"],
                    risk=1.5,
                    expected_return=3.2,
                    timeframe="15m",
                )

                self._recent_decisions.insert(0, new_decision)
                self._current_decisions += 1

        threading.Thread(target=_simulate, daemon=True).start()

        return RunDecisionResponse(ok=True, message="Processo iniciado")

    def _start_live_metrics(self) -> None:
        def _update_loop():
            while True:
                time.sleep(2)
                with self._lock:
                    new_load = max(30, min(99, self._system_load + (random.random() - 0.5) * 5))
                    self._system_load = float(new_load)

                    # Occasionally increment decisions
                    if random.random() > 0.7:
                        increment = random.randint(1, 3)
                        self._current_decisions += increment

        threading.Thread(target=_update_loop, daemon=True).start()


decision_service = DecisionService()

