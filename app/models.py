from sqlalchemy import TIMESTAMP, Column, Integer, String, Sequence
from sqlalchemy.sql.expression import text

from .database import Base


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    joined_on = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
