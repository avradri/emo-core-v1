from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PolicyInstrument:
    id: str
    instrument_type: str
    jurisdiction: str
    announced_at: str
    effective_at: str | None = None
    expires_at: str | None = None
    target_link: str | None = None
    diagnostic_link: str | None = None
    strength_score: float | None = None
    binding_score: float | None = None
    budget_linked: bool | None = None
