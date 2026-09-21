from fastapi import APIRouter, Depends, HTTPException, status, Depends, Security
from fastapi.security import OAuth2PasswordRequestForm
from app.database import DBconnection
from app.database.models import User
from app.database.schemas import UserBase, UserCreate, UserLogin, UserResponse, Token
from app.database.DBconnection import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.authentication import *
from typing import Annotated
import jwt

user_router = APIRouter(tags=["users"])


@user_router.post("/signup", response_model=UserResponse)
async def user_signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.scalar(select(User).where(User.email == user.email))
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered"
        )

    new_user = User(**user.model_dump(exclude={"password_hash"}),
    password_hash=hash_password(user.password_hash))

    # Stage the object
    db.add(new_user)

    # Save to PostgreSQL
    db.commit()

    # Load generated fields (id)
    db.refresh(new_user)
    return new_user




@user_router.post("/token")
async def user_login(creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == creds.username))
    if user is None or not verify_password (creds.password, user.password_hash):
         raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    else:
        access_token = create_access_token(data={"email": creds.username})
        return Token(access_token=access_token, token_type="bearer")
        #return { "message": f"Hi, {user.first_name} {user.last_name}


@user_router.get("/me", response_model=UserResponse)
async def read_users_me(user_data: Dict = Security(get_current_user)):
    user = user_data["user"]
    return {"email": user.email, "first_name": user.first_name, "last_name":user.last_name, "id": user.id}


@user_router.delete("/leave")
async def delete_user(user_data: Dict = Security(get_current_user), db: Session = Depends(get_db)):
    user = user_data["user"]
    token = user_data["token"]
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    blacklist.add(token)
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}