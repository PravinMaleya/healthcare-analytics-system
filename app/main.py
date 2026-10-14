from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Healthcare Analytics API",
    description="API for the Healthcare Analytics System",
    version="0.1.0",
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "message": "Healthcare Analytics API is running",
        "status": "healthy",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}
