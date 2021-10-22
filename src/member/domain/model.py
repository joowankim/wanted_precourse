import uuid
from dataclasses import dataclass
from typing import Dict

from pydantic import BaseModel


@dataclass(frozen=True)
class MembershipApplication:
    nickname: str
    email: str
    password: str


class Member(BaseModel):
    member_id: str
    email: str
    password: str
    nickname: str


@dataclass(frozen=True)
class MemberService:
    members: Dict[str, Member]

    @staticmethod
    def generate_member_id() -> str:
        return "member-" + str(uuid.uuid4())

    def register(self, application: MembershipApplication) -> None:
        if self.members.get(application.email, None) is None:
            member_id = MemberService.generate_member_id()
            self.members[application.email] = Member(
                member_id=member_id,
                email=application.email,
                password=application.password,
                nickname=application.nickname
            )
