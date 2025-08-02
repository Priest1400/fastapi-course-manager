from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm  # برای دریافت فرم لاگین با username و password
from sqlalchemy.orm.session import Session
from db import models  # مدل‌های دیتابیس
from db.database import get_db  # تابع گرفتن سشن دیتابیس
from db.hash import Hash  # کلاس هش برای رمز عبور
from auth1 import auth2  # برای ساخت توکن JWT

router = APIRouter(prefix='/login', tags=['login'])


# روت POST برای دریافت توکن با دریافت username و password
@router.post('/')
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # جستجوی کاربر در دیتابیس بر اساس username وارد شده
    user = db.query(models.DbUser).filter(models.DbUser.username == request.username).first()

    # اگر کاربر پیدا نشد، خطای اعتبارسنجی نامعتبر می‌دهد
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid credential')

    # اگر رمز عبور وارد شده با هش ذخیره شده مطابقت نداشت، خطا می‌دهد
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid password')

    # ساخت توکن JWT با اطلاعات کاربر (username، id، نقش)
    access_token = auth2.create_access_token(data={
        'sub': user.username,
        'user_id': user.id,
        'role': user.role
    })

    # بازگرداندن توکن، نام کاربری و نقش کاربر به کلاینت
    return {
        'access_token': access_token,
        'username': user.username,
        'role': user.role,
    }
