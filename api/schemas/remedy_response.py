from __future__ import annotations

from pydantic import BaseModel


class RemedyBottleneckResponse(BaseModel):
    profile: dict


class RemedyOptionsResponse(BaseModel):
    profile: dict
    options: list[dict]


class RemedyPortfolioResponse(BaseModel):
    profile: dict
    portfolio: dict


class RemedyScoreResponse(BaseModel):
    profile: dict
    portfolio: dict
    score: dict


class RemedyLibraryResponse(BaseModel):
    library: dict[str, list[dict]]
