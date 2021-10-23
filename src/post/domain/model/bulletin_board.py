import uuid
from typing import List

from src.post.domain.exception import NotExistPostException, NonAuthorException
from src.post.domain.model.post import Post
from src.post.domain.model.pre_published_post import PrePublishedPost
from src.post.infra.exception import DoesNotExistException
from src.post.infra.post_repository import AbstractPostRepository


class BulletinBoard:
    def __init__(self, repo: AbstractPostRepository):
        self.posts = repo

    @staticmethod
    def generate_post_id() -> str:
        return "post-" + str(uuid.uuid4())

    def put(self, author: str, pre_post: PrePublishedPost) -> None:
        post = Post(
            post_id=BulletinBoard.generate_post_id(),
            author=author,
            title=pre_post.title,
            content=pre_post.content
        )
        self.posts.add(post)

    def details(self, post_id: str) -> Post:
        post = self.posts.get_by_id(post_id=post_id)
        if post:
            return post
        else:
            raise NotExistPostException

    def get_all_posts(self) -> List[Post]:
        return self.posts.get_all()

    def update(self, changed: Post) -> None:
        current = self.posts.get_by_id(post_id=changed.post_id)
        if not current:
            raise NotExistPostException
        if current.author != changed.author:
            raise NonAuthorException
        latest = changed.apply_to(current)
        self.posts.update_to(latest)

    def delete(self, requester: str, post_id: str) -> None:
        target = self.posts.get_by_id(post_id=post_id)
        if not target:
            raise NotExistPostException
        if requester != target.author:
            raise NonAuthorException
        self.posts.delete(post_id=target.post_id)
