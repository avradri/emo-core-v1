from fastapi import APIRouter

router = APIRouter(prefix="/dac", tags=["dac"])


@router.get("/domains")
def get_dac_domains():
    return {
        "domains": [
            "disaster",
            "pandemic",
        ]
    }
