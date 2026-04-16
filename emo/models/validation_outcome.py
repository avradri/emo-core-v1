from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ValidationOutcome:
    id: str
    jurisdiction: str
    domain: str
    measured_at: str
    outcome_metric: str
    baseline: float | None = None
    observed_value: float | None = None
    counterfactual_method: str | None = None
    confidence: float | None = None
    notes: str | None = None
