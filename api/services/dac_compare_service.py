from api.schemas.dac_compare import DACCompareResponse, DACCompareSide
from api.services.dac_compare_shared_metrics_service import (
    get_disaster_compare_demo_metrics,
)


def get_dac_compare() -> DACCompareResponse:
    metrics = get_disaster_compare_demo_metrics()

    return DACCompareResponse(
        left=DACCompareSide(**metrics["left"]),
        right=DACCompareSide(**metrics["right"]),
    )
