from sqlalchemy.orm.session import  Session

from Exceptions import EmailNotValid
from schemas import UserBase, UserCreate
from db.models import DbUser
from db.hash import Hash

def create_user(db: Session, user: UserCreate) -> DbUser:
    db_user = DbUser(
        username=user.username,
        email=user.email,
        password=Hash.bcrypt(user.password),
        role=user.role,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(username , db:Session):
    db.query(DbUser).filter(DbUser.username == username).first()

