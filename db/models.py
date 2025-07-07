from sqlalchemy import Integer, Column, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import base


class DbUser(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    enrollments = relationship("Enrollment", back_populates="student")


class Course(base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False, index=True)
    instructor = Column(String, nullable=False, index=True)
    start_date = Column(DateTime, nullable=False, index=True)
    end_date = Column(DateTime, nullable=True)
    sessions_count = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    enrollments = relationship("Enrollment", back_populates="course")



class Enrollment(base):
    __tablename__ = 'enrollments'
    id = Column(Integer, primary_key=True)

    student_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))

    student = relationship("DbUser", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
