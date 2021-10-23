from fastapi import Depends
from sqlalchemy.orm import Session

from src.member.domain.model.member_service import MemberService
from src.member.domain.model.membership_application import MembershipApplication
from src.member.infra.member_repository import AbstractMemberRepository, MemberRepository, db_session


def member_repository(session: Session = Depends(db_session)):
    return MemberRepository(session=session)


class MemberApplication:
    def __init__(self, repository: AbstractMemberRepository = Depends(member_repository)):
        self.repository = repository

    def register_member(self, application: MembershipApplication):
        member_service = MemberService(repo=self.repository)
        member_service.register(application)
