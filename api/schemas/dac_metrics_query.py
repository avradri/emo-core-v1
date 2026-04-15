from pydantic import BaseModel


class DACMetricsQuery(BaseModel):
    domain: str | None = None
    jurisdiction: str | None = None
