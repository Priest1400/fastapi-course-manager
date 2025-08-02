from sqlalchemy import Integer, Column, String, Boolean, ForeignKey, DateTime, Float, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import base  # base برای تعریف مدل‌ها

# ------------------------- مدل کاربران -------------------------
class DbUser(base):
    __tablename__ = 'users'  # نام جدول در دیتابیس

    id = Column(Integer, primary_key=True, index=True)  # شناسه یکتا
    username = Column(String, unique=True, nullable=False, index=True)  # نام کاربری منحصر به فرد
    email = Column(String, unique=True, nullable=True)  # ایمیل (ممکن است اختیاری باشد)
    password = Column(String, nullable=False)  # رمز عبور هش‌شده
    is_active = Column(Boolean, default=True)  # وضعیت فعال یا غیرفعال بودن کاربر
    role = Column(String, nullable=False)  # نقش کاربر (مثلاً student یا admin)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # زمان ایجاد حساب

    enrollments = relationship("Enrollment", back_populates="student")  # ارتباط یک‌به‌چند با ثبت‌نام‌ها

# ------------------------- مدل دوره‌ها -------------------------
class Course(base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False, index=True)  # عنوان دوره
    instructor = Column(String, nullable=False, index=True)  # نام مدرس
    start_date = Column(DateTime, nullable=False, index=True)  # تاریخ شروع دوره
    end_date = Column(DateTime, nullable=True)  # تاریخ پایان دوره (اختیاری)
    sessions_count = Column(Integer, nullable=False)  # تعداد جلسات دوره
    is_active = Column(Boolean, default=True)  # فعال بودن یا نبودن دوره
    class_day = Column(String, nullable=False)  # روز برگزاری کلاس (مثلاً سه‌شنبه)
    class_start_time = Column(Time, nullable=False)  # زمان شروع کلاس (ساعت و دقیقه)
    class_end_time = Column(Time, nullable=False)  # زمان پایان کلاس

    enrollments = relationship("Enrollment", back_populates="course")  # ارتباط یک‌به‌چند با ثبت‌نام‌ها

# ------------------------- مدل ثبت‌نام -------------------------
class Enrollment(base):
    __tablename__ = 'enrollments'

    id = Column(Integer, primary_key=True)

    student_id = Column(Integer, ForeignKey('users.id'))  # کلید خارجی به جدول کاربران
    course_id = Column(Integer, ForeignKey('courses.id'))  # کلید خارجی به جدول دوره‌ها

    student = relationship("DbUser", back_populates="enrollments")  # رابطه با مدل کاربر
    course = relationship("Course", back_populates="enrollments")  # رابطه با مدل دوره
