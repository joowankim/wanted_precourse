from dataclasses import dataclass

from src.member.domain.model import MemberService


@dataclass(frozen=True)
class LoginInfo:
    email: str
    password: str


class AuthenticationService:
    member_service: MemberService

    def authenticate(self, login_info: LoginInfo) -> bool:
        member = self.member_service.members.get(login_info.email, None)
        if member is None:
            raise Exception
        return member.password == login_info.password
