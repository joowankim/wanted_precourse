from assertpy import assert_that
from jose import jwt, JWTError

from src.config.app_config import JWT_SECRET
from src.member.domain.model.membership_application import MembershipApplication
from src.security.application.authentication_application import AuthenticationApplication
from src.security.domain.exception import IncorrectPasswordException, NotExistMemberException, EmptyAuthTokenException
from src.security.domain.model.login_info import LoginInfo


def test_login_with_correct_login_info(member_service, authentication_service):
    membership_application = MembershipApplication(nickname='jack', password='123qwe123')
    member_service.register(membership_application)
    login_info = LoginInfo(nickname='jack', password='123qwe123')
    member = authentication_service.authenticate(login_info=login_info)

    application = AuthenticationApplication(service=authentication_service)

    actual = application.login(login_info=login_info)
    expected = "Bearer " + jwt.encode(
        {
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
    membership_application = MembershipApplication(nickname='jack', password='123qwe123')
    member_service.register(membership_application)
    login_info = LoginInfo(nickname='jack', password='123qwe111')
    application = AuthenticationApplication(service=authentication_service)

    assert_that(application.login).raises(IncorrectPasswordException).when_called_with(login_info)


def test_decode_with_token(member_service, authentication_service):
    membership_application = MembershipApplication(nickname='jack', password='123qwe123')
    member_service.register(membership_application)
    login_info = LoginInfo(nickname='jack', password='123qwe123')
    member = authentication_service.authenticate(login_info=login_info)

    application = AuthenticationApplication(service=authentication_service)
    token = application.login(login_info=login_info)

    actual = application.decode(token)
    expected = member.nickname
    assert_that(actual).is_equal_to(expected)


def test_decode_with_incorrect_token(authentication_service):
    application = AuthenticationApplication(service=authentication_service)
    incorrect_token = "asdfasdfasfafads"

    assert_that(application.decode).raises(JWTError).when_called_with(incorrect_token)


def test_decode_without_token(authentication_service):
    application = AuthenticationApplication(service=authentication_service)
    nonetype_token = None

    assert_that(application.decode).raises(EmptyAuthTokenException).when_called_with(nonetype_token)


def test_decode_with_empty_string_token(authentication_service):
    application = AuthenticationApplication(service=authentication_service)
    empty_token = ""

    assert_that(application.decode).raises(EmptyAuthTokenException).when_called_with(empty_token)
