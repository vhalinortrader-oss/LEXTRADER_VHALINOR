from __future__ import annotations

import os
from typing import Any, Dict, List, Optional




from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

try:
    from pydantic import BaseModel  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    class BaseModel:  # type: ignore
        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)


from lextrader.api.decision_service import (
    decision_service,
    DecisionAlgorithmDTO,
    DecisionFlowNodeDTO,
    MarketDecisionDTO,
    RunDecisionResponse,
    ToggleAlgorithmResponse,
    DecisionStateResponse,
)

app = FastAPI(title="LEXTRADER Decision API", version="1.0")





# Allow local dev (Next/React). Adjust if needed.

origins = os.getenv("LEXTRADER_CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/decision/state", response_model=DecisionStateResponse)
def get_state() -> DecisionStateResponse:
    return decision_service.get_state()


@app.post("/api/decision/run", response_model=RunDecisionResponse)
def run_decision() -> RunDecisionResponse:
    return decision_service.run()


class TogglePayload(BaseModel):
    algorithm_id: str


@app.post("/api/decision/toggle", response_model=ToggleAlgorithmResponse)
def toggle_algorithm(payload: TogglePayload) -> ToggleAlgorithmResponse:
    return decision_service.toggle(payload.algorithm_id)

