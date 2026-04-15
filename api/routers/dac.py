from fastapi import APIRouter

from api.schemas.dac import DACDomainsResponse

router = APIRouter(prefix="/dac", tags=["dac"])


@router.get("/domains", response_model=DACDomainsResponse)
def get_dac_domains():
    return {
        "domains": [
            "disaster",
            "pandemic",
        ]
    }
