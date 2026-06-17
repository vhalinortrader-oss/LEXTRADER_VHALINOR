"""decision_app.py

Este arquivo estava corrompido (continha bytes nulos) e não podia ser executado.
Ele é um entrypoint mínimo para manter compatibilidade com a migração para
`lextrader/`.

Execute:
  python decision_app.py
ou
  python -m lextrader.main
"""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--dry-run", action="store_true", help="não executa ordens")
    args = parser.parse_args()

    # Migração futura: aqui deve chamar o motor/estratégia.
    # Para smoke test, apenas confirma carregamento.
    print("decision_app entrypoint ok; dry-run=", args.dry_run)


if __name__ == "__main__":
    main()
