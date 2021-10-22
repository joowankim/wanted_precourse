from fastapi import APIRouter


router = APIRouter(
    prefix="/members"
)


@router.get("/hello")
def hello():
    return "Hello member"
