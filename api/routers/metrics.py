# api/routers/metrics.py
from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel

from emo.services.metrics import MetricEngine

router = APIRouter(prefix="/metrics", tags=["metrics"])

_engine = MetricEngine()


class OrganismalityPayload(BaseModel):
    """
    Request payload for computing the Organismality Index (OI).

    treaties:
        List of records used to build a treaties DataFrame.
        Example schema (you can adapt this to your data):
        {
          "region": "EU",
          "treaty_count": 42,
          "year": 2020
        }

    conflicts:
        List of records used to build a conflicts DataFrame.
        Example schema:
        {
          "region": "EU",
          "conflict_deaths": 0,
          "year": 2020
        }
    """

    treaties: List[Dict[str, Any]]
    conflicts: List[Dict[str, Any]]


@router.get("/ping")
async def ping() -> Dict[str, str]:
    """
    Lightweight ping endpoint for quick connectivity checks.
    """
    return {"status": "ok"}


@router.post("/organismality")
async def compute_organismality(payload: OrganismalityPayload) -> Dict[str, Any]:
    """
    Compute the Organismality Index (OI) from treaty and conflict records.

    This is a reference endpoint meant for experimentation and integration
    testing. In production deployments you would typically plug this into
    your own treaty/conflict data sources.
    """
    treaties_df = pd.DataFrame(payload.treaties)
    conflicts_df = pd.DataFrame(payload.conflicts)

    result = _engine.organismality_from_frames(
        treaties_df=treaties_df,
        conflicts_df=conflicts_df,
    )
    # result is already JSON-friendly thanks to the service layer
    return result
