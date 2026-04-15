from dataclasses import dataclass
from typing import Optional


@dataclass
class PolicyInstrument:
    id: str
    instrument_type: str
    jurisdiction: str
    announced_at: str
    effective_at: Optional[str] = None
    expires_at: Optional[str] = None
    target_link: Optional[str] = None
    diagnostic_link: Optional[str] = None
    strength_score: Optional[float] = None
    binding_score: Optional[float] = None
    budget_linked: Optional[bool] = None
