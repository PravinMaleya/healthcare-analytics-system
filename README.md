# Healthcare Analytics System

An end-to-end machine learning project that demonstrates healthcare data cleaning, PostgreSQL storage, exploratory data analysis, model development, automated retraining, API development, and deployment of a web-based prediction interface.

**Live application:** https://healthcare-analytics-api.onrender.com  
**GitHub repository:** https://github.com/PravinMaleya/healthcare-analytics-system

## Project Overview

The Healthcare Analytics System explores the machine learning lifecycle, from raw healthcare data to a deployed application that accepts patient-related features and predicts a recorded test-result category.

**Prediction target:** `test_results`

The model predicts one of three classes:

- Normal
- Abnormal
- Inconclusive

The project is designed to demonstrate practical data science and software engineering skills, including data preparation, database integration, model evaluation, API development, testing, automation, and deployment.

## System Workflow

1. **Data cleaning:** Inspect, clean, and prepare the raw healthcare dataset using Python and Pandas.
2. **Data storage:** Load cleaned records into PostgreSQL.
3. **Data validation:** Use SQL queries to validate the stored records and database structure.
4. **Exploratory data analysis:** Investigate the dataset, its distributions, and relationships between features and the target.
5. **Model development:** Train and evaluate classification models using scikit-learn and other selected machine learning tools.
6. **Model persistence:** Save trained preprocessing and prediction pipelines for reuse.
7. **API development:** Build a REST API with FastAPI to accept prediction requests and return model results.
8. **Testing:** Use pytest and FastAPI's test client to check application endpoints and input validation.
9. **Automated retraining:** Configure scheduled model retraining using a Python training script and Windows Task Scheduler.
10. **Deployment:** Deploy the API and web interface on Render.

## Web Application

The application provides a simple web form where users can enter the supported input features and request a prediction.

The interface includes:

- Patient-related feature inputs.
- A **Predict Result** button.
- A **Clear Form** button.
- A section displaying the predicted test-result category.
- Input validation and error feedback.

The frontend is built with HTML, CSS, and JavaScript and communicates with the FastAPI prediction endpoint.

## Tech Stack

| Area | Technologies |
|---|---|
| Programming | Python |
| Data preparation | Pandas, NumPy |
| Machine learning | scikit-learn, XGBoost |
| Database | PostgreSQL |
| Database tools | DBeaver |
| API | FastAPI, Pydantic |
| Frontend | HTML, CSS, JavaScript |
| Testing | pytest, FastAPI TestClient |
| Environment and dependencies | uv |
| Automation | PowerShell, Windows Task Scheduler |
| Deployment | Render |
| Version control | Git, GitHub |

## Project Structure

```text
healthcare-analytics-system/
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   ├── model_loader.py
│   └── ...
├── data/
│   ├── raw/
│   └── processed/
├── database/
│   ├── db_connection.py
│   ├── models.py
│   └── queries.sql
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── ml/
│   ├── train.py
│   ├── train_deployment.py
│   └── ...
├── models/
│   └── ...
├── notebooks/
├── scripts/
├── tests/
├── logs/
├── run_retraining.ps1
├── pyproject.toml
├── uv.lock
└── README.md
```

## Running the Project Locally

### 1. Prerequisites

Install Python and [uv](https://docs.astral.sh/uv/). PostgreSQL is needed for the database components.

Clone the repository and enter the project directory:

```bash
git clone https://github.com/PravinMaleya/healthcare-analytics-system.git
cd healthcare-analytics-system
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure the model

The application requires a compatible trained model artifact.

For the lightweight deployment model, configure the environment variable to point to its location:

**PowerShell:**

```powershell
$env:HEALTHCARE_MODEL_PATH = "models/deployment_model.joblib"
```

The model artifacts are not necessarily committed to Git. Ensure the required artifact exists locally before starting the application.

### 4. Start the application

```bash
uv run uvicorn app.main:app --reload
```

Open the following addresses in your browser:

- Web interface: http://127.0.0.1:8000/
- Interactive API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

### 5. Run the tests

```bash
uv run pytest -v
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Serves the web interface |
| `GET` | `/health` | Checks whether the application is responding |
| `POST` | `/predict` | Accepts input features and returns a prediction |
| `GET` | `/docs` | Opens the interactive API documentation |

### Example prediction request

Send a JSON request to `POST /predict`:

```json
{
  "age": 45,
  "gender": "Female",
  "blood_type": "A+",
  "medical_condition": "Diabetes",
  "insurance_provider": "Aetna",
  "admission_type": "Elective",
  "medication": "Aspirin"
}
```

The API returns a predicted test-result category, for example:

```json
{
  "predicted_test_result": "Normal"
}
```

*The response above illustrates the expected format; it is not a guaranteed prediction for the example input.*

Refer to `/docs` for the actual request schema and validation requirements.

## Model Development and Evaluation

The project compares classification approaches and evaluates their performance before selecting a model for the application.

The development process includes:

- Preparing input features and the target variable.
- Training and comparing classification models.
- Evaluating performance using classification metrics.
- Saving fitted preprocessing and prediction pipelines.
- Using a lightweight model artifact for deployment.

The deployment model is a demonstration of the end-to-end serving workflow. Its predictions should be interpreted in light of the dataset's limitations and the model's measured performance.

## Automated Retraining

The project includes a Python training script and a PowerShell wrapper for scheduled retraining using Windows Task Scheduler.

The configured schedule is **Saturday at 12:00 noon** on the machine running the scheduled task.

This automation is configured on the development environment; it should not be assumed to run automatically on Render. A production-grade retraining pipeline would need its own hosted scheduler, artifact management, validation, and deployment workflow.

## Deployment

The application is deployed on Render:

**Live application:** https://healthcare-analytics-api.onrender.com

The deployed service serves the frontend and exposes the prediction API through the same application. The frontend sends prediction requests to the API, which loads the configured model and returns the result.

Deployment requires the application dependencies, a compatible model artifact, and the appropriate model-path configuration.

## Limitations and Responsible Use

This project is an educational machine learning demonstration, **not a clinically validated diagnostic tool**.

- Predictions reflect patterns learned from the available dataset.
- The dataset may not represent real-world clinical populations or relationships.
- Model performance is limited by the quality and predictive value of the available features.
- Predictions must not be used to diagnose, treat, or make medical decisions about real patients.

## Future Improvements

- Improve predictive performance through further analysis, feature investigation, and appropriate model evaluation.
- Add structured application logging and error monitoring.
- Expand automated testing and deployment checks.
- Develop a more robust hosted retraining and model-versioning workflow.
- Improve deployment reliability and operational monitoring.
- Document reproducible database setup and data-ingestion procedures.
