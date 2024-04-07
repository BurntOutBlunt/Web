from datetime import datetime

from pydantic import BaseModel


class ArticleCreate(BaseModel):
    id: int
    title: str
    score: str
    instrument_type: str
    date: datetime
    type: str
