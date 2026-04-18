from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RemedyTradeoff:
    dimension: str
    value: float
    interpretation: str


@dataclass
class RemedyTradeoffReport:
    summary: str
    tradeoffs: list[RemedyTradeoff] = field(default_factory=list)
