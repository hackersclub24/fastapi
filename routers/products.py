from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from models import Products, Category
from schemas import ProductBase, ProductRead, ProductUpdate
from sqlalchemy import select, and_
from typing import List, Optional


app = APIRouter(prefix="/prodducts", tags=["proucts"])


@app.get("/list-products", response_model=List[ProductRead])
async def list_products(
    min: Optional[int] = None,
    max: Optional[int] = None,
    filter: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Products)
    options = []
    if min:
        stmt = stmt.where(Products.id >= min)
    if max:
        stmt = stmt.where(Products.id <= max)
    if options:
        stmt = stmt.options(and_(*options))
    if filter:
        stmt = stmt.where(Products.title.ilike(f"%{filter}%"))
    result = await db.execute(stmt)
    return result.scalars().all()


@app.get("/products/{id}")
async def read(id: int, db: AsyncSession = Depends(get_db)):
    return await db.get(Products, id)


@app.post("/add-product", response_model=ProductRead)
async def add_products(product: ProductBase, db: AsyncSession = Depends(get_db)):
    val = await db.get(Category, product.category_id)
    new_product = Products(
        title=product.title, price=product.price, category_id=product.category_id
    )
    if val is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    await db.flush()
    return {"message": "Product added successfully", "product": new_product}


@app.delete("/delete-product/{id}")
async def delete_product(id: int, db: AsyncSession = Depends(get_db)):
    data = await db.get(Products, id)
    if not data:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(data)
    await db.commit()
    return {"message": "Product deleted successfully"}


@app.put("/update-product")
async def update_product(product: ProductUpdate, db: AsyncSession = Depends(get_db)):
    data = await db.get(Products, product.id)
    if not data:
        raise HTTPException(status_code=404, detail="Product not found")
    data.title = product.title
    data.price = product.price
    data.category_id = product.category_id
    await db.commit()
    await db.refresh(data)
    await db.flush()
    return {"message": "Product updated successfully", "product": data}
