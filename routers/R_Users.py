
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.models import DbUser
from db.database import get_db
from schemas import UserBase, UserOut, UserCreate
from db import db_user

router = APIRouter(prefix='/user', tags=['user'])

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(DbUser).filter(DbUser.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="این نام کاربری قبلاً ثبت شده است"
        )
    new_user = db_user.create_user(db, user)
    return new_user