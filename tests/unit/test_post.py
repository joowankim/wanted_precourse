from assertpy import assert_that

from src.post.domain.model import Document, Author, BulletinBoard


def test_add_post():
    board = BulletinBoard(posts=dict())
    author = Author(member_id="1", pen_name="john", board=board)
    document = Document(title="title", content="description")

    author.write(document)
    # todo: check post created event

    actual_posts = board.get_all_posts()
    expected_posts_length = 1
    assert_that(len(actual_posts)).is_equal_to(expected_posts_length)

    actual_post = actual_posts[0]
    expected_document = document
    expected_pen_name = author.pen_name
    assert_that(actual_post.pen_name).is_equal_to(expected_pen_name)
    assert_that(actual_post.document.title).is_equal_to(expected_document.title)
    assert_that(actual_post.document.content).is_equal_to(expected_document.content)


def test_post_updated_by_author():
    board = BulletinBoard(posts=dict())
    author = Author(member_id="1", pen_name="john", board=board)
    document = Document(title="title", content="description")

    author.write(document)
    post = board.get_all_posts()[0]

    changes = Document(title="title", content="content")
    author.update(post, changes)
    # todo: check post updated event

    actual_document = board.posts[post.post_id].document
    expected_document = changes
    assert_that(actual_document).is_equal_to(expected_document)


def test_post_updated_by_other_user():
    board = BulletinBoard(posts=dict())
    author = Author(member_id="1", pen_name="john", board=board)
    document = Document(title="title", content="description")

    author.write(document)
    post = board.get_all_posts()[0]

    other = Author(member_id="2", pen_name="kim", board=board)
    changes = Document(title="title", content="desdesdes")
    assert_that(other.update).raises(Exception).when_called_with(post, changes)


def test_post_deleted_by_author():
    board = BulletinBoard(posts=dict())
    author = Author(member_id="1", pen_name="john", board=board)
    document = Document(title="title", content="description")

    author.write(document)
    post = board.get_all_posts()[0]

    author.delete(post)
    # todo: check post deleted event

    actual_posts = board.get_all_posts()
    expected_posts = []
    assert_that(actual_posts).is_equal_to(expected_posts)


def test_post_deleted_by_other_user():
    board = BulletinBoard(posts=dict())
    author = Author(member_id="1", pen_name="john", board=board)
    document = Document(title="title", content="description")

    author.write(document)
    post = board.get_all_posts()[0]

    other = Author(member_id="2", pen_name="kim", board=board)
    assert_that(other.delete).raises(Exception).when_called_with(post)
