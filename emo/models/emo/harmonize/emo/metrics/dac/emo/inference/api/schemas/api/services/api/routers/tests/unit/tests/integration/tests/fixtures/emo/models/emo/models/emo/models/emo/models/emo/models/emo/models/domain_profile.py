from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class DomainProfile:
    domain: str
    diagnostic_types: List[str] = field(default_factory=list)
    policy_types: List[str] = field(default_factory=list)
    budget_types: List[str] = field(default_factory=list)
    delivery_types: List[str] = field(default_factory=list)
    validation_metrics: List[str] = field(default_factory=list)
    weighting_scheme: Dict[str, float] = field(default_factory=dict)
    lag_targets: Dict[str, float] = field(default_factory=dict)
    coverage_rules: List[str] = field(default_factory=list)
    contradiction_rules: List[str] = field(default_factory=list)
