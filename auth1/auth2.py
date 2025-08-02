# وارد کردن ابزارها و کلاس‌های مورد نیاز از FastAPI و دیگر کتابخانه‌ها
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from typing import Optional
from datetime import datetime, timedelta
from db.database import get_db
from sqlalchemy.orm import Session
from jose import jwt
from jose.exceptions import JWTError

# تعریف schema برای گرفتن توکن از کلاینت (آدرس endpoint ورود)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# کلید مخفی و الگوریتم برای امضای JWT
SECRET_KEY = '6c7d438d2ea66cc11ee315566bda6f45336930dc2a40eaa96ec009524c20aa69'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# تابع ساخت توکن JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()  # کپی‌برداری از اطلاعات اولیه
    if expires_delta:
        expire = datetime.utcnow() + expires_delta  # اگر زمان انقضا داده شده بود
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # پیش‌فرض ۱۵ دقیقه
    to_encode.update({"exp": expire})  # افزودن زمان انقضا به داده‌ها
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # ساخت توکن
    return encoded_jwt

# تابع استخراج اطلاعات کاربر فعلی از روی توکن دریافتی
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    error_credential = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid credentials',
        headers={'WWW-authenticate': 'bearer'}
    )

    try:
        _dict = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)  # دیکد کردن توکن
        username = _dict.get('sub')  # گرفتن نام کاربری
        user_id = _dict.get('user_id')  # گرفتن شناسه کاربر
        role = _dict.get('role')  # گرفتن نقش
        email = _dict.get('email')  # گرفتن ایمیل
        data = {
            "sub": username,
            "user_id": user_id,
            "role": role,
            "email": email
        }

        if not username:
            raise error_credential  # اگر توکن نامعتبر بود
    except JWTError:
        raise error_credential  # اگر خطایی در دیکد رخ داد

    return data  # بازگرداندن اطلاعات کاربر

# محدود کردن دسترسی فقط برای ادمین‌ها
def require_admin(current_user = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admins only"
        )
    return current_user

# محدود کردن دسترسی فقط برای دانش‌آموزها
def require_student(current_user = Depends(get_current_user)):
    if current_user["role"] != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Students only"
        )
    return current_user
