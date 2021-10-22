import uuid
from dataclasses import dataclass
from typing import Dict

from pydantic import BaseModel


@dataclass(frozen=True)
class MembershipApplication:
    nickname: str
    password: str


class Member(BaseModel):
    member_id: str
    password: str
    nickname: str


@dataclass(frozen=True)
class MemberService:
    members: Dict[str, Member]

    @staticmethod
    def generate_member_id() -> str:
        return "member-" + str(uuid.uuid4())

    def register(self, application: MembershipApplication) -> None:
        if self.members.get(application.nickname, None) is None:
            member_id = MemberService.generate_member_id()
            self.members[application.nickname] = Member(
                member_id=member_id,
                password=application.password,
                nickname=application.nickname
            )
        else:
            # todo: change to duplicated nickname Exception
            raise Exception
