from api.schemas.dac_metrics import DACMetricsSummaryResponse
from api.services.dac_shared_metrics_service import get_romania_disaster_demo_metrics


def get_dac_metrics_summary() -> DACMetricsSummaryResponse:
    metrics = get_romania_disaster_demo_metrics()

    return DACMetricsSummaryResponse(**metrics)
