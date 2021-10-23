from sqlalchemy import Column, String, Table
from sqlalchemy.orm import mapper

from src.config.db_config import metadata
from src.member.domain.model.member import Member


members = Table(
    "members",
    metadata,
    Column("member_id", String, primary_key=True, index=True),
    Column("nickname", String),
    Column("password", String)
)


def start_member_mappers():
    mapper(Member, members)
