import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from src.config.db_config import metadata
from src.config.table_mapper_config import start_mappers


pytest_plugins = [
    "tests.unit.fixtures.repository",
    "tests.unit.fixtures.service",
]


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


