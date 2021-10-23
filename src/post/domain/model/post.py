from dataclasses import dataclass

from src.post.domain.view_model.displayed_post import DisplayedPost


@dataclass
class Post:
    post_id: str
    author: str
    title: str
    content: str

    def to_view_model(self) -> DisplayedPost:
        return DisplayedPost(
            post_id=self.post_id,
            author=self.author,
            title=self.title,
            content=self.content
        )
