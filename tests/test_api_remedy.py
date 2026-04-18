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
    assert "legitimacy_penalty" in score
    assert score["legitimacy_penalty"] >= 0.0


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


def test_remedy_explain_endpoint_returns_explanation() -> None:
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

    response = client.post("/remedy/explain", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "explanation" in data
    assert "profile" in data
    assert "portfolio" in data
    assert "score" in data

    assert isinstance(data["explanation"], str)
    assert "Dominant bottlenecks" in data["explanation"]
    assert "Recommended portfolio" in data["explanation"]
    assert "Legitimacy penalty" in data["explanation"]
    assert "Tradeoff summary" in data["explanation"]

def test_remedy_simulate_endpoint_returns_simulations() -> None:
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

    response = client.post("/remedy/simulate", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "profile" in data
    assert "portfolio" in data
    assert "score" in data
    assert "simulations" in data

    simulations = data["simulations"]
    assert isinstance(simulations, list)
    assert len(simulations) == 3

    scenario_names = {item["scenario"] for item in simulations}
    assert "do_nothing" in scenario_names
    assert "selected_portfolio" in scenario_names
    assert "high_friction" in scenario_names


def test_remedy_tradeoffs_endpoint_returns_tradeoff_report() -> None:
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

    response = client.post("/remedy/tradeoffs", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "profile" in data
    assert "portfolio" in data
    assert "score" in data
    assert "tradeoff_report" in data

    report = data["tradeoff_report"]
    assert "summary" in report
    assert "tradeoffs" in report
    assert isinstance(report["tradeoffs"], list)
    assert len(report["tradeoffs"]) >= 1

    dimensions = {item["dimension"] for item in report["tradeoffs"]}
    assert "feasibility" in dimensions
    assert "contradiction_risk" in dimensions
    assert "overall_score" in dimensions


def test_remedy_legitimacy_endpoint_returns_legitimacy_report() -> None:
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

    response = client.post("/remedy/legitimacy", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "profile" in data
    assert "portfolio" in data
    assert "legitimacy_report" in data

    report = data["legitimacy_report"]
    assert "summary" in report
    assert "flags" in report
    assert isinstance(report["flags"], list)
    assert len(report["flags"]) >= 1

    categories = {item["category"] for item in report["flags"]}
    assert "rights_risk" in categories
    assert "transparency" in categories
    assert "contestability" in categories


def test_remedy_library_endpoint_returns_climate_mitigation_domain() -> None:
    response = client.get("/remedy/library?domain=climate_mitigation")

    assert response.status_code == 200

    data = response.json()
    assert "library" in data
    assert "climate_mitigation" in data["library"]

    options = data["library"]["climate_mitigation"]
    assert isinstance(options, list)
    assert len(options) >= 1

    names = {item["name"] for item in options}
    assert "Climate budget alignment rule" in names
    assert "Contradictory subsidy phaseout" in names


def test_remedy_compare_endpoint_returns_comparison_report() -> None:
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

    response = client.post("/remedy/compare", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "profile" in data
    assert "portfolio" in data
    assert "comparison_report" in data

    report = data["comparison_report"]
    assert "summary" in report
    assert "comparisons" in report

    comparisons = report["comparisons"]
    assert isinstance(comparisons, list)
    assert len(comparisons) == 3

    labels = {item["portfolio_label"] for item in comparisons}
    assert "baseline" in labels
    assert "compact" in labels
    assert "full" in labels
def test_remedy_learn_endpoint_returns_learning_report() -> None:
    payload = {
        "domain": "disaster",
        "jurisdiction": "RO",
        "validation_score": 0.8,
        "translation_score": 0.4,
        "budget_score": 0.5,
        "deployment_score": 0.6,
        "persistence_score": 0.45,
        "contradiction_score": 0.7,
        "observed_dac_gain": 0.52,
        "observed_persistence": 0.41,
    }

    response = client.post("/remedy/learn", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "profile" in data
    assert "portfolio" in data
    assert "score" in data
    assert "learning_report" in data

    report = data["learning_report"]
    assert "portfolio_id" in report
    assert "expected_dac_gain" in report
    assert "observed_dac_gain" in report
    assert "learning_gap" in report
    assert "persistence_gap" in report
    assert "adjustment_signal" in report

    assert report["adjustment_signal"] in {"upweight", "hold", "downweight"}
def test_remedy_library_endpoint_returns_food_security_domain() -> None:
    response = client.get("/remedy/library?domain=food_security")

    assert response.status_code == 200

    data = response.json()
    assert "library" in data
    assert "food_security" in data["library"]

    options = data["library"]["food_security"]
    assert isinstance(options, list)
    assert len(options) >= 1

    names = {item["name"] for item in options}
    assert "Buffer stock release protocol" in names
    assert "Targeted food income support" in names
