import uuid

from src.post.domain.exception import NotExistPostException
from src.post.domain.model.post import Post
from src.post.domain.model.pre_published_post import PrePublishedPost
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

    # def update(self, post: Post) -> None:
    #     self.posts[post.post_id] = post
    #
    # def delete(self, post: Post) -> None:
    #     del self.posts[post.post_id]
    #
    # def get_all_posts(self) -> List[Post]:
    #     return list(self.posts.values())
