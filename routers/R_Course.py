from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.models import Course  # مدل دوره‌ها
from db.database import get_db  # تابع گرفتن سشن دیتابیس

# تعریف APIRouter برای مسیرهای مربوط به دوره‌ها
router = APIRouter(prefix='/course', tags=['course'])

# روت برای نمایش همه‌ی دوره‌ها (فقط عنوان و آیدی)
@router.get("/show_all")
def get_all_courses(db: Session = Depends(get_db)):
    # گرفتن همه دوره‌ها با فیلدهای id و title
    courses = db.query(Course.id, Course.title).all()

    # استخراج عنوان‌ها و شناسه‌ها در لیست‌های جداگانه
    titles = [course.title for course in courses]
    ids = [course.id for course in courses]

    # بازگرداندن لیست عناوین و آیدی‌ها در قالب دیکشنری
    return {"titles": titles, "ids": ids}
