from pydantic import BaseModel


class DACCompareSide(BaseModel):
    jurisdiction: str
    warning_to_policy_lag_days: int | None
    declared_vs_funded_gap: float | None


class DACCompareResponse(BaseModel):
    left: DACCompareSide
    right: DACCompareSide
