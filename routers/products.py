from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from models import Products

app = APIRouter(prefix="/prodducts", tags=["proucts"])

@app.get("/products/{id}")
async def read(id : int ,db : AsyncSession = Depends(get_db)):
    return await db.get(Products,id)