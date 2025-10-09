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
    # one to many relationship
    category=relationship("Category",back_populates="products",lazy="selectin")
    
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True, index=True
    )
    title: Mapped[str] = mapped_column(String(50))
    products=relationship("Products",back_populates="category",lazy="selectin")

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True, index=True
    )
    name : Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[EmailStr] = mapped_column(String(50), unique=True, nullable=False)
    password : Mapped[str] =mapped_column(String(255), nullable=False)
    # one to one relationship
    user_profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan", lazy="selectin")
        
class UserProfile(Base):
    __tablename__= "user_profiles"
    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True, index=True
    )
    user_id : Mapped[int] = mapped_column(Integer,ForeignKey("users.id",ondelete="CASCADE"),unique=True)
    address : Mapped[str] = mapped_column(String(255))
    phone : Mapped[str] = mapped_column(String(15))
    # one to one relationship
    