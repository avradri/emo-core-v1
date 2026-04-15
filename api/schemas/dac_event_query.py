from pydantic import BaseModel


class DACEventQuery(BaseModel):
    domain: str | None = None
    jurisdiction: str | None = None
