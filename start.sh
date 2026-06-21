#!/usr/bin/env bash
# LEXTRADER VHALINOR — Inicialização do backend real
set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  LEXTRADER VHALINOR 5.0 — Backend IA Real"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Cria ambiente virtual (opcional)
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Ambiente virtual criado"
fi

source venv/bin/activate

# 2. Instala dependências
pip install -q -r requirements.txt
echo "✓ Dependências instaladas"

# 3. Inicializa banco de dados
python3 -c "from db.database import init_db; init_db(); print('✓ Banco de dados inicializado')"

# 4. Sobe API
echo ""
echo "▶ Iniciando API em http://localhost:8000"
echo "  Documentação: http://localhost:8000/docs"
echo ""
uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload
