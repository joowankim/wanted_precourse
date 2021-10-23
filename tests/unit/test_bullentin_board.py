from assertpy import assert_that

from src.post.domain.exception import NotExistPostException, NonAuthorException
from src.post.domain.model.bulletin_board import BulletinBoard
from src.post.domain.model.post import Post
from src.post.domain.model.pre_published_post import PrePublishedPost


def test_get_with_exist_post(post_repo):
    bulletin_board = BulletinBoard(repo=post_repo)
    author = "jack"
    pre_post = PrePublishedPost(title="title", content="content")
    bulletin_board.put(author=author, pre_post=pre_post)

    post = post_repo.get_all()[0]
    actual = bulletin_board.details(post_id=post.post_id)
    expected = Post(post_id=post.post_id, author=author, title=pre_post.title, content=pre_post.content)
    assert_that(actual).is_equal_to(expected)


def test_get_with_not_exist_post(post_repo):
    bulletin_board = BulletinBoard(repo=post_repo)
    author = "jack"
    pre_post = PrePublishedPost(title="title", content="content")
    bulletin_board.put(author=author, pre_post=pre_post)

    not_exist_post_id = "post-2"
    assert_that(bulletin_board.details).raises(NotExistPostException).when_called_with(not_exist_post_id)


def test_get_all_posts(post_repo):
    bulletin_board = BulletinBoard(repo=post_repo)
    author1, author2 = "jack", "johi"
    pre_post1 = PrePublishedPost(title="title", content="content")
    pre_post2 = PrePublishedPost(title="asdfasf", content="asdfaf")

    bulletin_board.put(author=author1, pre_post=pre_post1)
    bulletin_board.put(author=author2, pre_post=pre_post1)
    bulletin_board.put(author=author1, pre_post=pre_post2)
    bulletin_board.put(author=author2, pre_post=pre_post2)

    all_posts = bulletin_board.get_all_posts()
    assert_that(len(all_posts)).is_equal_to(4)


def test_update_with_changed(post_repo):
    bulletin_board = BulletinBoard(repo=post_repo)
    author = "jack"
    pre_post = PrePublishedPost(title="title", content="content")
    bulletin_board.put(author=author, pre_post=pre_post)

    post = bulletin_board.get_all_posts()[0]
    changed = Post(post_id=post.post_id, author=author, title="123123", content="asdqwesad")
    bulletin_board.update(changed)

    actual = bulletin_board.details(post_id=changed.post_id)
    expected = changed
    assert_that(actual).is_equal_to(expected)


def test_update_with_not_exist_post(post_repo):
    bulletin_board = BulletinBoard(repo=post_repo)
    not_exist_post = Post(post_id="post-1", author="adsaf", title="asdfadsf", content="content")

    assert_that(bulletin_board.update)\
        .raises(NotExistPostException)\
        .when_called_with(not_exist_post)


def test_delete_with_exist_post(post_repo):
    bulletin_board = BulletinBoard(repo=post_repo)
    author1, author2 = "jack", "johi"
    pre_post1 = PrePublishedPost(title="title", content="content")
    pre_post2 = PrePublishedPost(title="asdfasf", content="asdfaf")

    bulletin_board.put(author=author1, pre_post=pre_post1)
    bulletin_board.put(author=author2, pre_post=pre_post1)
    bulletin_board.put(author=author1, pre_post=pre_post2)
    bulletin_board.put(author=author2, pre_post=pre_post2)

    posts = bulletin_board.get_all_posts()
    target = posts[0]

    bulletin_board.delete(requester=target.author, post_id=target.post_id)
    actual = bulletin_board.get_all_posts()
    assert_that(actual).does_not_contain(target)


def test_delete_with_not_exist_post(post_repo):
    bulletin_board = BulletinBoard(repo=post_repo)
    not_exist_post = Post(post_id="post-1", author="adsaf", title="asdfadsf", content="content")

    assert_that(bulletin_board.delete)\
        .raises(NotExistPostException)\
        .when_called_with(requester=not_exist_post.author, post_id=not_exist_post.post_id)


def test_update_with_non_author(post_repo):
    bulletin_board = BulletinBoard(repo=post_repo)
    author = "jack"
    pre_post = PrePublishedPost(title="title", content="content")
    bulletin_board.put(author=author, pre_post=pre_post)

    post = bulletin_board.get_all_posts()[0]
    changed = Post(post_id=post.post_id, author="other author", title="123123", content="asdqwesad")

    assert_that(bulletin_board.update).raises(NonAuthorException).when_called_with(changed)


def test_delete_with_non_author(post_repo):
    bulletin_board = BulletinBoard(repo=post_repo)
    author = "jack"
    pre_post = PrePublishedPost(title="title", content="content")
    bulletin_board.put(author=author, pre_post=pre_post)

    post = bulletin_board.get_all_posts()[0]
    other = "asdfafasfdsa"
    assert_that(bulletin_board.delete)\
        .raises(NonAuthorException)\
        .when_called_with(requester=other, post_id=post.post_id)

