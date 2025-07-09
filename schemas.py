from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import time

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    role: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    created_at: datetime
    is_active: bool

class CourseBase(BaseModel):
    title: str
    instructor: str
    start_date: datetime
    end_date: datetime
    sessions_count: int
    is_active: bool = True
    class_day: str
    class_start_time: time
    class_end_time: time
