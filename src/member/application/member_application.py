from src.member.domain.exception import DuplicatedNicknameException
from src.member.domain.model.member_service import MemberService
from src.member.domain.model.membership_application import MembershipApplication
from src.member.infra.member_repository import AbstractMemberRepository


class MemberApplication:
    def __init__(self, repository: AbstractMemberRepository):
        self.repository = repository

    def register_member(self, application: MembershipApplication):
        member_service = MemberService(repo=self.repository)
        try:
            member_service.register(application)
        except DuplicatedNicknameException:
            raise Exception
