
from fastapi import APIRouter, Depends, HTTPException, status, Query , Request , Header
from sqlalchemy.orm import Session

from auth1.auth2 import oauth2_scheme
from db.models import DbUser
from db.database import get_db
from schemas import UserBase, UserOut, UserCreate
from db import db_user
from auth1 import auth2
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


@router.get('/me')
def read_current_user(current_user = Depends(auth2.get_current_user)):
    return current_user.get('role')




