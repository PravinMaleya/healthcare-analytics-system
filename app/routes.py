import pandas as pd
from fastapi import APIRouter

from app.model_loader import load_model
from app.schemas import PredictionRequest, PredictionResponse

router = APIRouter()

model = load_model()

@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    features = pd.DataFrame([request.model_dump()])
    prediction = model.predict(features)[0]

    return PredictionResponse(predicted_test_result=str(prediction))

