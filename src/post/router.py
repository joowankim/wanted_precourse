from fastapi import APIRouter, Depends
from starlette import status

from src.post.application.post_application import PostApplication, bulletin_board
from src.post.domain.model.bulletin_board import BulletinBoard
from src.post.domain.model.pre_published_post import PrePublishedPost
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
