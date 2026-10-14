# Healthcare Analytics System

An end-to-end machine learning project that demonstrates healthcare data cleaning, PostgreSQL storage, model training, and a REST API for predicting recorded test-result categories.

## Project Overview

This project explores a complete machine learning workflow, from raw healthcare data to an API that serves model predictions.

**Prediction target:** `test_results`

The model predicts one of three classes:
- Normal
- Abnormal
- Inconclusive

## System Workflow

1. **Data cleaning:** Inspect and clean the raw healthcare dataset using Python and Pandas.
2. **Data storage:** Load cleaned records into PostgreSQL.
3. **Data validation:** Use SQL queries to check the stored data.
4. **Model development:** Train and evaluate classification models using scikit-learn.
5. **Model persistence:** Save the fitted preprocessing and prediction pipeline.
6. **API development:** Serve predictions through FastAPI.
7. **Testing:** Use pytest and FastAPI's test client to verify endpoints and input validation.
8. **Deployment:** Planned.

## Tech Stack

- Python
- Pandas and scikit-learn
- PostgreSQL
- FastAPI
- Pydantic
- pytest
- uv

## Running the API Locally

### 1. Install dependencies

Install [uv](https://docs.astral.sh/uv/) if you don't already have it, then run:

```bash
uv sync
```

### 2. Provide the trained model

Place the locally trained model at:

```text
models/model.joblib
```

The model artifact is not committed to Git because of its large file size.

### 3. Start the API

```bash
uv run uvicorn app.main:app --reload
```

### 4. Explore the endpoints

- `GET /` — API status
- `GET /health` — Health check
- `POST /predict` — Generate a prediction
- `/docs` — Interactive API documentation

## Running Tests

```bash
uv run pytest -v
```

## Important Limitations

This is an educational machine learning project, not a clinically validated diagnostic tool. Its predictions reflect patterns in the available dataset and must not be used to make medical decisions.

The model's performance and feature limitations should be considered when interpreting its predictions.

## Future Improvements

- Deploy the API and make the model artifact available securely.
- Implement scheduled model retraining.
- Add monitoring and logging.
- Expand automated testing.

