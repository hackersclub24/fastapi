from fastapi import APIRouter, Depends, HTTPException, Response


app = APIRouter(prefix="/user", tags=["users"])

@app.get("/")
def welcome():
    return {"message": "Welcome to users router"}