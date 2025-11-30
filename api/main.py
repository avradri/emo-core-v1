from __future__ import annotations

from fastapi import FastAPI

from emo.config import get_settings
from .routers import metrics, uia, interfaces


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Emergent Mind Observatory – EMO-Core v1.0",
        version="0.1.0",
        description=(
            "Core metric engine and UIA layer for EMO, exposing species-mind "
            "metrics and UIA summaries via HTTP."
        ),
    )

    app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
    app.include_router(uia.router, prefix="/uia", tags=["uia"])
    app.include_router(interfaces.router, prefix="/interfaces", tags=["interfaces"])

    @app.get("/health", tags=["system"])
    async def health() -> dict:
        return {"status": "ok", "env": settings.env}

    return app


app = create_app()
