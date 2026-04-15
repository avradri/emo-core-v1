from pydantic import BaseModel


class DACMetricsSummaryResponse(BaseModel):
    warning_to_policy_lag_days: int | None
    warning_to_delivery_lag_days: int | None
    alert_to_policy_conversion_rate: float | None
    implementation_persistence_30d: float | None
    declared_vs_funded_gap: float | None
