from api.schemas.dac_metrics import DACMetricsSummaryResponse


def get_dac_metrics_summary() -> DACMetricsSummaryResponse:
    return DACMetricsSummaryResponse(
        warning_to_policy_lag_days=3,
        warning_to_delivery_lag_days=5,
        alert_to_policy_conversion_rate=0.4,
        implementation_persistence_30d=0.7,
        declared_vs_funded_gap=0.2,
    )
