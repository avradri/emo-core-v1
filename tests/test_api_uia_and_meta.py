# tests/test_api_uia_and_meta.py
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health_and_version_endpoints() -> None:
    """
    Basic smoke tests for /health and /version.
    """
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json().get("status") == "ok"

    version = client.get("/version")
    assert version.status_code == 200
    body = version.json()
    assert "version" in body
    assert isinstance(body["version"], str)


def test_uia_summary_endpoint_smoke() -> None:
    """
    End-to-end smoke test for the /uia/summary endpoint.

    Posts a tiny synthetic C/S/I bundle and checks that we obtain a
    JSON-serializable UIASummary-like structure.
    """
    payload = {
        "interface_id": "test_interface",
        "R_scalar": 1.0,
        "B_scalar": 1.0,
        "C": [0.2, 0.3, 0.4],
        "S": [1.0, 0.95, 0.9],
        "I": [0.1, 0.2, 0.35],
        "timestamps": None,
        "M_E": 0.5,
        "metadata": {"lab": "api-smoke"},
    }

    response = client.post("/uia/summary", json=payload)
    assert response.status_code == 200

    data = response.json()
    # Core UIASummary fields
    for key in ("interface_id", "A_uia_bar", "a_uia", "timestamps", "metadata"):
        assert key in data

    assert data["interface_id"] == payload["interface_id"]
    assert isinstance(data["A_uia_bar"], float)
    assert isinstance(data["a_uia"], list)
    assert len(data["a_uia"]) == len(payload["C"])
    assert isinstance(data["metadata"], dict)
    assert data["metadata"].get("lab") == "api-smoke"
