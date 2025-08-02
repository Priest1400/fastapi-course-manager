from sqlalchemy.orm.session import Session

from schemas import UserCreate           # اسکیمای ورودی برای ساخت کاربر جدید
from db.models import DbUser             # مدل دیتابیس برای کاربران
from db.hash import Hash                 # ماژول هش کردن رمز عبور

# تابع برای ساخت کاربر جدید
def create_user(db: Session, user: UserCreate) -> DbUser:
    db_user = DbUser(
        username=user.username,                   # نام کاربری
        email=user.email,                         # ایمیل
        password=Hash.bcrypt(user.password),      # رمز عبور هش‌شده
        role=user.role,                           # نقش (admin یا student)
        is_active=True                            # فعال بودن حساب
    )
    db.add(db_user)       # اضافه کردن به session
    db.commit()           # ذخیره در دیتابیس
    db.refresh(db_user)   # دریافت مقادیر جدید مانند id از دیتابیس
    return db_user        # بازگشت شی کاربر ساخته‌شده

# گرفتن کاربر از دیتابیس بر اساس نام کاربری
def get_user_by_username(username, db: Session):
    return db.query(DbUser).filter(DbUser.username == username).first()
    # جست‌وجو در جدول کاربران و بازگرداندن اولین نتیجه‌ای که نام کاربری‌اش مطابق باشد
