from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class BottleneckProfile:
    domain: str
    jurisdiction: str
    validation_score: float
    translation_score: float
    budget_score: float
    deployment_score: float
    persistence_score: float
    contradiction_score: float
    dominant_bottlenecks: list[str] = field(default_factory=list)
    confidence: float = 0.0
