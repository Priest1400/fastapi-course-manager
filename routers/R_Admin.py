from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth1.auth2 import require_admin  # وابستگی برای محدود کردن دسترسی فقط به ادمین‌ها
from db.models import Course  # مدل دوره‌ها
from db.database import get_db  # تابع گرفتن سشن دیتابیس
from schemas import CourseBase  # اسکیمای دوره
from db import Db_admin  # توابع دیتابیسی مربوط به ادمین

# تعریف روت‌های مربوط به بخش ادمین
router = APIRouter(
    prefix="/admin",  # همه‌ی روت‌ها با /admin شروع می‌شن
    tags=["admin"],  # تگ برای مستندات OpenAPI
    dependencies=[Depends(require_admin)]  # فقط کاربران با نقش admin اجازه دسترسی دارن
)


# روت ساده برای داشبورد ادمین
@router.get("/")
def admin_dashboard():
    return {"message": f"خوش آمدی ادمین "}  # پیام خوشامدگویی


# روت برای اضافه کردن دوره جدید
@router.post("/add_course", response_model=CourseBase)
def add_course(course: CourseBase, db: Session = Depends(get_db)):
    # بررسی اینکه آیا دوره‌ای با همین عنوان قبلاً ثبت شده یا نه
    existing_course = db.query(Course).filter(Course.title == course.title).first()
    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="این دوره قبلا ثبت شده است"
        )

    # اگر دوره جدید است، آن را اضافه کن
    new_course = Db_admin.add_course(db, course)
    return new_course  # دوره‌ی اضافه شده را برگردان
