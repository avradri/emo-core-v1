from dataclasses import dataclass
from typing import Optional


@dataclass
class BudgetCommitment:
    id: str
    jurisdiction: str
    program: str
    amount: float
    currency: str
    allocated_at: str
    execution_window_start: Optional[str] = None
    execution_window_end: Optional[str] = None
    funder: Optional[str] = None
    diagnostic_link: Optional[str] = None
    instrument_link: Optional[str] = None
