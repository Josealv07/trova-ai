from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"

UPLOADS_DIR.mkdir(exist_ok=True)
