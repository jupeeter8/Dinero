from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
import sqlalchemy
from app.oAuth2 import get_current_user
from app.service.usersService import UserValidator


router = APIRouter(tags=["Friends"])


@router.post("/friend/addfriend", status_code=status.HTTP_201_CREATED)
async def add_friend(
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

    check_integriy = (
        db.query(models.FriendRequests)
        .filter(
            models.FriendRequests.sender == friend_ID,
            models.FriendRequests.reciver == current_user_ID,
        )
        .first()
    )

    if check_integriy:
        if not check_integriy.status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User alredy has a pending request from user {friend_ID}",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User are alredy friends. status: {check_integriy}",
            )

    if vu_ID.validate_user(db):
        add_friend_data = {
            "sender": current_user_ID,
            "reciver": friend_ID,
        }

        friend_request = models.FriendRequests(**add_friend_data)

        try:
            db.add(friend_request)
            db.commit()
            db.refresh(friend_request)
            return friend_request

        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User {current_user_ID} has alredy sent a friend request to user with userID: {friend_ID}",
            )


@router.get("/friend/getall_request", status_code=status.HTTP_200_OK)
async def get_all_requests(
    current_user_ID: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    friend_req_query = (
        db.query(models.FriendRequests)
        .filter(models.FriendRequests.reciver == current_user_ID)
        .all()
    )

    return friend_req_query


@router.post("/friend/acceptrequest", status_code=status.HTTP_201_CREATED)
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
