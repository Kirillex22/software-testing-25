import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from impl.orm.order import Base
from config import Settings, set_settings

@pytest.fixture(scope="session")
def db_engine(settings):
    """Создаём движок SQLAlchemy"""
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture()
def db_session(db_engine) -> Session:
    """Сессия SQLAlchemy на каждый тест"""
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()
