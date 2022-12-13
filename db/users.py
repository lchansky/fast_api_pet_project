from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime

from .base import metadata
import datetime

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
    Column("email", String, primary_key=True, unique=True),
    Column("name", String),
    Column("password", String),
    Column("is_company", Boolean),
    Column("created_at", DateTime, default=datetime.datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.datetime.utcnow),
)
