from api.schemas.dac_mode import DACModeResponse
from api.services.dac_shared_metrics_service import get_romania_disaster_demo_metrics
from emo.inference.behavioral_modes import infer_behavioral_mode


def get_current_dac_mode(
    domain: str | None = None,
    jurisdiction: str | None = None,
) -> DACModeResponse:
    if domain not in (None, "disaster"):
        return DACModeResponse(mode="selective_stabilization")

    if jurisdiction not in (None, "RO"):
        return DACModeResponse(mode="selective_stabilization")

    metrics = get_romania_disaster_demo_metrics()

    mode = infer_behavioral_mode(metrics)
    return DACModeResponse(mode=mode)
