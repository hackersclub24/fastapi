from fastapi import APIRouter, Depends, HTTPException, Response

app = APIRouter(prefix="/categories", tags=["categories"])
@app.get("/")
def welcome():
    return {"message": "Welcome to categories router"}
