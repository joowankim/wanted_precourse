from fastapi import FastAPI
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

from . import post, security, member
from .config.db_config import engine, metadata
from .config.table_mapper_config import start_mappers
from .member.domain.exception import DuplicatedNicknameException
from .security.domain.exception import NotExistMemberException, IncorrectPasswordException

metadata.create_all(bind=engine)
start_mappers()

app = FastAPI()
app.include_router(post.router)
app.include_router(member.router)
app.include_router(security.router)


@app.exception_handler(ValidationError)
def validation_error_handler(request: Request, exc: ValidationError):
    return PlainTextResponse(str(exc), status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(DuplicatedNicknameException)
def duplicated_nickname_exception_handler(request: Request, exc: DuplicatedNicknameException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": "nickname is duplicated"}
    )


@app.exception_handler(NotExistMemberException)
def not_exist_member_exception_handler(request: Request, exc: NotExistMemberException):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)


@app.exception_handler(IncorrectPasswordException)
def incorrect_password_exception_handler(request: Request, exc: IncorrectPasswordException):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)
