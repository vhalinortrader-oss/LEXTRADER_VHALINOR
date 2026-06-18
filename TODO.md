# TODO

- [ ] Migração para estrutura `lextrader/`

## Status
- [x] Criar pasta `lextrader/` e subpastas base (`engine/`, `decision/`, `dashboard/tk/`, `dashboard/streamlit/`)
- [x] Criar wrapper `lextrader/engine/inteligencia_artificial_central.py` (reexporta `Inteligencia_artificial_central.py`)
- [x] Criar wrapper `lextrader/decision/decision_engine.py` (reexporta `DecisionEngine.py`)
- [x] Criar wrapper `lextrader/dashboard/streamlit/automation_dashboard.py` (reexporta `AutomationDashboard.py`)
- [x] Criar camada `lextrader/dashboard/tk/decision_dashboard.py` (import do DecisionEngine)
- [ ] Mapear/migrar módulos do projeto raiz para `lextrader/` (demais arquivos)
- [ ] Atualizar `README.md` e instruções de execução
- [ ] Validar execução final (ex.: `python -m lextrader.main --mode core`)

