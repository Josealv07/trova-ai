from pathlib import Path

from groq import Groq

from app.core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def transcribe_audio(audio_path: str) -> str:
    try:
        path_obj = Path(audio_path).resolve()

        if not path_obj.exists():
            return "Archivo de audio no encontrado."

        print(f"Transcribiendo con Groq Cloud: {path_obj.name}")

        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=(path_obj.name, audio_file.read()),
                model="whisper-large-v3",
                response_format="text",
                language="es",
            )

        return transcription

    except Exception as e:
        print(f"Error detallado: {e}")
        return f"Error al transcribir: {str(e)}"
