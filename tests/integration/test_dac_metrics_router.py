from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_get_dac_metrics_summary():
    response = client.get("/dac/metrics/summary")

    assert response.status_code == 200
    assert response.json() == {
        "warning_to_policy_lag_days": 3,
        "warning_to_delivery_lag_days": 5,
        "alert_to_policy_conversion_rate": 1.0,
        "implementation_persistence_30d": 1.0,
        "declared_vs_funded_gap": 0.0,
    }


def test_get_dac_metrics_summary_filtered_by_domain():
    response = client.get("/dac/metrics/summary?domain=disaster")

    assert response.status_code == 200
    assert response.json() == {
        "warning_to_policy_lag_days": 3,
        "warning_to_delivery_lag_days": 5,
        "alert_to_policy_conversion_rate": 1.0,
        "implementation_persistence_30d": 1.0,
        "declared_vs_funded_gap": 0.0,
    }


def test_get_dac_metrics_summary_filtered_by_jurisdiction():
    response = client.get("/dac/metrics/summary?jurisdiction=RO")

    assert response.status_code == 200
    assert response.json() == {
        "warning_to_policy_lag_days": 3,
        "warning_to_delivery_lag_days": 5,
        "alert_to_policy_conversion_rate": 1.0,
        "implementation_persistence_30d": 1.0,
        "declared_vs_funded_gap": 0.0,
    }


def test_get_dac_metrics_summary_filtered_to_empty_values():
    response = client.get("/dac/metrics/summary?domain=pandemic")

    assert response.status_code == 200
    assert response.json() == {
        "warning_to_policy_lag_days": None,
        "warning_to_delivery_lag_days": None,
        "alert_to_policy_conversion_rate": None,
        "implementation_persistence_30d": None,
        "declared_vs_funded_gap": None,
    }
