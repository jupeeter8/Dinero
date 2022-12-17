from sqlalchemy import TIMESTAMP, Column, Integer, String, ForeignKey
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


class Friends(Base):
    __tablename__ = "friends"

    user_a = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    user_b = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    relation = Column(String, nullable=False)
    friends_since = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
