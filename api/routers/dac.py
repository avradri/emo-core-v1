from fastapi import APIRouter

from api.schemas.dac import DACDomainsResponse
from api.schemas.dac_mode import DACModeResponse
from api.services.dac_mode_service import get_current_dac_mode
from api.services.dac_service import get_supported_dac_domains

router = APIRouter(prefix="/dac", tags=["dac"])


@router.get("/domains", response_model=DACDomainsResponse)
def get_dac_domains():
    return get_supported_dac_domains()


@router.get("/modes/current", response_model=DACModeResponse)
def get_current_mode():
    demo_metrics = {
        "warning_to_policy_lag_days": 3,
        "implementation_persistence_30d": 0.8,
        "declared_vs_funded_gap": 0.1,
    }
    return get_current_dac_mode(demo_metrics)
