import abc

from sqlalchemy.orm import Session

from src.post.domain.model.post import Post


class AbstractPostRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, post: Post):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, post_id: str) -> Post:
        raise NotImplementedError

    # @abc.abstractmethod
    # def update(self, post: Post):
    #     raise NotImplementedError
    #
    # @abc.abstractmethod
    # def delete(self, post: Post):
    #     raise NotImplementedError


class PostRepository(AbstractPostRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, post: Post):
        self.session.add(post)
        self.session.commit()

    def get_by_id(self, post_id: str) -> Post:
        return self.session.query(Post)\
            .filter_by(post_id=post_id)\
            .first()

    def get_all(self):
        return list(self.session.query(Post).all())

