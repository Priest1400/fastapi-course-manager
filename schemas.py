from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    role: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    created_at: datetime
    is_active: bool