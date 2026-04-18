from __future__ import annotations

from pydantic import BaseModel


class RemedyRequest(BaseModel):
    domain: str
    jurisdiction: str
    validation_score: float | None = None
    translation_score: float | None = None
    budget_score: float | None = None
    deployment_score: float | None = None
    persistence_score: float | None = None
    contradiction_score: float | None = None


class RemedyLearningRequest(RemedyRequest):
    observed_dac_gain: float
    observed_persistence: float
