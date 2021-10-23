import abc

from sqlalchemy.orm import Session

from src.member.domain import model


class AbstractMemberRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, member: model.Member):
        raise NotImplementedError


class MemberRepository(AbstractMemberRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, member):
        self.session.add(member)
        self.session.commit()

    def get_by_id(self, member_id: str) -> model.Member:
        return self.session\
            .query(model.Member)\
            .filter_by(member_id=member_id)\
            .first()
