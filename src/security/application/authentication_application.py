from fastapi import Depends
from jose import jwt

from src.config.app_config import JWT_SECRET
from src.member.domain.model.member_service import MemberService
from src.security.domain.model.authentication_service import AuthenticationService
from src.security.domain.model.login_info import LoginInfo
from src.member.application.member_application import member_service


def authentication_service(service: MemberService = Depends(member_service)):
    return AuthenticationService(member_service=service)


class AuthenticationApplication:
    def __init__(self, service: AuthenticationService = Depends(authentication_service)):
        self.service = service

    def login(self, login_info: LoginInfo) -> str:
        member = self.service.authenticate(login_info)
        token = jwt.encode(
            {
                "member_id": member.member_id,
                "nickname": member.nickname
            },
            JWT_SECRET,
            algorithm="HS256"
        )
        return f"Bearer {token}"

