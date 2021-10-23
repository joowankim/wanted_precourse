from pydantic import BaseModel


class DisplayedPost(BaseModel):
    post_id: str
    author: str
    title: str
    content: str
