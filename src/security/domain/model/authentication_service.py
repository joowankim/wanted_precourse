from src.member.domain.exception import MemberNotFoundException
from src.member.domain.model.member_service import MemberService
from src.security.domain.exception import NotExistMemberException, IncorrectPasswordException
from src.security.domain.model.login_info import LoginInfo


class AuthenticationService:
    def __init__(self, member_service: MemberService):
        self.member_service = member_service

    def authenticate(self, login_info: LoginInfo):
        try:
            member = self.member_service.get_member(login_info.nickname)
        except MemberNotFoundException:
            raise NotExistMemberException
        else:
            if member.password != login_info.password:
                raise IncorrectPasswordException
