from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# connect and create new sqlite db
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'


# used in other areas of the app
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})


# instance of DBSession
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


# allows to create each DBModel
Base = declarative_base()


