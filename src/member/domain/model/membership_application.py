from dataclasses import dataclass


@dataclass(frozen=True)
class MembershipApplication:
    nickname: str
    password: str
