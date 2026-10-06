import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database.models import Base
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database.DBconnection import get_db

TEST_DATABASE_URL = "postgresql+psycopg://test_user:test_password@localhost:5433/test_db"

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def session():
    Base.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session
        session.rollback()

    Base.metadata.drop_all(test_engine)


@pytest.fixture
def client(session):

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()