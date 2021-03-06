from fastapi import FastAPI
from fastapi_pagination import add_pagination
from jose import JWTError
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

from . import post, security, member
from .config.db_config import engine, metadata
from .config.table_mapper_config import start_mappers
from .member.domain.exception import DuplicatedNicknameException
from .post.domain.exception import NotExistPostException, NonAuthorException
from .security.domain.exception import NotExistMemberException, IncorrectPasswordException, EmptyAuthTokenException

metadata.create_all(bind=engine)
start_mappers()

app = FastAPI()
app.include_router(post.router)
app.include_router(member.router)
app.include_router(security.router)

add_pagination(app)


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


@app.exception_handler(JWTError)
def jwt_error_handler(request: Request, exc: JWTError):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)


@app.exception_handler(EmptyAuthTokenException)
def empty_auth_token_handler(request: Request, exc: EmptyAuthTokenException):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)


@app.exception_handler(NotExistPostException)
def not_exist_post_exception_handler(request: Request, exc: NotExistPostException):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(NonAuthorException)
def non_author_exception_handler(request: Request, exc: NonAuthorException):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)
