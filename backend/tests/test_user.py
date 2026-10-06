import pytest
from sqlalchemy.exc import IntegrityError
from app.authentication import hash_password, verify_password
from app.database.models import User
from app.database.schemas import UserBase, UserCreate
from pydantic import ValidationError

def test_create_user(session):
    user = User(
        email="john@example.com",
        password_hash="some_hash",
        first_name="John",
        last_name="Doe",
    )

    session.add(user)
    session.commit()

    assert user.id is not None
def test_email_must_be_unique(session):
    user1 = User(
        email="john@example.com",
        password_hash="hash1",
        first_name="John",
        last_name="Doe",
    )

    user2 = User(
        email="john@example.com",
        password_hash="hash2",
        first_name="Jane",
        last_name="Doe",
    )

    session.add(user1)
    session.commit()

    session.add(user2)

    with pytest.raises(IntegrityError):
        session.commit()

def test_valid_email():
    user = UserCreate(
        email="john@example.com",
        password="password123",
        first_name="John",
        last_name="Doe",
    )

    assert user.email == "john@example.com"


def test_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            email="johnexample.com",
            password_hash="hash1",
            first_name="John",
            last_name="Doe",
         )
   


def test_hash_password():
    password = "myPassword123"

    hashed = hash_password(password)

    assert isinstance(hashed, str)
    assert hashed != password
    assert verify_password(password, hashed)

def test_wrong_password():
    password = "secret123"

    hashed = hash_password(password)

    assert not verify_password("wrong_password", hashed)


def test_user_password_is_stored(session):
    password = "secret123"

    user = User(
        email="john@example.com",
        password_hash=hash_password(password),
        first_name="John",
        last_name="Doe",
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    assert verify_password(password, user.password_hash)

@pytest.mark.parametrize(
    "field",
    ["email", "password_hash", "first_name", "last_name"],
)
def test_required_fields(session, field):
    values = {
        "email": "john@example.com",
        "password_hash": "hash",
        "first_name": "John",
        "last_name": "Doe",
    }

    values[field] = None

    user = User(**values)
    session.add(user)

    with pytest.raises(IntegrityError):
        session.commit()

