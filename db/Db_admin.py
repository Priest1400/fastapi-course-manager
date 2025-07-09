from fastapi import Depends
from sqlalchemy.orm.session import Session

from Exceptions import EmailNotValid
from auth1 import auth2
from schemas import UserBase, UserCreate, CourseBase
from db.models import DbUser, Course, Enrollment
from db.hash import Hash


def add_course(db: Session, course: CourseBase) -> Course:
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
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_time_of_course(current_user, db: Session):
    enrollments = db.query(Enrollment).filter(Enrollment.student_id == current_user.get("user_id")).all()
    course_ids = [e.course_id for e in enrollments]
    return {"enrolled_course_ids": course_ids}
