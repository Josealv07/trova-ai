from fastapi import FastAPI

from app.api.audio import router as audio_router
from app.api.health import router as health_router

app = FastAPI(title="Trova AI", version="0.1.0")

app.include_router(health_router)
app.include_router(audio_router)


@app.get("/")
def root():
    return {"message": "🎤 Trova AI está vivo"}
