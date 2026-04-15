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
