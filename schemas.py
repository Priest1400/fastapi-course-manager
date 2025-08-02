from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import time

# مدل پایه کاربر، شامل فیلدهای پایه‌ای مثل نام کاربری، ایمیل اختیاری و نقش کاربر
class UserBase(BaseModel):
    username: str  # نام کاربری
    email: Optional[EmailStr] = None  # ایمیل (اختیاری، نوع ایمیل اعتبارسنجی می‌شود)
    role: str  # نقش کاربر مثل "student" یا "admin"

# مدل ثبت نام کاربر، که علاوه بر فیلدهای UserBase شامل پسورد هم هست
class UserCreate(UserBase):
    password: str  # رمز عبور

# مدل خروجی اطلاعات کاربر، شامل فیلدهای پایه به همراه زمان ایجاد و وضعیت فعال بودن
class UserOut(UserBase):
    created_at: datetime  # زمان ایجاد کاربر
    is_active: bool  # وضعیت فعال بودن حساب

# مدل پایه دوره آموزشی، شامل مشخصات دوره و زمان‌بندی کلاس‌ها
class CourseBase(BaseModel):
    title: str  # عنوان دوره
    instructor: str  # مدرس دوره
    start_date: datetime  # تاریخ شروع دوره
    end_date: datetime  # تاریخ پایان دوره
    sessions_count: int  # تعداد جلسات
    is_active: bool = True  # وضعیت فعال بودن دوره (پیش‌فرض فعال)
    class_day: str  # روز برگزاری کلاس (مثلا "سه‌شنبه")
    class_start_time: time  # ساعت شروع کلاس (مثلا 08:00)
    class_end_time: time  # ساعت پایان کلاس (مثلا 09:30)
