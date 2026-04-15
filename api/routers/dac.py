from fastapi import APIRouter

from api.schemas.dac import DACDomainsResponse
from api.schemas.dac_compare import DACCompareResponse
from api.schemas.dac_events import DACEventsResponse
from api.schemas.dac_metrics import DACMetricsSummaryResponse
from api.schemas.dac_mode import DACModeResponse
from api.schemas.dac_snapshot import DACSnapshotResponse
from api.services.dac_compare_service import get_dac_compare
from api.services.dac_events_service import get_dac_events
from api.services.dac_metrics_service import get_dac_metrics_summary
from api.services.dac_mode_service import get_current_dac_mode
from api.services.dac_service import get_supported_dac_domains
from api.services.dac_snapshot_service import get_dac_snapshot

router = APIRouter(prefix="/dac", tags=["dac"])


@router.get("/domains", response_model=DACDomainsResponse)
def get_dac_domains():
    return get_supported_dac_domains()


@router.get("/events", response_model=DACEventsResponse)
def get_events():
    return get_dac_events()


@router.get("/compare
