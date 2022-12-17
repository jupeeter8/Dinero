from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.service.usersService import UserValidator
from ..schema import CreateNewUser, CreateNewUserResponse, InviteFriend
from .. import models
from ..oAuth2 import get_current_user, password_utils

router = APIRouter(tags=["User"])


@router.post(
    "/user/create",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateNewUserResponse,
)
async def create_new_user(new_user_data: CreateNewUser, db: Session = Depends(get_db)):
    customer_query = db.query(models.Users).filter(
        models.Users.username == new_user_data.username
        or models.Users.email == new_user_data.email
    )
    data: models.Users = customer_query.first()

    if data:
        username = data.username
        email = data.email
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username {username} and email {email} alredy exits",
        )
    data = models.Users(**new_user_data.dict())

    password = data.password
    data.password = password_utils.get_password_hash(password)

    db.add(data)
    db.commit()
    db.refresh(data)

    return data


@router.post("/user/addfriend", status_code=status.HTTP_201_CREATED)
async def invite_friend(
    current_user_ID: int = Depends(get_current_user),
    friend_ID: int = None,
    db: Session = Depends(get_db),
):
    if current_user_ID == friend_ID:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User can not add themselv as a friend",
        )

    vu_ID = UserValidator(friend_ID)
    if vu_ID.validate_user(db):
        friend_model_data = {
            "user_a": current_user_ID,
            "user_b": friend_ID,
            "relation": "Invitation",
        }

        friend = models.Friends(**friend_model_data)
        db.add(friend)
        db.commit()
        db.refresh(friend)
        return friend
