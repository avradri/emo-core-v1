from __future__ import annotations

from fastapi import APIRouter

from api.schemas.remedy_request import RemedyRequest
from api.schemas.remedy_response import (
    RemedyBottleneckResponse,
    RemedyLibraryResponse,
    RemedyOptionsResponse,
    RemedyPortfolioResponse,
    RemedyScoreResponse,
)
from api.services.remedy_service import (
    build_remedy_library_result,
    build_remedy_options,
    build_remedy_portfolio_result,
    build_remedy_profile,
    build_remedy_score_result,
)

router = APIRouter(prefix="/remedy", tags=["remedy"])


@router.get("/library", response_model=RemedyLibraryResponse)
def remedy_library(domain: str | None = None) -> RemedyLibraryResponse:
    result = build_remedy_library_result(domain)
    return RemedyLibraryResponse(**result)


@router.post("/bottlenecks", response_model=RemedyBottleneckResponse)
def remedy_bottlenecks(payload: RemedyRequest) -> RemedyBottleneckResponse:
    result = build_remedy_profile(payload)
    return RemedyBottleneckResponse(profile=result)


@router.post("/options", response_model=RemedyOptionsResponse)
def remedy_options(payload: RemedyRequest) -> RemedyOptionsResponse:
    result = build_remedy_options(payload)
    return RemedyOptionsResponse(**result)


@router.post("/portfolio", response_model=RemedyPortfolioResponse)
def remedy_portfolio(payload: RemedyRequest) -> RemedyPortfolioResponse:
    result = build_remedy_portfolio_result(payload)
    return RemedyPortfolioResponse(**result)


@router.post("/score", response_model=RemedyScoreResponse)
def remedy_score(payload: RemedyRequest) -> RemedyScoreResponse:
    result = build_remedy_score_result(payload)
    return RemedyScoreResponse(**result)
