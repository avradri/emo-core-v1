from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_get_dac_events():
    response = client.get("/dac/events")

    assert response.status_code == 200
    assert response.json() == {
        "events": [
            {
                "id": "diag-ro-001",
                "kind": "diagnostic",
                "domain": "disaster",
                "jurisdiction": "RO",
                "timestamp": "2026-01-01T00:00:00",
            },
            {
                "id": "policy-ro-001",
                "kind": "policy",
                "domain": "disaster",
                "jurisdiction": "RO",
                "timestamp": "2026-01-04T00:00:00",
            },
        ]
    }


def test_get_dac_events_filtered_by_domain():
    response = client.get("/dac/events?domain=disaster")

    assert response.status_code == 200
    assert len(response.json()["events"]) == 2


def test_get_dac_events_filtered_by_jurisdiction():
    response = client.get("/dac/events?jurisdiction=RO")

    assert response.status_code == 200
    assert len(response.json()["events"]) == 2


def test_get_dac_events_filtered_to_empty():
    response = client.get("/dac/events?domain=pandemic")

    assert response.status_code == 200
    assert response.json() == {"events": []}
