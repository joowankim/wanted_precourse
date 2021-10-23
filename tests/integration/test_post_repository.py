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


def test_add(session):
    repo = PostRepository(session=session)
    post = Post(post_id="post-1", author="jack", title="asdfasdf", content="zcxasdf")
    repo.add(post)

