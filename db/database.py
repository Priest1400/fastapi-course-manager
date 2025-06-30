from sqlalchemy import Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = create_engine("sqlite:///fastapi.db" , connect_args = {'check_same_thread' : False})
base = declarative_base()

sessionlocal = sessionmaker(bind = engine)

def get_db():
    session = sessionlocal()
    try:
        yield session
    finally:
        session.close()