# TODO - Integração Python (.py) <-> React/TSX (.tsx)

## Etapa 1 — Inspeção do Frontend
- [ ] Ler `src/calendar.tsx` para identificar componentes, estado atual e pontos de interação

## Etapa 2 — Inspeção do Backend
- [ ] Revisar `DecisionEngine.py` para extrair lógica de estado (algorithms/flow/decisions) sem depender de Tkinter

## Etapa 3 — Criar Serviço Headless
- [ ] Criar `lextrader/api/decision_service.py` com um “service” que mantém estado e executa `run`/`toggle`

## Etapa 4 — Criar API FastAPI
- [ ] Criar `lextrader/api/server.py` com endpoints:
  - [ ] `GET /api/decision/state`
  - [ ] `POST /api/decision/run`
  - [ ] `POST /api/decision/toggle`

## Etapa 5 — Integrar `calendar.tsx` com a API
- [ ] Ajustar `src/calendar.tsx` para chamar a API e renderizar:
  - [ ] lista/toggle de algoritmos
  - [ ] timeline do `decision_flow`
  - [ ] cards de `recent_decisions`

## Etapa 6 — Execução e Testes
- [ ] Garantir dependências no `requirements.txt`
- [ ] Subir backend e rodar frontend
- [ ] Validar fluxo completo: abrir UI → run → timeline atualiza

