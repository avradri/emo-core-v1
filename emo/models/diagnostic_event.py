from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DiagnosticEvent:
    id: str
    domain: str
    hazard_type: str
    source: str
    issued_at: str
    valid_from: str | None = None
    valid_to: str | None = None
    severity: float | None = None
    confidence: float | None = None
    geo_scope: str | None = None
    actor_scope: str | None = None
    diagnostic_class: str | None = None
    evidence_url: str | None = None
    validation_status: str | None = None
