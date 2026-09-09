

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from .config import settings




DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.postgres_user}:{settings.postgres_password}"
    f"@db:5432/{settings.postgres_db}"
)
#creates SQL academy seesion
engine = create_engine(DATABASE_URL)



SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()