from sqlalchemy.orm import mapper

from src.post.domain.model.post import Post
from src.post.infra.schema import posts


def start_post_mappers():
    mapper(Post, posts)
