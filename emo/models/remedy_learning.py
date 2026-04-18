from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RemedyLearningReport:
    portfolio_id: str
    expected_dac_gain: float
    observed_dac_gain: float
    learning_gap: float
    persistence_gap: float
    adjustment_signal: str
    notes: list[str] = field(default_factory=list)
