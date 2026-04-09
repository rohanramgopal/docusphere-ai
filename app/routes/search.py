from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Document
from app.services.embeddings import embed_text, cosine_similarity
from app.auth import require_employer_login
from app.utils.helpers import load_json

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/employer/search", response_class=HTMLResponse)
def search_documents(request: Request, q: str = "", db: Session = Depends(get_db)):
    user = require_employer_login(request)
    if not user:
        return RedirectResponse(url="/employer/login", status_code=303)

    docs = db.query(Document).order_by(Document.created_at.desc()).all()
    results = []

    if q.strip():
        query_embedding = embed_text(q)
        ranked = []
        for doc in docs:
            searchable = " ".join([
                doc.candidate_name or "",
                doc.filename or "",
                doc.document_type or "",
                doc.summary or "",
                doc.extracted_text or ""
            ])
            text_embedding = embed_text(searchable)
            score = cosine_similarity(query_embedding, text_embedding)
            fields = load_json(doc.extracted_fields)
            ranked.append({
                "doc": doc,
                "priority": fields.get("priority", "low"),
                "actions": fields.get("actions", []),
                "score": score
            })

        ranked.sort(key=lambda x: (-x["score"], x["doc"].id))
        results = ranked

    documents = []
    for doc in docs:
        fields = load_json(doc.extracted_fields)
        documents.append({
            "doc": doc,
            "priority": fields.get("priority", "low"),
            "actions": fields.get("actions", [])
        })

    priority_order = {"high": 0, "medium": 1, "low": 2}
    documents.sort(key=lambda x: (priority_order.get(x["priority"], 3), -x["doc"].id))

    return templates.TemplateResponse(
        request,
        "employer_documents.html",
        {
            "user": user,
            "documents": documents,
            "results": results,
            "query": q
        }
    )
