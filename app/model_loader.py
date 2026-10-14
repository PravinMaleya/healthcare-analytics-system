import os
from pathlib import Path

import joblib

PROJECT_ROOT = Path(__file__).resolve().parent.parent

configured_path = Path(
    os.getenv("HEALTHCARE_MODEL_PATH", "models/model.joblib")
)

MODEL_PATH = (
    configured_path
    if configured_path.is_absolute()
    else PROJECT_ROOT / configured_path
)


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. "
            "Train and save the model before starting the API."
        )

    return joblib.load(MODEL_PATH)
