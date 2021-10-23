from assertpy import assert_that
from jose import jwt

from src.config.app_config import JWT_SECRET
from src.member.domain.model.membership_application import MembershipApplication
from src.security.application.authentication_application import AuthenticationApplication
from src.security.domain.exception import IncorrectPasswordException, NotExistMemberException
from src.security.domain.model.login_info import LoginInfo


def test_login_with_correct_login_info(member_service, authentication_service):
    application = MembershipApplication(nickname='jack', password='123qwe123')
    member_service.register(application)
    login_info = LoginInfo(nickname='jack', password='123qwe123')
    member = authentication_service.authenticate(login_info=login_info)

    application = AuthenticationApplication(service=authentication_service)

    actual = application.login(login_info=login_info)
    expected = "Bearer " + jwt.encode(
        {
            "member_id": member.member_id,
            "nickname": member.nickname
        },
        JWT_SECRET,
        algorithm="HS256"
    )

    assert_that(actual).is_equal_to(expected)


def test_login_with_non_exist_member(authentication_service):
    login_info = LoginInfo(nickname='jack', password='123qwe111')
    application = AuthenticationApplication(service=authentication_service)

    assert_that(application.login).raises(NotExistMemberException).when_called_with(login_info)


def test_login_with_incorrect_password(member_service, authentication_service):
    application = MembershipApplication(nickname='jack', password='123qwe123')
    member_service.register(application)
    login_info = LoginInfo(nickname='jack', password='123qwe111')
    application = AuthenticationApplication(service=authentication_service)

    assert_that(application.login).raises(IncorrectPasswordException).when_called_with(login_info)
