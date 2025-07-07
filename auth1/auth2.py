from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from typing import Optional
from datetime import datetime, timedelta
from db.database import get_db
from db.db_user import get_user_by_username
from sqlalchemy.orm import Session
from jose import jwt
from jose.exceptions import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = '6c7d438d2ea66cc11ee315566bda6f45336930dc2a40eaa96ec009524c20aa69'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def get_current_user(token: str=Depends(oauth2_scheme), db: Session= Depends(get_db)):
  error_credential = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail='invalid credentials',
                                   headers={'WWW-authenticate': 'bearer'})

  try:
    _dict = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    username = _dict.get('sub')
    user_id = _dict.get('user_id')
    role = _dict.get('role')
    email = _dict.get('email')
    data = {
      "sub": username,
      "user_id": user_id,
      "role": role,
      "email": email
    }

    if not username:
      raise error_credential
  except JWTError:
    raise error_credential


  return data

def require_admin(current_user=Depends(get_current_user)):
  if current_user["role"] != "admin":
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Access denied: Admins only"
    )
  return current_user

def require_student(current_user=Depends(get_current_user)):
  if current_user["role"] != "student":
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Access denied: Students only"
    )
  return current_user
