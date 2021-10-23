import uuid

from src.member.domain.exception import DuplicatedNicknameException, MemberNotFoundException
from src.member.domain.model.member import Member
from src.member.domain.model.membership_application import MembershipApplication
from src.member.infra.member_repository import AbstractMemberRepository


class MemberService:
    def __init__(self, repo: AbstractMemberRepository):
        self.members = repo

    @staticmethod
    def generate_member_id() -> str:
        return "member-" + str(uuid.uuid4())

    def register(self, application: MembershipApplication) -> None:
        if not self.members.exists(nickname=application.nickname):
            member_id = MemberService.generate_member_id()
            new_member = Member(
                member_id=member_id,
                password=application.password,
                nickname=application.nickname
            )
            self.members.add(new_member)
        else:
            raise DuplicatedNicknameException

    def get_member(self, nickname: str) -> Member:
        member = self.members.get_by_nickname(nickname=nickname)
        if member:
            return member
        else:
            raise MemberNotFoundException
