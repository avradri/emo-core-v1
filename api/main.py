# api/main.py
from __future__ import annotations

import emo
from fastapi import FastAPI

from api.routers import metrics, uia

DESCRIPTION = """
EMO-Core API

This service exposes a thin HTTP layer over the EMO metric engine and
UIA aggregation. It is intended as a reference implementation for labs,
digital-twin teams, and funders who want to integrate EMO metrics into
their own infrastructure.
"""

app = FastAPI(
    title="EMO-Core API",
    version=getattr(emo, "__version__", "0.1.0"),
    description=DESCRIPTION,
)

# Routers ----------------------------------------------------------------

app.include_router(metrics.router)
app.include_router(uia.router)


# Health & meta ----------------------------------------------------------

@app.get("/health", tags=["meta"])
async def health() -> dict:
    """
    Basic health check for load balancers and smoke tests.
    """
    return {"status": "ok"}


@app.get("/version", tags=["meta"])
async def version() -> dict:
    """
    Return the EMO-Core library version as seen by this service.
    """
    return {"version": getattr(emo, "__version__", "0.1.0")}
