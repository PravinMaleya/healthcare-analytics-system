from pathlib import Path

import joblib


# Project root: parent directory of app/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "model.joblib"


def load_model():
    # Load the saved, fitted preprocessing and Random Forest pipeline.
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. "
            "Train and save the model before starting the API."
        )

    return joblib.load(MODEL_PATH)
