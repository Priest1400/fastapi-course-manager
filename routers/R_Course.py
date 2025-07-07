from fastapi import APIRouter, Depends, HTTPException, status, Query , Request , Header
from sqlalchemy.orm import Session

from auth1.auth2 import oauth2_scheme, require_admin
from db.models import DbUser, Course
from db.database import get_db
from schemas import UserBase, UserOut, UserCreate, CourseBase
from db import db_user, Db_admin
from auth1 import auth2


router = APIRouter(prefix='/course', tags=['course'])


@router.get("/show_all")
def get_all_courses(db: Session = Depends(get_db)):
    courses = db.query(Course.id, Course.title).all()
    titles = [course.title for course in courses]
    ids = [course.id for course in courses]
    return {"titles": titles, "ids": ids}
