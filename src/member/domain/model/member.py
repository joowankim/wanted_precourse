from dataclasses import dataclass


@dataclass
class Member:
    member_id: str
    nickname: str
    password: str
