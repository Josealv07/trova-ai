import os
from pathlib import Path

import whisper

model = whisper.load_model("turbo")


def transcribe_audio(audio_path: str) -> str:
    try:
        path_obj = Path(audio_path).resolve()
        path_str = str(path_obj)

        if not path_obj.exists():
            print(f"Error: No existe el archivo en {path_str}")
            return "Archivo de audio no encontrado."

        print(f"Transcribiendo archivo en: {path_str}")

        result = model.transcribe(path_str, fp16=False)

        return result["text"]

    except Exception as e:
        print(f"Error detallado: {e}")
        return f"Error al transcribir el audio: {str(e)}"
