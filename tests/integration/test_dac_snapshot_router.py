from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_get_dac_snapshot():
    response = client.get("/dac/report/snapshot")

    assert response.status_code == 200
    assert response.json() == {
        "domain": "disaster",
        "jurisdiction": "RO",
        "mode": "selective_stabilization",
        "metrics": {
            "warning_to_policy_lag_days": 3,
            "warning_to_delivery_lag_days": 5,
            "alert_to_policy_conversion_rate": 1.0,
            "implementation_persistence_30d": 1.0,
            "declared_vs_funded_gap": 0.0,
        },
    }
