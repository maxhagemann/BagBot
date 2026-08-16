from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from typing import Optional

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
    name: Optional[str] = None
    price: Optional[Decimal] = None
    weight: Optional[float] = None
    description: Optional[str] = None
    quantity_in_stock: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)