from sqlalchemy.orm import mapped_column, Mapped,relationship
from sqlalchemy import Integer, String,DECIMAL,ForeignKey
from db import Base
from pydantic import EmailStr
from enum import Enum


class Products(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True, index=True
    )
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[int] = mapped_column(DECIMAL)
    category_id: Mapped[int] = mapped_column(Integer,ForeignKey("categories.id",ondelete="CASCADE"))
    category=relationship("Category",back_populates="products",lazy="selectin")
    
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True, index=True
    )
    title: Mapped[str] = mapped_column(String(50))
    products=relationship("Products",back_populates="category",lazy="selectin")