from pydantic import BaseModel


class DACDomainsResponse(BaseModel):
    domains: list[str]
