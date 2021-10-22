from fastapi import APIRouter


router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("/hello")
async def hello():
    return "Hello post"
