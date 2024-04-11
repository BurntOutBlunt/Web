import time

from src.articles.models import article
from src.articles.schemas import ArticleCreate
from src.database import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/articles",
    tags=["Article"]
)


@router.get("/long_article")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "Много много данных, которые вычислялись сто лет"


@router.get("")
async def get_specific_articles(
        article_type: str,
        session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(article).where(article.c.type == article_type)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.all(),
            "details": None
        }
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.get("")
async def get_all_articles(
        session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(article)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.all(),
            "details": None
        }
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post("")
async def add_specific_articles(new_article: ArticleCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(article).values(**new_article.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/main")
async def main(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(1))
    return result.all()
