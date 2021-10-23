from assertpy import assert_that

from src.post.application.post_application import PostApplication
from src.post.domain.exception import NotExistPostException
from src.post.domain.model.post import Post


def test_get_with_exist_post(bulletin_board):
    application = PostApplication(board=bulletin_board)
    post = Post(post_id="post-1", author="javkc", title="title", content="conent")
    application.write(post)

    actual = application.get(post_id=post.post_id)
    expected = post
    assert_that(actual).is_equal_to(expected)


def test_get_with_not_exist_post(bulletin_board):
    application = PostApplication(board=bulletin_board)
    post = Post(post_id="post-1", author="javkc", title="title", content="conent")
    application.write(post)

    not_exist_post_id = "post-2"
    assert_that(application.get).raises(NotExistPostException).when_called_with(not_exist_post_id)


def test_write(bulletin_board):
    application = PostApplication(board=bulletin_board)
    post = Post(post_id="post-1", author="javkc", title="title", content="conent")
    application.write(post)
