import pytest

from src.member.domain.model.member_service import MemberService
from src.post.domain.model.bulletin_board import BulletinBoard
from src.security.domain.model.authentication_service import AuthenticationService


@pytest.fixture
def member_service(member_repo):
    return MemberService(repo=member_repo)


@pytest.fixture
def authentication_service(member_service):
    return AuthenticationService(member_service=member_service)


@pytest.fixture
def bulletin_board(post_repo):
    return BulletinBoard(repo=post_repo)
