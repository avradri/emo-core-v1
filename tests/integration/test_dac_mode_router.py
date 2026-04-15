from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_get_current_dac_mode():
    response = client.get("/dac/modes/current")

    assert response.status_code == 200
    assert response.json() == {
        "mode": "selective_stabilization"
    }
