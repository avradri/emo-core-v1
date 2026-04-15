from api.schemas.dac_mode import DACModeResponse
from api.services.dac_metrics_service import get_dac_metrics_summary
from emo.inference.behavioral_modes import infer_behavioral_mode


def get_current_dac_mode() -> DACModeResponse:
    metrics_summary = get_dac_metrics_summary()

    metrics = {
        "warning_to_policy_lag_days": metrics_summary.warning_to_policy_lag_days or 0,
        "implementation_persistence_30d": metrics_summary.implementation_persistence_30d or 0.0,
        "declared_vs_funded_gap": metrics_summary.declared_vs_funded_gap or 0.0,
    }

    mode = infer_behavioral_mode
