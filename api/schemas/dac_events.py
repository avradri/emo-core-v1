from pydantic import BaseModel


class DACEventRecord(BaseModel):
    id: str
    kind: str
    domain: str
    jurisdiction: str
    timestamp: str


class DACEventsResponse(BaseModel):
    events: list[DACEventRecord]
