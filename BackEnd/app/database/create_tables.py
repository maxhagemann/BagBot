from app.database.DBconnection import engine
from app.database.models import Base
from sqlalchemy.orm import declarative_base

Base = declarative_base()
Base.metadata.create_all(bind=engine)