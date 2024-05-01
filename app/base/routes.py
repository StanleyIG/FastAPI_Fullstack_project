from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse


router = APIRouter(
    prefix="",
    tags=["main"]
)


@router.get("/", response_class=HTMLResponse)
def start_page(request: Request):
    return RedirectResponse("pages/register")