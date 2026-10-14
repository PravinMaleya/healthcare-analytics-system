from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)



def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Healthcare Test Result Predictor" in response.text



def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_valid_request():
    payload = {
        "age": 27,
        "gender": "Female",
        "blood_type": "AB+",
        "medical_condition": "Hypertension",
        "insurance_provider": "UnitedHealthcare",
        "admission_type": "Emergency",
        "medication": "Lipitor",
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    assert response.json()["predicted_test_result"] in [
        "Normal",
        "Abnormal",
        "Inconclusive",
    ]


def test_predict_invalid_age():
    payload = {
        "age": -1,
        "gender": "Female",
        "blood_type": "AB+",
        "medical_condition": "Hypertension",
        "insurance_provider": "UnitedHealthcare",
        "admission_type": "Emergency",
        "medication": "Lipitor",
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_missing_required_field():
    payload = {
        "age": 27,
        "gender": "Female",
        "blood_type": "AB+",
        "medical_condition": "Hypertension",
        "insurance_provider": "UnitedHealthcare",
        "admission_type": "Emergency",
        # medication is intentionally missing
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422

