from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class InterventionOption:
    option_id: str
    family: str
    name: str
    description: str
    target_bottlenecks: list[str] = field(default_factory=list)
    required_capacity: str = "medium"
    time_to_effect: str = "medium"
    evidence_level: str = "conceptual"
    rights_risk: str = "low"
    coordination_cost: str = "medium"
    domains: list[str] = field(default_factory=list)
