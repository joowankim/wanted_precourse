import uuid
from dataclasses import dataclass

from pydantic import BaseModel
from typing import Dict, List


@dataclass(frozen=True)
class Document:
    title: str
    content: str


class Post(BaseModel):
    post_id: str
    pen_name: str
    document: Document

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

    def get_all_posts(self) -> List[Post]:
        return list(self.posts.values())

    def get(self, post_id: str):
        return self.posts[post_id]


@dataclass(frozen=True)
class Author:
    member_id: str
    pen_name: str
    board: BulletinBoard

    def write(self, document: Document) -> None:
        post_id = BulletinBoard.generate_post_id()
        self.board.add(
            Post(
                post_id=post_id,
                pen_name=self.pen_name,
                document=document
            )
        )

    def update(self, post: Post, changes: Document) -> None:
        if post.pen_name == self.pen_name:
            post.apply(changes)
            self.board.update(post)
            # publish post updated event
        else:
            raise Exception

    def delete(self, post: Post) -> None:
        if post.pen_name == self.pen_name:
            self.board.delete(post)
            # publish post deleted event
        else:
            raise Exception

