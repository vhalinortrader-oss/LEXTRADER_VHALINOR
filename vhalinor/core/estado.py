"""EstadoGlobal — barramento thread-safe para troca de informação entre neurônios."""
from __future__ import annotations

import threading
from typing import Any, Optional


class EstadoGlobal:
    """Dicionário compartilhado protegido por `RLock`.

    Suporta chaves com ponto (`percepcao.BTC-USD.novo_dado`) e fallback
    a partir de `config.<chave>` para evitar `KeyError` em leituras.
    """

    def __init__(self) -> None:
        self.dados: dict[str, Any] = {}
        self.config: dict[str, Any] = {}
        self.lock = threading.RLock()

    # ----- API básica -----
    def set(self, chave: str, valor: Any) -> None:
        with self.lock:
            self.dados[chave] = valor

    def get(self, chave: str, default: Any = None) -> Any:
        with self.lock:
            if chave in self.dados:
                return self.dados[chave]
        # fallback opcional: lê de `config.<chave>`
        if chave.startswith("config."):
            with self.lock:
                return self.config.get(chave[len("config."):], default)
        return default

    def has(self, chave: str) -> bool:
        with self.lock:
            return chave in self.dados

    def clear_prefix(self, prefixo: str) -> None:
        with self.lock:
            for k in list(self.dados.keys()):
                if k.startswith(prefixo):
                    del self.dados[k]

    # ----- helpers semânticos -----
    def registrar_config(self, config: dict[str, Any]) -> None:
        with self.lock:
            self.config.update(config or {})

    def snapshot(self) -> dict[str, Any]:
        with self.lock:
            return dict(self.dados)
