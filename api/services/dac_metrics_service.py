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

    warning_to_policy_lag = metrics["warning_to_policy_lag_days"]
    warning_to_delivery_lag = metrics["warning_to_delivery_lag_days"]
    alert_to_policy_conversion = metrics["alert_to_policy_conversion_rate"]
    implementation_persistence = metrics["implementation_persistence_30d"]
    funded_gap = metrics["declared_vs_funded_gap"]

    return DACMetricsSummaryResponse(
        warning_to_policy_lag_days=(
            int(warning_to_policy_lag)
            if warning_to_policy_lag is not None
            else None
        ),
        warning_to_delivery_lag_days=(
            int(warning_to_delivery_lag)
            if warning_to_delivery_lag is not None
            else None
        ),
        alert_to_policy_conversion_rate=(
            float(alert_to_policy_conversion)
            if alert_to_policy_conversion is not None
            else None
        ),
        implementation_persistence_30d=(
            float(implementation_persistence)
            if implementation_persistence is not None
            else None
        ),
        declared_vs_funded_gap=(
            float(funded_gap)
            if funded_gap is not None
            else None
        ),
    )
