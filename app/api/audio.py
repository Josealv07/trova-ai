import os
from datetime import datetime

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.audio_storage import save_and_convert_audio
from app.services.judge import judge_trova
from app.services.transcription import transcribe_audio

router = APIRouter(prefix="/audio", tags=["audio"])


@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    initial_time = datetime.now()
    if not file.filename.lower().endswith((".wav", ".mp3", ".m4a", ".ogg", ".webm")):
        raise HTTPException(status_code=400, detail="Formato no compatible")

    wav_path = save_and_convert_audio(file)

    try:
        transcription = transcribe_audio(wav_path)
        veredict = judge_trova(transcription)

        final_time = datetime.now()

        return {
            "message": "Transcripción completada",
            "filename": os.path.basename(wav_path),
            "transcription": transcription,
            "evaluation": veredict,
            "time": (final_time - initial_time).total_seconds(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
