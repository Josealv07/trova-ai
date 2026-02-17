import os
import uuid
from pathlib import Path

from fastapi import UploadFile

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_and_convert_audio(file: UploadFile) -> Path:
    ext = os.path.splitext(file.filename)[1] or ".webm"
    temp_path = UPLOAD_DIR / f"{uuid.uuid4()}{ext}"

    with open(temp_path, "wb") as f:
        f.write(file.file.read())

    return temp_path
