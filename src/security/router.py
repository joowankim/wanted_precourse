from fastapi import APIRouter, Depends
from starlette import status

from src.security.application.authentication_application import AuthenticationApplication, authentication_service
from src.security.domain.model.authentication_service import AuthenticationService
from src.security.domain.model.license import License
from src.security.domain.model.login_info import LoginInfo

router = APIRouter(
    prefix="/security",
    tags=["security"]
)


@router.get("/hello")
async def hello():
    return "Hello security"


def authentication_application(service: AuthenticationService = Depends(authentication_service)):
    return AuthenticationApplication(service=service)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=License)
def login_member(login_info: LoginInfo, application: AuthenticationApplication = Depends(authentication_application)):
    return License(auth=application.login(login_info=login_info))
