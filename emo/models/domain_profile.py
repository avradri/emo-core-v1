from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DomainProfile:
    domain: str
    diagnostic_types: list[str] = field(default_factory=list)
    policy_types: list[str] = field(default_factory=list)
    budget_types: list[str] = field(default_factory=list)
    delivery_types: list[str] = field(default_factory=list)
    validation_metrics: list[str] = field(default_factory=list)
    weighting_scheme: dict[str, float] = field(default_factory=dict)
    lag_targets: dict[str, float] = field(default_factory=dict)
    coverage_rules: list[str] = field(default_factory=list)
    contradiction_rules: list[str] = field(default_factory=list)
