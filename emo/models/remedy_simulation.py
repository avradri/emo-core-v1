from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RemedySimulationResult:
    scenario: str
    expected_dac_improvement: float
    persistence_outlook: float
    contradiction_warning: str
    narrative: str
    assumptions: list[str] = field(default_factory=list)
