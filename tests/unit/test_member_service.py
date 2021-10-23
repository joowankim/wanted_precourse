from assertpy import assert_that

from src.member.domain.model.member_service import MemberService
from src.member.domain.model.membership_application import MembershipApplication


def test_register_member(member_repo):
    member_service = MemberService(repo=member_repo)
    application = MembershipApplication(nickname="John", password="123qwe")
    member_service.register(application)

    # todo: check member created event


def test_register_member_with_duplicated_nickname(member_repo):
    member_service = MemberService(repo=member_repo)
    application = MembershipApplication(nickname="John", password="123qwe")
    member_service.register(application)

    assert_that(member_service.register).raises(Exception).when_called_with(application)

