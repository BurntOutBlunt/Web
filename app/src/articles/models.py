from src.database import metadata
from sqlalchemy import TIMESTAMP, Column, Integer, String, Table

article = Table(
    "article",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("score", String),
    Column("instrument_type", String, nullable=True),
    Column("date", TIMESTAMP),
    Column("type", String),
)