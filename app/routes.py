from fastapi import APIRouter

from app.model_loader import load_model
from app.schemas import PredictionRequest, PredictionResponse

router = APIRouter()

# Load the model.
model = load_model()


@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    # Convert the validated request into the feature format used during training.
    features = request.model_dump()
    prediction = model.predict([features])[0]

    return PredictionResponse(
        predicted_test_result=str(prediction)
    )
