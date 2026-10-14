
from pathlib import Path
from time import time

import joblib
import pandas as pd

from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from xgboost import XGBClassifier


# --------------------------------------------------
# 1. Project paths and configuration

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_healthcare.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "model.joblib"

RANDOM_STATE = 42
TEST_SIZE = 0.2


# --------------------------------------------------
# 2. Load data and define features

df = pd.read_csv(DATA_PATH)

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

X = df[feature_cols].copy()
y = df[target_col].copy()

print("Dataset shape:", df.shape)
print("Features shape:", X.shape)
print("Target shape:", y.shape)


# --------------------------------------------------
# 3. Split data

X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y,
)

print("Training rows:", len(X_train))
print("Validation rows:", len(X_val))


# --------------------------------------------------
# 4. Build preprocessing pipeline

numeric_features = ["age"]

categorical_features = [
    "gender",
    "blood_type",
    "medical_condition",
    "insurance_provider",
    "admission_type",
    "medication",
]

numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)


# --------------------------------------------------
# 5. Define models

models = {
    "Dummy Classifier": DummyClassifier(strategy="most_frequent"),
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        random_state=RANDOM_STATE,
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    ),
    "XGBoost": XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        objective="multi:softprob",
        eval_metric="mlogloss",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    ),
}


# --------------------------------------------------
# 6. Encode labels for XGBoost

label_encoder = LabelEncoder()

y_train_encoded = label_encoder.fit_transform(y_train)
y_val_encoded = label_encoder.transform(y_val)

class_labels = label_encoder.classes_

results = []
trained_models = {}

# --------------------------------------------------
# 7. Train and evaluate each model

for name, classifier in models.items():
    print(f"\nTraining {name}...")

    pipeline = Pipeline(
        steps=[
            ("preprocessor", clone(preprocessor)),
            ("classifier", classifier),
        ]
    )

    start_time = time()

    if name == "XGBoost":
        pipeline.fit(X_train, y_train_encoded)
        y_pred_encoded = pipeline.predict(X_val).astype(int)
        y_pred = label_encoder.inverse_transform(y_pred_encoded)
    else:
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_val)

    elapsed_seconds = round(time() - start_time, 2)

    results.append(
        {
            "Model": name,
            "Accuracy": accuracy_score(y_val, y_pred),
            "Precision (Macro)": precision_score(
                y_val, y_pred, average="macro", zero_division=0
            ),
            "Recall (Macro)": recall_score(
                y_val, y_pred, average="macro", zero_division=0
            ),
            "F1 (Macro)": f1_score(
                y_val, y_pred, average="macro", zero_division=0
            ),
            "Training + Prediction (seconds)": elapsed_seconds,
        }
    )

    trained_models[name] = pipeline

    print(f"Completed {name}.")
    print("Confusion matrix:")
    print(confusion_matrix(y_val, y_pred, labels=class_labels))
    print(
        classification_report(
            y_val,
            y_pred,
            labels=class_labels,
            target_names=class_labels,
            zero_division=0,
        )
    )


# --------------------------------------------------
# 8. Compare models and select an API-compatible one

results_df = (
    pd.DataFrame(results)
    .sort_values("F1 (Macro)", ascending=False)
    .reset_index(drop=True)
)

print("\nModel comparison:")
print(results_df.round(4).to_string(index=False))

# XGBoost uses encoded target labels, so exclude it from
# API selection until we implement a decoding wrapper.
deployable_models = ["Logistic Regression", "Random Forest"]

deployable_results = results_df[
    results_df["Model"].isin(deployable_models)
]

best_name = deployable_results.iloc[0]["Model"]
candidate_model = trained_models[best_name]

candidate_predictions = candidate_model.predict(X_val)
candidate_f1 = f1_score(
    y_val,
    candidate_predictions,
    average="macro",
    zero_division=0,
)

print(f"\nSelected candidate: {best_name}")
print(f"Candidate macro F1: {candidate_f1:.4f}")


# --------------------------------------------------
# 9. Compare against the currently saved model

if MODEL_PATH.exists():
    print("\nExisting model found. Evaluating it...")

    existing_model = joblib.load(MODEL_PATH)
    existing_predictions = existing_model.predict(X_val)

    existing_f1 = f1_score(
        y_val,
        existing_predictions,
        average="macro",
        zero_division=0,
    )

    print(f"Existing model macro F1: {existing_f1:.4f}")

    if candidate_f1 < existing_f1:
        print("Candidate is worse. Existing model preserved.")
        raise SystemExit(0)

    print("Candidate meets or exceeds existing model performance.")

else:
    print("\nNo existing model found. Saving initial model.")


# --------------------------------------------------
# 10. Save the candidate model

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

joblib.dump(candidate_model, MODEL_PATH)

print(f"Model saved to: {MODEL_PATH}")
print(f"Model size: {MODEL_PATH.stat().st_size / (1024**2):.2f} MB")
