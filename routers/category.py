from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from sqlalchemy import select, and_
from typing import List, Optional
from models import Category
from schemas import CategoryCreate, CategoryRead, CategoryUpdate

app = APIRouter(prefix="/categories", tags=["categories"])


@app.get("/list-categories", response_model=List[CategoryRead])
async def list_categories(
    min: Optional[int] = None,
    max: Optional[int] = None,
    title: Optional[str] = None,
    filter: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Category)
    options = []
    if filter:
        options.append(Category.title.ilike(f"%{filter}%"))
    if title:
        options.append(Category.title == title)
    if min:
        options.append(Category.id >= min)
    if max:
        options.append(Category.id <= max)
    if options:
        stmt = stmt.where(and_(*options))

    result = await db.execute(stmt)
    # categories = result.scalars().all()
    return result.scalars().all()
    # return {"message": "Welcome to categories router"}


@app.get("/{id}", response_model=CategoryRead)
async def read(id: int, db: AsyncSession = Depends(get_db)):
    return await db.get(Category, id)


@app.post("/add-category")
async def add_category(title: str, db: AsyncSession = Depends(get_db)):
    new_category = Category(title=title)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    await db.flush()
    return new_category


@app.put("/update-category")
async def update_category(category: CategoryUpdate, db: AsyncSession = Depends(get_db)):
    # data = await db.get(Category, ident=category.id)
    data = await db.get(Category, category.id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    data.title = category.title
    await db.commit()
    await db.refresh(data)
    await db.flush()
    return data


@app.delete("/delete-category/{id}")
async def delete_category(id: int, db: AsyncSession = Depends(get_db)):
    data = await db.get(Category, id)
    if not data:
        raise HTTPException(status_code=404, detail="Category not found")
    await db.delete(data)
    await db.commit()
    return {"message": "Category deleted successfully"}
