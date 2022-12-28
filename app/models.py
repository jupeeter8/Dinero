from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, ForeignKey, JSON
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

    sender = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    reciver = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    status = Column(Boolean, nullable=False, server_default="false")

    sent_on = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )

    invite_code = Column(Integer, nullable=False)

    relation = Column(String, nullable=False)

    friends_since = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )


class Split(Base):
    __tablename__ = "split"

    split_id = Column(Integer, primary_key=True, nullable=False)
    paid_by = Column(
        Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True
    )
    p_username = Column(String, nullable=False)
    paid_amount = Column(Integer, nullable=False)
    owed_by = Column(
        Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True
    )
    o_username = Column(String, nullable=False)
    owed_amount = Column(Integer, nullable=False)
    group_id = Column(Integer, nullable=False, server_default="-1")
    paid_for = Column(String, nullable=True)
    category = Column(String, nullable=False)
    split_method = Column(JSON, nullable=False)
