from src.member.infra.mapper import start_member_mappers
from src.post.infra.mapper import start_post_mappers


def start_mappers():
    start_member_mappers()
    start_post_mappers()
