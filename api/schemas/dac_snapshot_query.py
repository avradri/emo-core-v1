from pydantic import BaseModel


class DACSnapshotQuery(BaseModel):
    domain: str | None = None
    jurisdiction: str | None = None
