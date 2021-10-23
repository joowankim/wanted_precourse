from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.db_config import db_session
from src.post.domain.model.bulletin_board import BulletinBoard
from src.post.domain.model.post import Post
from src.post.domain.model.pre_published_post import PrePublishedPost
from src.post.domain.view_model.displayed_post import DisplayedPost
from src.post.infra.post_repository import PostRepository, AbstractPostRepository


def post_repository(session: Session = Depends(db_session)):
    return PostRepository(session=session)


def bulletin_board(repository: AbstractPostRepository = Depends(post_repository)):
    return BulletinBoard(repo=repository)


class PostApplication:
    def __init__(self, board: BulletinBoard = Depends(bulletin_board)):
        self.board = board

    def write(self, author: str, pre_post: PrePublishedPost):
        self.board.put(author=author, pre_post=pre_post)

    def get(self, post_id: str) -> DisplayedPost:
        return self.board.details(post_id=post_id).to_view_model()

    def list(self) -> List[DisplayedPost]:
        return [post.to_view_model() for post in self.board.get_all_posts()]

    def change(self, post_id: str, author: str, title: str, content: str):
        changed = Post(
            post_id=post_id,
            author=author,
            title=title,
            content=content
        )
        self.board.update(changed)

    def remove(self, post_id: str, member: str):
        self.board.delete(requester=member, post_id=post_id)
