from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.schema import SplitDetails
from app.service.splitService import verify_split
from app.service.usersService import get_username, validate_user
from .. import models
from ..database import get_db
from ..oAuth2 import get_current_user

router = APIRouter(tags=["Balance and settle"])


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
    created_by = {split_detail.p_username: split_detail.paid_by}
    if not split_detail.paid_by == current_user_ID:
        if not split_detail.owed_by == current_user_ID:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User can not spli for other users",
            )
        created_by = {split_detail.o_username: split_detail.owed_by}

    # Check if the user is trying to add split with themselve
    if split_detail.paid_by == split_detail.owed_by:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User can not owe themselve"
        )

    # Check both users are firends
    # Just use two different queries

    # Maybe move this logic to servies?

    isfriend = (
        db.query(models.Friends)
        .filter(
            models.Friends.sender == split_detail.paid_by,
            models.Friends.reciver == split_detail.owed_by,
        )
        .first()
    )

    if not isfriend:
        isfriend = (
            db.query(models.Friends)
            .filter(
                models.Friends.sender == split_detail.owed_by,
                models.Friends.reciver == split_detail.paid_by,
            )
            .first()
        )
        if not isfriend:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Users are not friends"
            )

    if not isfriend.status:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Users are not friends"
        )

    # Validate amounts and convert to paise
    split_detail.paid_amount, split_detail.owed_amount = verify_split(
        split_detail.paid_amount, split_detail.owed_amount
    )

    data = models.Split(**split_detail.dict())
    data.created_by = created_by

    db.add(data)
    db.commit()
    db.refresh(data)
    return data
