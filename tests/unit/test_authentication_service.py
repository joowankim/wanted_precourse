from assertpy import assert_that

from src.member.domain.model.membership_application import MembershipApplication
from src.security.domain.exception import NotExistMemberException, IncorrectPasswordException
from src.security.domain.model.authentication_service import AuthenticationService
from src.security.domain.model.login_info import LoginInfo


def test_authenticate_with_correct_login_info(member_service):
    application = MembershipApplication(nickname='jack', password='123qwe123')
    member_service.register(application)

    authentication_service = AuthenticationService(member_service=member_service)
    login_info = LoginInfo(nickname=application.nickname, password=application.password)

    actual = authentication_service.authenticate(login_info)
    assert_that(actual.nickname).is_equal_to(application.nickname)
    assert_that(actual.password).is_equal_to(application.password)


def test_authenticate_with_not_exist_nickname(member_service):
    login_info = LoginInfo(nickname='jack', password='123qwe123')
    authentication_service = AuthenticationService(member_service=member_service)

    assert_that(authentication_service.authenticate).raises(NotExistMemberException).when_called_with(login_info)


def test_authenticate_with_incorrect_password(member_service):
    application = MembershipApplication(nickname='jack', password='123qwe123')
    member_service.register(application)

    login_info = LoginInfo(nickname='jack', password='123qweqwe')
    authentication_service = AuthenticationService(member_service=member_service)

    assert_that(authentication_service.authenticate).raises(IncorrectPasswordException).when_called_with(login_info)


