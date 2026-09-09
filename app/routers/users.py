from fastapi import APIRouter, Depends, HTTPException, status
from app.database import DBconnection
from app.database.models import User
from app.database.schemas import UserBase, UserCreate, UserLogin, UserResponse
from app.database.DBconnection import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.authentication import hash_password, verify_password


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




@user_router.post("/login")
async def user_login(creds: UserLogin, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == creds.email))
    if user is None or not verify_password (creds.password, user.password_hash):
         raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    else:
        return { "message": f"Hi, {user.first_name} {user.last_name}"
        }