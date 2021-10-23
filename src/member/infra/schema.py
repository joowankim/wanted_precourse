from sqlalchemy import Column, String, Table

from src.config.db_config import metadata


members = Table(
    "members",
    metadata,
    Column("member_id", String, primary_key=True, index=True),
    Column("nickname", String, primary_key=True, index=True),
    Column("password", String)
)
