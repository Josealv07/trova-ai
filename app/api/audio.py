from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.audio_storage import save_and_convert_audio

router = APIRouter(prefix="/audio", tags=["audio"])


@router.post("/upload")
def upload_audio(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".wav", ".mp3")):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos .wav o .mp3")

    wav_path = save_and_convert_audio(file)

    return {"message": "Audio recibido y convertido", "filename": wav_path.name}
