import tempfile
from pathlib import Path
from src.pdf_parser import parse_pdf
import asyncio

from fastapi import APIRouter, UploadFile, File, HTTPException

pdf_router = APIRouter(prefix="/pdf")


@pdf_router.post("")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.content_type or "application/pdf" not in file.content_type:
        raise HTTPException(status_code=400, detail="Uploaded file is not a PDF.")

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded PDF is empty.")

    # Check magic number
    if file_bytes[:4] != b"%PDF":
        raise HTTPException(status_code=400, detail="File is not a valid PDF.")

    temp_path = Path(tempfile.gettempdir()) / f"uploaded_{file.filename}"
    temp_path.write_bytes(file_bytes)
    
    pages = await asyncio.to_thread(parse_pdf, str(temp_path))
    

    return {"filename": file.filename, "path": str(temp_path), "size_bytes": len(file_bytes)}