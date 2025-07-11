from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, Header
from sqlalchemy.orm import Session

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


    existing = db.query(Enrollment).filter_by(
        student_id=current_user["user_id"],
        course_id=course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")


    enrollment = Enrollment(
        student_id=current_user["user_id"],
        course_id=course_id
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return {"message": "Successfully enrolled", "course": course.title}

@router.get("/test")
def test(current_user = Depends(auth2.get_current_user), db: Session = Depends(get_db)):
    return get_time_of_course(current_user, db)


