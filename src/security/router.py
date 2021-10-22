from fastapi import APIRouter


router = APIRouter(
    prefix="/security",
    tags=["security"]
)


@router.get("/hello")
async def hello():
    return "Hello security"
