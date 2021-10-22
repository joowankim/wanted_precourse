from dataclasses import dataclass

from src.member.domain.model import MemberService


@dataclass(frozen=True)
class LoginInfo:
    nickname: str
    password: str


class AuthenticationService:
    member_service: MemberService

    def authenticate(self, login_info: LoginInfo) -> bool:
        member = self.member_service.members.get(login_info.nickname, None)
        if member is None:
            # todo: change to member not found exception
            raise Exception
        return member.password == login_info.password
