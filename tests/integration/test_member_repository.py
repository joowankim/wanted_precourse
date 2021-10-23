from assertpy import assert_that

from src.member.domain.model.member import Member
from src.member.infra.member_repository import MemberRepository


def test_get_by_id(session):
    member_id = 'member-1'
    nickname = 'jack'
    password = '123qwe'
    session.execute(
        "INSERT INTO members ('member_id', 'nickname', 'password') VALUES "
        f"(\'{member_id}\', \'{nickname}\', \'{password}\')"
    )

    repo = MemberRepository(session=session)
    actual = repo.get_by_id(member_id=member_id)
    expected = Member(
        member_id=member_id,
        nickname=nickname,
        password=password
    )
    assert_that(actual).is_equal_to(expected)


def test_add(session):
    repo = MemberRepository(session=session)
    member = Member(member_id="member-1", nickname="jack", password="123qwe")
    repo.add(member)

    actual = repo.get_by_id(member_id=member.member_id)
    expected = member
    assert_that(actual).is_equal_to(expected)


def test_exists_with_exist_nickname(session):
    member_id = 'member-1'
    nickname = 'jack'
    password = '123qwe'
    session.execute(
        "INSERT INTO members ('member_id', 'nickname', 'password') VALUES "
        f"(\'{member_id}\', \'{nickname}\', \'{password}\')"
    )

    repo = MemberRepository(session=session)
    actual = repo.exists(nickname=nickname)
    expected = True
    assert_that(actual).is_equal_to(expected)


def test_exists_with_non_exist_nickname(session):
    nickname = 'jack'

    repo = MemberRepository(session=session)
    actual = repo.exists(nickname=nickname)
    expected = False
    assert_that(actual).is_equal_to(expected)


def test_get_by_nickname(session):
    member_id = 'member-1'
    nickname = 'jack'
    password = '123qwe'
    session.execute(
        "INSERT INTO members ('member_id', 'nickname', 'password') VALUES "
        f"(\'{member_id}\', \'{nickname}\', \'{password}\')"
    )

    repo = MemberRepository(session=session)
    actual = repo.get_by_nickname(nickname=nickname)
    expected = Member(member_id=member_id, nickname=nickname, password=password)
    assert_that(actual).is_equal_to(expected)


def test_get_by_nickname_without_member(session):
    repo = MemberRepository(session=session)
    actual = repo.get_by_nickname(nickname="qweasd")
    expected = None
    assert_that(actual).is_equal_to(expected)

