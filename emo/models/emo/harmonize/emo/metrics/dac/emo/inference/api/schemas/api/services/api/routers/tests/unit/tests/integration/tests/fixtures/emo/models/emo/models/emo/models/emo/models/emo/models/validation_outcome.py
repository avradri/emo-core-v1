from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationOutcome:
    id: str
    jurisdiction: str
    domain: str
    measured_at: str
    outcome_metric: str
    baseline: Optional[float] = None
    observed_value: Optional[float] = None
    counterfactual_method: Optional[str] = None
    confidence: Optional[float] = None
    notes: Optional[str] = None
