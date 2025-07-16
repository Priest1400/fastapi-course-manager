from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db
from auth1 import auth2
from db.models import Enrollment, Course

# تبدیل زمان HH:MM به دقیقه
def time_str_to_minutes(time_str: str) -> int:
    time_obj = datetime.strptime(time_str.strip(), "%H:%M")
    return time_obj.hour * 60 + time_obj.minute

# تابع اصلی: فقط روز می‌گیرد، بقیه را خودکار هندل می‌کند
def get_day_schedule_in_minutes(target_day: str, db: Session = Depends(get_db), current_user = Depends(auth2.get_current_user)):
    # گرفتن آیدی کلاس‌هایی که کاربر در آن‌ها ثبت‌نام کرده
    enrollments = db.query(Enrollment).filter(Enrollment.student_id == current_user.get("user_id")).all()
    course_ids = [e.course_id for e in enrollments]

    # گرفتن دوره‌ها از دیتابیس
    courses = db.query(Course).filter(Course.id.in_(course_ids)).all()

    # فیلتر کردن کلاس‌های مربوط به روز مورد نظر
    day_classes = [
        {
            "day": course.class_day,
            "time": f"{course.class_start_time.strftime('%H:%M')} - {course.class_end_time.strftime('%H:%M')}"
        }
        for course in courses if course.class_day.strip() == target_day.strip()
    ]

    # تبدیل به دقیقه
    result = []
    for item in day_classes:
        start_str, end_str = item["time"].split(" - ")
        start_minutes = time_str_to_minutes(start_str)
        end_minutes = time_str_to_minutes(end_str)
        result.append({"start_minutes": start_minutes, "end_minutes": end_minutes})

    # مرتب‌سازی
    result.sort(key=lambda x: x["start_minutes"])
    return result
def time_to_minutes(time_obj):
    return time_obj.hour * 60 + time_obj.minute