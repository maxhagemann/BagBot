from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Numeric
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from decimal import Decimal
from typing import List

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    weight: Mapped[float] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity_in_stock: Mapped[int] = mapped_column(nullable=False)
    order_item: Mapped["OrderItem"] = relationship(back_populates="item")
    cart_item: Mapped["CartItem"] = relationship(back_populates="item")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    order: Mapped[List["Order"]] = relationship(back_populates="user")
    cart: Mapped["Cart"] = relationship(back_populates="cart")

class Order(Base):
    __tablename__= "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="orders")
    status: Mapped[str] = mapped_column(String(255), nullable=False)
    order_item: Mapped[List["OrderItem"]] = relationship(back_populates="order")

class OrderItem(Base):
    __tablename__= "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column()
    order: Mapped[List["Order"]] = relationship(back_populates="order_items")
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    item: Mapped[List["Item"]] = relationship(back_populates="order_items")
    Item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))

class Cart(Base):
    _tablename__= "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Child"] = relationship(back_populates="cart")

class CartItem(Base):
    _tablename__= "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column()
    cart: Mapped[List["Cart"]] = relationship(back_populates="cart_items")
    cart_item_id: Mapped[int] = mapped_column(ForeignKey("cart.id"))
    item: Mapped[List["Item"]] = relationship(back_populates="cart_items")
    Item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))