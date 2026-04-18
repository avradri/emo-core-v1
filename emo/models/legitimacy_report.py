from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LegitimacyFlag:
    category: str
    level: str
    message: str


@dataclass
class LegitimacyReport:
    summary: str
    flags: list[LegitimacyFlag] = field(default_factory=list)
