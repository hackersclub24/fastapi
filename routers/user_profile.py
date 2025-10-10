from fastapi import APIRouter, Depends, HTTPException, Response


app = APIRouter(prefix="/userprofile", tags=["userprofile"])