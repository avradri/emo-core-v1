from pydantic import BaseModel


class DACCompareQuery(BaseModel):
    domain: str | None = None
    left: str | None = None
    right: str | None = None
