import os
from pathlib import Path

import joblib

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = Path(
    os.getenv(
        "HEALTHCARE_MODEL_PATH",
        str(PROJECT_ROOT / "models" / "model.joblib"),
    )
)


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. "
            "Train and save the model before starting the API."
        )

    return joblib.load(MODEL_PATH)
