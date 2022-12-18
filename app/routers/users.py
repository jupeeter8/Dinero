from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.service.usersService import UserValidator
from ..schema import CreateNewUser, UserDataResponse, InviteFriend
from .. import models
from ..oAuth2 import get_current_user, password_utils

router = APIRouter(tags=["User"])


@router.post(
    "/user/create",
    status_code=status.HTTP_201_CREATED,
    response_model=UserDataResponse,
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


@router.get("/user/getall_request", status_code=status.HTTP_200_OK)
async def get_all_requests(
    current_user_ID: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    friend_req_query = (
        db.query(models.FriendRequests)
        .filter(models.FriendRequests.reciver == current_user_ID)
        .all()
    )

    return friend_req_query


@router.post("/user/acceptrequest", status_code=status.HTTP_201_CREATED)
async def accept_friend_request(
    current_user_ID: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    sender: int = None,
):
    is_vs = UserValidator(sender)
    if is_vs.validate_user(db):
        friend_req_data: models.FriendRequests = (
            db.query(models.FriendRequests)
            .filter(
                models.FriendRequests.sender == sender,
                models.FriendRequests.reciver == current_user_ID,
            )
            .first()
        )
    if not friend_req_data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {current_user_ID} does not have a firend request from user {sender}",
        )
    if friend_req_data.status:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)

    friend = models.Friends(user_a=sender, user_b=current_user_ID, relation="Friends")
    db.add(friend)
    friend_req_data.status = True
    db.commit()
    db.refresh(friend)

    return friend
