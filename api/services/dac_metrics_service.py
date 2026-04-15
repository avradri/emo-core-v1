from api.schemas.dac_metrics import DACMetricsSummaryResponse
from api.services.dac_shared_metrics_service import get_romania_disaster_demo_metrics


def get_dac_metrics_summary(
    domain: str | None = None,
    jurisdiction: str | None = None,
) -> DACMetricsSummaryResponse:
    if domain not in (None, "disaster"):
        return DACMetricsSummaryResponse(
            warning_to_policy_lag_days=None,
            warning_to_delivery_lag_days=None,
            alert_to_policy_conversion_rate=None,
            implementation_persistence_30d=None,
            declared_vs_funded_gap=None,
        )

    if jurisdiction not in (None, "RO"):
        return DACMetricsSummaryResponse(
            warning_to_policy_lag_days=None,
            warning_to_delivery_lag_days=None,
            alert_to_policy_conversion_rate=None,
            implementation_persistence_30d=None,
            declared_vs_funded_gap=None,
        )

    metrics = get_romania_disaster_demo_metrics()
    return DACMetricsSummaryResponse(**metrics)
