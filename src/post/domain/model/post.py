from dataclasses import dataclass


@dataclass
class Post:
    post_id: str
    author: str
    title: str
    content: str
