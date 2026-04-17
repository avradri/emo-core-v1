from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DeliveryTrace:
    id: str
    delivery_type: str
    jurisdiction: str
    started_at: str
    completed_at: str | None = None
    coverage: float | None = None
    quantity: float | None = None
    implementing_actor: str | None = None
    diagnostic_link: str | None = None
    instrument_link: str | None = None
    budget_link: str | None = None
