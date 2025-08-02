from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db
from auth1 import auth2
from db.models import Enrollment, Course


# تبدیل رشته زمان (مثل "08:30") به دقیقه (مثلا 8*60 + 30 = 510)
def time_str_to_minutes(time_str: str) -> int:
    time_obj = datetime.strptime(time_str.strip(), "%H:%M")  # تبدیل رشته به datetime
    return time_obj.hour * 60 + time_obj.minute  # محاسبه کل دقیقه از نیمه شب


# گرفتن برنامه کلاسی روز مشخص شده (target_day) به صورت لیستی از بازه‌های دقیقه‌ای زمان کلاس‌ها
def get_day_schedule_in_minutes(target_day: str, db: Session = Depends(get_db), current_user=Depends(auth2.get_current_user)):

    # گرفتن همه ثبت‌نام‌های کاربر جاری
    enrollments = db.query(Enrollment).filter(Enrollment.student_id == current_user.get("user_id")).all()
    # استخراج شناسه کلاس‌ها
    course_ids = [e.course_id for e in enrollments]

    # گرفتن همه دوره‌ها با آن شناسه‌ها
    courses = db.query(Course).filter(Course.id.in_(course_ids)).all()

    # فیلتر دوره‌هایی که کلاس‌شان در روز مورد نظر است و ساخت دیکشنری برای هر کلاس
    day_classes = [
        {
            "day": course.class_day,
            "time": f"{course.class_start_time.strftime('%H:%M')} - {course.class_end_time.strftime('%H:%M')}"
        }
        for course in courses if course.class_day.strip() == target_day.strip()
    ]

    # تبدیل زمان‌های رشته‌ای شروع و پایان به دقیقه
    result = []
    for item in day_classes:
        start_str, end_str = item["time"].split(" - ")
        start_minutes = time_str_to_minutes(start_str)
        end_minutes = time_str_to_minutes(end_str)
        result.append({"start_minutes": start_minutes, "end_minutes": end_minutes})

    # مرتب‌سازی بر اساس زمان شروع کلاس‌ها
    result.sort(key=lambda x: x["start_minutes"])
    return result


# تبدیل مستقیم datetime.time به دقیقه (کمک به چک کردن زمان‌ها)
def time_to_minutes(time_obj):
    return time_obj.hour * 60 + time_obj.minute
