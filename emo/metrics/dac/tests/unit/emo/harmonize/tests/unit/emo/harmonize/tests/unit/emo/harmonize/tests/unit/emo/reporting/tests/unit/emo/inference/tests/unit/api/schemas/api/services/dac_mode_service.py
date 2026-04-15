from api.schemas.dac_mode import DACModeResponse
from emo.inference.behavioral_modes import infer_behavioral_mode


def get_current_dac_mode(metrics: dict[str, float]) -> DACModeResponse:
    mode = infer_behavioral_mode(metrics)
    return DACModeResponse(mode=mode)
