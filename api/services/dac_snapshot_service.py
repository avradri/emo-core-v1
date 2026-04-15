from api.schemas.dac_snapshot import DACSnapshotResponse
from api.services.dac_mode_service import get_current_dac_mode
from api.services.dac_shared_metrics_service import get_romania_disaster_demo_metrics
from emo.reporting.snapshots import build_dac_snapshot


def get_dac_snapshot() -> DACSnapshotResponse:
    metrics = get_romania_disaster_demo_metrics()
    mode_response = get_current_dac_mode()

    snapshot = build_dac_snapshot(
        domain="disaster",
        jurisdiction="RO",
        metrics=metrics,
        mode=mode_response.mode,
    )

    return DACSnapshotResponse(**snapshot)
