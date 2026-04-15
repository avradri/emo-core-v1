from api.schemas.dac_snapshot import DACSnapshotResponse
from api.services.dac_metrics_service import get_dac_metrics_summary
from api.services.dac_mode_service import get_current_dac_mode
from emo.reporting.snapshots import build_dac_snapshot


def get_dac_snapshot() -> DACSnapshotResponse:
    metrics_summary = get_dac_metrics_summary()
    mode_response = get_current_dac_mode()

    snapshot = build_dac_snapshot(
        domain="disaster",
        jurisdiction="RO",
        metrics={
            "warning_to_policy_lag_days": metrics_summary.warning_to_policy_lag_days,
            "warning_to_delivery_lag_days": metrics_summary.warning_to_delivery_lag_days,
            "alert_to_policy_conversion_rate": metrics_summary.alert_to_policy_conversion_rate,
            "implementation_persistence_30d": metrics_summary.implementation_persistence_30d,
            "declared_vs_funded_gap": metrics_summary.declared_vs_funded_gap,
        },
        mode=mode_response.mode,
    )

    return DACSnapshotResponse(**snapshot)
