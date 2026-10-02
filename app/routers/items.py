from fastapi import APIRouter, Depends, HTTPException, status
from app.database import DBconnection
from app.database.models import Item
from app.database.schemas import ItemBase, ItemCreate, ItemRead, ItemUpdate
from app.database.DBconnection import get_db
from sqlalchemy.orm import Session
from typing import List

item_router = APIRouter(prefix="/items", tags=["items"])

@item_router.get("/", response_model=List[ItemRead])
async def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()


@item_router.get("/{item_id}", response_model=ItemRead)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    return db.get(Item, item_id)

@item_router.post("/", response_model=ItemRead)
async def add_item(item: ItemCreate, db: Session = Depends(get_db)):
    # Create SQLAlchemy object
    db_item = Item(**item.model_dump())

    # Stage the object
    db.add(db_item)

    # Save to PostgreSQL
    db.commit()

    # Load generated fields (id), may change this if there's a more effienct way
    db.refresh(db_item)

    return db_item

@item_router.patch("/{item_id}", response_model=ItemRead)
async def update_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.get(Item, item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
        
    db.commit()
    db.refresh(db_item)
    return db_item

@item_router.delete("/{item_id}", response_model=ItemRead)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.get(Item, item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return db_item


