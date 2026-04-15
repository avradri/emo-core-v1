from api.services.dac_demo_flow_service import get_romania_disaster_demo_flow
from emo.metrics.dac.contradiction import declared_vs_funded_gap
from emo.metrics.dac.lag import (
    warning_to_delivery_lag_days,
    warning_to_policy_lag_days,
)
from emo.metrics.dac.persistence import implementation_persistence_30d


def get_romania_disaster_demo_metrics() -> dict[str, float | int | None]:
    flow = get_romania_disaster_demo_flow()

    diagnostic = flow["diagnostic"]
    policy = flow["policy"]
    delivery = flow["delivery"]

    return {
        "warning_to_policy_lag_days": warning_to_policy_lag_days(diagnostic, policy),
        "warning_to_delivery_lag_days": warning_to_delivery_lag_days(diagnostic, delivery),
        "alert_to_policy_conversion_rate": 1.0,
        "implementation_persistence_30d": implementation_persistence_30d(1, 1),
        "declared_vs_funded_gap": declared_vs_funded_gap(1, 1),
    }
