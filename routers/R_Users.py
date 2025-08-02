from fastapi import APIRouter, Depends, HTTPException, status, Query , Request , Header
from sqlalchemy.orm import Session

from db.models import DbUser  # مدل یوزر دیتابیس
from db.database import get_db  # گرفتن سشن دیتابیس
from schemas import UserOut, UserCreate  # اسکیمای ورودی و خروجی یوزر
from db import db_user  # توابع مرتبط با یوزر مثل create_user
from auth1 import auth2  # برای دریافت یوزر فعلی از توکن

router = APIRouter(prefix='/user', tags=['user'])


# مسیر ثبت نام کاربر جدید
@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # چک کن که آیا نام کاربری قبلا ثبت شده یا نه
    existing_user = db.query(DbUser).filter(DbUser.username == user.username).first()
    if existing_user:
        # اگر موجود بود خطای 400 بده
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="این نام کاربری قبلاً ثبت شده است"
        )
    # اگر نبود، کاربر جدید را بساز و ذخیره کن
    new_user = db_user.create_user(db, user)
    return new_user  # خروجی پاسخ با مدل UserOut


# مسیر برای دریافت اطلاعات یوزر فعلی از توکن (مثل نقش کاربر)
@router.get('/me')
def read_current_user(current_user = Depends(auth2.get_current_user)):
    # فقط نقش کاربر را برمی‌گرداند
    return current_user.get('role')
