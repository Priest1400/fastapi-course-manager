from sqlalchemy.orm.session import  Session

from Exceptions import EmailNotValid
from schemas import UserBase, UserCreate, CourseBase
from db.models import DbUser, Course
from db.hash import Hash


def add_course(db: Session, course: CourseBase) -> Course:
    db_course = Course(
        title=course.title,
        instructor=course.instructor,
        start_date=course.start_date,
        end_date=course.end_date,
        sessions_count=course.sessions_count,
        is_active=course.is_active
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course