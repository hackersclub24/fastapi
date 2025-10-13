from fastapi import APIRouter, Depends, HTTPException, Response
from db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from sqlalchemy import select, and_
from typing import List, Optional
from schemas import UserBase, UserRead


app = APIRouter(prefix="/user", tags=["users"])


@app.get("/list-users",response_model=List[UserRead])
async def list_users(
    min: Optional[int] = None,
    max: Optional[int] = None,
    filter: Optional[str] = None,
    name: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(User)
    if min:
        stmt = stmt.where(User.id >= min)
    if max:
        stmt = stmt.where(User.id <= max)
    if filter:
        stmt = stmt.where(User.name.ilike(f"%{filter}%"))
    if name:
        stmt = stmt.where(User.name == name)
    result = await db.execute(stmt)
    return result.scalars().all()


@app.get("/{id}",response_model=UserRead)
async def read(id: int, db: AsyncSession = Depends(get_db)):
    return await db.get(User, id)


@app.post("/add-user",response_model=UserRead)
async def add_user(user: UserBase, db: AsyncSession = Depends(get_db)):
    new_user = User(name=user.name, email=user.email, password=user.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    await db.flush()
    return new_user


@app.delete("/delete-user/{id}")
async def delete_user(id: int, db: AsyncSession = Depends(get_db)):
    data = await db.get(User, id)
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(data)
    await db.commit()
    return {"message": "User deleted successfully"}

@app.put("/update-user",response_model=UserRead)
async def update_user(user: UserRead, db: AsyncSession = Depends(get_db)):
    data = await db.get(User,user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    data.name = user.name
    data.email = user.email
    data.password = user.password
    await db.commit()
    await db.refresh(data)
    await db.flush()
    return data