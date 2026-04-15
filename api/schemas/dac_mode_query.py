from pydantic import BaseModel


class DACModeQuery(BaseModel):
    domain: str | None = None
    jurisdiction: str | None = None
