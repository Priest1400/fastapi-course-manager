from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, Header
from sqlalchemy.orm import Session
import h_to_m  # ماژول کمکی برای تبدیل زمان و چک تداخل زمانی
from auth1.auth2 import require_student  # دکوراتور برای اجازه فقط به دانشجوها
from db.models import Course, Enrollment  # مدل‌های دیتابیس دوره و ثبت‌نام
from db.database import get_db  # گرفتن سشن دیتابیس
from auth1 import auth2  # برای گرفتن یوزر جاری از توکن

router = APIRouter(
    prefix="/student",
    tags=["student"],
    dependencies=[Depends(require_student)]  # فقط کاربر با نقش student می‌تواند این روت‌ها را بزند
)

# مسیر ثبت نام دانشجو در دوره با id دوره
@router.post("/register_course_by_student{course_id}")
def register_course_by_id(course_id: int, db: Session = Depends(get_db), current_user=Depends(auth2.get_current_user)):
    # جستجو دوره در دیتابیس بر اساس course_id
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        # اگر دوره پیدا نشد خطای 404 برگردان
        raise HTTPException(status_code=404, detail="Course not found")

    # چک کن کاربر قبلاً در این دوره ثبت نام کرده یا نه
    existing = db.query(Enrollment).filter_by(
        student_id=current_user["user_id"],
        course_id=course_id
    ).first()
    if existing:
        # اگر قبلاً ثبت نام شده بود خطای 400 بده
        raise HTTPException(status_code=400, detail="این کلاس قبلا ثبت شده است")

    # تبدیل زمان شروع و پایان کلاس به دقیقه (مثلا 08:00 تبدیل به 480)
    start_time = h_to_m.time_to_minutes(course.class_start_time)
    end_time = h_to_m.time_to_minutes(course.class_end_time)

    # گرفتن زمان‌های کلاس‌های ثبت‌نام شده فعلی دانشجو در روز مشابه به صورت دقیقه
    x1 = h_to_m.get_day_schedule_in_minutes(course.class_day, db, current_user)

    # بررسی تداخل زمانی بین کلاس جدید و کلاس‌های فعلی دانشجو
    for item in x1:
        existing_start = item["start_minutes"]
        existing_end = item["end_minutes"]
        # اگر زمان کلاس جدید با هر کلاس دیگری تداخل داشت خطا بده
        if start_time < existing_end and end_time > existing_start:
            raise HTTPException(status_code=400, detail="تداخل زمانی با کلاس دیگری وجود دارد.")

    # اگر همه چیز درست بود، ثبت‌نام جدید ایجاد کن
    enrollment = Enrollment(
        student_id=current_user["user_id"],
        course_id=course_id
    )
    db.add(enrollment)  # افزودن به سشن
    db.commit()  # ذخیره در دیتابیس
    db.refresh(enrollment)  # بروزرسانی آبجکت از دیتابیس

    # پیام موفقیت همراه با نام دوره برگردان
    return {"message": "Successfully enrolled", "course": course.title}
