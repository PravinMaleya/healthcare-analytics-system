from typing import Literal

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    age: int = Field(ge=0, le=120)
    gender: Literal["Male", "Female"]
    blood_type: Literal[
        "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"
    ]
    medical_condition: Literal[
        "Arthritis",
        "Asthma",
        "Cancer",
        "Diabetes",
        "Hypertension",
        "Obesity",
    ]
    insurance_provider: Literal[
        "Aetna",
        "Blue Cross",
        "Cigna",
        "Medicare",
        "UnitedHealthcare",
    ]
    admission_type: Literal["Elective", "Emergency", "Urgent"]
    medication: Literal[
        "Aspirin",
        "Ibuprofen",
        "Lipitor",
        "Paracetamol",
        "Penicillin",
    ]


class PredictionResponse(BaseModel):
    predicted_test_result: Literal[
        "Normal", "Abnormal", "Inconclusive"
    ]
