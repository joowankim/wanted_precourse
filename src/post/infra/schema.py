from sqlalchemy import Column, String, ForeignKey, Table

from src.config.db_config import metadata

posts = Table(
    "posts",
    metadata,
    Column("post_id", String, primary_key=True),
    Column("author", ForeignKey('members.nickname')),
    Column("title", String),
    Column("content", String)
)

