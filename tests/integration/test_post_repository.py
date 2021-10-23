from assertpy import assert_that

from src.post.domain.model.post import Post
from src.post.infra.post_repository import PostRepository


def test_get_by_id(session):
    repo = PostRepository(session=session)
    post = Post(post_id="post-1", author="jack", title="asdfasdf", content="zcxasdf")
    repo.add(post)

    actual = repo.get_by_id(post.post_id)
    expected = post
    assert_that(actual).is_equal_to(expected)


def test_get_by_id_with_not_exist_post_id(session):
    repo = PostRepository(session=session)
    non_exist = "post-1"
    actual = repo.get_by_id(post_id=non_exist)
    expected = None
    assert_that(actual).is_equal_to(expected)


def test_get_all(session):
    session.execute(
        "INSERT INTO posts (post_id, author, title, content) VALUES "
        "('post-1', 'jack', 'json', 'json content'),"
        "('post-2', 'join', 'qwertt', 'qwert content'),"
        "('post-3', 'jack', 'sdafasdf', 'zxc content')"
    )
    repo = PostRepository(session=session)

    actual = repo.get_all()
    expected = [
        Post(post_id='post-1', author='jack', title='json', content='json content'),
        Post(post_id='post-2', author='join', title='qwertt', content='qwert content'),
        Post(post_id='post-3', author='jack', title='sdafasdf', content='zxc content'),
    ]
    assert_that(actual).is_equal_to(expected)
