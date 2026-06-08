import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Get absolute path to the templates directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/", response_class=HTMLResponse)
@router.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )

@router.get("/study/{user_id}", response_class=HTMLResponse)
async def read_study(request: Request, user_id: str):
    return templates.TemplateResponse(
        request=request, name="study.html", context={"user_id": user_id}
    )

@router.get("/studio/{user_id}", response_class=HTMLResponse)
async def read_studio(request: Request, user_id: str):
    return templates.TemplateResponse(
        request=request, name="studio.html", context={"user_id": user_id}
    )
