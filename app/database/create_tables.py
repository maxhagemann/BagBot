from app.database.DBconnection import engine
from app.database.models import Base

Base.metadata.create_all(bind=engine)