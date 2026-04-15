from pydantic import BaseModel


class DACSnapshotResponse(BaseModel):
    domain: str
    jurisdiction: str
    mode: str
    metrics: dict[str, float | int | None]
