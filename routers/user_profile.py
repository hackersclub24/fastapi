from fastapi import APIRouter, Depends, HTTPException, Response


app = APIRouter(prefix="/userprofile", tags=["userprofile"])

@app.get("/")
def welcome():
    return {"message": "Welcome to user_profile router"}