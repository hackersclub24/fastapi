from fastapi import APIRouter, Depends, HTTPException, Response
from db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from sqlalchemy import select, and_
from typing import List, Optional
from schemas import UserBase, UserRead
import bcrypt
from jwt import encode, decode
from datetime import datetime, timezone, timedelta

app = APIRouter(prefix="/user", tags=["users"])


@app.get("/list-users", response_model=List[UserRead])
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


from pydantic import BaseModel


class Token(BaseModel):
    token: str


@app.post("/", response_model=UserRead)
async def read(token: Token, db: AsyncSession = Depends(get_db)):
    id = 14
    decoded = decode(token.token, "abhi", algorithms=["HS256"])
    print("this is decoded", decoded)
    return await db.get(User, id)


@app.post("/add-user", response_model=UserRead)
async def add_user(user: UserBase, db: AsyncSession = Depends(get_db)):
    salt = bcrypt.gensalt(10)
    hashed = bcrypt.hashpw(bytes(user.password, "utf8"), salt)
    new_user = User(name=user.name, email=user.email, password=str(hashed, "utf8"))
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


@app.put("/update-user", response_model=UserRead)
async def update_user(user: UserRead, db: AsyncSession = Depends(get_db)):
    data = await db.get(User, user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    data.name = user.name
    data.email = user.email
    data.password = user.password
    await db.commit()
    await db.refresh(data)
    await db.flush()
    return data


@app.post("/login-user")
async def login_user(
    user: UserBase, response: Response, db: AsyncSession = Depends(get_db)
):
    try:
        stmt = select(User).where(User.email == user.email)
        result = await db.execute(stmt)
        user_data = result.scalar_one()
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        if bcrypt.checkpw(
            bytes(user.password, "utf8"), bytes(user_data.password, "utf8")
        ):
            token = encode(
                {
                    "id": user_data.id,
                    "exp": datetime.now(tz=timezone.utc) + timedelta(hours=2),
                },
                "abhi",
                "HS256",
            )
            response.set_cookie("access_token", token, max_age=10000)
            return {"message": "loged in", "token": token}
        else:
            return {"message": "password not found"}
    except Exception as e:
        print(e)
        return {"message": "unexpected error!"}
