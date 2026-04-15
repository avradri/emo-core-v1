from __future__ import annotations

import emo
from fastapi import FastAPI

from api.routers import dac, metrics, uia

DESCRIPTION = """
EMO-Core API

This service exposes a thin HTTP layer over the EMO metric engine and UIA
aggregation. It is intended as a reference implementation for labs,
digital-twin teams, and funders who want to integrate EMO metrics into their
own infrastructure.
"""

app = FastAPI(
    title="EMO-Core API",
    version=getattr(emo, "__version__", "0.1.0"),
    description=DESCRIPTION,
)

app.include_router(metrics.router)
app.include_router(uia.router)
app.include_router(dac.router)


@app.get("/health", tags=["meta"])
async def health() -> dict:
    return {"status": "ok"}


@app.get("/version", tags=["meta"])
async def version() -> dict:
    return {"version": getattr(emo, "__version__", "0.1.0")}
