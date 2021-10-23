from sqlalchemy.orm import mapper

from src.member.domain.model.member import Member
from src.member.infra.schema import members


def start_member_mappers():
    mapper(Member, members)
