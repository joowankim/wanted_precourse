import uuid
from dataclasses import dataclass

from pydantic import BaseModel
from typing import Dict


@dataclass(frozen=True)
class Document:
    title: str
    content: str


class Post(BaseModel):
    post_id: str
    author_name: str
    document: Document
    is_deleted: bool = False

    def apply(self, changes: Document) -> None:
        self.document = changes


@dataclass(frozen=True)
class BulletinBoard:
    posts: Dict[str, Post]

    @staticmethod
    def generate_post_id() -> str:
        return "post-" + str(uuid.uuid4())

    def add(self, post: Post) -> None:
        self.posts[post.post_id] = post

    def update(self, post: Post) -> None:
        self.posts[post.post_id] = post

    def delete(self, post: Post) -> None:
        del self.posts[post.post_id]


board = BulletinBoard(posts=dict())


@dataclass(frozen=True)
class Author:
    user_id: str
    name: str

    def write(self, document: Document) -> None:
        post_id = BulletinBoard.generate_post_id()
        board.add(
            Post(
                post_id=post_id,
                author_name=self.name,
                document=document
            )
        )

    def update(self, post: Post, changes: Document) -> None:
        if post.author_name == self.name:
            post.apply(changes)
            board.update(post)
            # publish post updated event
        else:
            raise Exception

    def delete(self, post: Post) -> None:
        if post.author_name == self.name:
            board.delete(post)
            # publish post deleted event
        else:
            raise Exception
