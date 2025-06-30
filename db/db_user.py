from sqlalchemy.orm.session import  Session

from Exceptions import EmailNotValid
from schemas import UserBase
from db.models import DbUser
from db.hash import Hash

def creat_user(db:Session, request: UserBase):
    if "@" not in request.email:
        raise EmailNotValid("mail", "lll")
    user = DbUser(
        username = request.username ,
        password = Hash.bcrypt(request.password),
        email = request.email

    )]
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
