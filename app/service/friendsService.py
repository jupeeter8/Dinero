from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import time

from app import models


def generate_code():
    # username = (
    #     db.query(models.Users).filter(models.Users.user_id == user_ID).first().username
    # )

    # username = "anirudh"
    # time_int = 9999999

    # char = [ord(i) for i in username]

    time_str = str(time.time()).replace(".", "")
    time_int = int(time_str[:-6:-1])

    return time_int


def check_friend_status(a: int, b: int, db: Session):
    # isfriend = (
    #     db.query(models.Friends)
    #     .filter(
    #         models.Friends.sender == a,
    #         models.Friends.reciver == b,
    #     )
    #     .first()
    # )

    # if not isfriend:
    #     isfriend = (
    #         db.query(models.Friends)
    #         .filter(
    #             models.Friends.sender == b,
    #             models.Friends.reciver == a,
    #         )
    #         .first()
    #     )
    #     if not isfriend:
    #         return False

    if (
        isfriend := (
            db.query(models.Friends)
            .filter(
                models.Friends.sender == a,
                models.Friends.reciver == b,
            )
            .first()
        )
    ) is None:
        if (
            isfriend := (
                db.query(models.Friends)
                .filter(
                    models.Friends.sender == b,
                    models.Friends.reciver == a,
                )
                .first()
            )
        ) is None:
            return False

    return True if isfriend.status else False
