from pathlib import Path
from fastapi import FastAPI, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import os


TOKEN = os.getenv("DASHBOARD_TOKEN", "changeme")


def create_app() -> FastAPI:
    """Create and configure the FastAPI dashboard application."""
    app = FastAPI()
    templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
    app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "secret"))

    def get_current_user(request: Request) -> str:
        user = request.session.get("user")
        if not user:
            raise HTTPException(status_code=401)
        return user

    @app.get("/login", response_class=HTMLResponse)
    async def login_form(request: Request) -> HTMLResponse:
        return templates.TemplateResponse("login.html", {"request": request})

    @app.post("/login")
    async def login(request: Request, token: str = Form(...)) -> RedirectResponse:
        if token != TOKEN:
            return templates.TemplateResponse(
                "login.html", {"request": request, "error": "Invalid token"}, status_code=400
            )
        request.session["user"] = "admin"
        return RedirectResponse(url="/", status_code=303)

    @app.get("/logout")
    async def logout(request: Request) -> RedirectResponse:
        request.session.clear()
        return RedirectResponse(url="/login", status_code=303)

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request, user: str = Depends(get_current_user)) -> HTMLResponse:
        return templates.TemplateResponse("index.html", {"request": request, "user": user})

    return app
