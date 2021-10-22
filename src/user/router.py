from fastapi import APIRouter


router = APIRouter(
    prefix="/users"
)


@router.get("/hello")
def hello():
    return "Hello user"
