# api/__init__.py
from __future__ import annotations

# This package contains the FastAPI service for EMO-Core.
#
# The main entry point is `api.main:app`, which can be served via:
#
#     uvicorn api.main:app --reload
#
# Routers live under `api/routers/`.

__all__ = ["main"]
