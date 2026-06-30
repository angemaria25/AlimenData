from fastapi import FastAPI
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="AlimenData API",
    description="Sistema Inteligente de Gestión y Distribución Alimentaria",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "AlimenData API - Sistema de Gestión Alimentaria"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
