from typing import Optional

from fastapi import APIRouter, Depends, Body
from fastapi_pagination import Page, paginate
from starlette import status

from src.post.application.post_application import PostApplication, bulletin_board
from src.post.domain.model.bulletin_board import BulletinBoard
from src.post.domain.model.post import Post
from src.post.domain.model.pre_published_post import PrePublishedPost
from src.post.domain.view_model.displayed_post import DisplayedPost
from src.security.router import authorize

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


def post_application(board: BulletinBoard = Depends(bulletin_board)):
    return PostApplication(board)


@router.post("", status_code=status.HTTP_201_CREATED)
def write_post(
        pre_post: PrePublishedPost,
        application: PostApplication = Depends(post_application),
        author: str = Depends(authorize)
):
    application.write(author=author, pre_post=pre_post)


@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=DisplayedPost)
def get_details(
        post_id: str,
        application: PostApplication = Depends(post_application)
):
    return application.get(post_id=post_id)


@router.get("", status_code=status.HTTP_200_OK, response_model=Page[DisplayedPost])
def get_posts(application: PostApplication = Depends(post_application)):
    return paginate(application.list())


@router.patch("/{post_id}", status_code=status.HTTP_200_OK)
def update_post(
        post_id: str,
        title: Optional[str] = Body(...),
        content: Optional[str] = Body(...),
        application: PostApplication = Depends(post_application),
        author: str = Depends(authorize)
):
    application.change(post_id=post_id, author=author, title=title, content=content)
