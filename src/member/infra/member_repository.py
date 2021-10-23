import abc

from sqlalchemy.orm import Session

from src.config.db_config import SessionLocal
from src.member.domain.model.member import Member


class AbstractMemberRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, member: Member):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, member_id: str) -> Member:
        raise NotImplementedError

    @abc.abstractmethod
    def exists(self, nickname: str) -> bool:
        raise NotImplementedError


def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


class MemberRepository(AbstractMemberRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, member):
        self.session.add(member)
        self.session.commit()

    def get_by_id(self, member_id: str) -> Member:
        return self.session.query(Member)\
            .filter_by(member_id=member_id)\
            .first()

    def exists(self, nickname: str) -> bool:
        if self.session.query(Member).filter_by(nickname=nickname).first():
            return True
        else:
            return False

