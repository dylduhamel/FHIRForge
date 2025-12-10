from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_convert_endpoint():
    response = client.post(
        "/convert",
        json={
            "clinical_note": "Patient has diabetes and is taking metformin"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["entities"]) > 0
    assert data["fhir_bundle"] is not None


def test_convert_with_empty_note():
    response = client.post(
        "/convert",
        json={
            "clinical_note": "No medical information here"
        }
    )
    assert response.status_code == 200
    # Should succeed but with no entities