from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Employer

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/employer/login", response_class=HTMLResponse)
def employer_login_page(request: Request):
    return templates.TemplateResponse(
        request,
        "employer_login.html",
        {"error": None}
    )


@router.post("/employer/login", response_class=HTMLResponse)
def employer_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    employer = db.query(Employer).filter(
        Employer.username == username,
        Employer.password == password
    ).first()

    if not employer:
        return templates.TemplateResponse(
            request,
            "employer_login.html",
            {"error": "Invalid username or password"}
        )

    request.session["user"] = {
        "username": employer.username,
        "role": employer.role
    }

    return RedirectResponse(url="/employer/dashboard", status_code=303)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
