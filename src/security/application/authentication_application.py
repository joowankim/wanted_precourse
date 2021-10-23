from fastapi import Depends
from jose import jwt

from src.config.app_config import JWT_SECRET, JWT_ALGORITHM
from src.member.domain.model.member_service import MemberService
from src.security.domain.exception import EmptyAuthTokenException
from src.security.domain.model.authentication_service import AuthenticationService
from src.security.domain.model.login_info import LoginInfo
from src.member.application.member_application import member_service


def authentication_service(service: MemberService = Depends(member_service)):
    return AuthenticationService(member_service=service)


class AuthenticationApplication:
    def __init__(self, service: AuthenticationService = Depends(authentication_service)):
        self.service = service
        self.secret = JWT_SECRET
        self.algorithm = JWT_ALGORITHM

    def login(self, login_info: LoginInfo) -> str:
        member = self.service.authenticate(login_info)
        token = jwt.encode(
            {
                "nickname": member.nickname
            },
            self.secret,
            algorithm=self.algorithm
        )
        return f"Bearer {token}"

    def decode(self, token: str) -> str:
        if not token:
            raise EmptyAuthTokenException
        token = token[len("Bearer "):]
        payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        return payload["nickname"]
