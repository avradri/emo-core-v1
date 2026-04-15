from api.services.dac_compare_demo_flow_service import get_disaster_compare_demo_flows
from emo.metrics.dac.contradiction import declared_vs_funded_gap
from emo.metrics.dac.lag import warning_to_policy_lag_days


def get_disaster_compare_demo_metrics() -> dict[str, dict[str, float | int | None | str]]:
    flows = get_disaster_compare_demo_flows()

    left = flows["left"]
    right = flows["right"]

    return {
        "left": {
            "jurisdiction": left["policy"].jurisdiction,
            "warning_to_policy_lag_days": warning_to_policy_lag_days(
                left["diagnostic"],
                left["policy"],
            ),
            "declared_vs_funded_gap": declared_vs_funded_gap(1, 1),
        },
        "right": {
            "jurisdiction": right["policy"].jurisdiction,
            "warning_to_policy_lag_days": warning_to_policy_lag_days(
                right["diagnostic"],
                right["policy"],
            ),
            "declared_vs_funded_gap": declared_vs_funded_gap(1, 1),
        },
    }
