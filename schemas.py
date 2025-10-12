from pydantic import BaseModel, EmailStr


class CategoryBase(BaseModel):
    title: str


class CategoryCreate(CategoryBase):
    title: str


class CategoryRead(CategoryBase):
    id: int


class CategoryUpdate(CategoryBase):
    id: int
    title: str


class ProductBase(BaseModel):
    title: str
    price: float
    category_id: int


class ProductRead(ProductBase):
    id: int
    
class ProductUpdate(ProductBase):
    id: int

