from pydantic import BaseModel, EmailStr


class CategoryBase(BaseModel):
    title: str


class CategoryCreate(CategoryBase):
    title: str


class CategoryRead(CategoryBase):
    id: int

class CategoryUpdate(CategoryBase):
    id : int
    title: str
