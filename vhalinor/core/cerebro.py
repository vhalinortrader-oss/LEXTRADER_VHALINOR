"""Classes de neurônios baseadas em threads (Percepção, Analítico, Preditivo, etc.)."""
from __future__ import annotations

import threading
import time
from collections import deque
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from ..indicators.technical import compute_indicators
from ..utils import logger
from .estado import EstadoGlobal
from .regras import RegraBase


@dataclass
class OrdemSimulada:
    ativo: str
    sinal: int                 # 1 compra, -1 venda, 0 neutro
    tamanho: float
    preco_entrada: float
    stop_loss: float
    take_profit: float
    aberta_em: float = 0.0
    fechada: bool = False
    preco_saida: Optional[float] = None
    lucro: float = 0.0
    risco: float = 0.0
    confianca: float = 0.0
    sinal_origem: str = ""     # "regra:..." ou "ml"


# ----------------------------------------------------------------------------
# Percepção
# ----------------------------------------------------------------------------
class NeuronioPercepcao(threading.Thread):
    """Coleta preços em intervalos regulares e armazena no buffer + EstadoGlobal."""

    def __init__(self, estado: EstadoGlobal, provider=None) -> None:
        super().__init__(daemon=True, name="NeuronioPercepcao")
        self.estado = estado
        self.ativos: List[str] = list(estado.get("config.ativos") or [])
        self.intervalo = float(estado.get("config.update_sec", 60))
        self.buffer: Dict[str, deque] = {a: deque(maxlen=5000) for a in self.ativos}
        self.provider = provider
        self._stop = threading.Event()

    def stop(self) -> None:
        self._stop.set()

    def run(self) -> None:
        while not self._stop.is_set():
            for ativo in self.ativos:
                if self._stop.is_set():
                    break
                try:
                    df = self._fetch(ativo)
                    if df is None or df.empty:
                        continue
                    self.buffer[ativo].extend(df.to_dict("records"))
                    self.estado.set(f"percepcao.{ativo}.df", pd.DataFrame(list(self.buffer[ativo])))
                    self.estado.set(f"percepcao.{ativo}.novo_dado", True)
                except Exception as exc:  # pragma: no cover
                    logger.warning(f"[percepção] {ativo}: {exc}")
            self._stop.wait(self.intervalo)

    def _fetch(self, ativo: str) -> Optional[pd.DataFrame]:
        if self.provider is not None:
            return self.provider.fetch(ativo, period="1d", interval="1m").df
        import yfinance as yf
        return yf.download(ativo, period="1d", interval="1m", progress=False, auto_adjust=True)


# ----------------------------------------------------------------------------
# Analítico
# ----------------------------------------------------------------------------
class NeuronioAnalitico(threading.Thread):
    """Calcula indicadores/features sempre que houver novos dados."""

    def __init__(self, estado: EstadoGlobal) -> None:
        super().__init__(daemon=True, name="NeuronioAnalitico")
        self.estado = estado
        self.indicadores: List[str] = list(estado.get("config.indicadores") or
                                            ["rsi", "macd", "bbands", "sma_50", "sma_200",
                                             "ema_20", "stoch", "atr"])
        self._stop = threading.Event()

    def stop(self) -> None:
        self._stop.set()

    def run(self) -> None:
        while not self._stop.is_set():
            for ativo in self.estado.get("config.ativos") or []:
                if not self.estado.get(f"percepcao.{ativo}.novo_dado", False):
                    continue
                df = self.estado.get(f"percepcao.{ativo}.df")
                if df is None or df.empty:
                    continue
                try:
                    feats = compute_indicators(df, self.indicadores)
                    feats["retorno"] = feats["close"].pct_change() if "close" in feats.columns else 0.0
                    feats["volatilidade"] = feats["retorno"].rolling(20).std() if "retorno" in feats.columns else 0.0
                    if "SMA_50" in feats.columns:
                        feats["mm_dist_50"] = (feats["close"] - feats["SMA_50"]) / feats["SMA_50"]
                    if "SMA_200" in feats.columns or "SMA_50" in feats.columns:
                        long = feats["SMA_200"] if "SMA_200" in feats.columns else feats["SMA_50"]
                        feats["mm_dist_long"] = (feats["close"] - long) / long
                    self.estado.set(f"analitico.{ativo}.features", feats)
                    self.estado.set(f"analitico.{ativo}.processado", True)
                    self.estado.set(f"percepcao.{ativo}.novo_dado", False)
                except Exception as exc:  # pragma: no cover
                    logger.warning(f"[analítico] {ativo}: {exc}")
            self._stop.wait(0.5)


# ----------------------------------------------------------------------------
# Preditivo
# ----------------------------------------------------------------------------
class NeuronioPreditivo:
    """Ensemble de RF + LSTM com pesos dinâmicos."""

    def __init__(self, estado: EstadoGlobal, config_modelos: Dict[str, Any], ensemble, feature_cols) -> None:
        self.estado = estado
        self.config_modelos = config_modelos or {}
        self.ensemble = ensemble
        self.feature_cols = list(feature_cols)
        self.modelos: Dict[str, Dict[str, Any]] = {}

    def _modelos_para(self, ativo: str) -> Dict[str, Any]:
        if ativo not in self.modelos:
            from ..models.random_forest import RandomForestModel
            from ..models.lstm import LSTM_AVAILABLE, LSTMModel
            rf_cfg = self.config_modelos.get("rf", {})
            lstm_cfg = self.config_modelos.get("lstm", {})
            self.modelos[ativo] = {
                "rf": RandomForestModel(
                    n_estimators=int(rf_cfg.get("n_estimadores", 200)),
                    max_depth=int(rf_cfg.get("max_depth", 8)),
                ),
                "lstm": LSTMModel(
                    sequence_length=int(lstm_cfg.get("sequence_length", 60)),
                    epochs=int(lstm_cfg.get("camadas", 1)) * int(lstm_cfg.get("epocas", 10)),
                ) if LSTM_AVAILABLE else None,
            }
        return self.modelos[ativo]

    def treinar(self, ativo: str, df: pd.DataFrame) -> None:
        modelos = self._modelos_para(ativo)
        modelos["rf"].fit(df, self.feature_cols)
        if modelos["lstm"] is not None:
            modelos["lstm"].fit(df, self.feature_cols)
        self.estado.set(f"preditivo.{ativo}.treinado", True)
        logger.info(f"[preditivo] modelos treinados para {ativo}")

    def prever(self, ativo: str) -> Dict[str, Any]:
        df = self.estado.get(f"analitico.{ativo}.features")
        if df is None or len(df) < 30:
            return {"direcao": 0, "prob": 0.5, "conf": 0.0, "per_model": {}}
        # usa ensemble que combina TODOS os modelos já treinados para este símbolo
        pred = self.ensemble.predict(df, self.feature_cols)
        if pred is None:
            return {"direcao": 0, "prob": 0.5, "conf": 0.0, "per_model": {}}
        direcao = 1 if pred.prob_up > 0.5 else -1
        out = {
            "direcao": direcao,
            "prob": float(pred.prob_up),
            "conf": float(min(1.0, abs(pred.prob_up - 0.5) * 2)),
            "per_model": (pred.extra or {}).get("per_model", {}),
        }
        self.estado.set(f"preditivo.{ativo}.previsao", (out["direcao"], out["prob"]))
        self.estado.set(f"preditivo.{ativo}.confianca", out["conf"])
        return out


# ----------------------------------------------------------------------------
# Estrategista
# ----------------------------------------------------------------------------
class NeuronioEstrategista:
    def __init__(self, estado: EstadoGlobal, regras: Optional[List[RegraBase]] = None) -> None:
        self.estado = estado
        from .regras import RegraCruzamentoMM, RegraRSIMACD, RegraBollingerReversao
        nomes_cfg = set((estado.get("config.regras") or
                         ["cruzamento_sma", "rsi_macd", "bollinger_reversao"]))
        pool = {
            "cruzamento_sma": RegraCruzamentoMM(),
            "rsi_macd": RegraRSIMACD(),
            "bollinger_reversao": RegraBollingerReversao(),
        }
        self.regras = regras or [pool[n] for n in nomes_cfg if n in pool]

    def decidir(self, ativo: str) -> Dict[str, Any]:
        df = self.estado.get(f"analitico.{ativo}.features")
        if df is None or df.empty:
            return {"sinal": 0, "confianca": 0.0, "detalhes": {}}

        votos = []
        detalhes: Dict[str, Any] = {}
        for regra in self.regras:
            sinal, conf = regra.avaliar(df)
            peso = float(self.estado.get(f"memoria.{ativo}.peso_regra_{regra.nome}", 1.0))
            votos.append((sinal * conf, peso))
            detalhes[regra.nome] = {"sinal": sinal, "conf": conf, "peso": peso}

        from .regras import agregar_votos
        sinal_tecnico, conf_tecnico = agregar_votos(votos)

        pred_ml = self.estado.get(f"preditivo.{ativo}.previsao") or (0, 0.5)
        ml_dir, ml_prob = float(pred_ml[0]), float(pred_ml[1])
        ml_conf = self.estado.get(f"preditivo.{ativo}.confianca", 0.0) or 0.0

        # pesos adaptativos (60% técnico, 40% ML por padrão)
        w_tecnico = float(self.estado.get(f"memoria.{ativo}.w_tecnico", 0.6))
        w_ml = 1.0 - w_tecnico
        sinal_final = w_tecnico * sinal_tecnico + w_ml * ml_dir * ml_conf
        confianca = w_tecnico * conf_tecnico + w_ml * ml_conf

        if abs(sinal_final) < 0.3:
            sinal_final = 0.0

        self.estado.set(f"estrategista.{ativo}.sinal", int(np.sign(sinal_final)))
        self.estado.set(f"estrategista.{ativo}.confianca", float(confianca))
        self.estado.set(f"estrategista.{ativo}.detalhes", detalhes)
        return {"sinal": int(np.sign(sinal_final)), "confianca": float(confianca), "detalhes": detalhes}

    def otimizar_pesos(self, ativo: str) -> None:
        """Ajusta `w_tecnico` em direção ao componente que tem melhor Sharpe recente."""
        sharpe_tecnico = self.estado.get(f"memoria.{ativo}.sharpe_tecnico", 0.0) or 0.0
        sharpe_ml = self.estado.get(f"memoria.{ativo}.sharpe_ml", 0.0) or 0.0
        w = 0.5 + 0.5 * np.tanh((sharpe_tecnico - sharpe_ml) / 2.0)  # em (0,1)
        self.estado.set(f"memoria.{ativo}.w_tecnico", float(w))
        logger.debug(f"[estrategista] {ativo}: w_tecnico={w:.2f}")


# ----------------------------------------------------------------------------
# Executor
# ----------------------------------------------------------------------------
class NeuronioExecutor:
    def __init__(self, estado: EstadoGlobal, config_risco: Dict[str, Any]) -> None:
        self.estado = estado
        self.risco_por_trade = float((config_risco or {}).get("risco_por_trade", 0.02))
        self.capital = float((config_risco or {}).get("capital_inicial", 100_000))
        self.perfil = (config_risco or {}).get("perfil", "moderado")

    def executar(self, ativo: str) -> Optional[OrdemSimulada]:
        sinal = int(self.estado.get(f"estrategista.{ativo}.sinal", 0) or 0)
        conf = float(self.estado.get(f"estrategista.{ativo}.confianca", 0.0) or 0.0)
        if sinal == 0:
            return None
        df = self.estado.get(f"analitico.{ativo}.features")
        if df is None or df.empty:
            return None
        preco_atual = float(df["close"].iloc[-1])
        atr = float(df["ATRr_14"].iloc[-1]) if "ATRr_14" in df.columns else preco_atual * 0.01

        risco_dinheiro = self.capital * self.risco_por_trade
        tamanho = risco_dinheiro / max(atr * 2.0, 1e-8)
        if self.perfil == "conservador":
            tamanho *= 0.5
        elif self.perfil == "agressivo":
            tamanho *= 1.5
        if sinal == 1:
            stop_loss = preco_atual - 2 * atr
            take_profit = preco_atual + 3 * atr
        else:
            stop_loss = preco_atual + 2 * atr
            take_profit = preco_atual - 3 * atr

        # escala por confiança
        tamanho *= max(0.25, min(1.5, conf))

        ordem = OrdemSimulada(
            ativo=ativo, sinal=sinal, tamanho=float(tamanho),
            preco_entrada=preco_atual, stop_loss=stop_loss,
            take_profit=take_profit, aberta_em=time.time(),
            risco=risco_dinheiro, confianca=conf, sinal_origem="regra+ml",
        )
        self.estado.set(f"executor.{ativo}.ordem", ordem)
        self.estado.set(f"memoria.{ativo}.nova_ordem", ordem)
        return ordem
