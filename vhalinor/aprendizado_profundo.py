"""📚 Aprendizado Profundo — modelos supervisionados (MLP / CNN) com fallback sklearn."""
from __future__ import annotations

import pickle
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import numpy as np
import pandas as pd

from .utils import logger

try:
    from sklearn.neural_network import MLPClassifier, MLPRegressor
    HAVE_SK = True
except Exception:  # pragma: no cover
    HAVE_SK = False

try:
    import torch
    from torch import nn
    HAVE_TORCH = True
except Exception:  # pragma: no cover
    HAVE_TORCH = False


@dataclass
class ResultadoTreino:
    n_amostras: int
    acc_treino: float
    acc_validacao: float
    perda_final: float
    backbone: str
    extras: Dict[str, Any] = field(default_factory=dict)


class _TorchMLP(nn.Module if HAVE_TORCH else object):  # type: ignore[misc]
    def __init__(self, n_in: int, n_out: int, hidden: int = 64):
        if not HAVE_TORCH:
            raise RuntimeError("torch indisponível")
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_in, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, n_out),
        )

    def forward(self, x):
        return self.net(x)


class AprendizadoProfundo:
    """Wrapper para treino de redes neurais com sklearn ou torch."""

    def __init__(self, modelo: str = "mlp", epochs: int = 25, learning_rate: float = 1e-3,
                 hidden: int = 64, models_dir: Optional[Path] = None) -> None:
        self.modelo = modelo.lower()
        self.epochs = int(epochs)
        self.learning_rate = float(learning_rate)
        self.hidden = int(hidden)
        self._sk = None
        self._torch: Optional[_TorchMLP] = None
        self.scaler_mean: Optional[np.ndarray] = None
        self.scaler_std: Optional[np.ndarray] = None
        self._task: str = "classificacao"
        self._models_dir = models_dir

    def _build(self, n_in: int, n_out: int) -> None:
        if self.modelo == "torch" and HAVE_TORCH:
            self._torch = _TorchMLP(n_in, n_out, hidden=self.hidden)
            return
        if not HAVE_SK:
            raise RuntimeError(
                "Nenhum backend de DL disponível (sklearn/torch ausentes).")
        if self._task == "classificacao":
            self._sk = MLPClassifier(hidden_layer_sizes=(self.hidden, self.hidden), max_iter=self.epochs,
                                     learning_rate_init=self.learning_rate, random_state=42)
        else:
            self._sk = MLPRegressor(hidden_layer_sizes=(self.hidden, self.hidden), max_iter=self.epochs,
                                    learning_rate_init=self.learning_rate, random_state=42)

    def treinar(self, X: np.ndarray, y: np.ndarray, task: str = "classificacao",
                validacao: float = 0.2) -> ResultadoTreino:
        if X is None or len(X) == 0:
            raise ValueError("Sem dados para treinar.")
        self._task = task
        n = len(X)
        idx = np.arange(n)
        np.random.RandomState(42).shuffle(idx)
        corte = int(n * (1 - validacao))
        tr, va = idx[:corte], idx[corte:]
        Xtr, Xva = X[tr], X[va]
        ytr, yva = y[tr], y[va]

        self.scaler_mean = Xtr.mean(axis=0)
        self.scaler_std = Xtr.std(axis=0) + 1e-8
        Xtr_n = (Xtr - self.scaler_mean) / self.scaler_std
        Xva_n = (Xva - self.scaler_mean) / self.scaler_std

        n_out = int(max(ytr.max() if task == "classificacao" else 1, 1)) if task == "regressao" \
            else int(max(np.max(ytr), np.max(yva) if len(yva) else 0) + 1)
        self._build(Xtr_n.shape[1], n_out if task == "classificacao" else 1)

        backbone = "torch" if self._torch is not None else "sklearn"
        perda_final = 0.0
        if self._torch is not None:
            device = torch.device(
                "cuda" if torch.cuda.is_available() else "cpu")
            self._torch.to(device)
            opt = torch.optim.Adam(
                self._torch.parameters(), lr=self.learning_rate)
            loss_fn = nn.CrossEntropyLoss() if task == "classificacao" else nn.MSELoss()
            Xtr_t = torch.tensor(Xtr_n, dtype=torch.float32, device=device)
            ytr_t = torch.tensor(ytr, dtype=torch.long, device=device) if task == "classificacao" \
                else torch.tensor(ytr, dtype=torch.float32, device=device)
            self._torch.train()
            for _ in range(self.epochs):
                opt.zero_grad()
                out = self._torch(Xtr_t)
                if task == "classificacao":
                    l = loss_fn(out, ytr_t)
                else:
                    l = loss_fn(out.squeeze(-1), ytr_t)
                l.backward()
                opt.step()
                perda_final = float(l.item())
            self._torch.eval()
        else:
            self._sk.fit(Xtr_n, ytr)
            perda_final = float(
                getattr(self._sk, "loss_", [0.0])[-1] if hasattr(self._sk, "loss_") else 0.0)

        acc_tr = self._avaliar(Xtr_n, ytr, task)
        acc_va = self._avaliar(Xva_n, yva, task) if len(yva) else 0.0
        return ResultadoTreino(n_amostras=int(n), acc_treino=acc_tr, acc_validacao=acc_va,
                               perda_final=perda_final, backbone=backbone)

    def prever(self, X: np.ndarray) -> np.ndarray:
        if self.scaler_mean is None:
            raise RuntimeError("Modelo não treinado.")
        Xn = (X - self.scaler_mean) / self.scaler_std
        if self._torch is not None:
            self._torch.eval()
            with torch.no_grad():
                out = self._torch(torch.tensor(Xn, dtype=torch.float32))
            return out.numpy()
        return self._sk.predict(Xn)

    def _avaliar(self, X: np.ndarray, y: np.ndarray, task: str) -> float:
        try:
            pred = self.prever(
                X) if self.scaler_mean is not None else np.zeros_like(y)
        except Exception:
            return 0.0
        if task == "classificacao":
            return float((pred == y).mean()) if len(y) else 0.0
        # R² aproximado
        ss_res = float(((y - pred) ** 2).sum())
        ss_tot = float(((y - y.mean()) ** 2).sum() or 1.0)
        return max(0.0, 1.0 - ss_res / ss_tot)

    def salvar(self, path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump({
                "modelo": self.modelo, "epochs": self.epochs, "learning_rate": self.learning_rate,
                "hidden": self.hidden, "scaler_mean": self.scaler_mean, "scaler_std": self.scaler_std,
                "sk": self._sk, "torch_state": (self._torch.state_dict() if self._torch is not None else None),
                "task": self._task,
            }, f)

    def carregar(self, path) -> None:
        with open(path, "rb") as f:
            d = pickle.load(f)
        self.modelo = d["modelo"]
        self.epochs = d["epochs"]
        self.learning_rate = d["learning_rate"]
        self.hidden = d["hidden"]
        self.scaler_mean = d["scaler_mean"]
        self.scaler_std = d["scaler_std"]
        self._sk = d["sk"]
        self._task = d["task"]
        if d.get("torch_state") is not None and HAVE_TORCH:
            n_in = (self.scaler_mean.shape[0]
                    if self.scaler_mean is not None else 1)
            n_out = 2 if self._task == "classificacao" else 1
            self._torch = _TorchMLP(n_in, n_out, hidden=self.hidden)
            self._torch.load_state_dict(d["torch_state"])
