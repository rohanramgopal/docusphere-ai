from fastapi import Request
from fastapi.responses import RedirectResponse


def get_current_user(request: Request):
    return request.session.get("user")


def require_employer_login(request: Request):
    user = get_current_user(request)
    if not user:
        return None
    return user


def redirect_to_login():
    return RedirectResponse(url="/employer/login", status_code=303)
