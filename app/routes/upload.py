import os
import shutil
import uuid

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Document
from app.services.classifier import classify_document
from app.services.summarizer import summarize_text
from app.services.extractor import extract_fields
from app.utils.helpers import allowed_file, extract_text, save_json

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/submit")
async def submit_document(
    request: Request,
    candidate_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename or not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    extension = os.path.splitext(file.filename)[1].lower()
    unique_name = f"{uuid.uuid4().hex}{extension}"
    saved_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        text = extract_text(saved_path)
    except Exception:
        text = "Could not extract text from this file."

    doc_type = classify_document(text, file.filename)
    fields = extract_fields(text, doc_type)
    summary = summarize_text(text, doc_type)

    new_doc = Document(
        candidate_name=candidate_name,
        filename=file.filename,
        stored_path=saved_path,
        content_type=file.content_type,
        extracted_text=text,
        document_type=doc_type,
        summary=summary,
        extracted_fields=save_json(fields)
    )

    db.add(new_doc)
    db.commit()

    return RedirectResponse(url="/success", status_code=303)
