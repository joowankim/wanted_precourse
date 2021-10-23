from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from src.post.domain.view_model.displayed_post import DisplayedPost


@dataclass
class Post:
    post_id: str
    author: str
    title: Optional[str]
    content: Optional[str]

    def apply_to(self, current: Post) -> Post:
        return Post(
            post_id=self.post_id,
            author=self.author,
            title=self.title if self.title is not None else current.title,
            content=self.content if self.content is not None else current.content
        )

    def to_view_model(self) -> DisplayedPost:
        return DisplayedPost(
            post_id=self.post_id,
            author=self.author,
            title=self.title,
            content=self.content
        )
