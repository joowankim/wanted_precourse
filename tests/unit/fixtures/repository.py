import pytest

from src.member.infra.member_repository import MemberRepository


@pytest.fixture
def member_repo(session):
    return MemberRepository(session=session)
