import pytest

from src.member.domain.model.member_service import MemberService


@pytest.fixture
def member_service(member_repo):
    return MemberService(repo=member_repo)
