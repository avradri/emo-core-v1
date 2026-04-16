from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BudgetCommitment:
    id: str
    jurisdiction: str
    program: str
    amount: float
    currency: str
    allocated_at: str
    execution_window_start: str | None = None
    execution_window_end: str | None = None
    funder: str | None = None
    diagnostic_link: str | None = None
    instrument_link: str | None = None
