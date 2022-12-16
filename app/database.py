from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from .config import env_var

new_url = env_var.database_url
new_url = new_url[8::]
new_url = "postgresql" + new_url

DATABASE_URL = new_url

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()
