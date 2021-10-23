import pytest

from src.member.infra.member_repository import MemberRepository
from src.post.infra.post_repository import PostRepository


@pytest.fixture
def member_repo(session):
    return MemberRepository(session=session)


@pytest.fixture
def post_repo(session):
    return PostRepository(session=session)
