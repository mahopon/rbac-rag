import os
from pathlib import Path
from src.pdf_parser import parse_pdf
import asyncio
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from src.db import add_document

UPLOAD_DIR = Path(__file__).parent.parent / "uploads"

pdf_router = APIRouter(prefix="/pdf")

upload_dir = UPLOAD_DIR / "pdf"
upload_dir.mkdir(parents=True, exist_ok=True)

@pdf_router.post("")
async def upload_pdf(file: UploadFile = File(...), is_viewer: str = Form(default="non-viewer")):
    if not file.content_type or "application/pdf" not in file.content_type:
        raise HTTPException(status_code=400, detail="Uploaded file is not a PDF.")

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded PDF is empty.")

    # Check magic number
    if file_bytes[:4] != b"%PDF":
        raise HTTPException(status_code=400, detail="File is not a valid PDF.")

    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a name.")

    safe_filename = file.filename.replace(" ", "_")
    stored_filename = f"upload_{uuid.uuid4()}.pdf"
    stored_path = upload_dir / stored_filename

    stored_path.write_bytes(file_bytes)

    try:
        pages = await asyncio.to_thread(parse_pdf, str(stored_path))
        privileged = is_viewer == "viewer"
        add_document(safe_filename, str(stored_path), privileged=privileged)
    except Exception as e:
        print(e)
        stored_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"PDF parsing failed: {e}")

    return {"filename": file.filename, "path": str(stored_path), "size_bytes": len(file_bytes)}