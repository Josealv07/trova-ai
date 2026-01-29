import uuid
from pathlib import Path

from fastapi import UploadFile
from pydub import AudioSegment

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_and_convert_audio(file: UploadFile) -> Path:
    temp_path = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"

    with open(temp_path, "wb") as f:
        f.write(file.file.read())

    # Convertir a wav
    audio = AudioSegment.from_file(temp_path)
    wav_path = temp_path.with_suffix(".wav")
    audio.export(wav_path, format="wav")

    temp_path.unlink()  # borrar el mp3 temporal

    return wav_path
