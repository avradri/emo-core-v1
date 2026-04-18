from __future__ import annotations

from fastapi import APIRouter

from api.schemas.remedy_request import RemedyLearningRequest, RemedyRequest
from api.schemas.remedy_response import (
    RemedyBottleneckResponse,
    RemedyComparisonResponse,
    RemedyExplainResponse,
    RemedyLearningResponse,
    RemedyLegitimacyResponse,
    RemedyLibraryResponse,
    RemedyOptionsResponse,
    RemedyPortfolioResponse,
    RemedyScoreResponse,
    RemedySimulationResponse,
    RemedyTradeoffResponse,
)
from api.services.remedy_service import (
    build_remedy_comparison_result,
    build_remedy_explain_result,
    build_remedy_learning_result,
    build_remedy_legitimacy_result,
    build_remedy_library_result,
    build_remedy_options,
    build_remedy_portfolio_result,
    build_remedy_profile,
    build_remedy_score_result,
    build_remedy_simulation_result,
    build_remedy_tradeoff_result,
)

router = APIRouter(prefix="/remedy", tags=["remedy"])


@router.get("/library", response_model=RemedyLibraryResponse)
def remedy_library(domain: str | None = None) -> RemedyLibraryResponse:
    result = build_remedy_library_result(domain)
    return RemedyLibraryResponse(**result)


@router.post("/compare", response_model=RemedyComparisonResponse)
def remedy_compare(payload: RemedyRequest) -> RemedyComparisonResponse:
    result = build_remedy_comparison_result(payload)
    return RemedyComparisonResponse(**result)


@router.post("/explain", response_model=RemedyExplainResponse)
def remedy_explain(payload: RemedyRequest) -> RemedyExplainResponse:
    result = build_remedy_explain_result(payload)
    return RemedyExplainResponse(**result)


@router.post("/simulate", response_model=RemedySimulationResponse)
def remedy_simulate(payload: RemedyRequest) -> RemedySimulationResponse:
    result = build_remedy_simulation_result(payload)
    return RemedySimulationResponse(**result)


@router.post("/tradeoffs", response_model=RemedyTradeoffResponse)
def remedy_tradeoffs(payload: RemedyRequest) -> RemedyTradeoffResponse:
    result = build_remedy_tradeoff_result(payload)
    return RemedyTradeoffResponse(**result)


@router.post("/legitimacy", response_model=RemedyLegitimacyResponse)
def remedy_legitimacy(payload: RemedyRequest) -> RemedyLegitimacyResponse:
    result = build_remedy_legitimacy_result(payload)
    return RemedyLegitimacyResponse(**result)


@router.post("/learn", response_model=RemedyLearningResponse)
def remedy_learn(payload: RemedyLearningRequest) -> RemedyLearningResponse:
    result = build_remedy_learning_result(payload)
    return RemedyLearningResponse(**result)


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
