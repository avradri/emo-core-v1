from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_get_dac_compare():
    response = client.get("/dac/compare")

    assert response.status_code == 200
    assert response.json() == {
        "left": {
            "jurisdiction": "RO",
            "warning_to_policy_lag_days": 3,
            "declared_vs_funded_gap": 0.0,
        },
        "right": {
            "jurisdiction": "BG",
            "warning_to_policy_lag_days": 5,
            "declared_vs_funded_gap": 0.0,
        },
    }


def test_get_dac_compare_filtered_by_domain_and_sides():
    response = client.get("/dac/compare?domain=disaster&left=RO&right=BG")

    assert response.status_code == 200
    assert response.json() == {
        "left": {
            "jurisdiction": "RO",
            "warning_to_policy_lag_days": 3,
            "declared_vs_funded_gap": 0.0,
        },
        "right": {
            "jurisdiction": "BG",
            "warning_to_policy_lag_days": 5,
            "declared_vs_funded_gap": 0.0,
        },
    }


def test_get_dac_compare_filtered_to_empty_values():
    response = client.get("/dac/compare?domain=pandemic&left=RO&right=BG")

    assert response.status_code == 200
    assert response.json() == {
        "left": {
            "jurisdiction": "RO",
            "warning_to_policy_lag_days": None,
            "declared_vs_funded_gap": None,
        },
        "right": {
            "jurisdiction": "BG",
            "warning_to_policy_lag_days": None,
            "declared_vs_funded_gap": None,
        },
    }
