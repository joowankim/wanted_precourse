from dataclasses import dataclass


@dataclass
class LoginInfo:
    nickname: str
    password: str
