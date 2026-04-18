from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_remedy_score_endpoint_returns_expected_shape() -> None:
    payload = {
        "domain": "disaster",
        "jurisdiction": "RO",
        "validation_score": 0.8,
        "translation_score": 0.4,
        "budget_score": 0.5,
        "deployment_score": 0.6,
        "persistence_score": 0.45,
        "contradiction_score": 0.7,
    }

    response = client.post("/remedy/score", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "profile" in data
    assert "portfolio" in data
    assert "score" in data

    profile = data["profile"]
    assert profile["domain"] == "disaster"
    assert profile["jurisdiction"] == "RO"
    assert "dominant_bottlenecks" in profile
    assert "translation" in profile["dominant_bottlenecks"]
    assert "contradiction" in profile["dominant_bottlenecks"]

    portfolio = data["portfolio"]
    assert portfolio["domain"] == "disaster"
    assert portfolio["jurisdiction"] == "RO"
    assert "options" in portfolio
    assert isinstance(portfolio["options"], list)
    assert len(portfolio["options"]) >= 1

    score = data["score"]
    assert score["portfolio_id"] == portfolio["portfolio_id"]
    assert 0.0 <= score["overall_score"] <= 1.0


def test_remedy_portfolio_endpoint_returns_portfolio_only() -> None:
    payload = {
        "domain": "disaster",
        "jurisdiction": "RO",
        "validation_score": 0.8,
        "translation_score": 0.4,
        "budget_score": 0.5,
        "deployment_score": 0.6,
        "persistence_score": 0.45,
        "contradiction_score": 0.7,
    }

    response = client.post("/remedy/portfolio", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "profile" in data
    assert "portfolio" in data
    assert "score" not in data

    portfolio = data["portfolio"]
    assert portfolio["domain"] == "disaster"
    assert portfolio["jurisdiction"] == "RO"
    assert "sequence" in portfolio
    assert isinstance(portfolio["sequence"], list)
    assert len(portfolio["sequence"]) >= 1


def test_remedy_bottlenecks_endpoint_returns_profile_only() -> None:
    payload = {
        "domain": "pandemic",
        "jurisdiction": "RO",
        "validation_score": 0.9,
        "translation_score": 0.3,
        "budget_score": 0.4,
        "deployment_score": 0.5,
        "persistence_score": 0.4,
        "contradiction_score": 0.2,
    }

    response = client.post("/remedy/bottlenecks", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "profile" in data
    assert "domain" in data["profile"]
    assert data["profile"]["domain"] == "pandemic"
    assert data["profile"]["jurisdiction"] == "RO"


def test_remedy_options_endpoint_returns_profile_and_options() -> None:
    payload = {
        "domain": "disaster",
        "jurisdiction": "RO",
        "validation_score": 0.8,
        "translation_score": 0.4,
        "budget_score": 0.5,
        "deployment_score": 0.6,
        "persistence_score": 0.45,
        "contradiction_score": 0.7,
    }

    response = client.post("/remedy/options", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "profile" in data
    assert "options" in data
    assert isinstance(data["options"], list)
    assert len(data["options"]) >= 1

    first_option = data["options"][0]
    assert "option_id" in first_option
    assert "family" in first_option
    assert "name" in first_option


def test_remedy_library_endpoint_returns_domain_library() -> None:
    response = client.get("/remedy/library?domain=disaster")

    assert response.status_code == 200

    data = response.json()
    assert "library" in data
    assert "disaster" in data["library"]
    assert isinstance(data["library"]["disaster"], list)
    assert len(data["library"]["disaster"]) >= 1

    first_option = data["library"]["disaster"][0]
    assert "option_id" in first_option
    assert "family" in first_option
    assert "name" in first_option
