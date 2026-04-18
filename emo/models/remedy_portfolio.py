from __future__ import annotations

from dataclasses import dataclass, field

from emo.models.intervention_option import InterventionOption


@dataclass
class RemedyPortfolio:
    portfolio_id: str
    domain: str
    jurisdiction: str
    options: list[InterventionOption] = field(default_factory=list)
    sequence: list[str] = field(default_factory=list)
    rationale: str = ""
    assumptions: list[str] = field(default_factory=list)
