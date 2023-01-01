from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.schema import SplitDetails
from app.service.friendsService import check_friend_status
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

    # Check if the user is trying to add split with themselve

    if split_detail.paid_by == split_detail.owed_by:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User can not owe themselve"
        )

    # Check if user is not requesting to add split data for someone else

    created_by = {split_detail.p_username: split_detail.paid_by}
    if not split_detail.paid_by == current_user_ID:
        if not split_detail.owed_by == current_user_ID:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User can not spli for other users",
            )
        created_by = {split_detail.o_username: split_detail.owed_by}

    # Validate both user_id
    if split_detail.paid_by == current_user_ID:
        validate_user(split_detail.owed_by, db)
    else:
        validate_user(split_detail.paid_by, db)

    # Check both users are firends

    if not check_friend_status(split_detail.paid_by, split_detail.owed_by, db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Users are not friends"
        )
    # Validate amounts and convert to paise
    split_detail.paid_amount, split_detail.owed_amount = verify_split(
        split_detail.paid_amount, split_detail.owed_amount
    )

    data = models.Split(**split_detail.dict())
    data.created_by = created_by

    print(created_by)

    db.add(data)
    db.commit()
    db.refresh(data)
    return data
