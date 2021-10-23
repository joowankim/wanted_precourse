from dataclasses import dataclass


@dataclass
class MembershipApplication:
    nickname: str
    password: str
