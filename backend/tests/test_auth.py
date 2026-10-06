import pytest
from sqlalchemy.exc import IntegrityError
from app.authentication import hash_password, verify_password
from app.database.models import User
from app.database.schemas import UserBase, UserCreate
from pydantic import ValidationError
from app.routers import users
from fastapi.testclient import TestClient
from app.main import app




def test_login_success(client, session):
    user = User(
        email="test@example.com",
        first_name="John",
        last_name="Doe",
        password_hash=hash_password("password123")
    )

    session.add(user)
    session.commit()

    response = client.post(
        "/users/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hi John Doe"
    }


def test_login_user_not_found(client, session):
    response = client.post(
        "/users/login",
        json={
            "email": "doesnotexist@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"



def test_login_incorrect_password(client, session):
    response = client.post(
        "/users/login",
        json={
            "email": "test@example.com",
            "password": "notpassword123"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_missing_value(client):
    response = client.post(
        "users/login",
        json={
            "email": "test@example.com"
        }
    )

    assert response.status_code == 422
