from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from db import engine, get_db,Base
from contextlib import asynccontextmanager
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from models import Products, Category
from routers import app_router


@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as conn:
        res = await conn.run_sync(lambda s: engine.dialect.has_table(s,Products.__tablename__))
        if not res : 
            conn.run_sync(Base.metadata.create)
    yield
# adding github comment
app = FastAPI(lifespan= lifespan)


@app.get("/")
def welcome():
    return {"message": "Welcome"}


"""
@app.get("/")
def mainpage():
    return {"message": "Hello World"}

@app.get("/products/{id}")
async def read(id : int ,db : AsyncSession = Depends(get_db)):
    return await db.get(Products,id)

@app.get("/categorie/{id}")
async def read(id : int ,db : AsyncSession = Depends(get_db)):
    return await db.get(Category,id)

"""
app.include_router(app_router)
