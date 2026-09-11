"""Validation helpers used by the UI and service layer."""
from __future__ import annotations
from pathlib import Path
from config import MAX_UPLOAD_MB
from utils.file_parser import SUPPORTED_EXTENSIONS

def validate_upload(file_name: str, size_bytes: int) -> tuple[bool, str]:
    ext = Path(file_name).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return False, f"Unsupported file type '{ext}'. Use PDF, DOCX, or TXT."
    if size_bytes > MAX_UPLOAD_MB * 1024 * 1024:
        return False, f"'{file_name}' exceeds the {MAX_UPLOAD_MB} MB upload limit."
    if size_bytes == 0:
        return False, f"'{file_name}' is empty."
    return True, ""
