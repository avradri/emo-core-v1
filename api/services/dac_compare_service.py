from api.schemas.dac_compare import DACCompareResponse, DACCompareSide
from api.services.dac_compare_shared_metrics_service import (
    get_disaster_compare_demo_metrics,
)


def get_dac_compare(
    domain: str | None = None,
    left: str | None = None,
    right: str | None = None,
) -> DACCompareResponse:
    if domain not in (None, "disaster"):
        return DACCompareResponse(
            left=DACCompareSide(
                jurisdiction=left or "UNKNOWN",
                warning_to_policy_lag_days=None,
                declared_vs_funded_gap=None,
            ),
            right=DACCompareSide(
                jurisdiction=right or "UNKNOWN",
                warning_to_policy_lag_days=None,
                declared_vs_funded_gap=None,
            ),
        )

    if left not in (None, "RO") or right not in (None, "BG"):
        return DACCompareResponse(
            left=DACCompareSide(
                jurisdiction=left or "UNKNOWN",
                warning_to_policy_lag_days=None,
                declared_vs_funded_gap=None,
            ),
            right=DACCompareSide(
                jurisdiction=right or "UNKNOWN",
                warning_to_policy_lag_days=None,
                declared_vs_funded_gap=None,
            ),
        )

    metrics = get_disaster_compare_demo_metrics()
    left_metrics = metrics["left"]
    right_metrics = metrics["right"]

    return DACCompareResponse(
        left=DACCompareSide(
            jurisdiction=str(left_metrics["jurisdiction"]),
            warning_to_policy_lag_days=(
                int(left_metrics["warning_to_policy_lag_days"])
                if left_metrics["warning_to_policy_lag_days"] is not None
                else None
            ),
            declared_vs_funded_gap=(
                float(left_metrics["declared_vs_funded_gap"])
                if left_metrics["declared_vs_funded_gap"] is not None
                else None
            ),
        ),
        right=DACCompareSide(
            jurisdiction=str(right_metrics["jurisdiction"]),
            warning_to_policy_lag_days=(
                int(right_metrics["warning_to_policy_lag_days"])
                if right_metrics["warning_to_policy_lag_days"] is not None
                else None
            ),
            declared_vs_funded_gap=(
                float(right_metrics["declared_vs_funded_gap"])
                if right_metrics["declared_vs_funded_gap"] is not None
                else None
            ),
        ),
    )
