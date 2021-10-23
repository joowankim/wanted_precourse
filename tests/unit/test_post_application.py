from assertpy import assert_that

from src.post.application.post_application import PostApplication
from src.post.domain.exception import NotExistPostException, NonAuthorException
from src.post.domain.model.post import Post
from src.post.domain.model.pre_published_post import PrePublishedPost


def test_get_with_exist_post(bulletin_board):
    application = PostApplication(board=bulletin_board)
    author = "javkc"
    pre_post = PrePublishedPost(title="title", content="content")
    application.write(author=author, pre_post=pre_post)

    actual = application.list()[0]
    assert_that(actual.author).is_equal_to(author)
    assert_that(actual.title).is_equal_to(pre_post.title)
    assert_that(actual.content).is_equal_to(pre_post.content)


def test_get_with_not_exist_post(bulletin_board):
    application = PostApplication(board=bulletin_board)
    author = "javkc"
    pre_post = PrePublishedPost(title="title", content="content")
    application.write(author=author, pre_post=pre_post)

    not_exist_post_id = "post-2"
    assert_that(application.get).raises(NotExistPostException).when_called_with(not_exist_post_id)


def test_write(bulletin_board):
    application = PostApplication(board=bulletin_board)
    author = "javkc"
    pre_post = PrePublishedPost(title="title", content="content")
    application.write(author=author, pre_post=pre_post)

    actual = application.list()[0]
    assert_that(actual.author).is_equal_to(author)
    assert_that(actual.title).is_equal_to(pre_post.title)
    assert_that(actual.content).is_equal_to(pre_post.content)


def test_list(bulletin_board):
    application = PostApplication(board=bulletin_board)
    author1, author2 = "jack", "johi"
    pre_post1 = PrePublishedPost(title="title", content="content")
    pre_post2 = PrePublishedPost(title="asdfasf", content="asdfaf")

    application.write(author=author1, pre_post=pre_post1)
    application.write(author=author2, pre_post=pre_post1)
    application.write(author=author1, pre_post=pre_post2)
    application.write(author=author2, pre_post=pre_post2)

    actual = application.list()
    assert_that(len(actual)).is_equal_to(4)


def test_change_with_exist_post(bulletin_board):
    application = PostApplication(board=bulletin_board)
    author = "javkc"
    pre_post = PrePublishedPost(title="title", content="content")
    application.write(author=author, pre_post=pre_post)

    post = application.list()[0]
    changed = Post(post_id=post.post_id, author=author, title="asdfsafd", content="asdfafs")
    application.change(post_id=changed.post_id, author=changed.author, title=changed.title, content=changed.content)

    actual = application.get(post_id=changed.post_id)
    expected = changed
    assert_that(actual.title).is_equal_to(expected.title)
    assert_that(actual.content).is_equal_to(expected.content)


def test_change_with_changed_include_none(bulletin_board):
    application = PostApplication(board=bulletin_board)
    author = "javkc"
    pre_post = PrePublishedPost(title="title", content="content")
    application.write(author=author, pre_post=pre_post)

    post = application.list()[0]
    changed = Post(post_id=post.post_id, author=author, title="asdfsafd", content=None)
    application.change(post_id=changed.post_id, author=changed.author, title=changed.title, content=changed.content)

    actual = application.get(post_id=changed.post_id)
    expected = changed
    assert_that(actual.title).is_equal_to(expected.title)
    assert_that(actual.content).is_not_none()


def test_change_with_not_exist_post(bulletin_board):
    application = PostApplication(board=bulletin_board)
    changed = Post(post_id="post-1", author="adsf", title="asdfsafd", content="asdfafs")
    assert_that(application.change)\
        .raises(NotExistPostException)\
        .when_called_with(post_id=changed.post_id, author=changed.author, title=changed.title, content=changed.content)


def test_remove_with_author(bulletin_board):
    application = PostApplication(board=bulletin_board)
    author = "javkc"
    pre_post = PrePublishedPost(title="title", content="content")
    application.write(author=author, pre_post=pre_post)

    post = application.list()[0]
    application.remove(member=author, post_id=post.post_id)

    posts = application.list()
    assert_that(len(posts)).is_equal_to(0)


def test_remove_with_non_author(bulletin_board):
    application = PostApplication(board=bulletin_board)
    author = "javkc"
    pre_post = PrePublishedPost(title="title", content="content")
    application.write(author=author, pre_post=pre_post)

    post = application.list()[0]
    non_author = "asdfasf"
    assert_that(application.remove)\
        .raises(NonAuthorException)\
        .when_called_with(member=non_author, post_id=post.post_id)
