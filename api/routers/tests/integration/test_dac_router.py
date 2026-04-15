from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_get_dac_domains():
    response = client.get("/dac/domains")

    assert response.status_code == 200
    assert response.json() == {
        "domains": [
            "disaster",
            "pandemic",
        ]
    }
