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


class RemedyExplainResponse(BaseModel):
    explanation: str
    profile: dict
    portfolio: dict
    score: dict


class RemedySimulationResponse(BaseModel):
    profile: dict
    portfolio: dict
    score: dict
    simulations: list[dict]


class RemedyTradeoffResponse(BaseModel):
    profile: dict
    portfolio: dict
    score: dict
    tradeoff_report: dict


class RemedyLegitimacyResponse(BaseModel):
    profile: dict
    portfolio: dict
    legitimacy_report: dict
