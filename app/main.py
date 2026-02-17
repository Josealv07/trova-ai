from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.audio import router as audio_router
from app.api.health import router as health_router

app = FastAPI(title="Trova AI", version="0.1.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(audio_router)


@app.get("/")
def root():
    return {"message": "🎤 Trova AI está vivo"}


@app.get("/test-audio")
async def read_index():
    return FileResponse("static/index.html")
