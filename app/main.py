from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session

from app.db.database import Base, engine, SessionLocal
from app.db.models import Employer
from app.routes.upload import router as upload_router
from app.routes.search import router as search_router
from app.routes.qa import router as qa_router
from app.routes.auth_routes import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Workflow Assistant")
app.add_middleware(SessionMiddleware, secret_key="super-secret-key-change-this")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(search_router)
app.include_router(qa_router)


def seed_employer():
    db: Session = SessionLocal()
    existing = db.query(Employer).filter(Employer.username == "employer1").first()
    if not existing:
        demo = Employer(username="employer1", password="1234", role="employer")
        db.add(demo)
        db.commit()
    db.close()


seed_employer()


@app.get("/", response_class=HTMLResponse)
def candidate_page(request: Request):
    return templates.TemplateResponse(request, "candidate_upload.html", {})


@app.get("/success", response_class=HTMLResponse)
def success_page(request: Request):
    return templates.TemplateResponse(request, "success.html", {})
