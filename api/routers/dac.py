from fastapi import APIRouter

from api.schemas.dac import DACDomainsResponse
from api.services.dac_service import get_supported_dac_domains

router = APIRouter(prefix="/dac", tags=["dac"])


@router.get("/domains", response_model=DACDomainsResponse)
def get_dac_domains():
    return get_supported_dac_domains()
