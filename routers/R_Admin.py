from fastapi import APIRouter, Depends, HTTPException, status, Query , Request , Header
from sqlalchemy.orm import Session

from auth1.auth2 import oauth2_scheme, require_admin
from db.models import DbUser, Course
from db.database import get_db
from schemas import UserBase, UserOut, UserCreate, CourseBase
from db import db_user, Db_admin
from auth1 import auth2



router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)]  # 👈 فقط ادمین‌ها مجازند
)
@router.get("/")
def admin_dashboard():
    return {"message": f"خوش آمدی ادمین "}
@router.post("/add_course", response_model=CourseBase)
def add_course(course : CourseBase , db : Session = Depends(get_db)):
    existing_course = db.query(Course).filter(Course.title == course.title).first()
    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="این دوره قبلا ثبت شده است"
        )
    new_course = Db_admin.add_course(db, course)
    return new_course