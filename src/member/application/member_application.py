from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.db_config import db_session
from src.member.domain.model.member_service import MemberService
from src.member.domain.model.membership_application import MembershipApplication
from src.member.infra.member_repository import AbstractMemberRepository, MemberRepository


def member_repository(session: Session = Depends(db_session)):
    return MemberRepository(session=session)


def member_service(repo: AbstractMemberRepository = Depends(member_repository)):
    return MemberService(repo=repo)


class MemberApplication:
    def __init__(self, service: MemberService):
        self.service = service

    def register_member(self, application: MembershipApplication):
        self.service.register(application)
