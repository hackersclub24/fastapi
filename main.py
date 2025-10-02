from fastapi import FastAPI,Depends
from pydantic import BaseModel
from db import engine, get_db
from contextlib import asynccontextmanager
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from models import Products,Category

#adding github comment
app = FastAPI()

@app.get("/")
def mainpage():
    return {"message": "Hello World"}

@app.get("/products/{id}")
async def read(id : int ,db : AsyncSession = Depends(get_db)):
    return await db.get(Products,id)

@app.get("/categorie/{id}")
async def read(id : int ,db : AsyncSession = Depends(get_db)):
    return await db.get(Category,id)
