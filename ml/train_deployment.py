
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_healthcare.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "deployment_model.joblib"

RANDOM_STATE = 42
TEST_SIZE = 0.2

feature_cols = [
    "age",
    "gender",
    "blood_type",
    "medical_condition",
    "insurance_provider",
    "admission_type",
    "medication",
]
target_col = "test_results"

df = pd.read_csv(DATA_PATH)
X = df[feature_cols].copy()
y = df[target_col].copy()

X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y,
)

numeric_features = ["age"]
categorical_features = [
    "gender",
    "blood_type",
    "medical_condition",
    "insurance_provider",
    "admission_type",
    "medication",
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]),
            numeric_features,
        ),
        (
            "cat",
            Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore")),
            ]),
            categorical_features,
        ),
    ]
)

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
])

model.fit(X_train, y_train)
predictions = model.predict(X_val)
macro_f1 = f1_score(y_val, predictions, average="macro", zero_division=0)

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_PATH)

size_mb = MODEL_PATH.stat().st_size / (1024**2)

print(f"Logistic Regression macro F1: {macro_f1:.4f}")
print(f"Deployment model saved: {MODEL_PATH}")
print(f"Deployment model size: {size_mb:.2f} MiB")
