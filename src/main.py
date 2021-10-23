from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from . import post
from . import member
from .config.db_config import engine, metadata
from .config.table_mapper_config import start_mappers
from .member.domain.exception import DuplicatedNicknameException

metadata.create_all(bind=engine)
start_mappers()

app = FastAPI()
app.include_router(post.router)
app.include_router(member.router)


@app.exception_handler(DuplicatedNicknameException)
def duplicated_nickname_exception_handler(request: Request, exc: DuplicatedNicknameException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": "nickname is duplicated"}
    )


