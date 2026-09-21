from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr

"""
class ItemCreate(BaseModel):
    name: str
    price: Decimal
    weight: float
    description: str
    quantity_in_stock: int
"""

class ItemBase(BaseModel):
    name: str
    price: Decimal
    weight: float
    description: str
    quantity_in_stock: int
    model_config = ConfigDict(from_attributes=True)


class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ItemUpdate(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    weight: float | None = None
    description: str | None = None
    quantity_in_stock: int | None = None
    model_config = ConfigDict(from_attributes=True)

    # user schemas

class UserBase(BaseModel):
    email: EmailStr
    password_hash: str
    first_name: str
    last_name: str
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None