from pathlib import Path
from typing import Optional


def save_upload_file(upload_file, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as buffer:
        buffer.write(upload_file.read())


def read_pdf_text(path: Path) -> str:
    from PyPDF2 import PdfReader
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)
