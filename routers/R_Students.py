from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, Header
from sqlalchemy.orm import Session

import check
from auth1.auth2 import oauth2_scheme, require_student
from db.Db_admin import get_time_of_course
from db.models import DbUser, Course, Enrollment
from db.database import get_db
from schemas import UserBase, UserOut, UserCreate, CourseBase
from db import db_user, Db_admin
from auth1 import auth2

router = APIRouter(
    prefix="/student",
    tags=["student"],
    dependencies=[Depends(require_student)]
)


@router.post("/register_course_by_student{course_id}")
def register_course_by_id(course_id: int, db: Session = Depends(get_db), current_user=Depends(auth2.get_current_user)):
    # بررسی وجود داشتن دوره
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # بررسی اینکه کاربر قبلاً ثبت‌نام کرده یا نه
    existing = db.query(Enrollment).filter_by(
        student_id=current_user["user_id"],
        course_id=course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")

    # چک تداخل زمانی
    start_time = check.time_to_minutes(course.class_start_time)
    end_time = check.time_to_minutes(course.class_end_time)
    x1 = check.get_day_schedule_in_minutes(course.class_day, db, current_user)

    for item in x1:
        existing_start = item["start_minutes"]
        existing_end = item["end_minutes"]
        if start_time < existing_end and end_time > existing_start:
            raise HTTPException(status_code=400, detail="تداخل زمانی با کلاس دیگری وجود دارد.")

    # ثبت‌نام در کلاس
    enrollment = Enrollment(
        student_id=current_user["user_id"],
        course_id=course_id
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return {"message": "Successfully enrolled", "course": course.title}


@router.get("/test")
def test(current_user=Depends(auth2.get_current_user), db: Session = Depends(get_db)):
    x1 = Db_admin.get_time_of_course(current_user, db)
    return x1


