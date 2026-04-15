from dataclasses import dataclass
from typing import Optional


@dataclass
class DiagnosticEvent:
    id: str
    domain: str
    hazard_type: str
    source: str
    issued_at: str
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    severity: Optional[float] = None
    confidence: Optional[float] = None
    geo_scope: Optional[str] = None
    actor_scope: Optional[str] = None
    diagnostic_class: Optional[str] = None
    evidence_url: Optional[str] = None
    validation_status: Optional[str] = None
