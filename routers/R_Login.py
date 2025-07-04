from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from db import models
from db.database import get_db
from db.hash import Hash
from auth1 import auth2


router = APIRouter(prefix='/login', tags=['login'])


@router.post('/')
def get_token(request: OAuth2PasswordRequestForm=Depends(), db: Session= Depends(get_db)):
    user = db.query(models.DbUser).filter(models.DbUser.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid credential')

    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid password')

    access_token = auth2.create_access_token(data={
        'sub': user.username,
        'user_id': user.id,
        'role': user.role
    })

    return {
        'access_token': access_token,
        'type_token': 'bearer',
        'userID': user.id,
        'username': user.username,
        'role' : user.role,
        'email' : user.email
    }






