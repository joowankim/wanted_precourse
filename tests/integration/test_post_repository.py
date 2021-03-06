from assertpy import assert_that

from src.post.domain.model.post import Post
from src.post.infra.exception import DoesNotExistException
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


def test_update_to_with_changed(session):
    session.execute(
        "INSERT INTO posts (post_id, author, title, content) VALUES "
        "('post-1', 'jack', 'json', 'json content'),"
        "('post-2', 'join', 'qwertt', 'qwert content'),"
        "('post-3', 'jack', 'sdafasdf', 'zxc content')"
    )
    repo = PostRepository(session=session)
    changed = Post(post_id='post-1', author='jack', title='jsasdfasfdon', content='json content')
    repo.update_to(changed)

    actual = repo.get_by_id(post_id=changed.post_id)
    expected = changed
    assert_that(actual).is_equal_to(expected)


def test_update_to_with_not_exist_post(session):
    repo = PostRepository(session=session)
    not_exist_post = Post(post_id='post-1', author='jack', title='jsasdfasfdon', content='json content')

    assert_that(repo.update_to).raises(DoesNotExistException).when_called_with(not_exist_post)


def test_delete_with_exist_post(session):
    session.execute(
        "INSERT INTO posts (post_id, author, title, content) VALUES "
        "('post-1', 'jack', 'json', 'json content'),"
        "('post-2', 'join', 'qwertt', 'qwert content'),"
        "('post-3', 'jack', 'sdafasdf', 'zxc content')"
    )
    repo = PostRepository(session=session)
    repo.delete(post_id='post-1')

    actual = repo.get_all()
    expected = [
        Post(post_id='post-2', author='join', title='qwertt', content='qwert content'),
        Post(post_id='post-3', author='jack', title='sdafasdf', content='zxc content'),
    ]
    assert_that(actual).is_equal_to(expected)
