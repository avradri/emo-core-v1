from api.schemas.dac import DACDomainsResponse


def get_supported_dac_domains() -> DACDomainsResponse:
    return DACDomainsResponse(
        domains=[
            "disaster",
            "pandemic",
        ]
    )
