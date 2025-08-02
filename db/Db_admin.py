from sqlalchemy.orm.session import Session
from schemas import CourseBase
from db.models import Course, Enrollment


# افزودن یک دوره جدید به دیتابیس
def add_course(db: Session, course: CourseBase) -> Course:
    # ایجاد یک نمونه از مدل Course با داده‌های دریافتی از کاربر
    db_course = Course(
        title=course.title,
        instructor=course.instructor,
        start_date=course.start_date,
        end_date=course.end_date,
        sessions_count=course.sessions_count,
        is_active=course.is_active,
        class_day=course.class_day,
        class_start_time=course.class_start_time,
        class_end_time=course.class_end_time
    )
    db.add(db_course)  # اضافه کردن به session
    db.commit()  # ذخیره تغییرات در دیتابیس
    db.refresh(db_course)  # به‌روزرسانی شی از دیتابیس (دریافت مقدار id و ...)
    return db_course  # بازگشت شی دوره ثبت شده


# گرفتن زمان کلاس‌های یک دانش‌آموز (با استفاده از اطلاعات توکن)
def get_time_of_course(current_user, db: Session):
    # پیدا کردن تمام ثبت‌نام‌های کاربر (بر اساس user_id داخل توکن)
    enrollments = db.query(Enrollment).filter(Enrollment.student_id == current_user.get("user_id")).all()

    # استخراج شناسه دوره‌هایی که کاربر در آن‌ها ثبت‌نام کرده
    course_ids = [e.course_id for e in enrollments]

    # گرفتن اطلاعات دوره‌ها از دیتابیس
    courses = db.query(Course).filter(Course.id.in_(course_ids)).all()

    # ساخت یک لیست شامل روز و بازه زمانی هر کلاس
    return [
        {
            "day": course.class_day,
            "time": f"{course.class_start_time.strftime('%H:%M')} - {course.class_end_time.strftime('%H:%M')}"
        }
        for course in courses
    ]
