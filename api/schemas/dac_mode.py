from pydantic import BaseModel


class DACModeResponse(BaseModel):
    mode: str
