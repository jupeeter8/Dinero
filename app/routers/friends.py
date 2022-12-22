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

    if current_user_ID == friend_ID:  # Check User is not adding themselve as a friend
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User can not add themselv as a friend",
        )

    vu_ID = UserValidator(friend_ID)
    if vu_ID.validate_user(db):  # Check if freind is a valid user
        pass

    # Check if firend has alredy sent a friend request
    check_integriy = (
        db.query(models.Friends)
        .filter(
            models.Friends.sender == friend_ID,
            models.Friends.reciver == current_user_ID,
        )
        .first()
    )

    if check_integriy:

        if not check_integriy.status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User alredy has a pending request from user {friend_ID}",
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User are alredy friends. status: {check_integriy.status}",
        )

    # Check if user has alredy sent a firend request
    check_integriy = (
        db.query(models.Friends)
        .filter(
            models.Friends.sender == current_user_ID,
            models.Friends.reciver == friend_ID,
        )
        .first()
    )

    if check_integriy:
        if not check_integriy.status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User has already sent a request to user {friend_ID}",
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User are alredy friends. status: {check_integriy.status}",
        )

    add_friend_data = {
        "sender": current_user_ID,
        "reciver": friend_ID,
        "invite_code": 1234,
        "relation": "Friends",
    }

    friend_data = models.Friends(**add_friend_data)

    db.add(friend_data)
    db.commit()
    db.refresh(friend_data)
    return friend_data

    #     except sqlalchemy.exc.IntegrityError:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail=f"User {current_user_ID} has alredy sent a friend request to user with userID: {friend_ID}",
    #         )


@router.get("/friend/getall_request", status_code=status.HTTP_200_OK)
async def get_all_requests(
    current_user_ID: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    friend_req_query = (
        db.query(models.Friends).filter(models.Friends.reciver == current_user_ID).all()
    )

    return friend_req_query


# Todo generate a invite code and use that to add firend
# Maybe i don't need invite code
@router.post("/friend/acceptrequest", status_code=status.HTTP_201_CREATED)
async def accept_friend_request(
    current_user_ID: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    sender: int = None,
):
    is_vs = UserValidator(sender)
    if is_vs.validate_user(db):
        pass

    friend_data: models.Friends = (
        db.query(models.Friends)
        .filter(
            models.Friends.sender == sender,
            models.Friends.reciver == current_user_ID,
        )
        .first()
    )
    if not friend_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User does not have a friend request from user: {sender}",
        )

    if friend_data.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Users are alredy firends"
        )

    friend_data.status = True
    db.commit()
    db.refresh(friend_data)

    return friend_data
