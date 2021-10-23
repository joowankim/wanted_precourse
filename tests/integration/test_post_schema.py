from assertpy import assert_that

from src.post.domain.model.post import Post


def test_retrieving_posts(session):
    session.execute(
        "INSERT INTO posts (post_id, author, title, content) VALUES "
        "('post-1', 'jack', 'json', 'json content'),"
        "('post-2', 'join', 'qwertt', 'qwert content'),"
        "('post-3', 'jack', 'sdafasdf', 'zxc content')"
    )

    actual = session.query(Post).all()
    expected = [
        Post(post_id='post-1', author='jack', title='json', content='json content'),
        Post(post_id='post-2', author='join', title='qwertt', content='qwert content'),
        Post(post_id='post-3', author='jack', title='sdafasdf', content='zxc content'),
    ]
    assert_that(actual).is_equal_to(expected)
