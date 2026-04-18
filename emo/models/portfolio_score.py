from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PortfolioScore:
    portfolio_id: str
    feasibility: float
    expected_dac_gain: float
    persistence_likelihood: float
    contradiction_risk: float
    semantic_efficiency: float
    justice_risk: float
    legitimacy_penalty: float
    overall_score: float
    notes: list[str] = field(default_factory=list)
