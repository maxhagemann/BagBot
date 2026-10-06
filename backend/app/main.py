from fastapi import FastAPI
from app.routers import items, users
from app.database.DBconnection import engine
from app.database.models import Base


app = FastAPI(title="BagBot API")

#Base.metadata.create_all(bind=engine)

app.include_router(items.item_router ,prefix="/items")
app.include_router(users.user_router ,prefix="/users")
