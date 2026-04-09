from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Document
from app.utils.helpers import load_json
from app.auth import require_employer_login

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/employer/dashboard", response_class=HTMLResponse)
def employer_dashboard(request: Request, db: Session = Depends(get_db)):
    user = require_employer_login(request)
    if not user:
        return RedirectResponse(url="/employer/login", status_code=303)

    documents = db.query(Document).order_by(Document.created_at.desc()).all()

    decorated = []
    for doc in documents:
        fields = load_json(doc.extracted_fields)
        decorated.append({
            "doc": doc,
            "priority": fields.get("priority", "low"),
            "actions": fields.get("actions", [])
        })

    priority_order = {"high": 0, "medium": 1, "low": 2}
    decorated.sort(key=lambda x: (priority_order.get(x["priority"], 3), -x["doc"].id))

    return templates.TemplateResponse(
        request,
        "employer_dashboard.html",
        {
            "user": user,
            "documents": decorated
        }
    )


@router.get("/employer/documents", response_class=HTMLResponse)
def list_documents(request: Request, db: Session = Depends(get_db)):
    user = require_employer_login(request)
    if not user:
        return RedirectResponse(url="/employer/login", status_code=303)

    documents = db.query(Document).order_by(Document.created_at.desc()).all()

    decorated = []
    for doc in documents:
        fields = load_json(doc.extracted_fields)
        decorated.append({
            "doc": doc,
            "priority": fields.get("priority", "low"),
            "actions": fields.get("actions", [])
        })

    priority_order = {"high": 0, "medium": 1, "low": 2}
    decorated.sort(key=lambda x: (priority_order.get(x["priority"], 3), -x["doc"].id))

    return templates.TemplateResponse(
        request,
        "employer_documents.html",
        {
            "user": user,
            "documents": decorated,
            "results": [],
            "query": ""
        }
    )


@router.get("/employer/documents/{doc_id}", response_class=HTMLResponse)
def document_detail(request: Request, doc_id: int, db: Session = Depends(get_db)):
    user = require_employer_login(request)
    if not user:
        return RedirectResponse(url="/employer/login", status_code=303)

    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    fields = load_json(doc.extracted_fields)

    return templates.TemplateResponse(
        request,
        "document_detail.html",
        {
            "user": user,
            "doc": doc,
            "fields": fields
        }
    )


@router.get("/employer/documents/{doc_id}/download")
def download_document(request: Request, doc_id: int, db: Session = Depends(get_db)):
    user = require_employer_login(request)
    if not user:
        return RedirectResponse(url="/employer/login", status_code=303)

    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return FileResponse(
        path=doc.stored_path,
        filename=doc.filename,
        media_type=doc.content_type or "application/octet-stream"
    )
