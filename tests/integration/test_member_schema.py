from assertpy import assert_that

from src.member.domain.model.member import Member


def test_add_member(session):
    session.execute(
        "INSERT INTO members (member_id, nickname, password) VALUES "
        "('member-1', 'john', '123qwe'),"
        "('member-2', 'asm', '123qwe'),"
        "('member-3', 'qwaszx', '123qwe')"
    )

    actual = session.query(Member).all()
    expected = [
        Member(member_id='member-1', nickname='john', password='123qwe'),
        Member(member_id='member-2', nickname='asm', password='123qwe'),
        Member(member_id='member-3', nickname='qwaszx', password='123qwe'),
    ]

    assert_that(actual).is_equal_to(expected)
