import pytest
from sqlalchemy.exc import IntegrityError
from app.database.models import User, Item, Order, OrderItem
from app.database.schemas import UserBase, UserCreate
from pydantic import ValidationError
from app.routers import users
from app.main import app

def test_create_order_without_user(client):
    sample_order = {
        "status": "pending",
        "order_items": [
            {
                "item_id": 1,
                "quantity": 2,
                "price": 19.99
            }
        ]
    }

    response = client.post("/orders/", json=sample_order)
    assert response.status_code == 422
    assert response.json() == {"detail": "invalid input."}


def test_create_order_nonexisting_user(client):
    response = client.post("/orders/", json={"user_id": 999, "status": "pending", "order_items": [{"item_id": 1, "quantity": 1, "price": 5.99}]})
    assert response.status_code == 400
    assert response.json() == {"detail": "User not found."}

