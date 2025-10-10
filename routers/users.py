from fastapi import APIRouter, Depends, HTTPException, Response


app = APIRouter(prefix="/user", tags=["users"])