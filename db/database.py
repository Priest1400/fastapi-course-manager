# ایمپورت ابزارهای لازم از SQLAlchemy
from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ایجاد یک اتصال به پایگاه‌داده SQLite
# گزینه check_same_thread=False برای اجازه استفاده از session در تردهای مختلف است (ویژه SQLite)
engine = create_engine("sqlite:///fastapi.db", connect_args={'check_same_thread': False})

# تعریف پایه برای مدل‌های ORM (پایه‌ای برای همه کلاس‌های دیتابیس)
base = declarative_base()

# ساخت یک کلاس session برای تعامل با دیتابیس
sessionlocal = sessionmaker(bind=engine)

# تابع Dependency که در FastAPI برای دریافت session از آن استفاده می‌شود
def get_db():
    session = sessionlocal()  # ایجاد یک session جدید
    try:
        yield session  # ارسال session به صورت generator
    finally:
        session.close()  # بستن session بعد از پایان کار (حتی در صورت وقوع خطا)
