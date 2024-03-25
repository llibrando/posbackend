# model/users.py
from fastapi import Depends, HTTPException, APIRouter
from .db import get_db

router = APIRouter()

# CRUD operations

@router.get("/users/", response_model=list)
async def read_users(db=Depends(get_db)):
    query = "SELECT id, username FROM users"
    db.execute(query)
    users = [{"id": user[0], "username": user[1]} for user in db.fetchall()]
    return users

@router.get("/users/{user_id}", response_model=dict)
async def read_user(user_id: int, db=Depends(get_db)):
    query = "SELECT id, username FROM users WHERE id = %s"
    db.execute(query, (user_id,))
    user = db.fetchone()
    if user:
        return {"id": user[0], "username": user[1]}
    raise HTTPException(status_code=404, detail="User not found")
