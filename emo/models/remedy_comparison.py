from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RemedyComparisonItem:
    portfolio_label: str
    sequence: list[str] = field(default_factory=list)
    overall_score: float = 0.0
    feasibility: float = 0.0
    expected_dac_gain: float = 0.0
    persistence_likelihood: float = 0.0
    contradiction_risk: float = 0.0
    justice_risk: float = 0.0
    semantic_efficiency: float = 0.0


@dataclass
class RemedyComparisonReport:
    summary: str
    comparisons: list[RemedyComparisonItem] = field(default_factory=list)
