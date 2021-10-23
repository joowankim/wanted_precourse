from assertpy import assert_that

from src.member.domain.exception import DuplicatedNicknameException, MemberNotFoundException
from src.member.domain.model.member_service import MemberService
from src.member.domain.model.membership_application import MembershipApplication


def test_register_member(member_repo):
    member_service = MemberService(repo=member_repo)
    application = MembershipApplication(nickname="John", password="123qwe")
    member_service.register(application)


def test_register_member_with_duplicated_nickname(member_repo):
    member_service = MemberService(repo=member_repo)
    application = MembershipApplication(nickname="John", password="123qwe")
    member_service.register(application)

    assert_that(member_service.register).raises(DuplicatedNicknameException).when_called_with(application)


def test_get_member_with_exist_member(member_repo):
    member_service = MemberService(repo=member_repo)
    application = MembershipApplication(nickname="John", password="123qwe")
    member_service.register(application)

    actual = member_service.get_member(nickname=application.nickname)
    assert_that(actual.nickname).is_equal_to(application.nickname)
    assert_that(actual.password).is_equal_to(application.password)


def test_get_member_without_exist_member(member_repo):
    member_service = MemberService(repo=member_repo)
    application = MembershipApplication(nickname="John", password="123qwe")

    assert_that(member_service.get_member).raises(MemberNotFoundException).when_called_with(application.nickname)

