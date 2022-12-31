from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.schema import SplitDetails
from app.service.splitService import verify_split
from app.service.usersService import get_username, validate_user
from .. import models
from ..database import get_db
from ..oAuth2 import get_current_user

router = APIRouter(tags=["Balance and settle"])

# TODO Check the two user are friends
@router.post("/record/split")
async def split(
    split_detail: SplitDetails,
    current_user_ID: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Validate both user_id
    validate_user(split_detail.paid_by, db)
    validate_user(split_detail.owed_by, db)

    # Check if user is not requesting to add split data for someone else
    if (
        not split_detail.paid_by == current_user_ID
        and not split_detail.owed_by == current_user_ID
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User Can only add balance for themselves",
        )

    # Check if the user is trying to add split with themselve
    if split_detail.paid_by == split_detail.owed_by:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User can not owe themselve"
        )

    # Check both users are firends
    isfriend = db.query(models.Friends).filter(
        (
            models.Friends.sender == split_detail.paid_by,
            models.Friends.reciver == split_detail.owed_by,
        )
        or (
            models.Friends.sender == split_detail.owed_by,
            models.Friends.reciver == split_detail.paid_by,
        )
    )

    print(isfriend)

    if not isfriend:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User is not friends with the other user",
        )

    # Validate amounts and convert to paise
    split_detail.paid_amount, split_detail.owed_amount = verify_split(
        split_detail.paid_amount, split_detail.owed_amount
    )

    return None
