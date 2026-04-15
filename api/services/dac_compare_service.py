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

    return DACCompareResponse(
        left=DACCompareSide(**metrics["left"]),
        right=DACCompareSide(**metrics["right"]),
    )
