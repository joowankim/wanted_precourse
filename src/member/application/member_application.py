from src.member.domain import model
from src.member.infra.member_repository import AbstractMemberRepository


class MemberApplication:
    def __init__(self, repository: AbstractMemberRepository):
        self.repository = repository

    def register_member(self, membership_application: model.MembershipApplication):
        member_service = model.MemberService(repo=self.repository)
