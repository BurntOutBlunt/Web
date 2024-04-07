from datetime import timedelta, datetime

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.articles.router import get_specific_articles, get_all_articles
from src.auth.base_config import fastapi_users
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.auth.schemas import UserCreate

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/search")
def get_search_page(request: Request, articles=Depends(get_all_articles)):
    return templates.TemplateResponse("search.html", {"request": request, "articles": articles["data"]})


@router.get("/search/{article_type}")
def get_search_page(request: Request, articles=Depends(get_specific_articles)):
    return templates.TemplateResponse("search.html", {"request": request, "articles": articles["data"]})


@router.get("/registration")
def get_register_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.post("/registration")
async def register_user(request: Request, user_data: UserCreate, user_manager=Depends(get_user_manager)):
    try:
        await user_manager.create(user_data)
        return templates.TemplateResponse("registration.html", {"request": request})
    except Exception as e:
        return templates.TemplateResponse("registration.html", {"request": request, "error": str(e)})


@router.get("/sign-in")
def get_sign_in_page(request: Request):
    return templates.TemplateResponse("sign_in.html", {"request": request})


@router.post("/sign-in")
async def sign_in_user(request: Request, username: str, password: str, user_manager=Depends(get_user_manager)):
    try:
        user = await user_manager.authenticate(username=username, password=password)
        if user:
            # В случае успешного входа
            return templates.TemplateResponse("my_account.html", {"request": request, "username": user.username})
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/my-account")
async def my_account_page(request: Request, current_user=Depends(fastapi_users.current_user(active=True))):
    if current_user:
        return templates.TemplateResponse("my_account.html", {"request": request, "username": current_user.username})
    else:
        return templates.TemplateResponse("registration.html", {"request": request})

